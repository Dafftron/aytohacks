#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Actualiza el estado completo de la campaña desde IMAP
Genera archivos listos para GitHub
"""

import imaplib
import json
from datetime import datetime
from config import IMAP_SERVER, IMAP_PORT, EMAIL_USER, EMAIL_PASS, BASE_DIR, ESTADO_CAMPANA
import os

def obtener_estado_desde_imap():
    """Obtiene el estado real desde IMAP"""
    print("Conectando a IMAP...")
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    imap.login(EMAIL_USER, EMAIL_PASS)

    provincias = [
        'Toledo', 'Ciudad_Real', 'Cuenca', 'Guadalajara', 'Albacete',
        'Madrid', 'Avila', 'Segovia', 'Valladolid', 'Salamanca', 'Zamora',
        'Leon', 'Palencia', 'Burgos', 'Soria',
        'Barcelona', 'Girona', 'Lleida', 'Tarragona',
        'Valencia', 'Alicante', 'Castellon',
        'Sevilla', 'Malaga', 'Granada', 'Cordoba', 'Jaen', 'Huelva', 'Cadiz', 'Almeria',
        'Zaragoza', 'Huesca', 'Teruel',
        'A_Coruna', 'Lugo', 'Ourense', 'Pontevedra',
        'Asturias', 'Cantabria',
        'Vizcaya', 'Guipuzcoa', 'Alava', 'Navarra', 'La_Rioja',
        'Murcia', 'Badajoz', 'Caceres',
        'Baleares', 'Las_Palmas', 'Santa_Cruz_Tenerife',
        'Ceuta', 'Melilla'
    ]

    estado_provincias = {}
    total_enviados = 0

    for provincia in provincias:
        carpeta = f'INBOX.Sent.{provincia}'
        try:
            status, messages = imap.select(carpeta, readonly=True)
            if status == 'OK':
                status, data = imap.search(None, 'ALL')
                if status == 'OK' and data[0]:
                    num_emails = len(data[0].split())
                else:
                    num_emails = 0

                if num_emails > 0:
                    estado_provincias[provincia] = num_emails
                    total_enviados += num_emails
        except:
            pass

    imap.logout()

    return estado_provincias, total_enviados

def generar_progreso_md(estado_provincias, total_enviados):
    """Genera archivo PROGRESO.md para GitHub"""

    completadas = {k: v for k, v in estado_provincias.items() if v >= 50}
    en_progreso = {k: v for k, v in estado_provincias.items() if 0 < v < 50}

    contenido = f"""# 📊 PROGRESO DE LA CAMPAÑA AYTOHACKS

**Última actualización:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

---

## 🎯 RESUMEN GENERAL

- **Total emails enviados:** {total_enviados}
- **Provincias completadas:** {len(completadas)}
- **Provincias en progreso:** {len(en_progreso)}
- **Provincias pendientes:** {52 - len(estado_provincias)}
- **Progreso estimado:** {(total_enviados / 2893 * 100):.1f}% de España

---

## ✅ PROVINCIAS COMPLETADAS ({len(completadas)})

"""

    for prov, num in sorted(completadas.items(), key=lambda x: x[1], reverse=True):
        contenido += f"- **{prov}**: {num} emails ✅\n"

    contenido += f"\n---\n\n## ⏳ PROVINCIAS EN PROGRESO ({len(en_progreso)})\n\n"

    for prov, num in sorted(en_progreso.items(), key=lambda x: x[1], reverse=True):
        contenido += f"- **{prov}**: {num} emails 🔄\n"

    contenido += f"""
---

## 📈 ESTADÍSTICAS

### Emails por día (estimado)
- Velocidad actual: ~{total_enviados / 7:.0f} emails/día
- Tiempo para completar: ~{(2893 - total_enviados) / (total_enviados / 7):.0f} días

### Top 5 Provincias
"""

    top5 = sorted(estado_provincias.items(), key=lambda x: x[1], reverse=True)[:5]
    for i, (prov, num) in enumerate(top5, 1):
        contenido += f"{i}. **{prov}**: {num} emails\n"

    contenido += f"""
---

## 🎯 PRÓXIMAS PROVINCIAS RECOMENDADAS

### Periferia (sin restricción horaria)
- Barcelona (83 municipios)
- Valencia (88 municipios)
- Sevilla (69 municipios)
- Málaga (71 municipios)

### Centro (horario 9:00-14:30)
- Guadalajara (91 municipios)
- Salamanca (89 municipios)
- Valladolid (77 municipios)

---

## 🔄 ÚLTIMA ACTUALIZACIÓN

Este archivo se actualiza automáticamente cada 10 envíos.

**Sistema:** Aytohacks v2.0
**Empresa:** TecnoHita Instrumentación
**Contacto:** david@tecnohita.com

---

_Generado automáticamente por `actualizar_estado_completo.py`_
"""

    return contenido

def actualizar_estado_json(estado_provincias, total_enviados):
    """Actualiza estado_campana.json"""
    estado = {
        "ultima_actualizacion": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "total_emails_enviados": total_enviados,
        "provincias_con_envios": len(estado_provincias),
        "provincias_completadas": [k for k, v in estado_provincias.items() if v >= 50],
        "provincias_en_progreso": {k: v for k, v in estado_provincias.items() if 0 < v < 50},
        "detalle_por_provincia": estado_provincias,
        "progreso_porcentaje": round(total_enviados / 2893 * 100, 2)
    }

    with open(ESTADO_CAMPANA, 'w', encoding='utf-8') as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)

    return estado

def main():
    print("="*70)
    print("ACTUALIZANDO ESTADO COMPLETO DE LA CAMPAÑA")
    print("="*70)

    # Obtener estado desde IMAP
    estado_provincias, total_enviados = obtener_estado_desde_imap()

    print(f"\nOK Estado obtenido: {total_enviados} emails en {len(estado_provincias)} provincias")

    # Actualizar estado_campana.json
    actualizar_estado_json(estado_provincias, total_enviados)
    print(f"OK Actualizado: {ESTADO_CAMPANA}")

    # Generar PROGRESO.md
    contenido_md = generar_progreso_md(estado_provincias, total_enviados)
    progreso_path = os.path.join(BASE_DIR, 'PROGRESO.md')
    with open(progreso_path, 'w', encoding='utf-8') as f:
        f.write(contenido_md)
    print(f"OK Generado: PROGRESO.md")

    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    print(f"Total emails enviados: {total_enviados}")
    print(f"Provincias con envíos: {len(estado_provincias)}")
    print(f"Progreso: {(total_enviados / 2893 * 100):.1f}%")
    print("="*70)

    return True

if __name__ == "__main__":
    main()
