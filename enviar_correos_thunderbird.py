#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para enviar correos automatizados a ayuntamientos usando Thunderbird
"""

import pandas as pd
import subprocess
import time
import os
from datetime import datetime
import urllib.parse
from config import (EXCEL_TOLEDO_COMPLETO, LOG_ENVIOS, PDF_ADJUNTO,
                    TIEMPO_ENTRE_ENVIOS, REMITENTE, ASUNTO)

# Usar las constantes del config
EXCEL_FILE = EXCEL_TOLEDO_COMPLETO
LOG_FILE = LOG_ENVIOS

def crear_cuerpo_email(nombre_ayuntamiento):
    """Crea el cuerpo del email personalizado para cada ayuntamiento"""
    cuerpo = f"""Estimado/a responsable del Ayuntamiento de {nombre_ayuntamiento},

Mi nombre es David Organero y le escribo en representación de TecnoHita Instrumentación, empresa especializada en el diseño y fabricación de equipamiento para astroturismo, con más de 20 años de experiencia en instrumentación astronómica aplicada a espacios públicos, educativos y turísticos.

Desde TecnoHita desarrollamos instalaciones que permiten dotar de contenido astronómico a parques y espacios urbanos, convirtiéndolos en puntos de interés diferenciados y de valor turístico y didáctico. Entre otros recursos, diseñamos y fabricamos:

    • Parques astronómicos urbanos.
    • Elementos interpretativos astronómicos.
    • Relojes de sol de distintos formatos.
    • Paneles y señalética didáctica.

Le adjuntamos un documento PDF descriptivo donde se recogen los equipamientos para astroturismo que desarrollamos, concebidos para implantarse de forma modular o individual, adaptándonos a las necesidades concretas de cada municipio y espacio.

El objetivo de este contacto es presentarnos y facilitarles esta información, para que puedan tenerla en cuenta en caso de que el Ayuntamiento valore proyectos relacionados con:

    • Puesta en valor de espacios públicos,
    • Divulgación científica,
    • Educación,
    • Turismo cultural y de naturaleza,
    • Dinamización del entorno urbano.

Quedamos a su disposición para ampliar información o mantener, si lo consideran oportuno, una breve reunión informativa sin compromiso.

Reciba un cordial saludo,

David Organero
TecnoHita Instrumentación
Email: david@tecnohita.com
Tel: 611 44 33 63
Web: https://tecnohita.com/
"""
    return cuerpo

def escribir_log(mensaje):
    """Escribe en el archivo de log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {mensaje}\n")
    print(f"[{timestamp}] {mensaje}")

def enviar_email_thunderbird(destinatario, asunto, cuerpo, adjunto=None):
    """
    Envía un email usando Thunderbird mediante el protocolo mailto
    """
    try:
        # Codificar el asunto y cuerpo para URL
        asunto_encoded = urllib.parse.quote(asunto)
        cuerpo_encoded = urllib.parse.quote(cuerpo)

        # Construir la URL mailto
        mailto_url = f"mailto:{destinatario}?subject={asunto_encoded}&body={cuerpo_encoded}"

        # Si hay adjunto, agregarlo (Thunderbird puede no soportar adjuntos vía mailto)
        if adjunto and os.path.exists(adjunto):
            adjunto_encoded = urllib.parse.quote(adjunto)
            mailto_url += f"&attachment={adjunto_encoded}"

        # Abrir Thunderbird con el email pre-rellenado
        # En Windows
        subprocess.Popen(['start', 'thunderbird', '-compose', mailto_url], shell=True)

        return True

    except Exception as e:
        escribir_log(f"ERROR al preparar email: {str(e)}")
        return False

def obtener_emails_ayuntamiento(row):
    """Extrae todos los emails válidos de un ayuntamiento"""
    emails = []

    # Lista de columnas de email a revisar
    columnas_email = ['Email_TodosAyto_1', 'Email_TodosAyto_2', 'Email_TodosAyto_3',
                      'Email_1', 'Email_2', 'Email_3', 'Email_Original',
                      'Email_Diputacion']

    for col in columnas_email:
        if col in row and pd.notna(row[col]) and row[col] != '':
            email = str(row[col]).strip()
            if '@' in email and email not in emails:
                emails.append(email)

    return emails

def main():
    """Función principal"""
    escribir_log("="*60)
    escribir_log("INICIANDO CAMPAÑA DE ENVIO DE CORREOS")
    escribir_log("="*60)

    # Verificar que existe el archivo adjunto
    if not os.path.exists(PDF_ADJUNTO):
        escribir_log(f"ERROR: No se encuentra el archivo adjunto: {PDF_ADJUNTO}")
        return

    # Cargar el Excel
    try:
        df = pd.read_excel(EXCEL_FILE)
        escribir_log(f"Excel cargado: {len(df)} ayuntamientos")
    except Exception as e:
        escribir_log(f"ERROR al cargar Excel: {str(e)}")
        return

    # Agregar columna de estado si no existe
    if 'Email_Enviado' not in df.columns:
        df['Email_Enviado'] = ''

    # Contador de envíos
    total_enviados = 0
    total_errores = 0

    # Procesar cada ayuntamiento
    for index, row in df.iterrows():
        municipio = row['NOMBRE']

        # Verificar si ya fue enviado
        if pd.notna(row.get('Email_Enviado', '')) and row['Email_Enviado'] != '':
            escribir_log(f"[{index+1}/{len(df)}] {municipio} - YA ENVIADO (saltando)")
            continue

        # Obtener emails del ayuntamiento
        emails = obtener_emails_ayuntamiento(row)

        if not emails:
            escribir_log(f"[{index+1}/{len(df)}] {municipio} - SIN EMAILS (saltando)")
            continue

        # Enviar a cada email
        escribir_log(f"[{index+1}/{len(df)}] {municipio} - {len(emails)} email(s) encontrado(s)")

        for email in emails:
            escribir_log(f"  Preparando envío a: {email}")

            # Crear cuerpo personalizado
            cuerpo = crear_cuerpo_email(municipio)

            # Enviar email
            if enviar_email_thunderbird(email, ASUNTO, cuerpo, PDF_ADJUNTO):
                escribir_log(f"  OK Email preparado en Thunderbird para: {email}")
                total_enviados += 1

                # Marcar como enviado en el Excel
                df.at[index, 'Email_Enviado'] = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"

                # Guardar progreso
                df.to_excel(EXCEL_FILE, index=False)

                # IMPORTANTE: Aquí el usuario debe revisar el email en Thunderbird y enviarlo manualmente
                escribir_log(f"  ATENCION ACCION REQUERIDA: Revisar y enviar el email en Thunderbird")
                input("  Presiona ENTER después de enviar el email en Thunderbird para continuar...")

            else:
                escribir_log(f"  ERROR ERROR al preparar email para: {email}")
                total_errores += 1

        # Pausa entre ayuntamientos (solo si hay más ayuntamientos pendientes)
        if index < len(df) - 1:
            escribir_log(f"  Esperando {TIEMPO_ENTRE_ENVIOS} segundos antes del siguiente envío...")
            time.sleep(TIEMPO_ENTRE_ENVIOS)

    # Resumen final
    escribir_log("="*60)
    escribir_log("CAMPAÑA FINALIZADA")
    escribir_log(f"Total emails enviados: {total_enviados}")
    escribir_log(f"Total errores: {total_errores}")
    escribir_log("="*60)

if __name__ == "__main__":
    main()
