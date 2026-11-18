"""Lectura y validación de los artículos de articulos/*.md (español) y articulos/en/*.md (inglés)."""
from __future__ import annotations

import datetime as dt
import json
import re
import unicodedata
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

TZ = ZoneInfo("Europe/Madrid")
RAIZ = Path(__file__).resolve().parent.parent
DIR_ARTICULOS = RAIZ / "articulos"
TEMAS = RAIZ / "temas.json"
SITE = "https://jardineriafranciscogomez.com"
IDIOMAS = ("es", "en")

CAMPOS = ["tema", "fecha", "titulo", "slug", "meta_titulo", "meta_descripcion",
          "keyword", "keywords_secundarias", "extracto", "imagen_busqueda", "imagen_alt"]
DIAS_PUBLICACION = {"es": {1: "martes", 4: "viernes"}, "en": {3: "jueves"}}  # weekday() de Python
HORA_PUBLICACION = (9, 0)

# Enlaces internos a otros artículos del blog: [ancla](articulo:slug)
RE_ENLACE_ARTICULO = re.compile(r"\]\(articulo:([a-z0-9-]+)\)")
RE_ENLACE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
PAGINAS_PERMITIDAS = {
    f"{SITE}/",
    f"{SITE}/servicios/",
    f"{SITE}/contacto/",
    f"{SITE}/quienes-somos/",
    f"{SITE}/proyectos/",
    f"{SITE}/jardinero-en-calpe/",
    f"{SITE}/jardinero-en-moraira/",
    f"{SITE}/servicio/mantenimiento-de-comunidades/",
    f"{SITE}/servicio/mantenimiento-de-jardines/",
    f"{SITE}/servicio/construccion-de-jardines-con-rocallas-fuentes-cesped/",
    f"{SITE}/servicio/poda-de-arboles-y-palmeras/",
    f"{SITE}/servicio/tratamiento-del-picudo/",
    f"{SITE}/servicio/instalacion-de-sistemas-de-riego/",
    f"{SITE}/servicio/limpieza-de-parcelas/",
}
PAGINAS_PERMITIDAS_EN = {
    f"{SITE}/en/",
    f"{SITE}/en/services/",
    f"{SITE}/en/contact/",
    f"{SITE}/en/about-us/",
    f"{SITE}/en/projects/",
    f"{SITE}/en/gardener-calpe/",
    f"{SITE}/en/gardener-moraira/",
    f"{SITE}/en/servicio/community-garden-maintenance/",
    f"{SITE}/en/servicio/garden-maintenance/",
    f"{SITE}/en/servicio/garden-design-and-landscaping/",
    f"{SITE}/en/servicio/tree-and-palm-pruning/",
    f"{SITE}/en/servicio/red-palm-weevil-treatment/",
    f"{SITE}/en/servicio/irrigation-installation/",
    f"{SITE}/en/servicio/land-clearing/",
}
WHATSAPP = "https://wa.me/34616779874"
ANCLAS_PROHIBIDAS = {"aquí", "aqui", "este artículo", "este enlace", "pincha aquí", "haz clic aquí", "más información", "leer más"}
ANCLAS_PROHIBIDAS_EN = {"here", "click here", "read more", "this article", "more information", "this link"}

# Lo que cambia según el idioma del artículo
POR_IDIOMA = {
    "es": {
        "dir": DIR_ARTICULOS,
        "temas": TEMAS,
        "paginas": PAGINAS_PERMITIDAS,
        "servicio": f"{SITE}/servicio/",
        "anclas": ANCLAS_PROHIBIDAS,
        "faq": "Preguntas frecuentes",
        "guia": "docs/redaccion.md",
        "permalink": SITE + "/{slug}/",
    },
    "en": {
        "dir": DIR_ARTICULOS / "en",
        "temas": RAIZ / "temas_en.json",
        "paginas": PAGINAS_PERMITIDAS_EN,
        "servicio": f"{SITE}/en/servicio/",
        "anclas": ANCLAS_PROHIBIDAS | ANCLAS_PROHIBIDAS_EN,
        "faq": "Frequently asked questions",
        "guia": "docs/writing-en.md",
        "permalink": SITE + "/en/{slug}/",
    },
}


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9 ]+", " ", texto)


def leer(path: Path) -> dict:
    texto = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    if not m:
        raise ValueError("falta la cabecera YAML entre líneas ---")
    meta = yaml.safe_load(m.group(1)) or {}
    meta = {k: (v.strip() if isinstance(v, str) else v) for k, v in meta.items()}
    meta["cuerpo"] = m.group(2).strip()
    meta["archivo"] = path.name
    # Ruta relativa a articulos/ («2026-11-10-x.md» o «en/2026-12-03-x.md»): clave en publicados.json
    meta["ruta"] = path.relative_to(DIR_ARTICULOS).as_posix()
    meta["idioma_dir"] = "en" if path.parent == POR_IDIOMA["en"]["dir"] else "es"
    meta["idioma"] = str(meta.get("idioma") or "es").strip()
    meta["fecha_dt"] = parse_fecha(meta.get("fecha"))
    return meta


def parse_fecha(valor) -> dt.datetime:
    if isinstance(valor, dt.datetime):
        d = valor
    else:
        d = dt.datetime.strptime(str(valor).strip(), "%Y-%m-%d %H:%M")
    return d.replace(tzinfo=TZ) if d.tzinfo is None else d.astimezone(TZ)


def rutas() -> list[Path]:
    return sorted(DIR_ARTICULOS.glob("*.md")) + sorted(POR_IDIOMA["en"]["dir"].glob("*.md"))


def temas(idioma: str = "es") -> list[dict]:
    ruta = POR_IDIOMA[idioma]["temas"]
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else []


def ids_temas(idioma: str = "es") -> set[str]:
    return {t["id"] for t in temas(idioma)}


def permalink(a: dict) -> str:
    return POR_IDIOMA[a.get("idioma", "es")]["permalink"].format(slug=a["slug"])


def preguntas_frecuentes(cuerpo: str, idioma: str = "es") -> list[tuple[str, str]]:
    """Pares (pregunta, respuesta) de la sección ## Preguntas frecuentes (en inglés, Frequently asked questions)."""
    titulo = re.escape(POR_IDIOMA[idioma]["faq"])
    m = re.search(rf"^## {titulo}\s*\n(.*?)(?=^## |\Z)", cuerpo, re.M | re.S)
    if not m:
        return []
    pares = []
    for bloque in re.split(r"^### ", m.group(1), flags=re.M)[1:]:
        pregunta, _, respuesta = bloque.partition("\n")
        respuesta = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", respuesta).strip()
        respuesta = re.sub(r"[*_`]", "", respuesta)
        if pregunta.strip() and respuesta:
            pares.append((pregunta.strip(), " ".join(respuesta.split())))
    return pares


def primer_parrafo(cuerpo: str) -> str:
    return cuerpo.split("\n\n", 1)[0].strip()


def errores_de(a: dict, todos: dict[str, dict] | None = None) -> list[str]:
    """Errores de un artículo. `todos` = {slug: artículo} para comprobar enlaces entre artículos."""
    e = []
    for c in CAMPOS:
        if not a.get(c):
            e.append(f"falta el campo «{c}»")
    if e:
        return e

    idioma = a["idioma"]
    if idioma not in IDIOMAS:
        return [f"idioma «{idioma}» no válido (pon «en» o quítalo para español)"]
    if idioma != a["idioma_dir"]:
        return ["los artículos en inglés van en articulos/en/ con «idioma: en»; los de español, en articulos/ sin idioma"]
    cfg = POR_IDIOMA[idioma]

    f = a["fecha_dt"]
    dias = DIAS_PUBLICACION[idioma]
    if f.weekday() not in dias:
        e.append(f"la fecha {f:%d/%m/%Y} no cae en {' ni '.join(dias.values())}")
    if (f.hour, f.minute) != HORA_PUBLICACION:
        e.append("la hora debe ser 09:00")
    esperado = f"{f:%Y-%m-%d}-{a['slug']}.md"
    if a["archivo"] != esperado:
        e.append(f"el archivo debería llamarse {esperado}")

    # --- SEO de la cabecera
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a["slug"]) or len(a["slug"]) > 60:
        e.append("slug no válido (minúsculas, números y guiones, máx. 60)")
    if len(a["titulo"]) > 70:
        e.append(f"titulo demasiado largo ({len(a['titulo'])} > 70)")
    if len(a["meta_titulo"]) > 60:
        e.append(f"meta_titulo demasiado largo ({len(a['meta_titulo'])} > 60)")
    if not 120 <= len(a["meta_descripcion"]) <= 158:
        e.append(f"meta_descripcion debe tener 120-158 caracteres (tiene {len(a['meta_descripcion'])})")
    if not isinstance(a["keywords_secundarias"], list) or not 2 <= len(a["keywords_secundarias"]) <= 6:
        e.append("keywords_secundarias debe ser una lista de 2 a 6 búsquedas")

    kw = [w for w in normalizar(a["keyword"]).split() if len(w) > 2]
    def contiene_kw(texto: str) -> bool:
        t = normalizar(texto)
        return all(re.search(rf"\b{re.escape(w)}", t) for w in kw)

    if not contiene_kw(a["titulo"]):
        e.append("la keyword no está en el titulo")
    if not contiene_kw(a["meta_descripcion"]):
        e.append("la keyword no está en la meta_descripcion")

    # --- Cuerpo
    cuerpo = a["cuerpo"]
    texto_plano = re.sub(r"\]\([^)]*\)", "]", cuerpo)
    palabras = len(re.findall(r"\w+", texto_plano))
    if not 900 <= palabras <= 1800:
        e.append(f"el cuerpo tiene {palabras} palabras (debe estar entre 900 y 1800)")
    if re.search(r"^# ", cuerpo, re.M):
        e.append("el cuerpo no puede llevar H1 (# ); empieza en ##")

    intro = primer_parrafo(cuerpo)
    n_intro = len(re.findall(r"\w+", re.sub(r"\]\([^)]*\)", "]", intro)))
    if intro.startswith("#") or not 35 <= n_intro <= 90:
        e.append(f"el primer párrafo debe ser la respuesta directa, de 35 a 90 palabras (tiene {n_intro})")
    elif not contiene_kw(" ".join(texto_plano.split()[:120])):
        e.append("la keyword no aparece en las primeras 100 palabras")

    h2 = re.findall(r"^## (.+)$", cuerpo, re.M)
    if len(h2) < 5:
        e.append("hacen falta al menos 5 secciones ## (incluidas las preguntas frecuentes)")
    if not any(contiene_kw(t) for t in h2):
        e.append("la keyword no aparece en ningún ##")
    if not re.search(r"^(\d+\. |\| )", cuerpo, re.M):
        e.append("hace falta al menos una lista numerada o una tabla")

    faq = preguntas_frecuentes(cuerpo, idioma)
    if not 3 <= len(faq) <= 5:
        e.append(f"«## {cfg['faq']}» debe tener de 3 a 5 preguntas ### (tiene {len(faq)})")
    for pregunta, _ in faq:
        if not pregunta.endswith("?"):
            e.append(f"la pregunta frecuente «{pregunta}» debe terminar en ?")

    # --- Enlaces
    enlaces = RE_ENLACE.findall(cuerpo)
    for ancla, url in enlaces:
        if normalizar(ancla).strip() in {normalizar(x).strip() for x in cfg["anclas"]}:
            e.append(f"ancla poco descriptiva: «{ancla}»")
        if url.startswith(SITE) and url not in cfg["paginas"]:
            e.append(f"enlace interno desconocido: {url} (usa las URLs de {cfg['guia']})")
        elif url.startswith("http") and not url.startswith(SITE) and url != WHATSAPP:
            e.append(f"enlace externo no permitido: {url}")
    urls = [u for _, u in enlaces]
    if not any(u.startswith(cfg["servicio"]) for u in urls):
        e.append("falta el enlace a la página del servicio")
    if WHATSAPP not in urls:
        e.append("falta el enlace de WhatsApp en el cierre")

    if todos is not None:
        anteriores = [x for x in todos.values() if x["fecha_dt"] < f and x["idioma"] == idioma]
        destinos = RE_ENLACE_ARTICULO.findall(cuerpo)
        ahora = dt.datetime.now(TZ)
        for slug in destinos:
            destino = todos.get(slug)
            if not destino:
                e.append(f"enlace a un artículo que no existe: articulo:{slug}")
            elif destino["idioma"] != idioma:
                e.append(f"enlace a articulo:{slug}, que está en otro idioma (solo se enlazan artículos del mismo idioma)")
            elif slug == a["slug"]:
                e.append("el artículo se enlaza a sí mismo")
            elif destino["fecha_dt"] >= f and destino["fecha_dt"] > ahora:
                e.append(f"enlace a articulo:{slug}, que aún no estará publicado ese día")
        minimo = min(2, len(anteriores))
        if len(set(destinos)) < minimo:
            e.append(f"hacen falta al menos {minimo} enlaces a otros artículos del blog (articulo:slug)")

    if len(set(urls)) > 9:
        e.append("demasiados enlaces (máx. 9 distintos)")
    if re.search(r"\bTODO\b|\bXXX\b|\[\.\.\.\]|\[…\]", cuerpo) or re.search(r"\[(inserta|completa|nombre|pon )", cuerpo, re.I):
        e.append("hay huecos sin rellenar")
    return e


def cargar_todos() -> tuple[dict[str, dict], list[str]]:
    todos, errores = {}, []
    for p in rutas():
        try:
            a = leer(p)
            clave = a.get("slug") or p.stem
            if clave in todos:
                errores.append(f"{a['ruta']}: slug repetido con {todos[clave]['ruta']}")
                continue
            todos[clave] = a
        except Exception as ex:  # noqa: BLE001
            errores.append(f"{p.name}: {ex}")
    return todos, errores


def validar_todos() -> tuple[list[dict], list[str]]:
    todos, errores = cargar_todos()
    ids = {i: ids_temas(i) for i in IDIOMAS}
    vistos = {"slug": {}, "fecha": {}, "tema": {}}
    for a in todos.values():
        for err in errores_de(a, todos):
            errores.append(f"{a['ruta']}: {err}")
        idioma = a["idioma"] if a["idioma"] in IDIOMAS else "es"
        if a.get("tema") and a["tema"] not in ids[idioma]:
            errores.append(f"{a['ruta']}: el tema «{a['tema']}» no está en {POR_IDIOMA[idioma]['temas'].name}")
        for campo in vistos:
            valor = a["fecha_dt"].date() if campo == "fecha" else a.get(campo)
            if campo != "slug":  # fecha y tema, por idioma; el slug es único en todo WordPress
                valor = (idioma, valor)
            if valor in vistos[campo]:
                errores.append(f"{a['ruta']}: {campo} repetido con {vistos[campo][valor]}")
            vistos[campo][valor] = a["ruta"]
    return list(todos.values()), errores
