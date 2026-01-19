import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re

def limpiar_texto(texto):
    """Limpia espacios y caracteres extraños"""
    if texto:
        return texto.strip()
    return ""

def extraer_emails(texto):
    """Extrae emails de un texto"""
    if not texto:
        return []
    # Patrón para encontrar emails
    patron = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(patron, texto)
    return list(set(emails))  # Eliminar duplicados

def extraer_webs(texto):
    """Extrae URLs de un texto"""
    if not texto:
        return []
    # Patrón para encontrar URLs
    patron = r'(?:https?://)?(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    webs = re.findall(patron, texto)
    return list(set(webs))

def buscar_en_todoslosayuntamientos(nombre_municipio, provincia="toledo"):
    """Busca información del ayuntamiento en todoslosayuntamientos.es"""
    try:
        # Normalizar nombre para URL
        nombre_url = nombre_municipio.lower().replace(" ", "-").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

        # Intentar varias URLs posibles
        urls_posibles = [
            f"https://www.todoslosayuntamientos.es/{provincia}/{nombre_url}",
            f"https://www.todoslosayuntamientos.es/ayuntamiento-{nombre_url}",
        ]

        for url in urls_posibles:
            print(f"  Intentando: {url}")
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extraer todo el texto de la página
                    texto_completo = soup.get_text()

                    # Buscar emails
                    emails = extraer_emails(texto_completo)

                    # Buscar webs
                    webs = extraer_webs(texto_completo)

                    # Buscar teléfonos
                    telefonos = re.findall(r'\b\d{9}\b', texto_completo)

                    resultado = {
                        'emails': emails[:3],  # Máximo 3 emails
                        'webs': webs[:2],      # Máximo 2 webs
                        'telefonos': telefonos[:2],  # Máximo 2 teléfonos
                        'url_encontrada': url
                    }

                    print(f"  ✓ Encontrado: {len(emails)} emails, {len(webs)} webs")
                    return resultado

            except Exception as e:
                print(f"  Error en {url}: {str(e)}")
                continue

        print(f"  No se encontró información")
        return None

    except Exception as e:
        print(f"  Error general: {str(e)}")
        return None

# Cargar el Excel fusionado
print("Cargando Excel fusionado...")
df = pd.read_excel('D:/Aytohacks/Toledo_Fusionado.xlsx')
print(f"Total ayuntamientos: {len(df)}")

# Agregar columnas para nuevos emails si no existen
if 'Email_Buscado_1' not in df.columns:
    df['Email_Buscado_1'] = ''
if 'Email_Buscado_2' not in df.columns:
    df['Email_Buscado_2'] = ''
if 'Web_Buscada' not in df.columns:
    df['Web_Buscada'] = ''
if 'Telefono_Adicional' not in df.columns:
    df['Telefono_Adicional'] = ''

# Procesar cada ayuntamiento
contador = 0
for index, row in df.iterrows():
    contador += 1
    municipio = row['NOMBRE']

    print(f"\n[{contador}/{len(df)}] Buscando: {municipio}")

    # Buscar información
    info = buscar_en_todoslosayuntamientos(municipio)

    if info:
        # Guardar emails encontrados
        if len(info['emails']) > 0:
            df.at[index, 'Email_Buscado_1'] = info['emails'][0]
        if len(info['emails']) > 1:
            df.at[index, 'Email_Buscado_2'] = info['emails'][1]

        # Guardar web encontrada
        if len(info['webs']) > 0:
            df.at[index, 'Web_Buscada'] = info['webs'][0]

        # Guardar teléfono adicional
        if len(info['telefonos']) > 0:
            df.at[index, 'Telefono_Adicional'] = info['telefonos'][0]

    # Pausa para no saturar el servidor
    time.sleep(2)

    # Guardar progreso cada 10 ayuntamientos
    if contador % 10 == 0:
        print(f"\n--- Guardando progreso ({contador}/{len(df)}) ---")
        df.to_excel('D:/Aytohacks/Toledo_Completado_Progreso.xlsx', index=False)

# Guardar resultado final
print("\n\nGuardando resultado final...")
df.to_excel('D:/Aytohacks/Toledo_Completado.xlsx', index=False)
print(f"Archivo guardado en: D:/Aytohacks/Toledo_Completado.xlsx")

# Estadísticas
print("\n=== ESTADISTICAS ===")
print(f"Ayuntamientos procesados: {len(df)}")
print(f"Emails nuevos encontrados: {df['Email_Buscado_1'].notna().sum()}")
print(f"Webs nuevas encontradas: {df['Web_Buscada'].notna().sum()}")
