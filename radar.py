"""Radar de Pesos y Bits.

Busca noticias de economía de México y el mundo en Google Noticias y en feeds oficiales,
junta las notas que hablan de lo mismo, las ordena por relevancia para el canal
y genera docs/index.html (la página) y docs/radar.json (los datos).

Uso: python radar.py
"""
import datetime as dt
import json
import math
import pathlib
import re
import time
import unicodedata
import urllib.parse

import feedparser

import config

RAIZ = pathlib.Path(__file__).parent
DOCS = RAIZ / "docs"
DATA = RAIZ / "data"
HISTORIAL = DATA / "vistos.json"
PLANTILLA = RAIZ / "plantilla.html"
AGENTE = "Mozilla/5.0 (RadarPesosYBits; +https://github.com)"
CDMX = dt.timezone(dt.timedelta(hours=-6))  # México centro no usa horario de verano desde 2022

VACIAS = set("""a al ante bajo con contra de del desde durante e el en entre esta este hacia hasta la las lo los
mas más mientras o para pero por que qué se según sin sobre su sus tras un una uno y ya hoy es son fue
será ha han hay le les como cómo cuánto cuanto cuál así asi tu tus te the of to in on for and is at by""".split())


def sin_acentos(texto):
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")


SINONIMOS = {
    "indice nacional de precios al consumidor": "inflacion inpc",
    "tasa de interes": "tasa",
    "tipo de cambio": "dolar",
    "banco de mexico": "banxico",
    "reserva federal": "fed",
    "federal reserve": "fed",
    "presupuesto de egresos": "presupuesto",
}


def fichas(titulo):
    """Palabras clave de un titular, sin acentos ni palabras vacías."""
    texto = sin_acentos(titulo.lower())
    for largo, corto in SINONIMOS.items():
        texto = texto.replace(largo, corto)
    limpio = re.sub(r"[^\w\s%.]", " ", texto)
    return {p.strip(".") for p in limpio.split() if len(p.strip(".")) > 2 and p not in VACIAS}


def parecido(a, b):
    """Qué tanto se parecen dos titulares (0 a 1). Compartir una cifra (6.25%, 3.75%) pesa mucho."""
    if not a or not b:
        return 0.0
    comunes = a & b
    base = len(comunes) / min(len(a), len(b))
    cifras = {c for c in comunes if re.search(r"\d", c) and not re.fullmatch(r"20\d\d|\d{1,2}", c)}
    if cifras and len(comunes) >= 3:
        base = max(base, 0.6)
    return base


def url_google(consulta, idioma="es"):
    q = urllib.parse.quote(f"{consulta} when:2d")
    if idioma == "en":
        return f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
    return f"https://news.google.com/rss/search?q={q}&hl=es-419&gl=MX&ceid=MX:es-419"


def lista_de_feeds():
    feeds = []
    for clave, tema in config.TEMAS.items():
        for c in tema.get("consultas", []):
            feeds.append({"nombre": f"Google Noticias: {c}", "url": url_google(c), "tema": clave})
        for c in tema.get("consultas_en", []):
            feeds.append({"nombre": f"Google News (EN): {c}", "url": url_google(c, "en"), "tema": clave})
    feeds.extend(config.FEEDS_DIRECTOS)
    return feeds


def leer_feed(feed):
    datos = feedparser.parse(feed["url"], agent=AGENTE)
    estado = getattr(datos, "status", 200)
    if estado >= 400 or (datos.bozo and not datos.entries):
        raise RuntimeError(f"HTTP {estado}" if estado >= 400 else str(datos.get("bozo_exception", "feed ilegible"))[:80])
    notas = []
    for e in datos.entries:
        fecha = e.get("published_parsed") or e.get("updated_parsed")
        if not fecha:
            continue
        cuando = dt.datetime(*fecha[:6], tzinfo=dt.timezone.utc)
        fuente = (e.get("source") or {}).get("title") or feed["nombre"].split(" (")[0]
        titulo = e.get("title", "").strip()
        sufijo = f" - {fuente}"
        if titulo.endswith(sufijo):
            titulo = titulo[: -len(sufijo)].strip()
        if titulo:
            notas.append({"titulo": titulo, "fuente": fuente, "link": e.get("link", ""),
                          "fecha": cuando, "tema": feed["tema"]})
    return notas


def es_oficial(fuente):
    f = fuente.lower()
    return any(o in f for o in config.FUENTES_OFICIALES)


def es_confiable(fuente):
    f = fuente.lower()
    return any(o in f for o in config.FUENTES_CONFIABLES)


def agrupar(notas):
    """Junta las notas que cuentan la misma historia."""
    grupos = []
    for n in sorted(notas, key=lambda x: x["fecha"], reverse=True):
        n["fichas"] = fichas(n["titulo"])
        mejor, mejor_sim = None, 0.0
        for g in grupos:
            sim = max(parecido(n["fichas"], m["fichas"]) for m in g["notas"])
            if sim > mejor_sim:
                mejor, mejor_sim = g, sim
        if mejor and mejor_sim >= 0.55:
            if not any(x["link"] == n["link"] or x["titulo"] == n["titulo"] for x in mejor["notas"]):
                mejor["notas"].append(n)
                mejor["fichas"] |= n["fichas"]
            mejor["temas"][n["tema"]] = mejor["temas"].get(n["tema"], 0) + 1
        else:
            grupos.append({"fichas": set(n["fichas"]), "notas": [n], "temas": {n["tema"]: 1}})
    return grupos


def puntuar(g, ahora):
    textos = " ".join(sin_acentos(n["titulo"].lower()) for n in g["notas"])
    fuentes = {n["fuente"] for n in g["notas"]}
    tema = max(g["temas"], key=lambda t: (g["temas"][t], config.TEMAS[t]["peso"]))
    p = config.TEMAS[tema]["peso"] * 2
    p += math.log2(1 + len(fuentes)) * 2                      # cobertura: cuántos medios distintos
    gancho = sum(v for k, v in config.PALABRAS_GANCHO.items() if sin_acentos(k) in textos)
    p += min(gancho, 3)
    if any(sin_acentos(k) in textos for k in config.PALABRAS_MEXICO):
        p += 1
    oficial = any(es_oficial(f) for f in fuentes)
    if oficial:
        p += 1.5
    if any(es_confiable(f) for f in fuentes):
        p += 0.5
    if any(sin_acentos(r) in textos for r in config.RUIDO):
        p -= 3
    horas = (ahora - max(n["fecha"] for n in g["notas"])).total_seconds() / 3600
    p *= max(0.4, 1 - horas / (config.VENTANA_HORAS * 1.5))
    return round(p, 2), tema, oficial, fuentes


def formatos(g, tema, n_fuentes):
    principal = g["notas"][0]["titulo"]
    textos = sin_acentos(" ".join(n["titulo"].lower() for n in g["notas"]))
    f = []
    if tema in config.TEMAS_LARGO and n_fuentes >= 4:
        f.append("Largo")
    if re.search(r"\d", principal):
        f.append("Short")
    if tema in ("proteccion", "cripto") or any(p in textos for p in ("fraude", "estafa", "hackeo", "quiebra", "alerta", "revoca")):
        f.append("TikTok")
    return f or ["Short"]


def cargar_historial(ahora):
    if not HISTORIAL.exists():
        return []
    limite = ahora - dt.timedelta(days=config.DIAS_MEMORIA)
    vistos = json.loads(HISTORIAL.read_text(encoding="utf-8"))
    return [v for v in vistos if dt.datetime.fromisoformat(v["visto"]) >= limite]


def main():
    ahora = dt.datetime.now(dt.timezone.utc)
    limite = ahora - dt.timedelta(hours=config.VENTANA_HORAS)
    notas, fallas = [], []
    for feed in lista_de_feeds():
        try:
            notas += [n for n in leer_feed(feed) if n["fecha"] >= limite]
        except Exception as error:  # un feed caído no detiene el radar
            fallas.append({"feed": feed["nombre"], "error": str(error)[:120]})
        time.sleep(1)

    historial = cargar_historial(ahora)
    historias = []
    for g in agrupar(notas):
        puntos, tema, oficial, fuentes = puntuar(g, ahora)
        visto = next((h for h in historial if parecido(g["fichas"], set(h["fichas"])) >= 0.6), None)
        if visto:
            puntos -= 1
        notas_ordenadas = sorted(g["notas"], key=lambda n: (not es_oficial(n["fuente"]), not es_confiable(n["fuente"]), n["fecha"]))
        historias.append({
            "titulo": g["notas"][0]["titulo"],
            "tema": tema,
            "tema_nombre": config.TEMAS[tema]["nombre"],
            "angulo": config.TEMAS[tema]["angulo"],
            "puntos": round(puntos, 2),
            "oficial": oficial,
            "estado": "Sigue" if visto else "Nueva",
            "desde": visto["visto"][:10] if visto else None,
            "fuentes": sorted(fuentes),
            "formatos": formatos(g, tema, len(fuentes)),
            "notas": [{"titulo": n["titulo"], "fuente": n["fuente"], "link": n["link"],
                       "fecha": n["fecha"].astimezone(CDMX).strftime("%d/%m %H:%M")} for n in notas_ordenadas[:8]],
            "_fichas": sorted(g["fichas"]),
        })

    historias.sort(key=lambda h: h["puntos"], reverse=True)
    historias = historias[: config.MAX_HISTORIAS]

    nuevos = [{"fichas": h["_fichas"], "visto": ahora.isoformat()} for h in historias if h["estado"] == "Nueva"]
    DATA.mkdir(exist_ok=True)
    HISTORIAL.write_text(json.dumps(historial + nuevos, ensure_ascii=False, indent=1), encoding="utf-8")
    for h in historias:
        h.pop("_fichas")

    salida = {
        "generado": ahora.astimezone(CDMX).strftime("%Y-%m-%d %H:%M"),
        "ventana_horas": config.VENTANA_HORAS,
        "notas_leidas": len(notas),
        "historias": historias,
        "temas": {k: v["nombre"] for k, v in config.TEMAS.items()},
        "fallas": fallas,
    }
    DOCS.mkdir(exist_ok=True)
    texto = json.dumps(salida, ensure_ascii=False, indent=1)
    (DOCS / "radar.json").write_text(texto, encoding="utf-8")
    html = PLANTILLA.read_text(encoding="utf-8").replace("/*__DATOS__*/null", texto.replace("</", "<\\/"))
    (DOCS / "index.html").write_text(html, encoding="utf-8")
    print(f"{len(notas)} notas leídas, {len(historias)} historias, {len(fallas)} feeds con falla")


if __name__ == "__main__":
    main()
