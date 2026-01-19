# Aytohacks - Sistema de Email Marketing para Ayuntamientos

Sistema automatizado para buscar información de contacto de ayuntamientos y enviar correos personalizados.

## Características

- Búsqueda automática de emails y webs de ayuntamientos desde todoslosayuntamientos.es
- Fusión de múltiples fuentes de datos
- Sistema de envío de correos personalizado vía Thunderbird
- Control de velocidad de envío (5 minutos entre envíos)
- Logs y seguimiento de envíos
- Recuperación de progreso

## Archivos

### Scripts principales
- `fusionar_excels.py` - Fusiona datos de diferentes fuentes Excel
- `completar_todos.py` - Busca información de contacto de todos los ayuntamientos
- `buscar_primeros_20.py` - Script de prueba para los primeros 20 ayuntamientos
- `enviar_correos_thunderbird.py` - Sistema de envío automático de correos
- `prueba_envio.py` - Prueba de envío a correos específicos

### Scripts auxiliares
- `completar_ayuntamientos.py` - Versión antigua del buscador
- `completar_ayuntamientos_v2.py` - Versión con verificación manual

## Uso

### 1. Buscar información de ayuntamientos
```bash
python completar_todos.py
```

### 2. Enviar correos
```bash
python enviar_correos_thunderbird.py
```

## Configuración

Edita las rutas en los scripts según tu configuración:
- `EXCEL_FILE` - Ruta al archivo Excel con los datos
- `PDF_ADJUNTO` - Ruta al PDF a adjuntar
- `TIEMPO_ENTRE_ENVIOS` - Tiempo en segundos entre envíos (default: 300)

## Resultados

- 204 ayuntamientos de Toledo procesados
- 99% de tasa de éxito en búsqueda de información
- Todos los ayuntamientos tienen al menos 1 email

## Autor

Proyecto desarrollado para TecnoHita Instrumentación
