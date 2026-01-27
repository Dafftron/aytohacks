#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar que todo está correctamente instalado
"""

import sys
import os

def test_imports():
    """Verifica que todas las librerías están instaladas"""
    print("=" * 60)
    print("VERIFICANDO INSTALACIÓN")
    print("=" * 60)

    libraries = [
        ('pandas', 'Manejo de Excel y DataFrames'),
        ('requests', 'Peticiones HTTP'),
        ('bs4', 'BeautifulSoup - Parseo HTML'),
        ('dns.resolver', 'Resolución DNS'),
        ('openpyxl', 'Lectura/escritura Excel')
    ]

    all_ok = True

    for lib, desc in libraries:
        try:
            __import__(lib)
            print(f"OK {lib:20} - {desc}")
        except ImportError as e:
            print(f"ERROR {lib:20} - ERROR: {e}")
            all_ok = False

    return all_ok

def test_config():
    """Verifica que el archivo de configuración funciona"""
    print("\n" + "=" * 60)
    print("VERIFICANDO CONFIGURACIÓN")
    print("=" * 60)

    try:
        from config import (BASE_DIR, DATOS_DIR, LOGS_DIR, RESULTADOS_DIR,
                           PDF_ADJUNTO, EXCEL_TOLEDO_COMPLETO)

        print(f"OK Directorio base: {BASE_DIR}")
        print(f"OK Directorio datos: {DATOS_DIR}")
        print(f"OK Directorio logs: {LOGS_DIR}")
        print(f"OK Directorio resultados: {RESULTADOS_DIR}")

        # Verificar que los directorios existen
        for dir_path in [DATOS_DIR, LOGS_DIR, RESULTADOS_DIR]:
            if os.path.exists(dir_path):
                print(f"  OK Existe: {os.path.basename(dir_path)}/")
            else:
                print(f"  ERROR NO existe: {os.path.basename(dir_path)}/")

        return True
    except Exception as e:
        print(f"ERROR Error al cargar configuración: {e}")
        return False

def test_pdf():
    """Verifica que el PDF existe"""
    print("\n" + "=" * 60)
    print("VERIFICANDO ARCHIVOS")
    print("=" * 60)

    from config import PDF_ADJUNTO

    if os.path.exists(PDF_ADJUNTO):
        size_mb = os.path.getsize(PDF_ADJUNTO) / (1024 * 1024)
        print(f"OK PDF encontrado: {os.path.basename(PDF_ADJUNTO)} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"ERROR PDF NO encontrado: {PDF_ADJUNTO}")
        return False

def test_provincias():
    """Verifica archivos de provincias"""
    from config import PROVINCIAS_DIR

    if os.path.exists(PROVINCIAS_DIR):
        xlsx_files = [f for f in os.listdir(PROVINCIAS_DIR) if f.endswith('.xlsx')]
        print(f"OK Carpeta provincias: {len(xlsx_files)} archivos Excel")
        return True
    else:
        print(f"ERROR Carpeta provincias NO encontrada")
        return False

def main():
    """Ejecuta todas las verificaciones"""
    print("\n")
    print("=" * 60)
    print("         AYTOHACKS - VERIFICACION DE INSTALACION")
    print("=" * 60)
    print("")

    results = []
    results.append(test_imports())
    results.append(test_config())
    results.append(test_pdf())
    results.append(test_provincias())

    print("\n" + "=" * 60)
    if all(results):
        print("OKOKOK TODO CORRECTO - El sistema está listo para usar OKOKOK")
        print("=" * 60)
        print("\nPróximos pasos:")
        print("  1. Lee el archivo INSTRUCCIONES.md")
        print("  2. Ejecuta: python completar_todos.py")
        print("  3. O ejecuta: python enviar_correos_thunderbird.py")
    else:
        print("ERRORERRORERROR HAY PROBLEMAS - Revisa los errores arriba ERRORERRORERROR")
        print("=" * 60)

    print("\n")

if __name__ == "__main__":
    main()
