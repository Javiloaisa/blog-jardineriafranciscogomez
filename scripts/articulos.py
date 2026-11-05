"""Lectura y validación de los artículos de articulos/*.md."""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml

TZ = ZoneInfo("Europe/Madrid")
RAIZ = Path(__file__).resolve().parent.parent
DIR_ARTICULOS = RAIZ / "articulos"
TEMAS = RAIZ / "temas.json"
SITE = "https://jardineriafranciscogomez.com"

CAMPOS = ["tema", "fecha", "titulo", "slug", "meta_titulo", "meta_descripcion",
          "keyword", "extracto", "imagen_busqueda", "imagen_alt"]
DIAS_PUBLICACION = {1: "martes", 4: "viernes"}  # weekday() de Python
HORA_PUBLICACION = (9, 0)


def leer(path: Path) -> dict:
    texto = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    if not m:
        raise ValueError("falta la cabecera YAML entre líneas ---")
    meta = yaml.safe_load(m.group(1)) or {}
    meta = {k: (v.strip() if isinstance(v, str) else v) for k, v in meta.items()}
    meta["cuerpo"] = m.group(2).strip()
    meta["archivo"] = path.name
    meta["fecha_dt"] = parse_fecha(meta.get("fecha"))
    return meta


def parse_fecha(valor) -> dt.datetime:
    if isinstance(valor, dt.datetime):
        d = valor
    else:
        d = dt.datetime.strptime(str(valor).strip(), "%Y-%m-%d %H:%M")
    return d.replace(tzinfo=TZ) if d.tzinfo is None else d.astimezone(TZ)


def rutas() -> list[Path]:
    return sorted(DIR_ARTICULOS.glob("*.md"))


def ids_temas() -> set[str]:
    return {t["id"] for t in json.loads(TEMAS.read_text(encoding="utf-8"))}


def errores_de(a: dict) -> list[str]:
    e = []
    for c in CAMPOS:
        if not a.get(c):
            e.append(f"falta el campo «{c}»")
    if e:
        return e

    f = a["fecha_dt"]
    if f.weekday() not in DIAS_PUBLICACION:
        e.append(f"la fecha {f:%d/%m/%Y} no cae en martes ni viernes")
    if (f.hour, f.minute) != HORA_PUBLICACION:
        e.append("la hora debe ser 09:00")
    esperado = f"{f:%Y-%m-%d}-{a['slug']}.md"
    if a["archivo"] != esperado:
        e.append(f"el archivo debería llamarse {esperado}")

    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", a["slug"]) or len(a["slug"]) > 70:
        e.append("slug no válido (minúsculas, números y guiones, máx. 70)")
    if len(a["titulo"]) > 70:
        e.append(f"titulo demasiado largo ({len(a['titulo'])} > 70)")
    if len(a["meta_titulo"]) > 60:
        e.append(f"meta_titulo demasiado largo ({len(a['meta_titulo'])} > 60)")
    if not 120 <= len(a["meta_descripcion"]) <= 160:
        e.append(f"meta_descripcion debe tener 120-160 caracteres (tiene {len(a['meta_descripcion'])})")

    cuerpo = a["cuerpo"]
    palabras = len(re.findall(r"\w+", re.sub(r"\(https?://[^)]*\)", "", cuerpo)))
    if not 800 <= palabras <= 1700:
        e.append(f"el cuerpo tiene {palabras} palabras (debe estar entre 800 y 1700)")
    if re.search(r"^# ", cuerpo, re.M):
        e.append("el cuerpo no puede llevar H1 (# ); empieza en ##")
    if len(re.findall(r"^## ", cuerpo, re.M)) < 4:
        e.append("hacen falta al menos 4 secciones ##")
    if "## Preguntas frecuentes" not in cuerpo:
        e.append("falta la sección «## Preguntas frecuentes»")
    if f"{SITE}/servicio/" not in cuerpo:
        e.append("falta el enlace interno a una página de servicio")
    if "wa.me/34616779874" not in cuerpo:
        e.append("falta el enlace de WhatsApp en el cierre")
    if re.search(r"\bTODO\b|\bXXX\b|\[\.\.\.\]|\[…\]", cuerpo) or re.search(r"\[(inserta|completa|nombre|pon )", cuerpo, re.I):
        e.append("hay huecos sin rellenar")
    return e


def validar_todos() -> tuple[list[dict], list[str]]:
    articulos, errores = [], []
    temas = ids_temas()
    vistos = {"slug": {}, "fecha": {}, "tema": {}}
    for p in rutas():
        try:
            a = leer(p)
        except Exception as ex:  # noqa: BLE001
            errores.append(f"{p.name}: {ex}")
            continue
        for err in errores_de(a):
            errores.append(f"{p.name}: {err}")
        if a.get("tema") and a["tema"] not in temas:
            errores.append(f"{p.name}: el tema «{a['tema']}» no está en temas.json")
        for campo in vistos:
            valor = a["fecha_dt"].date() if campo == "fecha" else a.get(campo)
            if valor in vistos[campo]:
                errores.append(f"{p.name}: {campo} repetido con {vistos[campo][valor]}")
            vistos[campo][valor] = p.name
        articulos.append(a)
    return articulos, errores
