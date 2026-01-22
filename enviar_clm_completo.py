#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para enviar correos a todas las provincias de CLM en secuencia
Ejecuta: Toledo -> Ciudad Real -> Cuenca
"""

import subprocess
import sys

provincias = ['Toledo', 'Ciudad Real', 'Cuenca']

for provincia in provincias:
    print(f"\n{'='*60}")
    print(f"INICIANDO ENVIOS: {provincia}")
    print(f"{'='*60}\n")

    resultado = subprocess.run(
        [sys.executable, 'enviar_verificado.py', provincia],
        cwd='D:/Aytohacks'
    )

    if resultado.returncode != 0:
        print(f"Error en {provincia}, continuando con la siguiente...")

    print(f"\n{'='*60}")
    print(f"COMPLETADO: {provincia}")
    print(f"{'='*60}\n")

print("\n" + "="*60)
print("TODAS LAS PROVINCIAS COMPLETADAS")
print("="*60)
