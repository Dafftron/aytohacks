#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GESTOR INTELIGENTE DE ENVÍOS
- En horario laboral (9:00-14:30): Envía a provincias del CENTRO
- Fuera de horario: Envía a provincias de PERIFERIA
- Guarda estado persistente en estado_campana.json
"""

import pandas as pd
import json
import os
from datetime import datetime, time as dt_time

from config import ESTADO_CAMPANA, PROVINCIAS_DIR, DATOS_DIR, BASE_DIR

ESTADO_FILE = ESTADO_CAMPANA

def cargar_estado():
    """Carga el estado actual de la campaña"""
    if os.path.exists(ESTADO_FILE):
        with open(ESTADO_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def guardar_estado(estado):
    """Guarda el estado actual de la campaña"""
    estado['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    with open(ESTADO_FILE, 'w', encoding='utf-8') as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)

def esta_en_horario_laboral():
    """Verifica si estamos en horario laboral (9:00-14:30)"""
    ahora = datetime.now().time()
    return dt_time(9, 0) <= ahora <= dt_time(14, 30)

def obtener_estado_provincia(nombre_provincia):
    """Obtiene el estado actual de una provincia desde su Excel"""
    archivo = f'{PROVINCIAS_DIR}/{nombre_provincia}.xlsx'

    import os
    # Caso especial para Toledo (usar el reorganizado o completo)
    if nombre_provincia.lower() == 'toledo':
        archivo = os.path.join(DATOS_DIR, 'Toledo_Completo_Final.xlsx')

    if not os.path.exists(archivo):
        return None

    try:
        df = pd.read_excel(archivo)
        total = len(df)

        # Buscar columna de envío
        col_enviado = None
        for col in ['Enviado', 'Email_Enviado']:
            if col in df.columns:
                col_enviado = col
                break

        if col_enviado:
            enviados = df[col_enviado].notna().sum()
        else:
            enviados = 0

        # Verificar si tiene emails
        col_email = None
        for col in ['Email_1', 'Email']:
            if col in df.columns:
                col_email = col
                break

        con_email = df[col_email].notna().sum() if col_email else 0

        return {
            'total': total,
            'enviados': enviados,
            'pendientes': total - enviados,
            'con_email': con_email
        }
    except Exception as e:
        print(f"Error al leer {nombre_provincia}: {e}")
        return None

def actualizar_estado_global():
    """Actualiza el estado completo de todas las provincias"""
    estado = cargar_estado()
    if not estado:
        print("ERROR: No se encuentra estado_campana.json")
        return

    print("="*60)
    print("ACTUALIZANDO ESTADO GLOBAL DE LA CAMPAÑA")
    print("="*60)

    # Obtener lista de todas las provincias
    archivos = [f.replace('.xlsx', '') for f in os.listdir(PROVINCIAS_DIR) if f.endswith('.xlsx')]

    total_enviados = 0
    total_municipios = 0

    completadas = []
    en_progreso = {}
    pendientes = {}

    for provincia in archivos:
        info = obtener_estado_provincia(provincia)
        if not info:
            continue

        total_municipios += info['total']
        total_enviados += info['enviados']

        # Clasificar provincia
        es_centro = provincia in estado['configuracion']['provincias_centro']
        tipo = 'centro' if es_centro else 'periferia'

        provincia_data = {
            'total': int(info['total']),
            'enviados': int(info['enviados']),
            'pendientes': int(info['pendientes']),
            'con_email': int(info['con_email']),
            'restriccion_horaria': es_centro,
            'tipo': tipo
        }

        if info['enviados'] >= info['total']:
            completadas.append(provincia)
        elif info['enviados'] > 0:
            en_progreso[provincia] = provincia_data
        else:
            pendientes[provincia] = provincia_data

        status = "COMPLETA" if provincia in completadas else f"{info['enviados']}/{info['total']}"
        print(f"  {provincia:20s} {status:15s} ({tipo})")

    # Actualizar estado
    estado['provincias_completadas'] = completadas
    estado['provincias_en_progreso'] = en_progreso
    estado['provincias_pendientes'] = pendientes
    estado['estadisticas_globales'] = {
        'total_municipios': total_municipios,
        'total_enviados': total_enviados,
        'total_pendientes': total_municipios - total_enviados,
        'porcentaje_completado': round((total_enviados / total_municipios * 100), 2) if total_municipios > 0 else 0
    }

    guardar_estado(estado)

    print("\n" + "="*60)
    print("RESUMEN GLOBAL")
    print("="*60)
    print(f"Provincias completadas: {len(completadas)}")
    print(f"Provincias en progreso: {len(en_progreso)}")
    print(f"Provincias pendientes: {len(pendientes)}")
    print(f"Total enviados: {total_enviados}/{total_municipios} ({estado['estadisticas_globales']['porcentaje_completado']}%)")
    print("="*60)

def recomendar_siguiente_provincia():
    """Recomienda qué provincia enviar según la hora actual"""
    estado = cargar_estado()
    if not estado:
        return None

    en_horario = esta_en_horario_laboral()

    print("\n" + "="*60)
    print(f"RECOMENDACIÓN DE ENVÍO - {datetime.now().strftime('%H:%M')}")
    print("="*60)
    print(f"Horario laboral: {'SÍ (9:00-14:30)' if en_horario else 'NO (fuera de 9:00-14:30)'}")

    # Determinar qué tipo de provincias podemos enviar
    if en_horario:
        print("Tipo recomendado: CENTRO (con restricción horaria)")
        tipo_objetivo = 'centro'
    else:
        print("Tipo recomendado: PERIFERIA (sin restricción horaria)")
        tipo_objetivo = 'periferia'

    # Buscar provincia en progreso del tipo adecuado
    for prov, data in estado['provincias_en_progreso'].items():
        if data['tipo'] == tipo_objetivo:
            print(f"\nCONTINUAR CON: {prov}")
            print(f"  Pendientes: {data['pendientes']}/{data['total']}")
            print(f"  Comando: python enviar_con_horario.py {prov} 20")
            return prov

    # Si no hay en progreso, buscar pendiente
    for prov, data in estado['provincias_pendientes'].items():
        if data['tipo'] == tipo_objetivo and data['con_email'] > 0:
            print(f"\nCOMENZAR CON: {prov}")
            print(f"  Total municipios: {data['total']}")
            print(f"  Con email: {data['con_email']}")
            print(f"  Comando: python enviar_con_horario.py {prov} 20")
            return prov

    print("\nNo hay provincias del tipo recomendado disponibles.")
    return None

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'actualizar':
        actualizar_estado_global()
    else:
        actualizar_estado_global()
        recomendar_siguiente_provincia()
