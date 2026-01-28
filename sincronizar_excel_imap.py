#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sincroniza el Excel maestro con los emails realmente enviados en IMAP
- Lee las carpetas Enviados/Provincia
- Extrae destinatarios de cada email
- Marca como enviados en el Excel
"""

import imaplib
import email
from email.header import decode_header
import pandas as pd
import re
from datetime import datetime
from config import IMAP_SERVER, EMAIL_USER, EMAIL_PASS, EXCEL_MAESTRO

def conectar_imap():
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL_USER, EMAIL_PASS)
    return imap

def obtener_emails_enviados(imap):
    """Obtiene todos los emails enviados por provincia desde IMAP"""
    enviados = {}  # email -> provincia

    status, lista = imap.list()

    for item in lista:
        decoded = item.decode('utf-8')
        if 'INBOX.Sent.' in decoded:
            parts = decoded.split('"')
            if len(parts) >= 1:
                carpeta = parts[-1].strip()
                if carpeta.startswith('INBOX.Sent.') and carpeta != 'INBOX.Sent':
                    provincia = carpeta.replace('INBOX.Sent.', '')

                    try:
                        status, data = imap.select(f'"{carpeta}"')
                        if status == 'OK':
                            count = int(data[0])
                            if count > 0:
                                # Obtener todos los emails
                                status, messages = imap.search(None, 'ALL')
                                if status == 'OK':
                                    for num in messages[0].split():
                                        try:
                                            status, msg_data = imap.fetch(num, '(RFC822)')
                                            if status == 'OK':
                                                msg = email.message_from_bytes(msg_data[0][1])
                                                to_header = msg.get('To', '')

                                                # Extraer email del header To
                                                match = re.search(r'[\w\.-]+@[\w\.-]+', to_header)
                                                if match:
                                                    email_dest = match.group().lower()
                                                    enviados[email_dest] = provincia
                                        except Exception as e:
                                            pass
                    except Exception as e:
                        print(f"Error en {carpeta}: {e}")

    return enviados

def sincronizar_excel(enviados):
    """Actualiza el Excel con los emails enviados"""
    df = pd.read_excel(EXCEL_MAESTRO)

    # Asegurar que existe la columna
    if 'Email_Enviado' not in df.columns:
        df['Email_Enviado'] = ''

    actualizados = 0

    for idx, row in df.iterrows():
        # Buscar si alguno de los emails fue enviado
        for col in ['Email_1', 'Email_2', 'Email_3']:
            if col in df.columns and pd.notna(row.get(col)):
                email_val = str(row[col]).strip().lower()
                if email_val in enviados:
                    if pd.isna(row.get('Email_Enviado')) or not str(row.get('Email_Enviado')).strip():
                        df.at[idx, 'Email_Enviado'] = f'IMAP-{enviados[email_val]}'
                        actualizados += 1
                    break

    # Guardar
    df.to_excel(EXCEL_MAESTRO, index=False)
    return actualizados

def main():
    print("=" * 60)
    print("SINCRONIZANDO EXCEL CON IMAP")
    print("=" * 60)
    print()

    print("Conectando a IMAP...")
    imap = conectar_imap()

    print("Leyendo emails enviados...")
    enviados = obtener_emails_enviados(imap)
    print(f"Encontrados: {len(enviados)} emails en carpetas Enviados/")

    imap.logout()

    print()
    print("Actualizando Excel...")
    actualizados = sincronizar_excel(enviados)
    print(f"Registros actualizados: {actualizados}")

    print()
    print("Sincronizacion completada!")

if __name__ == '__main__':
    main()
