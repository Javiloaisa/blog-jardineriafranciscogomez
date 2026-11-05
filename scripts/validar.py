#!/usr/bin/env python3
"""Comprueba que todos los artículos de articulos/ cumplen el formato. Sale con 1 si hay errores."""
import sys

from articulos import validar_todos

articulos, errores = validar_todos()
if errores:
    print("Errores en los artículos:")
    for e in errores:
        print(f"  - {e}")
    sys.exit(1)
print(f"OK: {len(articulos)} artículos válidos")
