#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para verificar la carpeta IMAP de enviados y sincronizar con el Excel
Lee INBOX.Sent.Toledo y actualiza el Excel con los municipios ya enviados
"""

import pandas as pd
import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime

# Configuración
IMAP_SERVER = 'mail.fundacionastrohita.org'
IMAP_PORT = 993
EMAIL_USER = 'david@tecnohita.com'
EMAIL_PASS = 'Indiana2025'
CARPETA_ENVIADOS = 'INBOX.Sent.Toledo'
EXCEL_FILE = 'D:/Aytohacks/Toledo_Reorganizado.xlsx'

print("="*60)
print("VERIFICANDO CARPETA IMAP DE ENVIADOS")
print("="*60)

try:
    # Conectar a IMAP
    print(f"\nConectando a {IMAP_SERVER}...")
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap.login(EMAIL_USER, EMAIL_PASS)

    # Seleccionar carpeta
    print(f"Accediendo a carpeta: {CARPETA_ENVIADOS}")
    status, messages = imap.select(CARPETA_ENVIADOS, readonly=True)

    if status != 'OK':
        print(f"ERROR: No se pudo acceder a {CARPETA_ENVIADOS}")
        print("Listando carpetas disponibles:")
        status, folders = imap.list()
        for folder in folders:
            print(f"  {folder.decode()}")
        imap.logout()
        exit(1)

    # Buscar todos los mensajes
    status, data = imap.search(None, 'ALL')
    mail_ids = data[0].split()

    print(f"\nCorreos encontrados en carpeta: {len(mail_ids)}")

    # Extraer nombres de ayuntamientos de los asuntos
    municipios_enviados = {}

    print("\nAnalizando correos...")
    for i, mail_id in enumerate(mail_ids, 1):
        if i % 10 == 0:
            print(f"  Procesados: {i}/{len(mail_ids)}")

        status, data = imap.fetch(mail_id, '(RFC822)')
        if status != 'OK':
            continue

        msg = email.message_from_bytes(data[0][1])

        # Obtener asunto
        subject = msg.get('Subject', '')
        if subject:
            # Decodificar asunto si es necesario
            decoded = decode_header(subject)
            subject = decoded[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode(decoded[0][1] or 'utf-8')

        # Obtener fecha
        date_str = msg.get('Date', '')
        try:
            date_parsed = email.utils.parsedate_to_datetime(date_str)
            fecha_envio = date_parsed.strftime('%Y-%m-%d %H:%M')
        except:
            fecha_envio = datetime.now().strftime('%Y-%m-%d %H:%M')

        # Buscar "Ayuntamiento de [Nombre]" en el cuerpo del mensaje
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

        # Extraer nombre del ayuntamiento
        match = re.search(r'Ayuntamiento de ([^,\n]+)', body)
        if match:
            municipio = match.group(1).strip()
            if municipio not in municipios_enviados:
                municipios_enviados[municipio] = fecha_envio

    imap.logout()

    print(f"\nMunicipios únicos encontrados: {len(municipios_enviados)}")

    # Cargar Excel
    print(f"\nCargando Excel: {EXCEL_FILE}")
    df = pd.read_excel(EXCEL_FILE)

    # Sincronizar con Excel
    print("\nSincronizando con Excel...")
    actualizados = 0

    for municipio, fecha in municipios_enviados.items():
        # Buscar municipio en Excel (normalizar comparación)
        match = df[df['NOMBRE'].str.upper().str.strip() == municipio.upper().strip()]

        if len(match) > 0:
            idx = match.index[0]
            # Solo actualizar si no tiene fecha de envío
            if pd.isna(df.at[idx, 'Enviado']) or df.at[idx, 'Enviado'] == '':
                df.at[idx, 'Enviado'] = fecha
                actualizados += 1
                print(f"  Actualizado: {municipio} -> {fecha}")

    # Guardar Excel actualizado
    if actualizados > 0:
        df.to_excel(EXCEL_FILE, index=False)
        print(f"\n{actualizados} municipios actualizados en el Excel")
    else:
        print("\nNo hay nuevos municipios para actualizar")

    # Estadísticas finales
    total_enviados = df['Enviado'].notna().sum()
    total = len(df)

    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    print(f"Total municipios en Excel: {total}")
    print(f"Correos en carpeta IMAP: {len(mail_ids)}")
    print(f"Municipios marcados como enviados: {total_enviados}")
    print(f"Pendientes: {total - total_enviados}")
    print(f"Progreso: {total_enviados/total*100:.1f}%")

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
