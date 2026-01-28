#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para limpiar emails enviados del servidor IMAP
- Mantiene el registro en el Excel (no se pierde nada)
- Borra los emails de las carpetas Enviados/Provincia
- Puede ejecutarse manualmente o automaticamente cada X envios
"""

import imaplib
import sys
from config import IMAP_SERVER, EMAIL_USER, EMAIL_PASS

def conectar_imap():
    """Conecta al servidor IMAP"""
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL_USER, EMAIL_PASS)
    return imap

def listar_carpetas_enviados(imap):
    """Lista carpetas de Enviados con su conteo"""
    carpetas = []
    status, lista = imap.list()

    for item in lista:
        decoded = item.decode('utf-8')
        if 'Enviados/' in decoded or 'Sent/' in decoded:
            # Extraer nombre de carpeta
            parts = decoded.split('"')
            if len(parts) >= 2:
                carpeta = parts[-2]
                if carpeta.startswith('Enviados/') or carpeta.startswith('Sent/'):
                    # Contar emails
                    try:
                        status, data = imap.select(f'"{carpeta}"')
                        if status == 'OK':
                            count = int(data[0])
                            if count > 0:
                                carpetas.append((carpeta, count))
                    except:
                        pass

    return sorted(carpetas, key=lambda x: x[1], reverse=True)

def limpiar_carpeta(imap, carpeta, mantener=0):
    """
    Limpia una carpeta de IMAP
    mantener: numero de emails a mantener (0 = borrar todos)
    """
    status, data = imap.select(f'"{carpeta}"')
    if status != 'OK':
        return 0

    total = int(data[0])
    if total == 0:
        return 0

    # Si queremos mantener algunos, calcular cuales borrar
    if mantener > 0 and total > mantener:
        # Borrar los mas antiguos, mantener los mas recientes
        borrar_hasta = total - mantener
        rango = f'1:{borrar_hasta}'
    else:
        rango = '1:*'

    # Marcar para borrar
    status, data = imap.search(None, 'ALL')
    if status == 'OK':
        ids = data[0].split()
        if mantener > 0:
            ids = ids[:-mantener] if len(ids) > mantener else []

        borrados = 0
        for email_id in ids:
            imap.store(email_id, '+FLAGS', '\\Deleted')
            borrados += 1

        # Ejecutar borrado permanente
        imap.expunge()
        return borrados

    return 0

def main():
    print("=" * 60)
    print("LIMPIEZA DE EMAILS ENVIADOS (IMAP)")
    print("=" * 60)
    print()
    print("NOTA: El registro se mantiene en el Excel, solo se borran")
    print("      las copias del servidor de correo.")
    print()

    # Parsear argumentos
    modo = 'interactive'
    provincia = None
    mantener = 0

    if len(sys.argv) > 1:
        if sys.argv[1] == '--todas':
            modo = 'todas'
        elif sys.argv[1] == '--auto':
            modo = 'auto'
            mantener = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        else:
            modo = 'provincia'
            provincia = sys.argv[1]

    imap = conectar_imap()

    # Listar carpetas
    carpetas = listar_carpetas_enviados(imap)

    if not carpetas:
        print("No hay carpetas de enviados con emails.")
        imap.logout()
        return

    total_emails = sum(c[1] for c in carpetas)
    print(f"Carpetas encontradas: {len(carpetas)}")
    print(f"Total emails en servidor: {total_emails}")
    print()

    for carpeta, count in carpetas:
        prov = carpeta.replace('Enviados/', '').replace('Sent/', '')
        print(f"  {prov:20} - {count:4} emails")
    print()

    if modo == 'interactive':
        print("Opciones:")
        print("  1. Borrar TODAS las carpetas")
        print("  2. Borrar una provincia especifica")
        print("  3. Mantener ultimos N emails por carpeta")
        print("  4. Cancelar")
        print()
        opcion = input("Selecciona opcion (1-4): ").strip()

        if opcion == '1':
            confirmar = input(f"Borrar {total_emails} emails? (si/no): ").strip().lower()
            if confirmar == 'si':
                for carpeta, count in carpetas:
                    borrados = limpiar_carpeta(imap, carpeta)
                    prov = carpeta.replace('Enviados/', '')
                    print(f"  {prov}: {borrados} emails borrados")
                print(f"\nTotal borrados: {total_emails}")

        elif opcion == '2':
            prov = input("Provincia a borrar: ").strip()
            carpeta_target = f'Enviados/{prov}'
            for carpeta, count in carpetas:
                if prov.lower() in carpeta.lower():
                    borrados = limpiar_carpeta(imap, carpeta)
                    print(f"Borrados {borrados} emails de {carpeta}")

        elif opcion == '3':
            n = int(input("Mantener ultimos N emails por carpeta: ").strip())
            for carpeta, count in carpetas:
                if count > n:
                    borrados = limpiar_carpeta(imap, carpeta, mantener=n)
                    prov = carpeta.replace('Enviados/', '')
                    print(f"  {prov}: {borrados} borrados, {n} mantenidos")

    elif modo == 'todas':
        for carpeta, count in carpetas:
            borrados = limpiar_carpeta(imap, carpeta)
            prov = carpeta.replace('Enviados/', '')
            print(f"  {prov}: {borrados} emails borrados")
        print(f"\nTotal borrados: {total_emails}")

    elif modo == 'auto':
        # Modo automatico: mantener ultimos N emails
        total_borrados = 0
        for carpeta, count in carpetas:
            if count > mantener:
                borrados = limpiar_carpeta(imap, carpeta, mantener=mantener)
                total_borrados += borrados
        if total_borrados > 0:
            print(f"Limpieza automatica: {total_borrados} emails borrados")

    elif modo == 'provincia' and provincia:
        for carpeta, count in carpetas:
            if provincia.lower() in carpeta.lower():
                borrados = limpiar_carpeta(imap, carpeta)
                print(f"Borrados {borrados} emails de {carpeta}")

    imap.logout()
    print("\nLimpieza completada. El registro sigue en el Excel.")

if __name__ == '__main__':
    main()
