#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cuenta emails reales enviados por provincia
"""

import imaplib
from config import IMAP_SERVER, IMAP_PORT, EMAIL_USER, EMAIL_PASS

print("="*70)
print("CONTANDO EMAILS ENVIADOS POR PROVINCIA")
print("="*70)

try:
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap.login(EMAIL_USER, EMAIL_PASS)

    # Lista de provincias
    provincias = [
        'Toledo', 'Ciudad_Real', 'Cuenca', 'Guadalajara', 'Albacete',
        'Madrid', 'Avila', 'Segovia', 'Valladolid', 'Salamanca', 'Zamora',
        'Leon', 'Palencia', 'Burgos', 'Soria',
        'Barcelona', 'Girona', 'Lleida', 'Tarragona',
        'Valencia', 'Alicante', 'Castellon',
        'Sevilla', 'Malaga', 'Granada', 'Cordoba', 'Jaen', 'Huelva', 'Cadiz', 'Almeria',
        'Zaragoza', 'Huesca', 'Teruel',
        'A_Coruna', 'Lugo', 'Ourense', 'Pontevedra',
        'Asturias', 'Cantabria',
        'Vizcaya', 'Guipuzcoa', 'Alava', 'Navarra', 'La_Rioja',
        'Murcia', 'Badajoz', 'Caceres',
        'Baleares', 'Las_Palmas', 'Santa_Cruz_Tenerife',
        'Ceuta', 'Melilla'
    ]

    enviadas = []
    total_emails = 0

    for provincia in provincias:
        carpeta = f'INBOX.Sent.{provincia}'
        try:
            status, messages = imap.select(carpeta, readonly=True)
            if status == 'OK':
                status, data = imap.search(None, 'ALL')
                if status == 'OK' and data[0]:
                    num_emails = len(data[0].split())
                else:
                    num_emails = 0

                if num_emails > 0:
                    enviadas.append((provincia, num_emails))
                    total_emails += num_emails
        except:
            pass

    imap.logout()

    # Resultados
    print(f"\nProvincias con envíos: {len(enviadas)}")
    print(f"Total emails enviados: {total_emails}\n")

    if enviadas:
        enviadas_sorted = sorted(enviadas, key=lambda x: x[1], reverse=True)
        print("="*70)
        print("PROVINCIAS ENVIADAS (ordenadas por cantidad)")
        print("="*70)
        for prov, num in enviadas_sorted:
            print(f"  {prov:25s} - {num:4d} emails")
        print("="*70)
    else:
        print("No hay emails enviados todavía")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
