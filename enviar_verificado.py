#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para enviar correos a ayuntamientos CON VERIFICACIÓN PREVIA
- Verifica que el email existe antes de enviar
- Usa el Excel maestro (Espana_Maestro_Completo.xlsx)
- Marca emails inválidos para no volver a intentar
"""

import pandas as pd
import smtplib
import imaplib
import dns.resolver
import socket
import time
import os
import sys
import re
import subprocess
from datetime import datetime, time as dt_time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Archivo de bloqueo para evitar ejecuciones múltiples
LOCK_FILE = 'D:/Aytohacks/envio.lock'

def adquirir_lock():
    """Adquiere el lock para evitar ejecuciones múltiples"""
    if os.path.exists(LOCK_FILE):
        # Verificar si es muy viejo (más de 4 horas = proceso muerto)
        try:
            mtime = os.path.getmtime(LOCK_FILE)
            if time.time() - mtime > 14400:  # 4 horas
                os.remove(LOCK_FILE)
            else:
                return False
        except:
            pass
    with open(LOCK_FILE, 'w') as f:
        f.write(f"{os.getpid()} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return True

def liberar_lock():
    """Libera el lock"""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

# ============================================
# CONFIGURACIÓN
# ============================================

EXCEL_FILE = 'D:/Aytohacks/Espana_Maestro_Completo.xlsx'
LOG_FILE = 'D:/Aytohacks/envios_log.txt'
PDF_ADJUNTO = 'D:/Aytohacks/Equipamiento Astroturismo 2026.pdf'

# Tiempo entre envíos (en segundos) - 3 minutos
TIEMPO_ENTRE_ENVIOS = 180

# Horario permitido: 19:00 - 09:00 (nocturno)
# Para envío nocturno: de 19:00 a 09:00 del día siguiente
HORA_INICIO = dt_time(0, 0)  # Medianoche
HORA_FIN = dt_time(23, 59)   # Todo el día (nocturno activado)

# Configuración del servidor
SMTP_SERVER = 'mail.fundacionastrohita.org'
SMTP_PORT = 465
IMAP_SERVER = 'mail.fundacionastrohita.org'
IMAP_PORT = 993
EMAIL_USER = 'david@tecnohita.com'
EMAIL_PASS = 'Indiana2025'

ASUNTO = 'Equipamiento para astroturismo en espacios públicos y naturales'
REMITENTE_NOMBRE = 'David Organero'

# Dominios problemáticos que aceptan verificación pero rebotan después
DOMINIOS_BLACKLIST = [
    'diputoledo.es',      # Diputación Toledo - emails obsoletos
    'promojaen.es',       # Muchos timeout/errores
    'terra.es',           # 136 rebotes - dominio obsoleto
    'gva.es',             # 104 rebotes - Generalitat Valenciana
    'animsa.es',          # 64 rebotes - Navarra
    'diba.es',            # 37 rebotes - Diputación Barcelona
    'dip-palencia.es',    # 35 rebotes - Diputación Palencia
    'diputacionavila.es', # 30 rebotes - Diputación Ávila
    'diputacionavila.net',# 13 rebotes
    'dip-badajoz.es',     # 26 rebotes - Diputación Badajoz
    'dipucuenca.es',      # 25 rebotes - Diputación Cuenca
    'sopde.es',           # 22 rebotes
    'cv.gva.es',          # 18 rebotes - Valencia
    'telefonica.net',     # 16 rebotes - obsoleto
    'dpz.es',             # 15 rebotes - Diputación Zaragoza
    'teleline.es',        # 13 rebotes - obsoleto
    # Nuevos añadidos
    'aragob.es',          # 10 rebotes - Gobierno Aragón antiguo
    'dip.palencia.es',    # 10 rebotes - Diputación Palencia variante
    'dipucadiz.es',       # 9 rebotes - Diputación Cádiz
    'espublico.com',      # 9 rebotes - Servicio terceros
    'aragon.es',          # 7 rebotes - Gobierno Aragón
    'inicia.es',          # 6 rebotes - ISP obsoleto
    'avired.com',         # 5 rebotes - ISP obsoleto
]

# ============================================
# FUNCIONES DE VERIFICACIÓN
# ============================================

def obtener_mx(dominio):
    """Obtiene el servidor MX del dominio"""
    try:
        registros = dns.resolver.resolve(dominio, 'MX')
        mx_list = sorted(registros, key=lambda x: x.preference)
        return str(mx_list[0].exchange).rstrip('.')
    except:
        return None


def verificar_email(email):
    """Verifica si el email existe antes de enviar"""
    try:
        email = email.strip().lower()
        dominio = email.split('@')[1]

        # Verificar blacklist de dominios problemáticos
        for dom_black in DOMINIOS_BLACKLIST:
            if dominio.endswith(dom_black):
                return False, f'BLACKLIST_{dom_black}'

        # Obtener MX
        mx = obtener_mx(dominio)
        if not mx:
            return False, 'SIN_MX'

        # Verificar SMTP
        smtp = smtplib.SMTP(timeout=10)
        smtp.connect(mx)
        smtp.helo('tecnohita.com')
        smtp.mail('david@tecnohita.com')
        code, msg = smtp.rcpt(email)
        smtp.quit()

        if code == 250:
            return True, 'OK'
        elif code == 550:
            return False, 'NO_EXISTE'
        else:
            return True, f'DUDOSO_{code}'  # Asumir válido si no es 550

    except socket.timeout:
        return True, 'TIMEOUT'  # Asumir válido si timeout
    except:
        return True, 'ERROR'  # Asumir válido si error


# ============================================
# FUNCIONES DE ENVÍO
# ============================================

def normalizar_nombre(nombre):
    """Convierte 'Mata (La)' -> 'La Mata'"""
    nombre = str(nombre).strip()
    patron = r'^(.+?)\s*\((El|La|Los|Las)\)$'
    match = re.match(patron, nombre, re.IGNORECASE)
    if match:
        nombre_base = match.group(1).strip()
        articulo = match.group(2)
        return f"{articulo} {nombre_base}"
    return nombre


def esta_en_horario():
    """Verifica si estamos en el horario permitido"""
    ahora = datetime.now().time()
    return HORA_INICIO <= ahora <= HORA_FIN


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
        Email: <a href="mailto:david@tecnohita.com" style="color: #0066cc;">david@tecnohita.com</a><br>
        Tel: 611 44 33 63<br>
        Web: <a href="https://tecnohita.com/" style="color: #0066cc;">https://tecnohita.com/</a>
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


def guardar_en_enviados(msg, provincia):
    """Guarda el correo en la carpeta Enviados de la provincia via IMAP"""
    try:
        # Reemplazar espacios por guiones bajos para el nombre de carpeta IMAP
        provincia_carpeta = provincia.replace(' ', '_')
        carpeta = f'INBOX.Sent.{provincia_carpeta}'
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap.login(EMAIL_USER, EMAIL_PASS)
        fecha = imaplib.Time2Internaldate(time.time())
        imap.append(carpeta, r'(\Seen)', fecha, msg.as_bytes())
        imap.logout()
        return True
    except:
        return False


def revisar_rebotes():
    """Revisa la bandeja de entrada, marca rebotes en el Excel y los mueve a carpeta 'rebotes'"""
    import email
    from email.header import decode_header

    try:
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap.login(EMAIL_USER, EMAIL_PASS)
        imap.select('INBOX')

        # Buscar mensajes de hoy
        hoy = datetime.now().strftime('%d-%b-%Y')
        status, messages = imap.search(None, 'SINCE', hoy)
        if status != 'OK':
            imap.logout()
            return 0

        ids = messages[0].split()
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
        rebotes_marcados = 0
        mensajes_a_mover = []

        for msg_id in ids:
            status, data = imap.fetch(msg_id, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])

            de = msg.get('From', '')
            if 'mailer-daemon' not in de.lower() and 'postmaster' not in de.lower():
                continue

            # Extraer email destino del cuerpo
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        payload = part.get_payload(decode=True)
                        if payload:
                            body = payload.decode('utf-8', errors='ignore')
                        break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body = payload.decode('utf-8', errors='ignore')

            # Buscar email en el cuerpo
            emails_encontrados = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', body)
            email_rebotado = ''
            for e in emails_encontrados:
                if 'tecnohita' not in e.lower() and 'mailer' not in e.lower():
                    email_rebotado = e.lower()
                    break

            if not email_rebotado:
                continue

            # Marcar mensaje para mover a carpeta rebotes
            mensajes_a_mover.append(msg_id)

            # Buscar y marcar en Excel
            for col in ['Email_Scrapeado_1', 'email', 'Email_Scrapeado_2']:
                if col in df.columns:
                    mask = df[col].astype(str).str.lower().str.strip() == email_rebotado
                    if mask.any():
                        for idx in df[mask].index:
                            if pd.isna(df.at[idx, 'Rebotado']) or not str(df.at[idx, 'Rebotado']).strip():
                                df.at[idx, 'Rebotado'] = 'REBOTADO: Email no entregado'
                                df.at[idx, 'Enviado'] = ''
                                escribir_log(f"  REBOTE detectado: {email_rebotado}")
                                rebotes_marcados += 1

        # Mover mensajes de rebote a carpeta 'rebotes'
        if mensajes_a_mover:
            for msg_id in mensajes_a_mover:
                try:
                    imap.copy(msg_id, 'rebotes')
                    imap.store(msg_id, '+FLAGS', '\\Deleted')
                except:
                    pass  # Si falla, continuar
            imap.expunge()

        if rebotes_marcados > 0:
            df.to_excel(EXCEL_FILE, index=False)

        imap.logout()
        return rebotes_marcados
    except Exception as e:
        escribir_log(f"  Error revisando rebotes: {str(e)[:50]}")
        return 0


def hacer_commit_push(enviados):
    """Hace commit y push a GitHub cada 10 envíos"""
    try:
        os.chdir('D:/Aytohacks')
        # Add
        subprocess.run(['git', 'add', 'Espana_Maestro_Completo.xlsx'], capture_output=True)
        # Commit
        mensaje = f"Actualizacion: {enviados} emails enviados - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', mensaje], capture_output=True)
        # Push
        resultado = subprocess.run(['git', 'push'], capture_output=True, text=True)
        if resultado.returncode == 0:
            escribir_log(f"  GIT: Commit y push OK ({enviados} enviados)")
            return True
        else:
            escribir_log(f"  GIT: Error en push - {resultado.stderr[:50]}")
            return False
    except Exception as e:
        escribir_log(f"  GIT: Error - {str(e)[:50]}")
        return False


def enviar_email(destinatarios, asunto, nombre_ayuntamiento, provincia, adjunto=None):
    """Envía un email HTML"""
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
                parte = MIMEBase('application', 'pdf')
                parte.set_payload(f.read())
                encoders.encode_base64(parte)
                nombre_archivo = os.path.basename(adjunto)
                parte.add_header('Content-Disposition', f'attachment; filename="{nombre_archivo}"')
                msg.attach(parte)

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=60)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, destinatarios, msg.as_string())
        server.quit()

        guardar_en_enviados(msg, provincia)
        return True

    except Exception as e:
        escribir_log(f"  ERROR al enviar: {str(e)}")
        return False


def obtener_email(row, solo_scrapeados=False):
    """Obtiene el mejor email disponible del municipio
    Prioridad: FEMPCLM > Scrapeado > Gobierno
    """
    if solo_scrapeados:
        # Solo emails scrapeados de todoslosayuntamientos.es
        col = 'Email_Scrapeado_1'
        if col in row.index and pd.notna(row[col]) and str(row[col]).strip() and '@' in str(row[col]):
            return str(row[col]).strip().lower()
        return None
    else:
        # Prioridad: FEMPCLM > Scrapeado > Gobierno
        for col in ['Email_FEMPCLM', 'Email_Scrapeado_1', 'email', 'Email_Scrapeado_2']:
            if col in row.index and pd.notna(row[col]) and str(row[col]).strip() and '@' in str(row[col]):
                return str(row[col]).strip().lower()
        return None


def main():
    if len(sys.argv) < 2:
        print("Uso: python enviar_verificado.py <provincia> [cantidad] [--solo-scrapeados]")
        print("Ejemplo: python enviar_verificado.py Toledo 20")
        print("         python enviar_verificado.py TODAS 50 --solo-scrapeados")
        sys.exit(1)

    provincia = sys.argv[1]
    cantidad = 999
    solo_scrapeados = False

    for arg in sys.argv[2:]:
        if arg == '--solo-scrapeados':
            solo_scrapeados = True
        elif arg.isdigit():
            cantidad = int(arg)

    escribir_log("=" * 60)
    escribir_log(f"ENVIANDO A {provincia.upper()} (con verificacion previa)")
    modo = "SOLO SCRAPEADOS" if solo_scrapeados else "TODOS"
    escribir_log(f"Horario: 9:00-20:00 | Verificacion: SI | Modo: {modo}")
    escribir_log("=" * 60)

    # Cargar Excel maestro
    df = pd.read_excel(EXCEL_FILE, engine='openpyxl')

    # Filtrar por provincia
    df_prov = df[df['PROV_nombre'].str.contains(provincia, case=False, na=False)].copy()
    escribir_log(f"Municipios en {provincia}: {len(df_prov)}")

    # Filtrar pendientes (no enviados, no rebotados, con email)
    pendientes = []
    for idx, row in df_prov.iterrows():
        # Saltar si rebotado
        if pd.notna(row.get('Rebotado')) and str(row.get('Rebotado')).strip():
            continue

        # Saltar si ya fue enviado
        if pd.notna(row.get('Enviado')) and str(row.get('Enviado')).strip():
            continue

        # Verificar que tiene email
        email = obtener_email(row, solo_scrapeados)
        if not email:
            continue

        pendientes.append((idx, row, email))

    escribir_log(f"Pendientes con email: {len(pendientes)}")

    if not pendientes:
        escribir_log("No hay municipios pendientes")
        return

    # Limitar cantidad
    pendientes = pendientes[:cantidad]
    escribir_log(f"Procesando: {len(pendientes)} municipios")

    total_enviados = 0
    total_invalidos = 0

    for i, (idx, row, email) in enumerate(pendientes, 1):
        # Verificar horario
        if not esta_en_horario():
            escribir_log(f"FUERA DE HORARIO - Enviados: {total_enviados}")
            break

        municipio_raw = row['NOMBRE']
        municipio = normalizar_nombre(municipio_raw)

        escribir_log(f"[{i}/{len(pendientes)}] {municipio} -> {email}")

        # VERIFICAR EMAIL ANTES DE ENVIAR
        escribir_log(f"  Verificando email...")
        valido, motivo = verificar_email(email)

        if not valido:
            escribir_log(f"  EMAIL INVALIDO: {motivo}")
            # Marcar como rebotado en Excel
            df.at[idx, 'Rebotado'] = f'VERIFICACION: {motivo}'
            df.to_excel(EXCEL_FILE, index=False)
            total_invalidos += 1
            continue

        escribir_log(f"  Email OK ({motivo})")

        # ENVIAR
        if enviar_email([email], ASUNTO, municipio, provincia, PDF_ADJUNTO):
            escribir_log(f"  ENVIADO OK")
            total_enviados += 1
            # Marcar como enviado
            df.at[idx, 'Enviado'] = datetime.now().strftime('%Y-%m-%d %H:%M')
            df.to_excel(EXCEL_FILE, index=False)

            # Cada 10 envíos: revisar rebotes y hacer commit
            if total_enviados % 10 == 0:
                escribir_log(f"  Revisando bandeja de rebotes...")
                rebotes = revisar_rebotes()
                if rebotes > 0:
                    escribir_log(f"  {rebotes} rebote(s) marcado(s)")
                hacer_commit_push(total_enviados)
        else:
            escribir_log(f"  ERROR al enviar")

        # Esperar entre envíos
        if i < len(pendientes):
            escribir_log(f"  Esperando 3 minutos...")
            time.sleep(TIEMPO_ENTRE_ENVIOS)

    escribir_log("=" * 60)
    escribir_log(f"RESUMEN: {total_enviados} enviados, {total_invalidos} invalidos")
    escribir_log("=" * 60)


if __name__ == '__main__':
    if not adquirir_lock():
        print("Ya hay otra instancia ejecutándose. Saliendo...")
        sys.exit(1)
    try:
        main()
    finally:
        liberar_lock()
