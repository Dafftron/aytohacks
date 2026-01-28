#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scraper para encontrar emails de municipios pendientes
- Lee pendientes_scraping.csv
- Visita la URL de cada ayuntamiento
- Busca direcciones de email en la pagina
- Actualiza el Excel maestro con los emails encontrados
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
import os
from config import EXCEL_MAESTRO, BASE_DIR

# Patrones para encontrar emails
EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Dominios a evitar (genericos, no oficiales)
DOMINIOS_EVITAR = [
    'example.com', 'test.com', 'email.com',
    'gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com',
    'facebook.com', 'twitter.com', 'instagram.com'
]

# Palabras clave que indican email oficial de ayuntamiento
PALABRAS_CLAVE_AYTO = [
    'ayuntamiento', 'ayto', 'alcaldia', 'secretaria',
    'registro', 'info', 'contacto', 'administracion',
    'oficial', 'municipal', 'concello', 'ajuntament'
]

def es_email_valido(email):
    """Verifica si el email parece ser oficial de ayuntamiento"""
    email_lower = email.lower()

    # Evitar dominios genericos
    for dominio in DOMINIOS_EVITAR:
        if dominio in email_lower:
            return False

    # Preferir emails con palabras clave de ayuntamiento
    return True

def extraer_emails_de_url(url, timeout=10):
    """Extrae emails de una URL"""
    emails_encontrados = []

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        # Buscar en el HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar en texto visible
        texto = soup.get_text()
        emails = re.findall(EMAIL_PATTERN, texto)

        # Buscar en atributos href (mailto:)
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'mailto:' in href:
                email = href.replace('mailto:', '').split('?')[0]
                if re.match(EMAIL_PATTERN, email):
                    emails.append(email)

        # Filtrar y limpiar
        for email in emails:
            email_clean = email.lower().strip()
            if es_email_valido(email_clean) and email_clean not in emails_encontrados:
                emails_encontrados.append(email_clean)

        # Ordenar: preferir emails con palabras clave de ayuntamiento
        def score_email(e):
            score = 0
            for palabra in PALABRAS_CLAVE_AYTO:
                if palabra in e:
                    score += 1
            return -score  # Negativo para ordenar descendente

        emails_encontrados.sort(key=score_email)

    except requests.exceptions.Timeout:
        print(f"    Timeout en {url}")
    except requests.exceptions.RequestException as e:
        print(f"    Error en {url}: {str(e)[:50]}")
    except Exception as e:
        print(f"    Error inesperado: {str(e)[:50]}")

    return emails_encontrados[:3]  # Maximo 3 emails por municipio

def scrapear_pendientes(limite=None):
    """Scrapea emails de municipios pendientes"""

    archivo_pendientes = os.path.join(BASE_DIR, 'pendientes_scraping.csv')

    if not os.path.exists(archivo_pendientes):
        print("ERROR: No existe pendientes_scraping.csv")
        print("Ejecuta primero: python informe_pendientes.py")
        return

    # Cargar pendientes
    df_pend = pd.read_csv(archivo_pendientes)
    print(f"Municipios pendientes: {len(df_pend)}")

    if limite:
        df_pend = df_pend.head(limite)
        print(f"Procesando primeros {limite}")

    # Cargar Excel maestro
    df_maestro = pd.read_excel(EXCEL_MAESTRO)

    # Asegurar columnas de email scrapeado
    for col in ['Email_Scrapeado_1', 'Email_Scrapeado_2', 'Email_Scrapeado_3']:
        if col not in df_maestro.columns:
            df_maestro[col] = ''

    encontrados = 0
    errores = 0

    print()
    print("=" * 60)
    print("SCRAPEANDO EMAILS")
    print("=" * 60)

    for i, row in df_pend.iterrows():
        municipio = row['Municipio']
        provincia = row['Provincia']
        url = row.get('URL', '')

        print(f"[{i+1}/{len(df_pend)}] {municipio} ({provincia})")

        if not url or pd.isna(url):
            print(f"    Sin URL, saltando...")
            errores += 1
            continue

        # Scrapear
        emails = extraer_emails_de_url(url)

        if emails:
            print(f"    Encontrados: {', '.join(emails)}")
            encontrados += 1

            # Actualizar Excel maestro
            mask = (df_maestro['Municipio'] == municipio) & (df_maestro['Provincia'] == provincia)
            if mask.any():
                idx = df_maestro[mask].index[0]
                for j, email in enumerate(emails[:3]):
                    col = f'Email_Scrapeado_{j+1}'
                    df_maestro.at[idx, col] = email
        else:
            print(f"    No se encontraron emails")

        # Pausa para no saturar
        time.sleep(1)

        # Guardar cada 10 municipios
        if (i + 1) % 10 == 0:
            df_maestro.to_excel(EXCEL_MAESTRO, index=False)
            print(f"    [Guardado progreso: {i+1} procesados]")

    # Guardar final
    df_maestro.to_excel(EXCEL_MAESTRO, index=False)

    print()
    print("=" * 60)
    print(f"RESUMEN: {encontrados} municipios con emails encontrados")
    print(f"         {errores} errores/sin URL")
    print("=" * 60)
    print()
    print("Ejecuta de nuevo enviar_verificado_v2.py para enviar a los nuevos emails")

def main():
    import sys

    print("=" * 60)
    print("SCRAPER DE EMAILS - SEGUNDA VUELTA")
    print("=" * 60)
    print()

    limite = None
    if len(sys.argv) > 1:
        try:
            limite = int(sys.argv[1])
            print(f"Limite: {limite} municipios")
        except:
            pass

    scrapear_pendientes(limite)

if __name__ == '__main__':
    main()
