#!/usr/bin/env python3
"""
Sincroniza los artículos de articulos/ con WordPress.

- Artículo nuevo        -> crea la entrada: programada (status=future) si su fecha es futura,
                           publicada si ya pasó.
- Artículo modificado   -> actualiza la entrada existente (texto, título, extracto, Yoast, FAQ),
                           sin tocar su fecha ni su estado. Así se añaden enlaces a artículos anteriores.
- Sin imagen destacada  -> busca una en Pexels (si hay PEXELS_API_KEY).
- Enlaces [ancla](articulo:slug) -> se convierten en la URL real del artículo.
- Preguntas frecuentes  -> se guardan como datos estructurados FAQPage (los imprime el mu-plugin).

Variables de entorno: WP_USER, WP_APP_PASSWORD, PEXELS_API_KEY (opcional), WP_URL (opcional).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import random
import re
import sys

import markdown
import requests

from articulos import RAIZ, RE_ENLACE_ARTICULO, SITE, cargar_todos, errores_de, preguntas_frecuentes

ESTADO = RAIZ / "publicados.json"
CATEGORIA = "Consejos de jardinería"
WP_URL = os.getenv("WP_URL", SITE).rstrip("/")
API = f"{WP_URL}/wp-json/wp/v2"
PERMALINK = WP_URL + "/{slug}/"  # estructura de enlaces permanentes /%postname%/
VERSION_FORMATO = "2"  # cambiarlo fuerza a reenviar todos los artículos

resumen: list[str] = []


def salir(msg: str) -> None:
    print(f"::error::{msg}")
    escribir_resumen([f"**Error:** {msg}"])
    sys.exit(1)


def escribir_resumen(lineas: list[str]) -> None:
    ruta = os.getenv("GITHUB_STEP_SUMMARY")
    if ruta:
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("\n".join(lineas) + "\n")


def cargar_estado() -> dict:
    e = json.loads(ESTADO.read_text(encoding="utf-8")) if ESTADO.exists() else {}
    e.setdefault("entradas", {})
    e.setdefault("fotos_usadas", [])
    return e


def guardar_estado(e: dict) -> None:
    ESTADO.write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def huella(ruta) -> str:
    return hashlib.sha256((VERSION_FORMATO + ruta.read_text(encoding="utf-8")).encode()).hexdigest()[:16]


def html_de(a: dict) -> str:
    cuerpo = RE_ENLACE_ARTICULO.sub(lambda m: f"]({PERMALINK.format(slug=m.group(1))})", a["cuerpo"])
    return markdown.markdown(cuerpo, extensions=["extra", "sane_lists"])


def faq_schema(a: dict) -> str:
    pares = preguntas_frecuentes(a["cuerpo"])
    if not pares:
        return ""
    url = PERMALINK.format(slug=a["slug"])
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": f"{url}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}}
            for q, r in pares
        ],
    }, ensure_ascii=False)


class WP:
    def __init__(self, usuario: str, clave: str):
        self.s = requests.Session()
        self.s.auth = (usuario, clave)
        self.s.headers["User-Agent"] = "blog-jardineria-github/1.0"

    def ok(self, r: requests.Response):
        if r.status_code >= 400:
            raise RuntimeError(f"WordPress {r.status_code} en {r.request.method} {r.url}: {r.text[:400]}")
        return r.json()

    def yo(self):
        return self.ok(self.s.get(f"{API}/users/me", timeout=30))

    def categoria(self, nombre: str) -> int:
        for c in self.ok(self.s.get(f"{API}/categories", params={"search": nombre, "per_page": 100}, timeout=30)):
            if c["name"].strip().lower() == nombre.lower():
                return c["id"]
        return self.ok(self.s.post(f"{API}/categories", json={"name": nombre}, timeout=30))["id"]

    def por_slug(self, slug: str):
        r = self.ok(self.s.get(f"{API}/posts", params={
            "slug": slug, "status": "publish,future,draft,pending,private",
            "_fields": "id,link,status,featured_media"}, timeout=30))
        return r[0] if r else None

    def entrada(self, post_id: int):
        r = self.s.get(f"{API}/posts/{post_id}", params={"context": "edit", "_fields": "id,link,status,featured_media"}, timeout=30)
        return None if r.status_code == 404 else self.ok(r)

    def subir_imagen(self, datos: bytes, nombre: str, alt: str, pie: str) -> int:
        m = self.ok(self.s.post(f"{API}/media", data=datos, timeout=120, headers={
            "Content-Disposition": f'attachment; filename="{nombre}"', "Content-Type": "image/jpeg"}))
        self.ok(self.s.post(f"{API}/media/{m['id']}", json={"alt_text": alt, "caption": pie, "title": alt}, timeout=30))
        return m["id"]

    def crear(self, payload: dict) -> dict:
        return self.ok(self.s.post(f"{API}/posts", json=payload, timeout=60))

    def actualizar(self, post_id: int, payload: dict) -> dict:
        return self.ok(self.s.post(f"{API}/posts/{post_id}", json=payload, timeout=60))


def foto_pexels(consulta: str, usadas: list[int]):
    clave = os.getenv("PEXELS_API_KEY", "").strip()
    if not clave:
        return None
    for q in (consulta, "mediterranean garden", "gardening"):
        r = requests.get("https://api.pexels.com/v1/search", timeout=30, headers={"Authorization": clave},
                         params={"query": q, "per_page": 30, "orientation": "landscape"})
        r.raise_for_status()
        fotos = [p for p in r.json().get("photos", []) if p["id"] not in usadas]
        if fotos:
            p = random.choice(fotos[:10])
            img = requests.get(p["src"]["large2x"], timeout=60)
            img.raise_for_status()
            return {"id": p["id"], "datos": img.content, "pie": f"Foto: {p['photographer']} en Pexels"}
    return None


def main() -> None:
    usuario, clave = os.getenv("WP_USER", "").strip(), os.getenv("WP_APP_PASSWORD", "").strip()
    if not usuario or not clave:
        salir("Faltan los secrets WP_USER y/o WP_APP_PASSWORD en el repositorio (Settings → Secrets → Actions).")

    estado = cargar_estado()
    todos, errores_lectura = cargar_todos()
    for err in errores_lectura:
        print(f"::error::{err}")

    hay_pexels = bool(os.getenv("PEXELS_API_KEY", "").strip())
    pendientes = []
    for a in todos.values():
        ruta = RAIZ / "articulos" / a["archivo"]
        reg = estado["entradas"].get(a["archivo"])
        cambiado = not reg or reg.get("huella") != huella(ruta)
        sin_imagen = reg and not reg.get("imagen") and hay_pexels
        if cambiado or sin_imagen:
            pendientes.append((a, ruta, reg))

    if not pendientes:
        print("Nada que publicar ni actualizar")
        escribir_resumen(["Nada que publicar ni actualizar: WordPress está al día."])
        return

    wp = WP(usuario, clave)
    try:
        yo = wp.yo()
    except RuntimeError as ex:
        salir(f"No se puede conectar con WordPress como «{usuario}»: {ex}")
    print(f"Conectado como {yo['name']}")
    cat = wp.categoria(CATEGORIA)
    ahora = dt.datetime.now(dt.timezone.utc)
    fallos = 0
    resumen.append("| Artículo | Acción | Estado | Fecha |\n|---|---|---|---|")

    for a, ruta, reg in sorted(pendientes, key=lambda x: x[0]["fecha_dt"]):
        try:
            errores = errores_de(a, todos)
            if errores:
                raise ValueError("; ".join(errores))

            payload = {
                "title": a["titulo"],
                "content": html_de(a),
                "excerpt": a["extracto"],
                "categories": [cat],
                "meta": {
                    "_yoast_wpseo_title": a["meta_titulo"],
                    "_yoast_wpseo_metadesc": a["meta_descripcion"],
                    "_yoast_wpseo_focuskw": a["keyword"],
                    "_jfg_faq_schema": faq_schema(a),
                },
            }

            existente = wp.entrada(reg["post_id"]) if reg else None
            if not existente:
                existente = wp.por_slug(a["slug"])

            if not existente or not existente.get("featured_media"):
                foto = foto_pexels(a["imagen_busqueda"], estado["fotos_usadas"])
                if foto:
                    payload["featured_media"] = wp.subir_imagen(foto["datos"], f"{a['slug']}.jpg", a["imagen_alt"], foto["pie"])
                    estado["fotos_usadas"].append(foto["id"])

            if existente:
                post = wp.actualizar(existente["id"], payload)
                accion = "actualizada"
            else:
                payload.update({"slug": a["slug"], "comment_status": "closed"})
                fecha_utc = a["fecha_dt"].astimezone(dt.timezone.utc)
                if fecha_utc > ahora + dt.timedelta(minutes=10):
                    payload["status"] = "future"
                    payload["date_gmt"] = fecha_utc.strftime("%Y-%m-%dT%H:%M:%S")
                else:
                    payload["status"] = "publish"
                post = wp.crear(payload)
                accion = "creada"

            meta = post.get("meta") or {}
            if "_yoast_wpseo_metadesc" not in meta or "_jfg_faq_schema" not in meta:
                print(f"::warning::{ruta.name}: WordPress no ha guardado los datos de Yoast/FAQ. ¿Está subido wordpress/yoast-rest-meta.php a mu-plugins?")
                yoast_ok = False
            else:
                yoast_ok = True

            estado["entradas"][ruta.name] = {
                "post_id": post["id"],
                "enlace": PERMALINK.format(slug=a["slug"]),
                "estado": post["status"],
                "fecha": a["fecha"],
                "imagen": bool(post.get("featured_media")),
                # Si Yoast no recibió los datos, no se guarda la huella: se reintentará en la próxima ejecución
                "huella": huella(ruta) if yoast_ok else "",
            }
            guardar_estado(estado)
            resumen.append(f"| [{a['titulo']}]({PERMALINK.format(slug=a['slug'])}) | {accion} | {post['status']} | {a['fecha']} |")
            print(f"{ruta.name}: {accion} ({post['status']}, id {post['id']})")
        except Exception as ex:  # noqa: BLE001
            fallos += 1
            print(f"::error::{ruta.name}: {ex}")
            motivo = re.sub(r"[|\n]", " ", str(ex))[:200]
            resumen.append(f"| {ruta.name} | ERROR: {motivo} | | |")

    escribir_resumen(["## Sincronización con WordPress", *resumen])
    if fallos:
        sys.exit(1)


if __name__ == "__main__":
    main()
