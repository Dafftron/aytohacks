#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para reorganizar el Excel manteniendo TODAS las columnas originales
Estructura: datos administrativos -> teléfonos -> webs -> emails -> enviado/llamado -> metadatos
"""

import pandas as pd

print("Cargando Excel actual...")
df = pd.read_excel('D:/Aytohacks/Toledo_Completo_Final.xlsx')

print(f"Total municipios: {len(df)}")

# Crear nuevo DataFrame con el orden deseado
df_nuevo = pd.DataFrame()

# 1. DATOS ADMINISTRATIVOS (mantener en su posición original)
df_nuevo['NOMBRE'] = df['NOMBRE']
df_nuevo['nombrevia'] = df['nombrevia']
df_nuevo['numvia'] = df['numvia']
df_nuevo['cdpostal'] = df['cdpostal']
df_nuevo['localidad'] = df['localidad']
df_nuevo['PROV_nombre'] = df['PROV_nombre']
df_nuevo['CCAA_nombre'] = df['CCAA_nombre']

# 2. TELÉFONOS (oficial + buscado)
df_nuevo['tfno'] = df['tfno']
df_nuevo['Tel_TodosAyto'] = df['Tel_TodosAyto']

# 3. WEBS (oficial + buscadas)
df_nuevo['siteweb'] = df['siteweb']
df_nuevo['Web_TodosAyto_1'] = df['Web_TodosAyto_1']
df_nuevo['Web_TodosAyto_2'] = df['Web_TodosAyto_2']
df_nuevo['Web_Diputacion'] = df['Web_Diputacion']

# 4. EMAILS - Solo 3 columnas
df_nuevo['Email_1'] = df['Email_1']  # Email original del gobierno
df_nuevo['Email_2'] = df['Email_TodosAyto_1']  # Email de todoslosayuntamientos.es (buscado)
df_nuevo['Email_3'] = df['Email_Diputacion']  # Email de la diputación

# 5. CAMPOS DE SEGUIMIENTO
df_nuevo['Enviado'] = df.get('Enviado', '')
df_nuevo['Llamado'] = df.get('Llamado', '')

# 6. METADATOS (al final para referencia)
if 'Origen_Email_1' in df.columns:
    df_nuevo['Origen_Email_1'] = df['Origen_Email_1']
if 'Origen_Email_2' in df.columns:
    df_nuevo['Origen_Email_2'] = df['Origen_Email_2']
if 'Origen_Email_3' in df.columns:
    df_nuevo['Origen_Email_3'] = df['Origen_Email_3']
df_nuevo['URL_TodosAyto'] = df['URL_TodosAyto']

# Estadísticas
print("\n" + "="*60)
print("ESTADISTICAS DE EMAILS")
print("="*60)
print(f"Email_1 (Original gobierno):      {df_nuevo['Email_1'].notna().sum()} municipios")
print(f"Email_2 (TodosAyto buscado):      {df_nuevo['Email_2'].notna().sum()} municipios")
print(f"Email_3 (Diputacion):             {df_nuevo['Email_3'].notna().sum()} municipios")

print("\n" + "="*60)
print("ESTADISTICAS DE WEBS Y TELEFONOS")
print("="*60)
print(f"siteweb (oficial):                {df_nuevo['siteweb'].notna().sum()} municipios")
print(f"Web_TodosAyto_1:                  {df_nuevo['Web_TodosAyto_1'].notna().sum()} municipios")
print(f"tfno (oficial):                   {df_nuevo['tfno'].notna().sum()} municipios")
print(f"Tel_TodosAyto:                    {df_nuevo['Tel_TodosAyto'].notna().sum()} municipios")

# Guardar
output_path = 'D:/Aytohacks/Toledo_Reorganizado.xlsx'
df_nuevo.to_excel(output_path, index=False)

print("\n" + "="*60)
print("ARCHIVO GUARDADO")
print("="*60)
print(f"Ruta: {output_path}")
print(f"Total columnas: {len(df_nuevo.columns)}")
print("\nEstructura de columnas:")
for i, col in enumerate(df_nuevo.columns, 1):
    print(f"  {i:2d}. {col}")

# Mostrar ejemplo
print("\n" + "="*60)
print("EJEMPLO: Primeros 3 municipios")
print("="*60)
columnas_ejemplo = ['NOMBRE', 'tfno', 'Tel_TodosAyto', 'Email_1', 'Email_2', 'Email_3']
print(df_nuevo[columnas_ejemplo].head(3).to_string())
