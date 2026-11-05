#!/usr/bin/env python3
"""
Publica en WordPress los artículos de articulos/ que todavía no estén en publicados.json.

- Fecha futura  -> entrada programada (status=future) para esa fecha.
- Fecha pasada  -> se publica en el momento.
- Imagen destacada de Pexels (si hay PEXELS_API_KEY).
- Título SEO, meta descripción y keyword de Yoast (requiere el snippet wordpress/yoast-rest-meta.php).

Variables de entorno: WP_USER, WP_APP_PASSWORD, PEXELS_API_KEY (opcional), WP_URL (opcional).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import random
import re
import sys

import markdown
import requests

from articulos import RAIZ, SITE, errores_de, leer, rutas

ESTADO = RAIZ / "publicados.json"
CATEGORIA = "Consejos de jardinería"
WP_URL = os.getenv("WP_URL", SITE).rstrip("/")
API = f"{WP_URL}/wp-json/wp/v2"

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
    if ESTADO.exists():
        e = json.loads(ESTADO.read_text(encoding="utf-8"))
    else:
        e = {}
    e.setdefault("entradas", {})
    e.setdefault("fotos_usadas", [])
    return e


def guardar_estado(e: dict) -> None:
    ESTADO.write_text(json.dumps(e, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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

    def existente(self, slug: str):
        r = self.ok(self.s.get(f"{API}/posts", params={
            "slug": slug, "status": "publish,future,draft,pending,private", "_fields": "id,link,status"}, timeout=30))
        return r[0] if r else None

    def subir_imagen(self, datos: bytes, nombre: str, alt: str, pie: str) -> int:
        m = self.ok(self.s.post(f"{API}/media", data=datos, timeout=120, headers={
            "Content-Disposition": f'attachment; filename="{nombre}"', "Content-Type": "image/jpeg"}))
        self.ok(self.s.post(f"{API}/media/{m['id']}", json={"alt_text": alt, "caption": pie, "title": alt}, timeout=30))
        return m["id"]

    def crear(self, payload: dict) -> dict:
        return self.ok(self.s.post(f"{API}/posts", json=payload, timeout=60))


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
    pendientes = [p for p in rutas() if p.name not in estado["entradas"]]
    if not pendientes:
        print("Nada que publicar")
        escribir_resumen(["Nada que publicar: todos los artículos ya están en WordPress."])
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
    resumen.append("| Artículo | Estado | Fecha |\n|---|---|---|")

    for ruta in pendientes:
        try:
            a = leer(ruta)
            errores = errores_de(a)
            if errores:
                raise ValueError("; ".join(errores))

            previo = wp.existente(a["slug"])
            if previo:
                estado["entradas"][ruta.name] = {"post_id": previo["id"], "enlace": previo["link"],
                                                 "estado": previo["status"], "fecha": a["fecha"]}
                guardar_estado(estado)
                resumen.append(f"| {a['titulo']} | ya existía ({previo['status']}) | {a['fecha']} |")
                continue

            payload = {
                "title": a["titulo"],
                "slug": a["slug"],
                "content": markdown.markdown(a["cuerpo"], extensions=["extra", "sane_lists"]),
                "excerpt": a["extracto"],
                "categories": [cat],
                "comment_status": "closed",
                "meta": {
                    "_yoast_wpseo_title": a["meta_titulo"],
                    "_yoast_wpseo_metadesc": a["meta_descripcion"],
                    "_yoast_wpseo_focuskw": a["keyword"],
                },
            }
            fecha_utc = a["fecha_dt"].astimezone(dt.timezone.utc)
            if fecha_utc > ahora + dt.timedelta(minutes=10):
                payload["status"] = "future"
                payload["date_gmt"] = fecha_utc.strftime("%Y-%m-%dT%H:%M:%S")
            else:
                payload["status"] = "publish"

            foto = foto_pexels(a["imagen_busqueda"], estado["fotos_usadas"])
            if foto:
                payload["featured_media"] = wp.subir_imagen(foto["datos"], f"{a['slug']}.jpg", a["imagen_alt"], foto["pie"])
                estado["fotos_usadas"].append(foto["id"])

            post = wp.crear(payload)
            if "_yoast_wpseo_metadesc" not in (post.get("meta") or {}):
                print(f"::warning::{ruta.name}: Yoast no ha recibido los metadatos. ¿Está activo el snippet yoast-rest-meta?")
            estado["entradas"][ruta.name] = {"post_id": post["id"], "enlace": post["link"],
                                             "estado": post["status"], "fecha": a["fecha"]}
            guardar_estado(estado)
            resumen.append(f"| [{a['titulo']}]({post['link']}) | {post['status']} | {a['fecha']} |")
            print(f"{ruta.name}: {post['status']} (id {post['id']})")
        except Exception as ex:  # noqa: BLE001
            fallos += 1
            print(f"::error::{ruta.name}: {ex}")
            motivo = re.sub(r"[|\n]", " ", str(ex))[:200]
            resumen.append(f"| {ruta.name} | ERROR: {motivo} | |")

    escribir_resumen(["## Publicación en WordPress", *resumen])
    if fallos:
        sys.exit(1)


if __name__ == "__main__":
    main()
