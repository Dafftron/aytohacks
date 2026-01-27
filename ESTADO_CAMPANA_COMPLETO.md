# ESTADO COMPLETO DE LA CAMPAÑA AYTOHACKS

**Fecha:** 27 de enero de 2026
**Última actualización estado:** 20 de enero de 2026 09:20

---

## 📊 RESUMEN EJECUTIVO

### Progreso Global
- **Total municipios:** 2,893
- **Total enviados:** 70 (2.4%)
- **Pendientes:** 2,823 (97.6%)

### Estado por Categoría
- **Completadas:** 0 provincias
- **En progreso:** 2 provincias (Almería, Cádiz)
- **Pendientes:** 34 provincias

---

## ✅ PROVINCIAS EN PROGRESO

### Almería - 🟢 CASI COMPLETA
- Total: 70 municipios
- Enviados: **69/70 (98.6%)**
- Pendiente: 1 municipio
- Tipo: Periferia (sin restricción horaria)

### Cádiz - 🟡 EMPEZADA
- Total: 45 municipios
- Enviados: **1/45 (2.2%)**
- Pendientes: 44 municipios
- Tipo: Periferia (sin restricción horaria)

---

## 🎯 PROVINCIAS CLAVE PENDIENTES

### CENTRO (Con restricción horaria 9:00-14:30)

| Provincia | Municipios | Con Email | Pendientes |
|-----------|------------|-----------|------------|
| **Toledo** | 204 | 161 | 204 |
| Cuenca | 89 | 62 | 89 |
| Guadalajara | 91 | 62 | 91 |
| Ávila | 78 | 69 | 78 |
| Salamanca | 89 | 62 | 89 |
| Segovia | 77 | 77 | 77 |
| Valladolid | 77 | 77 | 77 |
| Zamora | 85 | 85 | 85 |

**Total Centro:** 790 municipios pendientes

### PERIFERIA (Sin restricción horaria)

| Provincia | Municipios | Con Email | Pendientes |
|-----------|------------|-----------|------------|
| Barcelona | 83 | 82 | 83 |
| Valencia | 88 | 88 | 88 |
| Zaragoza | 87 | 85 | 87 |
| Sevilla | 69 | 69 | 69 |
| Málaga | 71 | 71 | 71 |
| Granada | 78 | 77 | 78 |
| Alicante | 72 | 72 | 72 |
| Córdoba | 64 | 64 | 64 |
| **Y 20 más...** | - | - | - |

**Total Periferia:** 2,033 municipios pendientes

---

## 🚀 FUNCIONALIDADES IMPLEMENTADAS

### ✅ Sistema de Verificación
- [x] Verificación DNS (registros MX)
- [x] Verificación SMTP (validación de buzón)
- [x] Lista negra de 23 dominios problemáticos
- [x] Resultados: OK, BLACKLIST, SIN_MX, NO_EXISTE, etc.

### ✅ Sistema de Envío
- [x] Envío automatizado con PDF adjunto
- [x] Personalización por municipio
- [x] Espera 3 minutos entre envíos
- [x] Guarda en carpetas IMAP por provincia
- [x] Marca enviado en Excel automáticamente

### ✅ Sistema de Rebotes
- [x] Cada 10 envíos revisa bandeja INBOX
- [x] Detecta mailer-daemon automáticamente
- [x] Extrae email rebotado del cuerpo
- [x] Marca en Excel: "Rebotado"
- [x] Mueve rebotes a carpeta especial

### ✅ Sistema Git
- [x] Cada 10 envíos: commit automático
- [x] Push a GitHub automático
- [x] Historial completo de cambios
- [x] Backup continuo del Excel

### ✅ Organización IMAP
- [x] Carpetas por provincia: INBOX.Sent.[Provincia]
- [x] Creación automática de carpetas
- [x] Sincronización con Excel
- [x] Auditoría completa de enviados

---

## 🎮 SCRIPTS DISPONIBLES

### Script Principal (RECOMENDADO)
```bash
# Enviar con verificación completa
python enviar_verificado_v2.py [Provincia] [Cantidad]

Ejemplos:
python enviar_verificado_v2.py Almeria 1      # Terminar Almería
python enviar_verificado_v2.py Cadiz 44       # Terminar Cádiz
python enviar_verificado_v2.py Barcelona 50   # Empezar Barcelona
python enviar_verificado_v2.py Valencia 100   # 100 municipios Valencia
```

### Gestión de Campaña
```bash
# Ver estado actualizado
python gestor_envios.py

# Ver recomendación según horario
python gestor_envios.py
```

### Con Restricción Horaria (9:00-14:30)
```bash
# Solo para provincias del CENTRO
python enviar_con_horario.py Toledo 20
python enviar_con_horario.py Cuenca 30
```

### Verificación y Sincronización
```bash
# Sincronizar carpeta IMAP con Excel
python verificar_carpeta_enviados.py
```

---

## 📂 CARPETAS IMAP CREADAS AUTOMÁTICAMENTE

El sistema crea carpetas dinámicamente según la provincia:

```
INBOX.Sent.Almeria        ← 69 emails
INBOX.Sent.Cadiz          ← 1 email
INBOX.Sent.Barcelona      ← Se creará al enviar
INBOX.Sent.Valencia       ← Se creará al enviar
INBOX.Sent.Madrid         ← Se creará al enviar
...
```

**No necesitas hacer nada**, el sistema lo hace automáticamente.

---

## 🎯 PLAN RECOMENDADO DE ENVÍO

### Fase 1: TERMINAR LO EMPEZADO (Hoy)
```bash
# 1. Terminar Almería (1 municipio)
python enviar_verificado_v2.py Almeria 1

# 2. Terminar Cádiz (44 municipios)
python enviar_verificado_v2.py Cadiz 44
```
**Resultado:** 2 provincias completas

### Fase 2: PROVINCIAS GRANDES (Esta semana)
```bash
# Periferia (sin restricción horaria)
python enviar_verificado_v2.py Barcelona 50
python enviar_verificado_v2.py Valencia 50
python enviar_verificado_v2.py Sevilla 50
python enviar_verificado_v2.py Málaga 50
```
**Resultado:** +200 municipios enviados

### Fase 3: CENTRO EN HORARIO LABORAL (9:00-14:30)
```bash
# Horario laboral únicamente
python enviar_con_horario.py Toledo 50
python enviar_con_horario.py Cuenca 30
python enviar_con_horario.py Guadalajara 30
```

### Fase 4: COMPLETAR RESTO (Próximas semanas)
- Usar `gestor_envios.py` para recomendaciones
- Alternar periferia (todo el día) y centro (9:00-14:30)

---

## 📋 ARCHIVOS DE DATOS

### Archivos Excel por Provincia (36 archivos)
```
provincias/Albacete.xlsx
provincias/Alicante.xlsx
provincias/Almeria.xlsx
...
provincias/Zaragoza.xlsx
```

### Estado de Campaña
```
estado_campana.json        ← Estado de todas las provincias
```

### Logs
```
logs/envios_log.txt        ← Log general
logs/envios_log_Almeria.txt
logs/envios_log_Cadiz.txt
...
```

---

## ⚙️ CONFIGURACIÓN ACTUAL

### Servidor Email
- **Servidor:** mail.fundacionastrohita.org
- **Cuenta:** david@tecnohita.com
- **SMTP:** Puerto 465 (SSL)
- **IMAP:** Puerto 993 (SSL)

### Parámetros de Envío
- **Tiempo entre envíos:** 3 minutos (180 segundos)
- **Horario centro:** 9:00-14:30
- **Horario periferia:** Todo el día
- **Verificación:** DNS + SMTP + Lista negra

### Lista Negra (23 dominios)
terra.es, gva.es, telefonica.net, teleline.es, diputoledo.es,
diba.es, dip-palencia.es, dipucuenca.es, y 15 más...

---

## 🔄 PROCESO AUTOMÁTICO CADA 10 ENVÍOS

1. ✅ **Revisar rebotes** en INBOX
2. ✅ **Marcar rebotados** en Excel
3. ✅ **Mover rebotes** a carpeta especial
4. ✅ **Git commit** con contador
5. ✅ **Git push** a GitHub
6. ✅ **Log completo** de operación

---

## 📊 ESTADÍSTICAS ESTIMADAS

### A ritmo actual (3 min/municipio):
- **50 municipios** = 2.5 horas
- **100 municipios** = 5 horas
- **200 municipios** = 10 horas

### Para completar toda España:
- **2,823 municipios pendientes** × 3 min = 141 horas
- **Días laborables (5h/día):** ~28 días
- **Días completos (8h/día):** ~18 días

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

### 1. Terminar provincias en progreso
```bash
python enviar_verificado_v2.py Almeria 1
python enviar_verificado_v2.py Cadiz 44
```

### 2. Actualizar estado
```bash
python gestor_envios.py
```

### 3. Continuar con provincias grandes
```bash
# Si es 9:00-14:30
python enviar_con_horario.py Toledo 50

# Si es fuera de horario
python enviar_verificado_v2.py Barcelona 50
```

### 4. Revisar logs en tiempo real
```bash
tail -f logs/envios_log.txt
```

---

## 📞 SOPORTE

**Empresa:** TecnoHita Instrumentación
**Email:** david@tecnohita.com
**Tel:** 611 44 33 63
**Web:** https://tecnohita.com/

**GitHub:** https://github.com/Dafftron/aytohacks

---

## ✅ SISTEMA COMPLETAMENTE OPERATIVO

- ✅ Python 3.12.1 instalado
- ✅ Todas las dependencias instaladas
- ✅ 36 provincias con datos
- ✅ Sistema de verificación activo
- ✅ Git configurado y conectado
- ✅ SMTP/IMAP accesibles
- ✅ Tests 7/7 aprobados

**El sistema está listo para enviar a cualquier provincia.**

---

**Última actualización:** 27 de enero de 2026
