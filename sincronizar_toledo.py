#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para sincronizar datos entre Toledo_Reorganizado.xlsx y provincias/Toledo.xlsx
Fusiona los envíos realizados desde ambos archivos
"""

import pandas as pd
from datetime import datetime

print("="*60)
print("SINCRONIZANDO DATOS DE TOLEDO")
print("="*60)

# Cargar ambos exceles
df_reorganizado = pd.read_excel('D:/Aytohacks/Toledo_Reorganizado.xlsx')
df_provincias = pd.read_excel('D:/Aytohacks/provincias/Toledo.xlsx')

print(f"\nToledo_Reorganizado: {len(df_reorganizado)} municipios")
print(f"provincias/Toledo: {len(df_provincias)} municipios")

# Buscar columna de envío en provincias
col_enviado_prov = 'Email_Enviado' if 'Email_Enviado' in df_provincias.columns else 'Enviado'

# Contar envíos en cada archivo
enviados_reorganizado = df_reorganizado['Enviado'].notna().sum()
enviados_provincias = df_provincias[col_enviado_prov].notna().sum() if col_enviado_prov in df_provincias.columns else 0

print(f"\nEnviados en Reorganizado: {enviados_reorganizado}")
print(f"Enviados en Provincias: {enviados_provincias}")

# Si hay envíos en provincias/ que no están en reorganizado, sincronizarlos
if enviados_provincias > 0:
    print("\nSincronizando envíos de provincias/ -> Reorganizado...")

    # Mapear municipios enviados
    enviados_prov = df_provincias[df_provincias[col_enviado_prov].notna()]

    for idx, row in enviados_prov.iterrows():
        municipio = row['Municipio']
        fecha_envio = row[col_enviado_prov]

        # Buscar en reorganizado (comparar nombres normalizados)
        match = df_reorganizado[df_reorganizado['NOMBRE'].str.upper().str.strip() == municipio.upper().strip()]

        if len(match) > 0:
            idx_reorg = match.index[0]
            if pd.isna(df_reorganizado.at[idx_reorg, 'Enviado']):
                df_reorganizado.at[idx_reorg, 'Enviado'] = fecha_envio
                print(f"  Sincronizado: {municipio}")

    # Guardar reorganizado actualizado
    df_reorganizado.to_excel('D:/Aytohacks/Toledo_Reorganizado.xlsx', index=False)
    print(f"\nActualizado Toledo_Reorganizado.xlsx")

# Estadísticas finales
enviados_final = df_reorganizado['Enviado'].notna().sum()
pendientes = len(df_reorganizado) - enviados_final

print("\n" + "="*60)
print("ESTADO FINAL")
print("="*60)
print(f"Total municipios: {len(df_reorganizado)}")
print(f"Enviados: {enviados_final}")
print(f"Pendientes: {pendientes}")
print(f"Progreso: {enviados_final/len(df_reorganizado)*100:.1f}%")

# Mostrar últimos enviados
if enviados_final > 0:
    print("\nÚltimos 10 municipios enviados:")
    ultimos = df_reorganizado[df_reorganizado['Enviado'].notna()].tail(10)
    print(ultimos[['NOMBRE', 'Enviado']].to_string(index=False))
