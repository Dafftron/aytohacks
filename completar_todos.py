#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para completar TODOS los 204 ayuntamientos de Toledo
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import unicodedata
import re
import time

def normalizar_nombre_url(nombre):
    """Normaliza el nombre del municipio para usarlo en URL"""
    nombre = unicodedata.normalize('NFKD', nombre)
    nombre = nombre.encode('ASCII', 'ignore').decode('ASCII')
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
    emails_validos = []
    for e in emails:
        if (not e.endswith('.png') and
            not e.endswith('.jpg') and
            'todoslosayuntamientos' not in e and
            'google' not in e):
            emails_validos.append(e)
    return list(set(emails_validos))[:3]

def extraer_webs(soup):
    """Extrae URLs del contenido HTML"""
    webs = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'http' in href and 'todoslosayuntamientos' not in href and 'google' not in href:
            match = re.search(r'(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', href)
            if match:
                web = match.group(1)
                if not web.endswith(('.png', '.jpg', '.pdf')):
                    webs.append(web)
    return list(set(webs))[:3]

def buscar_ayuntamiento(nombre_municipio):
    """Busca información del ayuntamiento"""
    try:
        nombre_url = normalizar_nombre_url(nombre_municipio)
        url = f"https://www.todoslosayuntamientos.es/castilla-la-mancha/toledo/{nombre_url}"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            texto_completo = soup.get_text()

            emails = extraer_emails(texto_completo)
            webs = extraer_webs(soup)
            telefonos = re.findall(r'\b9[0-9]{8}\b', texto_completo)
            telefonos = list(set(telefonos))[:2]

            return {
                'url': url,
                'emails': emails,
                'webs': webs,
                'telefonos': telefonos,
                'encontrado': True
            }
        else:
            return {'url': url, 'encontrado': False}

    except Exception as e:
        return {'encontrado': False, 'error': str(e)}

# Cargar Excel fusionado
print("Cargando Excel fusionado...")
df = pd.read_excel('D:/Aytohacks/Toledo_Fusionado.xlsx')

# Agregar columnas nuevas si no existen
if 'Email_TodosAyto_1' not in df.columns:
    df['Email_TodosAyto_1'] = ''
if 'Email_TodosAyto_2' not in df.columns:
    df['Email_TodosAyto_2'] = ''
if 'Email_TodosAyto_3' not in df.columns:
    df['Email_TodosAyto_3'] = ''
if 'Web_TodosAyto_1' not in df.columns:
    df['Web_TodosAyto_1'] = ''
if 'Web_TodosAyto_2' not in df.columns:
    df['Web_TodosAyto_2'] = ''
if 'Tel_TodosAyto' not in df.columns:
    df['Tel_TodosAyto'] = ''
if 'URL_TodosAyto' not in df.columns:
    df['URL_TodosAyto'] = ''

print(f"Total: {len(df)} ayuntamientos")
print("\n" + "="*80)
print("INICIANDO BUSQUEDA COMPLETA")
print("="*80)

# Contadores
total = len(df)
encontrados = 0
no_encontrados = 0

# Procesar todos
for index in range(len(df)):
    municipio = df.iloc[index]['NOMBRE']

    print(f"\n[{index+1}/{total}] {municipio}")

    info = buscar_ayuntamiento(municipio)

    if info['encontrado']:
        encontrados += 1
        print(f"  OK - Emails: {len(info['emails'])}, Webs: {len(info['webs'])}, Tels: {len(info['telefonos'])}")

        # Guardar datos
        df.at[index, 'URL_TodosAyto'] = info['url']

        if len(info['emails']) > 0:
            df.at[index, 'Email_TodosAyto_1'] = info['emails'][0]
        if len(info['emails']) > 1:
            df.at[index, 'Email_TodosAyto_2'] = info['emails'][1]
        if len(info['emails']) > 2:
            df.at[index, 'Email_TodosAyto_3'] = info['emails'][2]

        if len(info['webs']) > 0:
            df.at[index, 'Web_TodosAyto_1'] = info['webs'][0]
        if len(info['webs']) > 1:
            df.at[index, 'Web_TodosAyto_2'] = info['webs'][1]

        if len(info['telefonos']) > 0:
            df.at[index, 'Tel_TodosAyto'] = info['telefonos'][0]
    else:
        no_encontrados += 1
        print(f"  X No encontrado")

    # Guardar progreso cada 20 ayuntamientos
    if (index + 1) % 20 == 0:
        print(f"\n  >>> GUARDANDO PROGRESO ({index+1}/{total}) <<<")
        df.to_excel('D:/Aytohacks/Toledo_Completo_Progreso.xlsx', index=False)
        print(f"  >>> Encontrados: {encontrados}, No encontrados: {no_encontrados} <<<\n")

    # Pausa de 2 segundos entre búsquedas
    time.sleep(2)

# Guardar archivo final
print("\n" + "="*80)
print("GUARDANDO ARCHIVO FINAL...")
print("="*80)
df.to_excel('D:/Aytohacks/Toledo_Completo_Final.xlsx', index=False)

print("\n" + "="*80)
print("PROCESO COMPLETADO")
print("="*80)
print(f"Archivo guardado: D:/Aytohacks/Toledo_Completo_Final.xlsx")
print(f"\nEstadisticas finales:")
print(f"  Total procesados: {total}")
print(f"  Encontrados: {encontrados} ({encontrados*100/total:.1f}%)")
print(f"  No encontrados: {no_encontrados} ({no_encontrados*100/total:.1f}%)")
print(f"  Emails encontrados: {df['Email_TodosAyto_1'].notna().sum()}")
print(f"  Webs encontradas: {df['Web_TodosAyto_1'].notna().sum()}")
