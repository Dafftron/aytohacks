#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera informe de municipios pendientes de envio
- Sin email
- Con email rebotado
- Con email pero no enviado

Util para planificar segunda vuelta de scraping
"""

import pandas as pd
import os
from datetime import datetime
from config import EXCEL_MAESTRO, BASE_DIR

def generar_informe():
    print("=" * 60)
    print("INFORME DE MUNICIPIOS PENDIENTES")
    print("=" * 60)
    print()

    df = pd.read_excel(EXCEL_MAESTRO)

    # Estadisticas por provincia
    provincias = df['Provincia'].unique()

    resumen = []
    pendientes_scraping = []

    for prov in sorted(provincias):
        df_prov = df[df['Provincia'] == prov]
        total = len(df_prov)

        # Contar estados
        enviados = 0
        rebotados = 0
        sin_email = 0
        pendientes = 0

        for idx, row in df_prov.iterrows():
            tiene_email = False
            for col in ['Email_1', 'Email_2', 'Email_3']:
                if col in row.index and pd.notna(row[col]) and '@' in str(row[col]):
                    tiene_email = True
                    break

            enviado = pd.notna(row.get('Email_Enviado')) and str(row.get('Email_Enviado')).strip()
            rebotado = pd.notna(row.get('Email_Rebotado')) and str(row.get('Email_Rebotado')).strip()

            if rebotado:
                rebotados += 1
                pendientes_scraping.append({
                    'Provincia': prov,
                    'Municipio': row['Municipio'],
                    'Motivo': 'REBOTADO',
                    'URL': row.get('URL', '')
                })
            elif enviado:
                enviados += 1
            elif not tiene_email:
                sin_email += 1
                pendientes_scraping.append({
                    'Provincia': prov,
                    'Municipio': row['Municipio'],
                    'Motivo': 'SIN_EMAIL',
                    'URL': row.get('URL', '')
                })
            else:
                pendientes += 1

        if total > 0:
            pct_ok = (enviados / total) * 100
            resumen.append({
                'Provincia': prov,
                'Total': total,
                'Enviados': enviados,
                'Rebotados': rebotados,
                'Sin_Email': sin_email,
                'Pendientes': pendientes,
                'Pct_OK': pct_ok
            })

    # Mostrar resumen
    print(f"{'Provincia':<20} {'Total':>6} {'Env':>5} {'Reb':>5} {'NoMail':>6} {'Pend':>5} {'%OK':>6}")
    print("-" * 60)

    total_enviados = 0
    total_rebotados = 0
    total_sin_email = 0
    total_pendientes = 0
    total_municipios = 0

    for r in resumen:
        print(f"{r['Provincia']:<20} {r['Total']:>6} {r['Enviados']:>5} {r['Rebotados']:>5} {r['Sin_Email']:>6} {r['Pendientes']:>5} {r['Pct_OK']:>5.1f}%")
        total_enviados += r['Enviados']
        total_rebotados += r['Rebotados']
        total_sin_email += r['Sin_Email']
        total_pendientes += r['Pendientes']
        total_municipios += r['Total']

    print("-" * 60)
    pct_total = (total_enviados / total_municipios * 100) if total_municipios > 0 else 0
    print(f"{'TOTAL':<20} {total_municipios:>6} {total_enviados:>5} {total_rebotados:>5} {total_sin_email:>6} {total_pendientes:>5} {pct_total:>5.1f}%")

    print()
    print("=" * 60)
    print("RESUMEN PARA SEGUNDA VUELTA (SCRAPING)")
    print("=" * 60)
    print(f"Municipios para scrapear: {len(pendientes_scraping)}")
    print(f"  - Rebotados: {total_rebotados}")
    print(f"  - Sin email: {total_sin_email}")
    print()

    # Guardar lista de pendientes para scraping
    if pendientes_scraping:
        df_pendientes = pd.DataFrame(pendientes_scraping)
        archivo_pendientes = os.path.join(BASE_DIR, 'pendientes_scraping.csv')
        df_pendientes.to_csv(archivo_pendientes, index=False, encoding='utf-8')
        print(f"Lista guardada en: pendientes_scraping.csv")

        # Mostrar por provincia
        print()
        print("Por provincia:")
        for prov in sorted(df_pendientes['Provincia'].unique()):
            count = len(df_pendientes[df_pendientes['Provincia'] == prov])
            print(f"  {prov}: {count} municipios")

    # Guardar informe markdown
    with open(os.path.join(BASE_DIR, 'PENDIENTES.md'), 'w', encoding='utf-8') as f:
        f.write(f"# Municipios Pendientes - Segunda Vuelta\n\n")
        f.write(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(f"## Resumen\n\n")
        f.write(f"- **Total municipios**: {total_municipios}\n")
        f.write(f"- **Enviados OK**: {total_enviados} ({pct_total:.1f}%)\n")
        f.write(f"- **Rebotados**: {total_rebotados}\n")
        f.write(f"- **Sin email**: {total_sin_email}\n")
        f.write(f"- **Pendientes primera vuelta**: {total_pendientes}\n\n")
        f.write(f"## Para Scraping: {len(pendientes_scraping)} municipios\n\n")

        if pendientes_scraping:
            df_pend = pd.DataFrame(pendientes_scraping)
            for prov in sorted(df_pend['Provincia'].unique()):
                df_p = df_pend[df_pend['Provincia'] == prov]
                f.write(f"### {prov} ({len(df_p)})\n\n")
                for _, row in df_p.iterrows():
                    f.write(f"- {row['Municipio']} ({row['Motivo']})\n")
                f.write("\n")

    print(f"Informe guardado en: PENDIENTES.md")

if __name__ == '__main__':
    generar_informe()
