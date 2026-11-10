# Radar de Pesos y Bits

Bot que cada mañana (7:00 a. m., hora del centro de México) busca noticias de economía de México y el mundo, junta las notas que cuentan lo mismo, las ordena por relevancia para el canal y publica una página que abres desde el celular.

El radar **encuentra y ordena**; no verifica. Todo dato que entre a un guion se confirma en la fuente oficial.

## Cómo se ordenan las historias
- Qué tanto le importa el tema al canal (tasas, inflación y protección del dinero pesan más).
- Cuántos medios distintos la cubren.
- Si viene de una fuente oficial (Banxico, INEGI, CNBV, Fed…).
- Palabras de tensión (sorprende, recorte, quiebra, fraude, hackeo…).
- Si toca a México directamente.
- Qué tan reciente es. Las notas de rutina ("precio del dólar hoy") bajan.

Cada historia trae una sugerencia de formato (Largo, Short, TikTok) y el ángulo de bolsillo para arrancar. Son sugerencias, no reglas.

## Instalación (unos 20 minutos, una sola vez)
1. Entra a GitHub con tu cuenta y crea un repositorio nuevo llamado `radar-pesos-y-bits`, público.
2. En el repo vacío, elige **uploading an existing file** y arrastra todos los archivos de esta carpeta.
   La carpeta `.github` está oculta en el Finder: presiona `Cmd + Shift + .` para verla y arrástrala también.
   Si no se sube, créala a mano: **Add file → Create new file**, nombre `.github/workflows/radar.yml`, y pega el contenido del archivo.
3. Pestaña **Actions** → activa los workflows si te lo pide → **Radar Pesos y Bits** → **Run workflow**. Tarda 1–2 minutos.
4. **Settings → Pages** → Source: *Deploy from a branch* → rama `main`, carpeta `/docs` → **Save**.
5. En unos minutos tu radar queda en `https://rokymo.github.io/radar-pesos-y-bits/`. Desde Safari: Compartir → *Agregar a inicio*.

## Uso semanal (5 minutos)
1. Abre el radar, filtra por formato si quieres.
2. Marca "Llevar al prompt" en las que te interesen (si no marcas nada, van las 8 primeras).
3. **Copiar para Claude** y pégalo en un chat nuevo. Claude verifica y te propone ideas con tu skill del canal.

## Cambiar qué busca
Todo está en `config.py`: búsquedas por tema, pesos, palabras de gancho y ruido. Edítalo desde GitHub (ícono de lápiz) y guarda.

## Si algo falla
- Abajo de la página aparecen las búsquedas que fallaron ese día. Si una falla varios días seguidos, cámbiala o bórrala en `config.py`.
- Si el radar deja de actualizarse, entra a **Actions** y revisa si GitHub pausó el workflow; se reactiva con un clic.
- Si el paso "Guardar el radar" falla por permisos: **Settings → Actions → General → Workflow permissions → Read and write**.

La página es pública para quien tenga el enlace (no aparece en buscadores). Solo contiene titulares y enlaces a medios.
