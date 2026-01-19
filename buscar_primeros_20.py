#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para buscar información de los primeros 20 ayuntamientos
SIN interacción - solo muestra resultados
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import unicodedata
import re

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
    # Filtrar emails no deseados
    emails_validos = []
    for e in emails:
        if (not e.endswith('.png') and
            not e.endswith('.jpg') and
            'todoslosayuntamientos' not in e and
            'google' not in e):
            emails_validos.append(e)
    return list(set(emails_validos))

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
                'emails': emails[:3],
                'webs': webs,
                'telefonos': telefonos,
                'encontrado': True
            }
        else:
            return {'url': url, 'encontrado': False, 'error': f'HTTP {response.status_code}'}

    except Exception as e:
        return {'encontrado': False, 'error': str(e)}

# Cargar Excel
print("Cargando Excel...")
df = pd.read_excel('D:/Aytohacks/Toledo_Fusionado.xlsx')

print("\n" + "="*80)
print("BUSQUEDA DE INFORMACION - PRIMEROS 20 AYUNTAMIENTOS DE TOLEDO")
print("="*80)

resultados = []

for index in range(min(20, len(df))):
    municipio = df.iloc[index]['NOMBRE']

    print(f"\n[{index+1}/20] {municipio}")
    print("-" * 80)

    info = buscar_ayuntamiento(municipio)

    if info['encontrado']:
        print(f"URL: {info['url']}")
        print(f"Emails encontrados ({len(info['emails'])}): {', '.join(info['emails']) if info['emails'] else 'NINGUNO'}")
        print(f"Webs encontradas ({len(info['webs'])}): {', '.join(info['webs']) if info['webs'] else 'NINGUNA'}")
        print(f"Telefonos ({len(info['telefonos'])}): {', '.join(info['telefonos']) if info['telefonos'] else 'NINGUNO'}")
    else:
        print(f"NO SE ENCONTRO INFORMACION")
        if 'error' in info:
            print(f"Error: {info['error']}")

    resultados.append({
        'Municipio': municipio,
        'URL': info.get('url', ''),
        'Encontrado': info['encontrado'],
        'Emails': ', '.join(info.get('emails', [])),
        'Webs': ', '.join(info.get('webs', [])),
        'Telefonos': ', '.join(info.get('telefonos', []))
    })

# Guardar resultados en Excel
df_resultados = pd.DataFrame(resultados)
df_resultados.to_excel('D:/Aytohacks/Resultados_Busqueda_20.xlsx', index=False)

print("\n" + "="*80)
print("BUSQUEDA COMPLETADA")
print("="*80)
print(f"Resultados guardados en: D:/Aytohacks/Resultados_Busqueda_20.xlsx")
print(f"\nResumen:")
print(f"  Total procesados: 20")
print(f"  Encontrados: {sum(1 for r in resultados if r['Encontrado'])}")
print(f"  No encontrados: {sum(1 for r in resultados if not r['Encontrado'])}")
