#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exporta todo el historial de emails enviados desde IMAP a CSV
- Extrae: fecha, destinatario, asunto, provincia
- Crea registro permanente que se guarda en GitHub
- Nunca mas se pierde el historial
"""

import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import re
import csv
import os
from datetime import datetime
from config import IMAP_SERVER, EMAIL_USER, EMAIL_PASS, BASE_DIR

def decode_subject(subject):
    """Decodifica el asunto del email"""
    if not subject:
        return ""
    decoded = decode_header(subject)
    result = []
    for part, encoding in decoded:
        if isinstance(part, bytes):
            result.append(part.decode(encoding or 'utf-8', errors='replace'))
        else:
            result.append(part)
    return ''.join(result)

def exportar_historial():
    print("=" * 60)
    print("EXPORTANDO HISTORIAL DE EMAILS ENVIADOS")
    print("=" * 60)
    print()

    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL_USER, EMAIL_PASS)

    # Obtener todas las carpetas Sent
    status, lista = imap.list()
    carpetas_sent = []

    for item in lista:
        decoded = item.decode('utf-8')
        if 'INBOX.Sent.' in decoded:
            parts = decoded.split('"')
            if len(parts) >= 1:
                carpeta = parts[-1].strip()
                if carpeta.startswith('INBOX.Sent.') and carpeta != 'INBOX.Sent':
                    carpetas_sent.append(carpeta)

    print(f"Carpetas encontradas: {len(carpetas_sent)}")

    # Archivo de salida
    archivo_historial = os.path.join(BASE_DIR, 'historial_enviados.csv')
    registros = []

    for carpeta in sorted(carpetas_sent):
        provincia = carpeta.replace('INBOX.Sent.', '')
        print(f"  Procesando {provincia}...", end=" ")

        try:
            status, data = imap.select(f'"{carpeta}"')
            if status == 'OK':
                count = int(data[0])
                if count > 0:
                    status, messages = imap.search(None, 'ALL')
                    if status == 'OK':
                        ids = messages[0].split()
                        for num in ids:
                            try:
                                status, msg_data = imap.fetch(num, '(RFC822)')
                                if status == 'OK':
                                    msg = email.message_from_bytes(msg_data[0][1])

                                    # Extraer datos
                                    to_header = msg.get('To', '')
                                    subject = decode_subject(msg.get('Subject', ''))
                                    date_str = msg.get('Date', '')

                                    # Parsear fecha
                                    try:
                                        fecha = parsedate_to_datetime(date_str)
                                        fecha_str = fecha.strftime('%Y-%m-%d %H:%M')
                                    except:
                                        fecha_str = date_str[:20]

                                    # Extraer emails del To
                                    emails = re.findall(r'[\w\.-]+@[\w\.-]+', to_header)

                                    for email_dest in emails:
                                        registros.append({
                                            'Fecha': fecha_str,
                                            'Provincia': provincia,
                                            'Email': email_dest.lower(),
                                            'Asunto': subject[:100]
                                        })
                            except Exception as e:
                                pass

                        print(f"{count} emails")
                else:
                    print("0 emails")
        except Exception as e:
            print(f"Error: {e}")

    imap.logout()

    # Guardar CSV
    with open(archivo_historial, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Fecha', 'Provincia', 'Email', 'Asunto'])
        writer.writeheader()
        writer.writerows(registros)

    print()
    print("=" * 60)
    print(f"HISTORIAL EXPORTADO: {len(registros)} registros")
    print(f"Archivo: historial_enviados.csv")
    print("=" * 60)

    # Resumen por provincia
    print()
    print("Por provincia:")
    provincias = {}
    for r in registros:
        prov = r['Provincia']
        provincias[prov] = provincias.get(prov, 0) + 1

    for prov, count in sorted(provincias.items(), key=lambda x: -x[1]):
        print(f"  {prov}: {count}")

    return archivo_historial

if __name__ == '__main__':
    exportar_historial()
