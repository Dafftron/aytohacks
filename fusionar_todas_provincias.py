#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para fusionar TODOS los exceles de provincias en un único archivo
con datos extraídos de todoslosayuntamientos.es
"""

import pandas as pd
import glob
import os

print("="*60)
print("FUSIONANDO TODAS LAS PROVINCIAS EN UN ÚNICO EXCEL")
print("="*60)

# Buscar todos los archivos xlsx en la carpeta provincias
archivos = glob.glob('D:/Aytohacks/provincias/*.xlsx')
print(f"\nArchivos encontrados: {len(archivos)}")

# Lista para almacenar todos los DataFrames
dfs = []

# Leer cada archivo
for archivo in sorted(archivos):
    nombre_prov = os.path.basename(archivo).replace('.xlsx', '')
    try:
        df = pd.read_excel(archivo)

        # Asegurarse de que tiene las columnas necesarias
        if 'Municipio' in df.columns:
            # Agregar columna de provincia si no existe
            if 'Provincia' not in df.columns:
                df['Provincia'] = nombre_prov

            dfs.append(df)
            print(f"  OK: {nombre_prov} - {len(df)} municipios")
        else:
            print(f"  SKIP: {nombre_prov} - Sin columna Municipio")
    except Exception as e:
        print(f"  ERROR: {nombre_prov} - {e}")

# Fusionar todos los DataFrames
if len(dfs) > 0:
    df_completo = pd.concat(dfs, ignore_index=True)

    # Estadísticas
    print("\n" + "="*60)
    print("ESTADÍSTICAS DEL ARCHIVO COMPLETO")
    print("="*60)
    print(f"Total municipios: {len(df_completo)}")
    print(f"Total provincias: {df_completo['Provincia'].nunique()}")

    # Contar emails
    if 'Email_1' in df_completo.columns:
        total_con_email = df_completo['Email_1'].notna().sum()
        print(f"Municipios con Email_1: {total_con_email} ({total_con_email/len(df_completo)*100:.1f}%)")

    if 'Email_Enviado' in df_completo.columns:
        total_enviados = df_completo['Email_Enviado'].notna().sum()
        print(f"Correos enviados: {total_enviados} ({total_enviados/len(df_completo)*100:.1f}%)")

    # Por provincia
    print("\n" + "="*60)
    print("RESUMEN POR PROVINCIA")
    print("="*60)
    resumen = df_completo.groupby('Provincia').agg({
        'Municipio': 'count',
        'Email_1': lambda x: x.notna().sum(),
        'Email_Enviado': lambda x: x.notna().sum() if 'Email_Enviado' in df_completo.columns else 0
    }).rename(columns={
        'Municipio': 'Total',
        'Email_1': 'Con_Email',
        'Email_Enviado': 'Enviados'
    })
    resumen = resumen.sort_values('Total', ascending=False)
    print(resumen.to_string())

    # Guardar archivo completo
    output_file = 'D:/Aytohacks/Espana_Completa_TodosAyuntamientos.xlsx'
    df_completo.to_excel(output_file, index=False)

    print("\n" + "="*60)
    print(f"ARCHIVO GUARDADO: {output_file}")
    print(f"Total filas: {len(df_completo)}")
    print(f"Total columnas: {len(df_completo.columns)}")
    print("="*60)
else:
    print("\nERROR: No se encontraron archivos válidos para fusionar")
