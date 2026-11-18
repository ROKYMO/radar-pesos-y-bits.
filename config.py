# Configuración del Radar de Pesos y Bits.
# Aquí cambias QUÉ busca el bot y QUÉ considera importante. No hace falta tocar radar.py.

# Horas hacia atrás que revisa en cada corrida.
VENTANA_HORAS = 48

# Cuántas historias muestra la página.
MAX_HISTORIAS = 30

# Lugares asegurados por tema: aunque un tema tenga menos medios, sus 2 mejores historias siempre salen.
MIN_POR_TEMA = 2

# Días que recuerda una historia para marcarla como "Sigue" en vez de "Nueva".
DIAS_MEMORIA = 7

# EMPRESAS QUE SIGUES. Para agregar una, escribe su nombre entre comillas y una coma.
# El bot la busca en español e inglés todos los días y sube la prioridad de sus noticias.
EMPRESAS_SEGUIDAS = [
    "Nvidia", "Anthropic", "OpenAI", "Apple", "Microsoft", "Tesla", "Amazon", "Google",
    "Meta", "Walmex", "Banorte", "Femsa", "Cemex", "América Móvil", "Grupo México",
]

# peso: qué tanto le importa al canal (1 a 3).
# consultas: búsquedas en Google Noticias México (español).
# consultas_en: búsquedas en Google Noticias EE. UU. (inglés), opcional.
# angulo: la pregunta de bolsillo con la que conviene empezar.
TEMAS = {
    "tasas": {
        "nombre": "Tasas y Banxico", "peso": 3,
        "consultas": ["Banxico tasa de interés", "Cetes subasta tasa", "Banxico minuta"],
        "angulo": "¿Qué cambia para tus Cetes, tu tarjeta y tu crédito?",
    },
    "inflacion": {
        "nombre": "Inflación y precios", "peso": 3,
        "consultas": ["inflación México INEGI", "canasta básica precio México", "precio gasolina México"],
        "angulo": "¿Cuánto vale menos tu quincena? Cuéntalo con un producto concreto.",
    },
    "proteccion": {
        "nombre": "Tu dinero protegido", "peso": 3,
        "consultas": ["SOFIPO", "CNBV revoca autorización", "CONDUSEF alerta fraude", "Afore CONSAR", "IPAB ahorradores"],
        "angulo": "¿Tu dinero está protegido y qué puedes revisar hoy?",
    },
    "bolsa": {
        "nombre": "Bolsa y empresas", "peso": 2.5,
        "consultas": ["Wall Street hoy", "Nasdaq S&P 500", "salida a bolsa", "Bolsa Mexicana de Valores",
                      "resultados trimestrales empresa", "acciones inteligencia artificial", "concurso mercantil empresa"],
        "consultas_en": ["IPO", "stock market", "earnings report", "AI stocks bubble"],
        "angulo": "¿Quién gana, quién pierde y qué significa para alguien que invierte poco a poco?",
    },
    "peso": {
        "nombre": "Peso y dólar", "peso": 2.5,
        "consultas": ["peso mexicano dólar semana", "remesas México Banxico"],
        "angulo": "¿Qué significa para quien gana, gasta o recibe en dólares?",
    },
    "cripto": {
        "nombre": "Cripto", "peso": 2.5,
        "consultas": ["bitcoin precio", "stablecoin regulación", "exchange cripto hackeo", "criptomonedas México regulación"],
        "consultas_en": ["SEC crypto", "crypto exchange hack"],
        "angulo": "¿Cuál es el riesgo real y cuál es puro ruido?",
    },
    "finanzas_publicas": {
        "nombre": "Gobierno, impuestos y deuda", "peso": 2,
        "consultas": ["Presupuesto de Egresos", "Hacienda deuda pública México", "SAT recaudación", "impuestos México 2027"],
        "angulo": "¿De dónde sale y a dónde va el dinero? Divídelo por persona.",
    },
    "crecimiento": {
        "nombre": "Economía y empleo", "peso": 2,
        "consultas": ["PIB México INEGI", "empleo formal IMSS", "salario mínimo 2027"],
        "angulo": "¿Qué significa para tu trabajo y tu sueldo?",
    },
    "comercio": {
        "nombre": "T-MEC y aranceles", "peso": 2,
        "consultas": ["T-MEC revisión", "aranceles México Estados Unidos", "nearshoring inversión México"],
        "angulo": "¿Qué productos y empleos se juegan aquí?",
    },
    "mundo": {
        "nombre": "Economía mundial", "peso": 2,
        "consultas": ["Reserva Federal tasas", "FMI economía mundial", "petróleo precio OPEP", "China economía"],
        "consultas_en": ["Federal Reserve rates decision", "global economy recession"],
        "angulo": "¿Por dónde llega esto a México y a tu bolsillo?",
    },
}

# Feeds directos de fuentes oficiales (RSS). Si alguno deja de funcionar, la página lo avisa.
FEEDS_DIRECTOS = [
    {"nombre": "Reserva Federal (comunicados)", "url": "https://www.federalreserve.gov/feeds/press_all.xml", "tema": "mundo"},
]

# Fuentes oficiales: suben la prioridad de la historia.
FUENTES_OFICIALES = [
    "banco de méxico", "banxico", "inegi", "gob.mx", "gobierno de méxico", "cnbv", "condusef",
    "hacienda", "shcp", "sat", "consar", "ipab", "federal reserve", "reserva federal",
    "imf", "fmi", "banco mundial", "world bank", "sec.gov", "u.s. securities and exchange commission",
    "bmv", "bolsa mexicana de valores",
]

# Medios con buena trayectoria en economía: suben un poco la prioridad.
FUENTES_CONFIABLES = [
    "el economista", "el financiero", "expansión", "reuters", "bloomberg", "bloomberg línea",
    "associated press", "afp", "forbes méxico", "animal político", "la jornada", "milenio",
    "financial times", "the wall street journal", "cnbc", "the economist", "barron's", "marketwatch",
]

# Palabras que suelen anunciar una historia con tensión (y buen gancho).
PALABRAS_GANCHO = {
    "sorprende": 1.0, "récord": 1.0, "histórico": 1.0, "inesperad": 1.0,
    "quiebra": 1.5, "fraude": 1.5, "estafa": 1.5, "hackeo": 1.5, "hack": 1.0,
    "revoca": 1.5, "intervien": 1.0, "congela": 1.0, "demanda": 0.5,
    "recorte": 1.0, "recorta": 1.0, "dispara": 1.0, "desploma": 1.0,
    "ahorradores": 1.0, "tu dinero": 1.0, "aguinaldo": 1.0, "crédito": 0.5,
    "tarjeta": 0.5, "impuesto": 0.5, "comisión": 0.5,
    "salida a bolsa": 1.5, "ipo": 1.5, "valuación": 1.0, "valuation": 1.0, "burbuja": 1.0, "bubble": 1.0,
    "plunge": 1.0, "soar": 1.0, "record": 0.5,
}

# Señales de que la historia toca a México directamente.
PALABRAS_MEXICO = ["méxico", "mexicano", "mexicana", "banxico", "peso", "inegi", "sat ", "cdmx",
                   "sheinbaum", "hacienda", "pemex", "cfe", "t-mec", "bmv"]

# Notas de rutina que inflan resultados. Bajan la prioridad (no desaparecen).
RUIDO = ["precio del dólar hoy", "tipo de cambio hoy", "así amanece", "dólar hoy", "a cuánto está el dólar",
         "horóscopo", "lotería", "clima hoy", "cuánto cuesta el dólar",
         "predicción del precio", "predicción de precio", "price prediction", "pronóstico del precio",
         "mejores criptomonedas para invertir", "criptomonedas para invertir", "cuánto vale bitcoin hoy",
         "precio de bitcoin hoy", "bitcoin hoy",
         "stock to buy", "stocks to buy", "should you buy", "is it a buy", "acciones para comprar"]

# Temas que suelen dar para video largo (si hay buena cobertura).
TEMAS_LARGO = {"tasas", "inflacion", "proteccion", "finanzas_publicas", "comercio", "mundo", "cripto", "bolsa"}
