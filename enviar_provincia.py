#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para enviar correos a ayuntamientos de una provincia
SIN restricción de horario - para provincias periféricas

Uso: python enviar_provincia.py <provincia> [cantidad]
Ejemplo: python enviar_provincia.py Almeria 20
"""

import pandas as pd
import smtplib
import imaplib
import time
import os
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# ============================================
# CONFIGURACIÓN
# ============================================

# Provincia desde argumento
if len(sys.argv) < 2:
    print("Uso: python enviar_provincia.py <provincia> [cantidad]")
    print("Provincias disponibles:")
    for f in os.listdir('C:/aytohacks/provincias'):
        if f.endswith('.xlsx') and not f.startswith('_'):
            print(f"  - {f.replace('.xlsx', '')}")
    sys.exit(1)

PROVINCIA = sys.argv[1]
CANTIDAD = int(sys.argv[2]) if len(sys.argv) > 2 else 10  # Por defecto 10

# Archivo Excel de la provincia
EXCEL_FILE = f'C:/aytohacks/provincias/{PROVINCIA}.xlsx'
LOG_FILE = f'C:/aytohacks/envios_log_{PROVINCIA}.txt'
PDF_ADJUNTO = 'C:/aytohacks/Equipamiento Astroturismo 2026.pdf'

# Carpeta IMAP para guardar enviados
CARPETA_ENVIADOS = f'INBOX.Sent.{PROVINCIA}'

# Tiempo entre envíos (en segundos) - 3 minutos
TIEMPO_ENTRE_ENVIOS = 180

# Configuración del servidor
SMTP_SERVER = 'mail.fundacionastrohita.org'
SMTP_PORT = 465
IMAP_SERVER = 'mail.fundacionastrohita.org'
IMAP_PORT = 993
EMAIL_USER = 'david@tecnohita.com'
EMAIL_PASS = 'Indiana2025'

# Datos del correo
ASUNTO = 'Equipamiento para astroturismo en espacios públicos y naturales'
REMITENTE_NOMBRE = 'David Organero'

# ============================================

def crear_cuerpo_html(nombre_ayuntamiento):
    return f'''<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: Arial, Helvetica, sans-serif; font-size: 14px; color: #333333; line-height: 1.6;">
    <p>Estimado/a responsable del Ayuntamiento de <strong>{nombre_ayuntamiento}</strong>,</p>

    <p>Mi nombre es David Organero y le escribo en representación de <strong>TecnoHita Instrumentación</strong>, empresa especializada en el diseño y fabricación de equipamiento para astroturismo, con más de 20 años de experiencia en instrumentación astronómica aplicada a espacios públicos, educativos y turísticos.</p>

    <p>Desde TecnoHita desarrollamos instalaciones que permiten dotar de contenido astronómico a parques y espacios urbanos, convirtiéndolos en puntos de interés diferenciados y de valor turístico y didáctico. Entre otros recursos, diseñamos y fabricamos:</p>

    <ul style="margin-left: 20px;">
        <li>Parques astronómicos urbanos.</li>
        <li>Elementos interpretativos astronómicos.</li>
        <li>Relojes de sol de distintos formatos.</li>
        <li>Paneles y señalética didáctica.</li>
    </ul>

    <p>Le adjuntamos un documento PDF descriptivo donde se recogen los equipamientos para astroturismo que desarrollamos, concebidos para implantarse de forma modular o individual, adaptándonos a las necesidades concretas de cada municipio y espacio.</p>

    <p>El objetivo de este contacto es presentarnos y facilitarles esta información, para que puedan tenerla en cuenta en caso de que el Ayuntamiento valore proyectos relacionados con:</p>

    <ul style="margin-left: 20px;">
        <li>Puesta en valor de espacios públicos,</li>
        <li>Divulgación científica,</li>
        <li>Educación,</li>
        <li>Turismo cultural y de naturaleza,</li>
        <li>Dinamización del entorno urbano.</li>
    </ul>

    <p>Quedamos a su disposición para ampliar información o mantener, si lo consideran oportuno, una breve reunión informativa sin compromiso.</p>

    <p>Reciba un cordial saludo,</p>

    <p style="margin-top: 20px;">
        <strong>David Organero</strong><br>
        <strong>TecnoHita Instrumentación</strong><br>
        📧 <a href="mailto:david@tecnohita.com" style="color: #0066cc;">david@tecnohita.com</a><br>
        📞 611 44 33 63<br>
        🌐 <a href="https://tecnohita.com/" style="color: #0066cc;">https://tecnohita.com/</a>
    </p>
</body>
</html>'''


def crear_cuerpo_texto(nombre_ayuntamiento):
    return f'''Estimado/a responsable del Ayuntamiento de {nombre_ayuntamiento},

Mi nombre es David Organero y le escribo en representación de TecnoHita Instrumentación, empresa especializada en el diseño y fabricación de equipamiento para astroturismo, con más de 20 años de experiencia en instrumentación astronómica aplicada a espacios públicos, educativos y turísticos.

Desde TecnoHita desarrollamos instalaciones que permiten dotar de contenido astronómico a parques y espacios urbanos, convirtiéndolos en puntos de interés diferenciados y de valor turístico y didáctico. Entre otros recursos, diseñamos y fabricamos:

    - Parques astronómicos urbanos.
    - Elementos interpretativos astronómicos.
    - Relojes de sol de distintos formatos.
    - Paneles y señalética didáctica.

Le adjuntamos un documento PDF descriptivo donde se recogen los equipamientos para astroturismo que desarrollamos, concebidos para implantarse de forma modular o individual, adaptándonos a las necesidades concretas de cada municipio y espacio.

El objetivo de este contacto es presentarnos y facilitarles esta información, para que puedan tenerla en cuenta en caso de que el Ayuntamiento valore proyectos relacionados con:

    - Puesta en valor de espacios públicos,
    - Divulgación científica,
    - Educación,
    - Turismo cultural y de naturaleza,
    - Dinamización del entorno urbano.

Quedamos a su disposición para ampliar información o mantener, si lo consideran oportuno, una breve reunión informativa sin compromiso.

Reciba un cordial saludo,

David Organero
TecnoHita Instrumentación
Email: david@tecnohita.com
Tel: 611 44 33 63
Web: https://tecnohita.com/
'''


def escribir_log(mensaje):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {mensaje}\n")
    print(f"[{timestamp}] {mensaje}")


def guardar_en_enviados(msg):
    """Guarda el correo en la carpeta Enviados de la provincia via IMAP"""
    try:
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap.login(EMAIL_USER, EMAIL_PASS)
        fecha = imaplib.Time2Internaldate(time.time())
        resultado = imap.append(CARPETA_ENVIADOS, r'(\Seen)', fecha, msg.as_bytes())
        imap.logout()
        return resultado[0] == 'OK'
    except Exception as e:
        escribir_log(f"  AVISO IMAP: {str(e)}")
        return False


def enviar_email(destinatarios, asunto, nombre_ayuntamiento, adjunto=None):
    """Envía un email HTML a uno o varios destinatarios"""
    try:
        msg = MIMEMultipart('mixed')
        msg['From'] = f"{REMITENTE_NOMBRE} <{EMAIL_USER}>"
        msg['To'] = ', '.join(destinatarios)
        msg['Subject'] = asunto

        msg_alt = MIMEMultipart('alternative')
        msg_alt.attach(MIMEText(crear_cuerpo_texto(nombre_ayuntamiento), 'plain', 'utf-8'))
        msg_alt.attach(MIMEText(crear_cuerpo_html(nombre_ayuntamiento), 'html', 'utf-8'))
        msg.attach(msg_alt)

        if adjunto and os.path.exists(adjunto):
            with open(adjunto, 'rb') as f:
                parte = MIMEBase('application', 'octet-stream')
                parte.set_payload(f.read())
                encoders.encode_base64(parte)
                nombre_archivo = os.path.basename(adjunto)
                parte.add_header('Content-Disposition', f'attachment; filename="{nombre_archivo}"')
                msg.attach(parte)

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, destinatarios, msg.as_string())
        server.quit()

        guardar_en_enviados(msg)
        return True

    except Exception as e:
        escribir_log(f"  ERROR al enviar: {str(e)}")
        return False


def obtener_emails_ayuntamiento(row):
    """Obtiene lista de emails únicos del ayuntamiento"""
    emails = []
    for col in ['Email_1', 'Email_2', 'Email_3']:
        if col in row.index and pd.notna(row[col]) and row[col] != '':
            email = str(row[col]).strip().lower()
            if '@' in email and email not in emails:
                emails.append(email)
    return emails


def main():
    escribir_log("=" * 60)
    escribir_log(f"ENVIANDO A {PROVINCIA.upper()} - {CANTIDAD} ayuntamientos")
    escribir_log(f"Excel: {EXCEL_FILE}")
    escribir_log(f"Carpeta IMAP: {CARPETA_ENVIADOS}")
    escribir_log("=" * 60)

    if not os.path.exists(EXCEL_FILE):
        escribir_log(f"ERROR: No se encuentra {EXCEL_FILE}")
        return

    if PDF_ADJUNTO and not os.path.exists(PDF_ADJUNTO):
        escribir_log(f"AVISO: No se encuentra el PDF adjunto")

    # Cargar Excel
    try:
        df = pd.read_excel(EXCEL_FILE)
        escribir_log(f"Excel cargado: {len(df)} ayuntamientos")
    except Exception as e:
        escribir_log(f"ERROR al cargar Excel: {str(e)}")
        return

    # Buscar columna de nombre
    columna_nombre = None
    for col in ['Municipio', 'NOMBRE', 'Nombre', 'nombre']:
        if col in df.columns:
            columna_nombre = col
            break

    if not columna_nombre:
        escribir_log(f"ERROR: No se encuentra columna de nombre")
        return

    # Columna de estado
    if 'Email_Enviado' not in df.columns:
        df['Email_Enviado'] = ''

    # Filtrar pendientes con email
    pendientes = df[
        (df['Email_Enviado'].isna() | (df['Email_Enviado'] == '')) &
        (df['Email_1'].notna() & (df['Email_1'] != ''))
    ]

    escribir_log(f"Pendientes con email: {len(pendientes)}")

    if len(pendientes) == 0:
        escribir_log("No hay ayuntamientos pendientes de enviar")
        return

    # Limitar a la cantidad solicitada
    a_enviar = pendientes.head(CANTIDAD)
    escribir_log(f"Enviando a {len(a_enviar)} ayuntamientos...")

    # Contadores
    total_enviados = 0
    total_errores = 0

    for idx, (index, row) in enumerate(a_enviar.iterrows(), 1):
        municipio = row[columna_nombre]
        emails = obtener_emails_ayuntamiento(row)

        escribir_log(f"[{idx}/{len(a_enviar)}] {municipio} -> {emails}")

        if enviar_email(emails, ASUNTO, municipio, PDF_ADJUNTO):
            escribir_log(f"  OK enviado")
            total_enviados += 1
            df.at[index, 'Email_Enviado'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            df.to_excel(EXCEL_FILE, index=False)
        else:
            escribir_log(f"  ERROR")
            total_errores += 1

        # Esperar entre envíos (excepto el último)
        if idx < len(a_enviar):
            escribir_log(f"  Esperando {TIEMPO_ENTRE_ENVIOS//60} minutos...")
            time.sleep(TIEMPO_ENTRE_ENVIOS)

    escribir_log("=" * 60)
    escribir_log(f"COMPLETADO: {total_enviados}/{len(a_enviar)} enviados")
    if total_errores > 0:
        escribir_log(f"Errores: {total_errores}")
    escribir_log("=" * 60)


if __name__ == "__main__":
    main()
