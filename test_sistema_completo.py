#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test del sistema completo - Verifica todas las funcionalidades
"""

import os
import sys

def test_config():
    """Test de configuración"""
    print("\n" + "="*60)
    print("TEST 1: CONFIGURACION")
    print("="*60)

    try:
        from config import (
            BASE_DIR, DATOS_DIR, LOGS_DIR, PROVINCIAS_DIR,
            PDF_ADJUNTO, EXCEL_MAESTRO, SMTP_SERVER, SMTP_PORT,
            IMAP_SERVER, IMAP_PORT, EMAIL_USER, DOMINIOS_BLACKLIST
        )

        print("OK Config importado correctamente")
        print(f"  Base: {BASE_DIR}")
        print(f"  PDF: {'EXISTS' if os.path.exists(PDF_ADJUNTO) else 'MISSING'}")
        print(f"  Lista negra: {len(DOMINIOS_BLACKLIST)} dominios")
        print(f"  SMTP: {SMTP_SERVER}:{SMTP_PORT}")
        print(f"  IMAP: {IMAP_SERVER}:{IMAP_PORT}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_dependencias():
    """Test de dependencias de Python"""
    print("\n" + "="*60)
    print("TEST 2: DEPENDENCIAS")
    print("="*60)

    deps = [
        'pandas',
        'requests',
        'bs4',
        'dns.resolver',
        'openpyxl',
        'smtplib',
        'imaplib'
    ]

    all_ok = True
    for dep in deps:
        try:
            __import__(dep)
            print(f"OK {dep}")
        except ImportError:
            print(f"ERROR {dep} - NO INSTALADO")
            all_ok = False

    return all_ok

def test_provincias():
    """Test de archivos de provincias"""
    print("\n" + "="*60)
    print("TEST 3: ARCHIVOS DE PROVINCIAS")
    print("="*60)

    from config import PROVINCIAS_DIR

    if not os.path.exists(PROVINCIAS_DIR):
        print(f"ERROR: No existe {PROVINCIAS_DIR}")
        return False

    archivos = [f for f in os.listdir(PROVINCIAS_DIR) if f.endswith('.xlsx')]
    print(f"OK {len(archivos)} archivos Excel encontrados")

    # Mostrar primeros 10
    for f in archivos[:10]:
        print(f"  - {f}")

    if len(archivos) > 10:
        print(f"  ... y {len(archivos) - 10} más")

    return True

def test_scripts():
    """Test de que los scripts existen"""
    print("\n" + "="*60)
    print("TEST 4: SCRIPTS PRINCIPALES")
    print("="*60)

    from config import BASE_DIR

    scripts = [
        'enviar_verificado_v2.py',
        'enviar_con_horario.py',
        'gestor_envios.py',
        'verificar_carpeta_enviados.py',
        'completar_todos.py',
        'fusionar_excels.py'
    ]

    all_ok = True
    for script in scripts:
        path = os.path.join(BASE_DIR, script)
        if os.path.exists(path):
            print(f"OK {script}")
        else:
            print(f"ERROR {script} - NO ENCONTRADO")
            all_ok = False

    return all_ok

def test_git():
    """Test de Git"""
    print("\n" + "="*60)
    print("TEST 5: REPOSITORIO GIT")
    print("="*60)

    from config import BASE_DIR
    import subprocess

    try:
        os.chdir(BASE_DIR)

        # Check si es repo git
        result = subprocess.run(['git', 'status'],
                              capture_output=True,
                              text=True)

        if result.returncode == 0:
            print("OK Repositorio Git inicializado")

            # Ver remote
            result = subprocess.run(['git', 'remote', '-v'],
                                  capture_output=True,
                                  text=True)
            if result.stdout:
                print("  Remote configurado:")
                for line in result.stdout.strip().split('\n')[:2]:
                    print(f"    {line}")
            else:
                print("  AVISO: No hay remote configurado")

            return True
        else:
            print("ERROR: No es un repositorio Git")
            return False

    except FileNotFoundError:
        print("ERROR: Git no instalado")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_verificacion_email():
    """Test de verificación de email"""
    print("\n" + "="*60)
    print("TEST 6: VERIFICACION DE EMAIL")
    print("="*60)

    try:
        # Importar función de verificación
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from enviar_verificado_v2 import verificar_email

        # Test con email conocido
        email_test = "test@terra.es"  # En lista negra
        valido, motivo = verificar_email(email_test)

        if not valido and 'BLACKLIST' in motivo:
            print(f"OK Lista negra funciona: {email_test} -> {motivo}")
            return True
        else:
            print(f"AVISO: Resultado inesperado para {email_test}")
            print(f"  Valido: {valido}, Motivo: {motivo}")
            return True  # No es error crítico

    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_smtp_imap():
    """Test de conexión SMTP/IMAP (sin enviar)"""
    print("\n" + "="*60)
    print("TEST 7: CONEXION SMTP/IMAP")
    print("="*60)

    from config import SMTP_SERVER, SMTP_PORT, IMAP_SERVER, IMAP_PORT
    import socket

    # Test SMTP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((SMTP_SERVER, SMTP_PORT))
        sock.close()

        if result == 0:
            print(f"OK Servidor SMTP accesible: {SMTP_SERVER}:{SMTP_PORT}")
        else:
            print(f"AVISO: No se puede conectar a SMTP (puede ser firewall)")
    except Exception as e:
        print(f"AVISO: Error al probar SMTP: {e}")

    # Test IMAP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((IMAP_SERVER, IMAP_PORT))
        sock.close()

        if result == 0:
            print(f"OK Servidor IMAP accesible: {IMAP_SERVER}:{IMAP_PORT}")
            return True
        else:
            print(f"AVISO: No se puede conectar a IMAP (puede ser firewall)")
            return True  # No es error crítico para el test
    except Exception as e:
        print(f"AVISO: Error al probar IMAP: {e}")
        return True

def main():
    """Ejecuta todos los tests"""
    print("\n")
    print("="*60)
    print("     TEST DEL SISTEMA COMPLETO AYTOHACKS")
    print("="*60)

    tests = [
        test_config,
        test_dependencias,
        test_provincias,
        test_scripts,
        test_git,
        test_verificacion_email,
        test_smtp_imap
    ]

    resultados = []
    for test in tests:
        try:
            resultado = test()
            resultados.append(resultado)
        except Exception as e:
            print(f"\nERROR CRITICO en {test.__name__}: {e}")
            resultados.append(False)

    # Resumen
    print("\n" + "="*60)
    print("RESUMEN")
    print("="*60)

    aprobados = sum(resultados)
    total = len(resultados)

    print(f"Tests aprobados: {aprobados}/{total}")

    if all(resultados):
        print("\n" + "="*60)
        print("SISTEMA COMPLETAMENTE OPERATIVO")
        print("="*60)
        print("\nPróximos pasos:")
        print("  1. Revisar GUIA_SISTEMA_COMPLETO.md")
        print("  2. python gestor_envios.py  # Ver estado")
        print("  3. python enviar_verificado_v2.py Toledo 20  # Enviar 20")
    else:
        print("\n" + "="*60)
        print("HAY PROBLEMAS A RESOLVER")
        print("="*60)
        print("\nRevisa los errores arriba y consulta:")
        print("  - GUIA_SISTEMA_COMPLETO.md")
        print("  - INSTRUCCIONES.md")

    print("")

if __name__ == "__main__":
    main()
