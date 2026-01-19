#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script mejorado para completar información de ayuntamientos
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re
import unicodedata

def normalizar_nombre_url(nombre):
    """Normaliza el nombre del municipio para usarlo en URL"""
    # Eliminar acentos
    nombre = unicodedata.normalize('NFKD', nombre)
    nombre = nombre.encode('ASCII', 'ignore').decode('ASCII')

    # Convertir a minúsculas y reemplazar espacios por guiones
    nombre = nombre.lower()
    nombre = nombre.replace(' ', '-')
    nombre = nombre.replace('(', '').replace(')', '')

    return nombre

def extraer_emails(texto):
    """Extrae emails de un texto"""
    if not texto:
        return []
    patron = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(patron, texto)
    # Filtrar emails válidos
    emails_validos = [e for e in emails if not e.endswith('.png') and not e.endswith('.jpg')]
    return list(set(emails_validos))

def extraer_webs(soup):
    """Extrae URLs del contenido HTML"""
    webs = []

    # Buscar enlaces href
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'http' in href and 'todoslosayuntamientos' not in href:
            # Extraer dominio limpio
            match = re.search(r'(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', href)
            if match:
                webs.append(match.group(1))

    return list(set(webs))[:3]

def buscar_en_todoslosayuntamientos(nombre_municipio):
    """Busca información del ayuntamiento"""
    try:
        nombre_url = normalizar_nombre_url(nombre_municipio)
        url = f"https://www.todoslosayuntamientos.es/castilla-la-mancha/toledo/{nombre_url}"

        print(f"  URL: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            texto_completo = soup.get_text()

            # Extraer emails
            emails = extraer_emails(texto_completo)

            # Extraer webs
            webs = extraer_webs(soup)

            # Buscar teléfonos (formato 925XXXXXX o similar)
            telefonos = re.findall(r'\b9[0-9]{8}\b', texto_completo)
            telefonos = list(set(telefonos))[:2]

            resultado = {
                'emails': emails,
                'webs': webs,
                'telefonos': telefonos,
                'encontrado': True
            }

            print(f"  OK - Emails: {len(emails)}, Webs: {len(webs)}, Tels: {len(telefonos)}")
            return resultado
        else:
            print(f"  X Error {response.status_code}")
            return {'encontrado': False}

    except Exception as e:
        print(f"  X Error: {str(e)}")
        return {'encontrado': False}

def mostrar_y_confirmar(municipio, info):
    """Muestra la información encontrada y pide confirmación"""
    print(f"\n{'='*60}")
    print(f"MUNICIPIO: {municipio}")
    print(f"{'='*60}")

    if not info['encontrado']:
        print("X No se encontró información")
        respuesta = input("¿Quieres buscar manualmente? (s/n): ")
        if respuesta.lower() == 's':
            print("Introduce los datos manualmente (deja en blanco si no hay):")
            email1 = input("  Email 1: ").strip()
            email2 = input("  Email 2: ").strip()
            web = input("  Web: ").strip()
            return {
                'emails': [e for e in [email1, email2] if e],
                'webs': [web] if web else [],
                'telefonos': [],
                'manual': True
            }
        return None

    print("OK Información encontrada:")
    if info['emails']:
        print(f"  Email: Emails: {', '.join(info['emails'])}")
    if info['webs']:
        print(f"  Web: Webs: {', '.join(info['webs'])}")
    if info['telefonos']:
        print(f"  Tel: Teléfonos: {', '.join(info['telefonos'])}")

    respuesta = input("\n¿Es correcta esta información? (s/n/editar): ").lower()

    if respuesta == 's':
        return info
    elif respuesta == 'editar':
        print("Edita los datos (presiona Enter para mantener el valor actual):")
        emails_nuevos = []
        for i, email in enumerate(info['emails'][:2]):
            nuevo = input(f"  Email {i+1} [{email}]: ").strip()
            emails_nuevos.append(nuevo if nuevo else email)

        web_nueva = input(f"  Web [{info['webs'][0] if info['webs'] else ''}]: ").strip()

        return {
            'emails': emails_nuevos,
            'webs': [web_nueva] if web_nueva else info['webs'],
            'telefonos': info['telefonos'],
            'editado': True
        }
    else:
        return None

# Cargar Excel
print("Cargando Excel...")
df = pd.read_excel('D:/Aytohacks/Toledo_Fusionado.xlsx')
print(f"Total: {len(df)} ayuntamientos\n")

# Agregar columnas nuevas
if 'Email_Buscado_1' not in df.columns:
    df['Email_Buscado_1'] = ''
if 'Email_Buscado_2' not in df.columns:
    df['Email_Buscado_2'] = ''
if 'Web_Buscada' not in df.columns:
    df['Web_Buscada'] = ''
if 'Verificado' not in df.columns:
    df['Verificado'] = ''

print("="*60)
print("MODO VERIFICACIÓN - Primeros 20 ayuntamientos")
print("="*60)

# Procesar primeros 20 con verificación
for index in range(min(20, len(df))):
    row = df.iloc[index]
    municipio = row['NOMBRE']

    print(f"\n[{index+1}/20] {municipio}")

    # Buscar información
    info = buscar_en_todoslosayuntamientos(municipio)

    # Mostrar y confirmar
    info_confirmada = mostrar_y_confirmar(municipio, info)

    if info_confirmada:
        # Guardar en el DataFrame
        if len(info_confirmada['emails']) > 0:
            df.at[index, 'Email_Buscado_1'] = info_confirmada['emails'][0]
        if len(info_confirmada['emails']) > 1:
            df.at[index, 'Email_Buscado_2'] = info_confirmada['emails'][1]
        if len(info_confirmada['webs']) > 0:
            df.at[index, 'Web_Buscada'] = info_confirmada['webs'][0]

        df.at[index, 'Verificado'] = 'SI'
    else:
        df.at[index, 'Verificado'] = 'NO'

    # Guardar progreso
    df.to_excel('D:/Aytohacks/Toledo_Verificado.xlsx', index=False)

    time.sleep(1)

print("\n\n" + "="*60)
print("VERIFICACIÓN COMPLETADA")
print("="*60)
print(f"Archivo guardado: D:/Aytohacks/Toledo_Verificado.xlsx")
print("\n¿Quieres continuar con el resto en modo automático? (s/n)")
continuar = input().lower()

if continuar == 's':
    print("\nContinuando en modo automático...")

    for index in range(20, len(df)):
        row = df.iloc[index]
        municipio = row['NOMBRE']

        print(f"\n[{index+1}/{len(df)}] {municipio}")

        info = buscar_en_todoslosayuntamientos(municipio)

        if info['encontrado']:
            if len(info['emails']) > 0:
                df.at[index, 'Email_Buscado_1'] = info['emails'][0]
            if len(info['emails']) > 1:
                df.at[index, 'Email_Buscado_2'] = info['emails'][1]
            if len(info['webs']) > 0:
                df.at[index, 'Web_Buscada'] = info['webs'][0]

            df.at[index, 'Verificado'] = 'AUTO'

        # Guardar cada 10
        if (index + 1) % 10 == 0:
            print(f"  GUARDANDO Guardando progreso...")
            df.to_excel('D:/Aytohacks/Toledo_Completado.xlsx', index=False)

        time.sleep(2)

    # Guardar final
    df.to_excel('D:/Aytohacks/Toledo_Completado.xlsx', index=False)
    print("\nOK PROCESO COMPLETADO")
    print(f"Archivo final: D:/Aytohacks/Toledo_Completado.xlsx")
else:
    print("\nProceso detenido por el usuario.")
    print(f"Archivo parcial guardado: D:/Aytohacks/Toledo_Verificado.xlsx")
