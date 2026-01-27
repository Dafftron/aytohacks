# Instrucciones de Uso - Aytohacks

## Estado de la Instalación

✅ **Python 3.12.1** - Instalado
✅ **Dependencias** - Instaladas
- pandas 3.0.0
- requests 2.32.5
- beautifulsoup4 4.14.3
- dnspython 2.8.0
- openpyxl 3.1.5

## Estructura del Proyecto

```
aytohacks/
├── config.py                    # Configuración centralizada (NUEVO)
├── datos/                       # Archivos Excel de trabajo
├── logs/                        # Logs de ejecución
├── resultados/                  # Resultados procesados
├── provincias/                  # Archivos Excel por provincia (36 archivos)
├── Equipamiento Astroturismo 2026.pdf
└── scripts principales...
```

## Configuración Inicial

### 1. Archivos Necesarios (Opcional)

Si tienes archivos Excel previos, colócalos en la carpeta `datos/`:
- `Direcciones_Toledo_completo.xlsx`
- `comparativa_emails_toledo.xlsx`

### 2. Verificar PDF

El PDF está en: `C:\Users\david\aytohacks\Equipamiento Astroturismo 2026.pdf`

### 3. Instalar Thunderbird (Para envío de correos)

Descarga desde: https://www.thunderbird.net/
Configura la cuenta: david@tecnohita.com

## Scripts Principales (ACTUALIZADOS)

### 1. Buscar información de ayuntamientos

```bash
cd aytohacks
python completar_todos.py
```

**Qué hace:**
- Scrapea información de 204 ayuntamientos de Toledo
- Extrae emails, webs y teléfonos
- Guarda progreso cada 20 ayuntamientos
- Genera: `datos/Toledo_Completo_Final.xlsx`

### 2. Fusionar datos de múltiples fuentes

```bash
python fusionar_excels.py
```

**Qué hace:**
- Combina diferentes fuentes de datos
- Genera: `datos/Toledo_Fusionado.xlsx`

### 3. Enviar correos automatizados

```bash
python enviar_correos_thunderbird.py
```

**Qué hace:**
- Lee `datos/Toledo_Completo_Final.xlsx`
- Abre Thunderbird con emails pre-rellenados
- Espera confirmación manual para cada envío
- Guarda log en: `logs/envios_log.txt`

## Scripts Adicionales

### Por provincias

```bash
python scrapear_espana_completa.py    # Scrapea toda España
python enviar_provincia.py             # Envía a una provincia específica
python fusionar_todas_provincias.py   # Fusiona todas las provincias
```

### Utilidades

```bash
python buscar_primeros_20.py          # Prueba con 20 ayuntamientos
python prueba_envio.py                # Prueba de envío de correo
python reorganizar_excel.py           # Reorganiza columnas Excel
```

## Personalización

### Modificar el email

Edita el archivo [enviar_correos_thunderbird.py](enviar_correos_thunderbird.py#L24-L57):

```python
def crear_cuerpo_email(nombre_ayuntamiento):
    cuerpo = f"""Tu mensaje personalizado aquí..."""
    return cuerpo
```

### Cambiar tiempo entre envíos

Edita [config.py](config.py#L25):

```python
TIEMPO_ENTRE_ENVIOS = 300  # segundos (5 minutos)
```

### Modificar asunto del correo

Edita [config.py](config.py#L27):

```python
ASUNTO = 'Tu asunto aquí'
```

## Flujo de Trabajo Típico

### Para Toledo:

1. **Fusionar datos** (si tienes archivos previos):
   ```bash
   python fusionar_excels.py
   ```

2. **Completar información**:
   ```bash
   python completar_todos.py
   ```
   Esto puede tomar ~10-15 minutos para 204 ayuntamientos

3. **Enviar correos**:
   ```bash
   python enviar_correos_thunderbird.py
   ```
   Revisa y envía cada correo manualmente en Thunderbird

### Para otras provincias:

Los archivos están en `provincias/`:
```
A_Coruna.xlsx, Albacete.xlsx, Alicante.xlsx, ...
```

Puedes usar scripts como `enviar_provincia.py` modificando la variable PROVINCIA.

## Notas Importantes

- **Scraping**: Espera 2 segundos entre peticiones para no saturar el servidor
- **Envíos**: Espera 5 minutos entre ayuntamientos por defecto
- **Logs**: Todos los envíos se registran en `logs/envios_log.txt`
- **Progreso**: Se guarda automáticamente cada 20 ayuntamientos
- **Thunderbird**: Los emails se abren pero debes enviarlos manualmente

## Solución de Problemas

### "No se encuentra el archivo Excel"
- Verifica que el archivo existe en la carpeta `datos/`
- O ejecuta primero `fusionar_excels.py`

### "No se encuentra el PDF"
- El PDF debe estar en la raíz: `Equipamiento Astroturismo 2026.pdf`
- Ya está incluido en el proyecto

### "Thunderbird no se abre"
- Instala Thunderbird desde thunderbird.net
- Configura tu cuenta de correo primero

## Contacto

**TecnoHita Instrumentación**
- Email: david@tecnohita.com
- Tel: 611 44 33 63
- Web: https://tecnohita.com/
