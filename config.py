#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuración centralizada de rutas para el proyecto aytohacks
"""
import os

# Directorio base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Directorios principales
DATOS_DIR = os.path.join(BASE_DIR, 'datos')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
RESULTADOS_DIR = os.path.join(BASE_DIR, 'resultados')
PROVINCIAS_DIR = os.path.join(BASE_DIR, 'provincias')

# Crear directorios si no existen
for directory in [DATOS_DIR, LOGS_DIR, RESULTADOS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Archivos principales
PDF_ADJUNTO = os.path.join(BASE_DIR, 'Equipamiento Astroturismo 2026.pdf')

# Archivos de trabajo
EXCEL_MAESTRO = os.path.join(DATOS_DIR, 'Espana_Maestro_Completo.xlsx')
EXCEL_TOLEDO_FUSIONADO = os.path.join(DATOS_DIR, 'Toledo_Fusionado.xlsx')
EXCEL_TOLEDO_COMPLETO = os.path.join(DATOS_DIR, 'Toledo_Completo_Final.xlsx')
EXCEL_TOLEDO_PROGRESO = os.path.join(DATOS_DIR, 'Toledo_Completo_Progreso.xlsx')
LOCK_FILE = os.path.join(BASE_DIR, 'envio.lock')
ESTADO_CAMPANA = os.path.join(BASE_DIR, 'estado_campana.json')

# Logs
LOG_ENVIOS = os.path.join(LOGS_DIR, 'envios_log.txt')

# Configuración de envío básico
TIEMPO_ENTRE_ENVIOS = 180  # 3 minutos en segundos
REMITENTE = 'david@tecnohita.com'
REMITENTE_NOMBRE = 'David Organero'
ASUNTO = 'Equipamiento para astroturismo en espacios públicos y naturales'

# Configuración SMTP/IMAP
SMTP_SERVER = 'mail.fundacionastrohita.org'
SMTP_PORT = 465
IMAP_SERVER = 'mail.fundacionastrohita.org'
IMAP_PORT = 993
EMAIL_USER = 'david@tecnohita.com'
EMAIL_PASS = 'Indiana2025'

# Lista negra de dominios problemáticos (basado en historial de rebotes)
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
    'aragob.es',          # 10 rebotes - Gobierno Aragón antiguo
    'dip.palencia.es',    # 10 rebotes - Diputación Palencia variante
    'dipucadiz.es',       # 9 rebotes - Diputación Cádiz
    'espublico.com',      # 9 rebotes - Servicio terceros
    'aragon.es',          # 7 rebotes - Gobierno Aragón
    'inicia.es',          # 6 rebotes - ISP obsoleto
    'avired.com',         # 5 rebotes - ISP obsoleto
]

# Verificar que existe el PDF
if not os.path.exists(PDF_ADJUNTO):
    print(f"ADVERTENCIA: No se encuentra el archivo PDF: {PDF_ADJUNTO}")
