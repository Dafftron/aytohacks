# GUIA COMPLETA DEL SISTEMA AYTOHACKS

## ESTADO ACTUAL

Todo el sistema está **CONFIGURADO Y LISTO** para usar desde:
```
C:\Users\david\aytohacks
```

## ARQUITECTURA DEL SISTEMA

### 1. CONFIGURACIÓN CENTRALIZADA (config.py)

Todas las rutas y configuraciones están en un solo archivo:
- Rutas de archivos (Excel, PDF, logs)
- Configuración SMTP/IMAP
- Lista negra de dominios
- Credenciales de email

**NO necesitas editar rutas hardcodeadas nunca más.**

### 2. SCRIPTS PRINCIPALES ACTUALIZADOS

#### A. SCRAPING (Recopilación de datos)

**completar_todos.py**
- Scrapea info de 204 ayuntamientos de Toledo
- Extrae: emails, webs, teléfonos
- Guarda: `datos/Toledo_Completo_Final.xlsx`
```bash
python completar_todos.py
```

**scrapear_espana_completa.py**
- Scrapea toda España por provincias
- Guarda en: `provincias/[Provincia].xlsx`
```bash
python scrapear_espana_completa.py
```

#### B. ENVÍO CON VERIFICACIÓN (RECOMENDADO)

**enviar_verificado_v2.py** ⭐ PRINCIPAL
- Verifica emails ANTES de enviar (DNS + SMTP)
- Usa lista negra de dominios problemáticos
- Cada 10 envíos:
  - Revisa bandeja de rebotes
  - Marca rebotados en Excel
  - Hace commit + push a Git
- Guarda en carpeta IMAP por provincia

**Uso:**
```bash
# Enviar a Toledo (20 municipios)
python enviar_verificado_v2.py Toledo 20

# Enviar solo emails scrapeados
python enviar_verificado_v2.py Toledo 50 --solo-scrapeados

# Enviar todos los pendientes
python enviar_verificado_v2.py Toledo
```

**Qué hace:**
1. Verifica que el email existe (DNS + SMTP)
2. Revisa lista negra de dominios
3. Envía email con PDF adjunto
4. Guarda en `INBOX.Sent.Toledo`
5. Marca como enviado en Excel
6. Cada 10: revisa rebotes + git commit/push
7. Espera 3 minutos entre envíos

#### C. ENVÍO CON HORARIO

**enviar_con_horario.py**
- Solo envía 9:00-14:30 (horario laboral)
- Espera automáticamente fuera de horario
- Guarda en carpeta IMAP por provincia

```bash
python enviar_con_horario.py Toledo 20
```

#### D. GESTIÓN DE CAMPAÑA

**gestor_envios.py**
- Actualiza estado de todas las provincias
- Recomienda qué provincia enviar según horario
- Lee `estado_campana.json`

```bash
# Ver estado y recomendación
python gestor_envios.py

# Solo actualizar estado
python gestor_envios.py actualizar
```

**Lógica:**
- 9:00-14:30: Envía a provincias del CENTRO
- Resto del día: Envía a provincias de PERIFERIA

#### E. VERIFICACIÓN DE ENVIADOS

**verificar_carpeta_enviados.py**
- Lee carpeta IMAP `INBOX.Sent.Toledo`
- Sincroniza con Excel
- Marca como enviados los que faltan

```bash
python verificar_carpeta_enviados.py
```

### 3. SISTEMA DE VERIFICACIÓN DE EMAILS

**Niveles de verificación:**

1. **Lista Negra** - 23 dominios problemáticos con historial de rebotes
   - `terra.es` (136 rebotes)
   - `gva.es` (104 rebotes)
   - `telefonica.net`, `teleline.es` (obsoletos)
   - Y más...

2. **Verificación DNS** - Comprueba registros MX del dominio

3. **Verificación SMTP** - Conecta al servidor y valida el buzón

**Resultados posibles:**
- `OK` - Email válido
- `BLACKLIST_[dominio]` - En lista negra
- `SIN_MX` - Sin servidor de correo
- `NO_EXISTE` - Buzón no existe (550)
- `TIMEOUT` - Sin respuesta (se asume válido)
- `ERROR` - Error al verificar (se asume válido)

### 4. SISTEMA DE REBOTES

**Funcionamiento automático cada 10 envíos:**

1. Lee bandeja `INBOX` buscando `mailer-daemon`
2. Extrae email rebotado del cuerpo del mensaje
3. Busca ese email en el Excel
4. Marca: `Rebotado = 'REBOTADO: Email no entregado'`
5. Borra marca de enviado
6. Mueve mensaje a carpeta `rebotes`
7. Guarda cambios en Excel

### 5. SISTEMA GIT (COMMIT/PUSH AUTOMÁTICO)

**Cada 10 envíos:**
```bash
git add Espana_Maestro_Completo.xlsx
git commit -m "Actualizacion: 10 emails enviados - 2026-01-27 15:30"
git push
```

Mantiene historial de:
- Cuántos enviados
- Cuándo se enviaron
- Estado del Excel en cada momento

### 6. CARPETAS IMAP POR PROVINCIA

Los correos se guardan organizados:
```
INBOX.Sent.Toledo
INBOX.Sent.Madrid
INBOX.Sent.Barcelona
INBOX.Sent.Valencia
...
```

**Beneficios:**
- Organización por provincia
- Fácil auditoría
- Sincronización con Excel
- Backup de emails enviados

## FLUJO DE TRABAJO RECOMENDADO

### OPCIÓN 1: Campaña completa con verificación

```bash
# 1. Ver estado actual
python gestor_envios.py

# 2. Enviar con verificación (recomendado)
python enviar_verificado_v2.py Toledo 50

# 3. Verificar sincronización
python verificar_carpeta_enviados.py
```

### OPCIÓN 2: Campaña con horario laboral

```bash
# Enviar solo en horario 9:00-14:30
python enviar_con_horario.py Toledo 20
```

### OPCIÓN 3: Campaña a toda España

```bash
# Enviar a todas las provincias según horario
while true; do
  python gestor_envios.py
  # Ver recomendación y ejecutar manualmente
  sleep 3600
done
```

## ARCHIVOS IMPORTANTES

### Excel Maestro
**Ubicación:** `datos/Espana_Maestro_Completo.xlsx`

**Columnas clave:**
- `NOMBRE` - Nombre del municipio
- `PROV_nombre` - Provincia
- `Email_FEMPCLM` - Email de FEMPCLM (prioridad 1)
- `Email_Scrapeado_1` - Email scrapeado (prioridad 2)
- `email` - Email gobierno (prioridad 3)
- `Enviado` - Fecha/hora de envío
- `Rebotado` - Motivo del rebote

### Logs
**Ubicación:** `logs/envios_log.txt` o `logs/envios_log_[Provincia].txt`

**Contiene:**
```
[2026-01-27 15:30:42] ENVIANDO A TOLEDO (con verificacion previa)
[2026-01-27 15:30:43] Municipios en Toledo: 204
[2026-01-27 15:30:43] Pendientes con email: 150
[2026-01-27 15:30:43] [1/150] Ajofrín -> ayto@ajofrin.es
[2026-01-27 15:30:44]   Verificando email...
[2026-01-27 15:30:45]   Email OK (OK)
[2026-01-27 15:30:47]   ENVIADO OK
[2026-01-27 15:30:47]   Esperando 3 minutos...
```

### Estado de Campaña
**Ubicación:** `estado_campana.json`

**Contiene:**
- Provincias completadas
- Provincias en progreso
- Provincias pendientes
- Estadísticas globales

## CONFIGURACIÓN SMTP/IMAP

**Servidor:** mail.fundacionastrohita.org
**Cuenta:** david@tecnohita.com
**SMTP:** Puerto 465 (SSL)
**IMAP:** Puerto 993 (SSL)

Para cambiar credenciales, edita `config.py`

## SOLUCIÓN DE PROBLEMAS

### "No se encuentra el Excel maestro"
```bash
# Crear desde provincias
python fusionar_todas_provincias.py
```

### "No se puede conectar a IMAP"
- Verifica credenciales en `config.py`
- Comprueba firewall/antivirus
- Prueba conexión manual con Thunderbird

### "Git push falla"
```bash
cd C:\Users\david\aytohacks
git remote -v  # Verificar remoto
git pull       # Sincronizar primero
git push       # Reintentar
```

### "Muchos rebotes"
- Revisa `logs/envios_log.txt`
- Actualiza lista negra en `config.py`
- Usa `--solo-scrapeados` para emails más confiables

### "Email duplicado"
- El sistema previene duplicados automáticamente
- Revisa columna `Enviado` en Excel
- Ejecuta `verificar_carpeta_enviados.py`

## MEJORAS FUTURAS POSIBLES

- [ ] Dashboard web con estadísticas
- [ ] Detección automática de nuevos dominios problemáticos
- [ ] Reintento de rebotes temporales
- [ ] Integración con CRM
- [ ] Análisis de tasas de apertura
- [ ] Respuestas automáticas

## CONTACTO Y SOPORTE

**Proyecto:** Aytohacks
**Empresa:** TecnoHita Instrumentación
**Email:** david@tecnohita.com
**Tel:** 611 44 33 63
**Web:** https://tecnohita.com/

---

**Última actualización:** 27 de enero de 2026
**Versión del sistema:** 2.0
**Python requerido:** 3.12+
