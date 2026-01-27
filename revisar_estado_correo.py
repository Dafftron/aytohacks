#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Revisa el estado real de la campaña desde el correo IMAP
"""

import imaplib
from config import IMAP_SERVER, IMAP_PORT, EMAIL_USER, EMAIL_PASS

print("="*70)
print("REVISANDO ESTADO REAL DESDE CORREO IMAP")
print("="*70)

try:
    # Conectar a IMAP
    print(f"\nConectando a {IMAP_SERVER}...")
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap.login(EMAIL_USER, EMAIL_PASS)

    print("Conectado correctamente\n")

    # Listar todas las carpetas
    status, folders = imap.list()

    print("="*70)
    print("CARPETAS DE ENVIADOS POR PROVINCIA")
    print("="*70)

    enviadas = []
    total_emails = 0

    for folder in folders:
        folder_str = folder.decode()
        # Buscar carpetas INBOX.Sent.*
        if 'INBOX.Sent.' in folder_str:
            # Extraer nombre de carpeta
            parts = folder_str.split('"')
            if len(parts) >= 3:
                carpeta_nombre = parts[-2]

                # Contar emails en esta carpeta
                try:
                    status, messages = imap.select(carpeta_nombre, readonly=True)
                    if status == 'OK':
                        status, data = imap.search(None, 'ALL')
                        if status == 'OK' and data[0]:
                            num_emails = len(data[0].split())
                        else:
                            num_emails = 0

                        # Extraer nombre de provincia
                        provincia = carpeta_nombre.split('.')[-1]
                        enviadas.append((provincia, num_emails))
                        total_emails += num_emails

                        print(f"  {provincia:20s} - {num_emails:4d} emails enviados")
                except:
                    pass

    # Revisar también INBOX normal
    print("\n" + "="*70)
    print("BANDEJA DE ENTRADA (INBOX)")
    print("="*70)

    try:
        imap.select('INBOX', readonly=True)
        status, data = imap.search(None, 'ALL')
        if status == 'OK' and data[0]:
            num_inbox = len(data[0].split())
        else:
            num_inbox = 0
        print(f"  Emails en INBOX: {num_inbox}")
    except Exception as e:
        print(f"  Error al leer INBOX: {e}")

    # Revisar carpeta de rebotes
    print("\n" + "="*70)
    print("CARPETA DE REBOTES")
    print("="*70)

    try:
        status, messages = imap.select('rebotes', readonly=True)
        if status == 'OK':
            status, data = imap.search(None, 'ALL')
            if status == 'OK' and data[0]:
                num_rebotes = len(data[0].split())
            else:
                num_rebotes = 0
            print(f"  Emails rebotados: {num_rebotes}")
        else:
            print("  Carpeta 'rebotes' no existe")
    except:
        print("  Carpeta 'rebotes' no existe")

    imap.logout()

    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"Provincias con envíos: {len(enviadas)}")
    print(f"Total emails enviados: {total_emails}")
    print("")
    print("Provincias enviadas:")
    enviadas_sorted = sorted(enviadas, key=lambda x: x[1], reverse=True)
    for prov, num in enviadas_sorted:
        print(f"  - {prov}: {num} emails")
    print("="*70)

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
