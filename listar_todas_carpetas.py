#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Lista TODAS las carpetas del correo IMAP
"""

import imaplib
from config import IMAP_SERVER, IMAP_PORT, EMAIL_USER, EMAIL_PASS

print("="*70)
print("LISTANDO TODAS LAS CARPETAS IMAP")
print("="*70)

try:
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap.login(EMAIL_USER, EMAIL_PASS)

    status, folders = imap.list()

    print("\nCarpetas encontradas:\n")
    for folder in folders:
        folder_str = folder.decode()
        print(f"  {folder_str}")

        # Si es una carpeta de enviados, contar emails
        if 'Sent' in folder_str or 'Enviados' in folder_str or 'INBOX.Sent' in folder_str:
            parts = folder_str.split('"')
            if len(parts) >= 3:
                carpeta_nombre = parts[-2]
                try:
                    status, messages = imap.select(carpeta_nombre, readonly=True)
                    if status == 'OK':
                        status, data = imap.search(None, 'ALL')
                        if status == 'OK' and data[0]:
                            num_emails = len(data[0].split())
                            print(f"    → {num_emails} emails")
                except:
                    pass

    imap.logout()

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
