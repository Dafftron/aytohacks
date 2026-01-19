#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para enviar correo a emails de prueba
"""

import subprocess
import os

# Verificar que existe el PDF
PDF_ADJUNTO = 'D:/Tecnohita/Comercial/Equipamiento Astroturismo 2026.pdf'

if not os.path.exists(PDF_ADJUNTO):
    print(f"ERROR: No se encuentra el PDF: {PDF_ADJUNTO}")
    exit(1)

# Datos del correo
ASUNTO = 'Equipamiento para astroturismo en espacios publicos y naturales'
DESTINATARIO = 'david@tecnohita.com'  # Cambiar para probar con faustino@fundacionastrohita.org
MUNICIPIO_PRUEBA = 'Toledo'  # Municipio de prueba

# Cuerpo del email
CUERPO = f"""Estimado/a responsable del Ayuntamiento de {MUNICIPIO_PRUEBA},

Mi nombre es David Organero y le escribo en representacion de TecnoHita Instrumentacion, empresa especializada en el diseno y fabricacion de equipamiento para astroturismo, con mas de 20 anos de experiencia en instrumentacion astronomica aplicada a espacios publicos, educativos y turisticos.

Desde TecnoHita desarrollamos instalaciones que permiten dotar de contenido astronomico a parques y espacios urbanos, convirtiendolos en puntos de interes diferenciados y de valor turistico y didactico. Entre otros recursos, disenamos y fabricamos:

    • Parques astronomicos urbanos.
    • Elementos interpretativos astronomicos.
    • Relojes de sol de distintos formatos.
    • Paneles y senalética didactica.

Le adjuntamos un documento PDF descriptivo donde se recogen los equipamientos para astroturismo que desarrollamos, concebidos para implantarse de forma modular o individual, adaptandonos a las necesidades concretas de cada municipio y espacio.

El objetivo de este contacto es presentarnos y facilitarles esta informacion, para que puedan tenerla en cuenta en caso de que el Ayuntamiento valore proyectos relacionados con:

    • Puesta en valor de espacios publicos,
    • Divulgacion cientifica,
    • Educacion,
    • Turismo cultural y de naturaleza,
    • Dinamizacion del entorno urbano.

Quedamos a su disposicion para ampliar informacion o mantener, si lo consideran oportuno, una breve reunion informativa sin compromiso.

Reciba un cordial saludo,

David Organero
TecnoHita Instrumentacion
Email: david@tecnohita.com
Tel: 611 44 33 63
Web: https://tecnohita.com/
"""

print("="*70)
print("PRUEBA DE ENVIO DE CORREO")
print("="*70)
print(f"Destinatario: {DESTINATARIO}")
print(f"Asunto: {ASUNTO}")
print(f"Adjunto: {PDF_ADJUNTO}")
print("="*70)

# Crear archivo .eml temporal con el contenido
eml_path = 'D:/Aytohacks/correo_prueba.eml'

eml_content = f"""From: david@tecnohita.com
To: {DESTINATARIO}
Subject: {ASUNTO}
Content-Type: text/plain; charset=UTF-8

{CUERPO}
"""

with open(eml_path, 'w', encoding='utf-8') as f:
    f.write(eml_content)

print(f"\nArchivo .eml creado: {eml_path}")
print("\nAbriendo Thunderbird...")

# Abrir Thunderbird con el archivo .eml
try:
    subprocess.Popen(['thunderbird', '-compose', eml_path], shell=False)
    print("\nOK - Thunderbird abierto con el correo de prueba")
    print("\nINSTRUCCIONES:")
    print("1. Revisa el correo en Thunderbird")
    print("2. Adjunta manualmente el PDF desde: D:/Tecnohita/Comercial/")
    print("3. Envia el correo")
    print("4. Verifica que llega correctamente")
except Exception as e:
    print(f"\nERROR al abrir Thunderbird: {e}")
    print("\nAlternativa: Abre manualmente el archivo:")
    print(f"  {eml_path}")
