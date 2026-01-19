#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para scrapear TODOS los ayuntamientos de España
desde todoslosayuntamientos.es, organizados por comunidad autónoma y provincia.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re
import sys

BASE_URL = 'https://www.todoslosayuntamientos.es'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
OUTPUT_DIR = 'C:/aytohacks/provincias'

# Emails a ignorar
EMAILS_IGNORAR = ['info@todoslosayuntamientos.es', 'example.com', 'test@']

# Estructura completa de España
COMUNIDADES = {
    'Andalucia': {
        'slug': 'andalucia',
        'provincias': ['almeria', 'cadiz', 'cordoba', 'granada', 'huelva', 'jaen', 'malaga', 'sevilla']
    },
    'Aragon': {
        'slug': 'aragon',
        'provincias': ['huesca', 'teruel', 'zaragoza']
    },
    'Asturias': {
        'slug': 'principado-de-asturias',
        'provincias': ['asturias']
    },
    'Baleares': {
        'slug': 'islas-baleares',
        'provincias': ['islas-baleares']
    },
    'Canarias': {
        'slug': 'canarias',
        'provincias': ['las-palmas', 'santa-cruz-de-tenerife']
    },
    'Cantabria': {
        'slug': 'cantabria',
        'provincias': ['cantabria']
    },
    'Castilla_Leon': {
        'slug': 'castilla-leon',
        'provincias': ['avila', 'burgos', 'leon', 'palencia', 'salamanca', 'segovia', 'soria', 'valladolid', 'zamora']
    },
    'Castilla_La_Mancha': {
        'slug': 'castilla-la-mancha',
        'provincias': ['albacete', 'ciudad-real', 'cuenca', 'guadalajara', 'toledo']
    },
    'Cataluna': {
        'slug': 'cataluna',
        'provincias': ['barcelona', 'girona', 'lleida', 'tarragona']
    },
    'Comunidad_Valenciana': {
        'slug': 'comunidad-valenciana',
        'provincias': ['alicante', 'castellon', 'valencia']
    },
    'Extremadura': {
        'slug': 'extremadura',
        'provincias': ['badajoz', 'caceres']
    },
    'Galicia': {
        'slug': 'galicia',
        'provincias': ['a-coruna', 'lugo', 'ourense', 'pontevedra']
    },
    'Madrid': {
        'slug': 'comunidad-de-madrid',
        'provincias': ['madrid']
    },
    'Murcia': {
        'slug': 'region-de-murcia',
        'provincias': ['murcia']
    },
    'Navarra': {
        'slug': 'comunidad-foral-de-navarra',
        'provincias': ['navarra']
    },
    'Pais_Vasco': {
        'slug': 'pais-vasco',
        'provincias': ['alava', 'guipuzcoa', 'vizcaya']
    },
    'La_Rioja': {
        'slug': 'la-rioja',
        'provincias': ['la-rioja']
    },
    'Ceuta': {
        'slug': 'ceuta',
        'provincias': ['ceuta']
    },
    'Melilla': {
        'slug': 'melilla',
        'provincias': ['melilla']
    }
}

def obtener_municipios_provincia(comunidad_slug, provincia_slug):
    """Obtiene lista de municipios de una provincia"""
    url = f'{BASE_URL}/{comunidad_slug}/{provincia_slug}'
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            print(f'  Error HTTP {r.status_code} en {url}')
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        municipios = []

        # Buscar enlaces a municipios
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Los municipios tienen formato /{comunidad}/{provincia}/{municipio}
            if href.startswith(f'/{comunidad_slug}/{provincia_slug}/') and href.count('/') == 3:
                nombre = link.get_text(strip=True)
                slug = href.split('/')[-1]
                if nombre and slug:
                    municipios.append({'nombre': nombre, 'slug': slug, 'url': href})

        # Eliminar duplicados
        vistos = set()
        unicos = []
        for m in municipios:
            if m['slug'] not in vistos:
                vistos.add(m['slug'])
                unicos.append(m)

        return unicos

    except Exception as e:
        print(f'  Error obteniendo municipios: {e}')
        return []


def email_valido(email):
    """Verifica si un email es válido y no está en la lista de ignorados"""
    email = email.lower().strip()
    if not '@' in email:
        return False
    for ignorar in EMAILS_IGNORAR:
        if ignorar in email:
            return False
    return True


def scrapear_email_municipio(url_municipio):
    """Scrapea los emails de la página de un municipio"""
    try:
        url = f'{BASE_URL}{url_municipio}'
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        emails = []

        # Buscar emails en enlaces mailto:
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'mailto:' in href:
                email = href.replace('mailto:', '').split('?')[0].strip().lower()
                if email_valido(email) and email not in emails:
                    emails.append(email)

        # Buscar emails en el texto con regex
        texto = soup.get_text()
        patron = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        for match in re.findall(patron, texto):
            email = match.lower()
            if email_valido(email) and email not in emails:
                emails.append(email)

        return emails[:3]  # Máximo 3 emails

    except Exception as e:
        return []


def limpiar_nombre_municipio(nombre):
    """Limpia el nombre del municipio quitando información extra"""
    # El nombre viene como "Ayuntamiento deMunicipioProvinciaHabitantes..."
    # Intentar extraer solo el nombre del municipio
    if 'Ayuntamiento de' in nombre:
        nombre = nombre.replace('Ayuntamiento de', '').strip()
    # Quitar "Direccion..." y todo lo que sigue
    nombre = re.sub(r'Direccion.*', '', nombre, flags=re.IGNORECASE)
    # Quitar números de habitantes (números grandes pegados)
    nombre = re.sub(r'\d{4,}.*', '', nombre)
    nombre = re.sub(r'Habitantes:?\s*[\d.,]+.*', '', nombre)
    nombre = re.sub(r'Actualizado.*', '', nombre)
    # Quitar nombres de provincia pegados al final (lista común)
    provincias = ['Almería', 'Almeria', 'Cádiz', 'Cadiz', 'Córdoba', 'Cordoba', 'Granada',
                  'Huelva', 'Jaén', 'Jaen', 'Málaga', 'Malaga', 'Sevilla', 'Huesca',
                  'Teruel', 'Zaragoza', 'Asturias', 'Baleares', 'Las Palmas', 'Santa Cruz',
                  'Cantabria', 'Ávila', 'Avila', 'Burgos', 'León', 'Leon', 'Palencia',
                  'Salamanca', 'Segovia', 'Soria', 'Valladolid', 'Zamora', 'Albacete',
                  'Ciudad Real', 'Cuenca', 'Guadalajara', 'Toledo', 'Barcelona', 'Girona',
                  'Lleida', 'Tarragona', 'Alicante', 'Castellón', 'Castellon', 'Valencia',
                  'Badajoz', 'Cáceres', 'Caceres', 'A Coruña', 'A Coruna', 'Lugo',
                  'Ourense', 'Pontevedra', 'Madrid', 'Murcia', 'Navarra', 'Álava', 'Alava',
                  'Guipúzcoa', 'Guipuzcoa', 'Vizcaya', 'La Rioja', 'Ceuta', 'Melilla']
    for prov in provincias:
        if nombre.endswith(prov):
            nombre = nombre[:-len(prov)]
    nombre = nombre.strip()
    return nombre


def scrapear_provincia(comunidad_nombre, comunidad_slug, provincia_slug):
    """Scrapea todos los ayuntamientos de una provincia"""

    # Nombre bonito para el archivo
    provincia_nombre = provincia_slug.replace('-', '_').replace('_', ' ').title().replace(' ', '_')

    print(f'\n{"="*60}')
    print(f'PROVINCIA: {provincia_nombre} ({comunidad_nombre})')
    print(f'{"="*60}')
    sys.stdout.flush()

    # Obtener lista de municipios
    print(f'Obteniendo municipios de {provincia_slug}...')
    municipios = obtener_municipios_provincia(comunidad_slug, provincia_slug)
    print(f'Encontrados {len(municipios)} municipios')
    sys.stdout.flush()

    if not municipios:
        return None

    # Scrapear cada municipio
    datos = []
    for i, muni in enumerate(municipios, 1):
        nombre_limpio = limpiar_nombre_municipio(muni['nombre'])
        print(f'[{i}/{len(municipios)}] {nombre_limpio[:30]}...', end=' ')
        sys.stdout.flush()

        emails = scrapear_email_municipio(muni['url'])

        registro = {
            'Municipio': nombre_limpio,
            'Provincia': provincia_nombre,
            'Comunidad': comunidad_nombre,
            'Email_1': emails[0] if len(emails) > 0 else '',
            'Email_2': emails[1] if len(emails) > 1 else '',
            'Email_3': emails[2] if len(emails) > 2 else '',
            'URL': f'{BASE_URL}{muni["url"]}',
            'Email_Enviado': ''
        }
        datos.append(registro)

        if emails:
            print(f'{len(emails)} email(s)')
        else:
            print('sin email')
        sys.stdout.flush()

        time.sleep(0.3)  # Pausa entre requests

    # Guardar Excel
    if datos:
        df = pd.DataFrame(datos)

        # Crear directorio si no existe
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        archivo = f'{OUTPUT_DIR}/{provincia_nombre}.xlsx'
        df.to_excel(archivo, index=False)

        con_email = len(df[df['Email_1'] != ''])
        print(f'\nGuardado: {archivo}')
        print(f'Total: {len(df)} municipios, {con_email} con email')
        sys.stdout.flush()

        return df

    return None


def main():
    """Scrapea todas las comunidades y provincias de España"""

    print('='*60)
    print('SCRAPEANDO TODOS LOS AYUNTAMIENTOS DE ESPAÑA')
    print('='*60)
    sys.stdout.flush()

    # Crear directorio
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Resumen final
    resumen = []

    for comunidad_nombre, info in COMUNIDADES.items():
        comunidad_slug = info['slug']

        for provincia_slug in info['provincias']:
            df = scrapear_provincia(comunidad_nombre, comunidad_slug, provincia_slug)

            if df is not None:
                con_email = len(df[df['Email_1'] != ''])
                resumen.append({
                    'Comunidad': comunidad_nombre,
                    'Provincia': provincia_slug.replace('-', '_').title(),
                    'Total_Municipios': len(df),
                    'Con_Email': con_email
                })

            time.sleep(1)  # Pausa entre provincias

    # Guardar resumen
    if resumen:
        df_resumen = pd.DataFrame(resumen)
        df_resumen.to_excel(f'{OUTPUT_DIR}/_RESUMEN_ESPANA.xlsx', index=False)

        print('\n' + '='*60)
        print('RESUMEN FINAL')
        print('='*60)
        total_muni = sum(r['Total_Municipios'] for r in resumen)
        total_email = sum(r['Con_Email'] for r in resumen)
        print(f'Total provincias: {len(resumen)}')
        print(f'Total municipios: {total_muni}')
        print(f'Con email: {total_email}')
        print(f'\nArchivos guardados en: {OUTPUT_DIR}')
        sys.stdout.flush()


if __name__ == '__main__':
    main()
