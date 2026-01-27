# 🚀 Aytohacks - Sistema de Email Marketing para Ayuntamientos

Sistema automatizado de envío masivo de emails a ayuntamientos de España con verificación previa, detección de rebotes y sincronización automática con GitHub.

---

## 📊 PROGRESO ACTUAL

**Última actualización:** Ver [PROGRESO.md](PROGRESO.md) para detalles completos

```
Total emails enviados: 577 / ~2,893
Progreso: 19.9% de España

Provincias completadas: 4
- Toledo: 236 emails ✅
- Cuenca: 141 emails ✅
- Ciudad Real: 96 emails ✅
- Almería: 70 emails ✅

Provincias en progreso: 1
- Cádiz: 34 emails 🔄
```

📈 **[Ver progreso detallado →](PROGRESO.md)**

---

## ✨ Características

### 🔍 Verificación Inteligente
- **Verificación DNS** - Comprueba registros MX del dominio
- **Verificación SMTP** - Valida buzón antes de enviar
- **Lista negra** - 23 dominios problemáticos bloqueados automáticamente
- **Prevención de duplicados** - Sistema de lock y estado persistente

### 📧 Envío Automatizado
- **Personalización** - Cada email personalizado con nombre del municipio
- **PDF adjunto** - Catálogo de productos incluido automáticamente
- **Velocidad controlada** - 3 minutos entre envíos
- **Horarios inteligentes** - Restricción 9:00-14:30 para provincias del centro

### 🔄 Detección de Rebotes
- **Automática cada 10 envíos** - Revisa bandeja INBOX
- **Detección mailer-daemon** - Identifica rebotes automáticamente
- **Actualización Excel** - Marca rebotados con motivo
- **Carpeta especial** - Mueve rebotes a carpeta dedicada

### 📂 Organización IMAP
- **Carpetas por provincia** - INBOX.Sent.[Provincia] para cada una
- **52 provincias** - Todas las carpetas creadas automáticamente
- **Sincronización** - Sistema de verificación y sync con Excel

### 🔧 Git Automático
- **Cada 10 envíos** - Commit + push automático a GitHub
- **Estado completo** - Actualiza PROGRESO.md, estado_campana.json, Excel
- **Historial completo** - Backup continuo de todos los cambios
- **Visible desde cualquier lugar** - Clone y ve el progreso inmediatamente

---

## 🚀 Instalación Rápida

### 1. Clonar repositorio
```bash
git clone https://github.com/Dafftron/aytohacks.git
cd aytohacks
```

### 2. Instalar dependencias
```bash
python -m pip install pandas requests beautifulsoup4 dnspython openpyxl
```

### 3. Verificar instalación
```bash
python test_sistema_completo.py
```

Debe mostrar: **7/7 tests aprobados**

---

## 📖 Uso

### Ver estado actual
```bash
# Ver progreso desde IMAP (estado real)
python contar_enviados_real.py

# Actualizar archivos de estado
python actualizar_estado_completo.py

# Ver recomendación según horario
python gestor_envios.py
```

### Enviar emails (RECOMENDADO)
```bash
# Con verificación completa (DNS + SMTP + lista negra)
python enviar_verificado_v2.py [Provincia] [Cantidad]

# Ejemplos:
python enviar_verificado_v2.py Cadiz 15      # Terminar Cádiz
python enviar_verificado_v2.py Barcelona 50  # 50 municipios Barcelona
python enviar_verificado_v2.py Valencia 100  # 100 municipios Valencia
```

### Enviar con horario (9:00-14:30)
```bash
# Solo para provincias del CENTRO
python enviar_con_horario.py Guadalajara 30
python enviar_con_horario.py Segovia 30
```

---

## 🎯 Qué hace el sistema automáticamente

### Cada envío:
1. Verifica email (DNS + SMTP + lista negra)
2. Envía con PDF adjunto personalizado
3. Guarda en carpeta IMAP de la provincia
4. Marca como enviado en Excel
5. Registra en log detallado

### Cada 10 envíos:
1. **Revisa bandeja de rebotes** (INBOX)
2. **Detecta mailer-daemon** automáticamente
3. **Marca rebotados** en Excel con motivo
4. **Actualiza estado completo** desde IMAP
5. **Genera PROGRESO.md** actualizado
6. **Actualiza estado_campana.json**
7. **Git commit** con contador
8. **Git push** a GitHub

**Resultado:** GitHub siempre tiene el estado actualizado visible

---

## 📊 Estructura del Proyecto

```
aytohacks/
├── PROGRESO.md                      ← Estado visible en GitHub
├── estado_campana.json              ← Estado en JSON
├── config.py                        ← Configuración centralizada
│
├── enviar_verificado_v2.py         ← Sistema principal (RECOMENDADO)
├── enviar_con_horario.py           ← Con restricción 9:00-14:30
├── gestor_envios.py                ← Recomendaciones inteligentes
│
├── actualizar_estado_completo.py   ← Actualiza estado desde IMAP
├── contar_enviados_real.py         ← Verifica estado real
├── revisar_rebotes.py              ← Revisa rebotes manualmente
│
├── datos/                          ← Archivos Excel
├── logs/                           ← Logs de ejecución
├── provincias/                     ← 36 archivos Excel por provincia
└── Equipamiento Astroturismo 2026.pdf
```

---

## 🎮 Scripts Disponibles

### Principales
- `enviar_verificado_v2.py` - **Sistema principal con verificación completa**
- `enviar_con_horario.py` - Envío con horario 9:00-14:30
- `gestor_envios.py` - Gestión inteligente de campaña

### Utilidades
- `contar_enviados_real.py` - Cuenta emails reales en IMAP
- `actualizar_estado_completo.py` - Actualiza estado completo
- `listar_todas_carpetas.py` - Lista carpetas IMAP
- `test_sistema_completo.py` - Verifica instalación

### Scraping
- `completar_todos.py` - Scrapea datos de ayuntamientos
- `scrapear_espana_completa.py` - Scrapea toda España

---

## ⚙️ Configuración

### Archivo config.py
```python
# Servidor email
SMTP_SERVER = 'mail.fundacionastrohita.org'
EMAIL_USER = 'david@tecnohita.com'

# Parámetros de envío
TIEMPO_ENTRE_ENVIOS = 180  # 3 minutos

# Lista negra (23 dominios)
DOMINIOS_BLACKLIST = [
    'terra.es', 'gva.es', 'telefonica.net', ...
]
```

Todas las rutas son **relativas** - el sistema funciona desde cualquier ubicación.

---

## 📋 Provincias Disponibles

**52 provincias** con carpetas IMAP creadas:

<details>
<summary>Ver lista completa</summary>

- Albacete, Alicante, Almería, Asturias, Ávila, A Coruña
- Badajoz, Barcelona, Burgos
- Cáceres, Cádiz, Cantabria, Castellón, Córdoba, Cuenca, Ciudad Real
- Girona, Granada, Guadalajara
- Huelva, Huesca
- Jaén
- León, Lleida, Lugo
- Madrid, Málaga, Murcia
- Navarra
- Ourense
- Palencia, Pontevedra
- La Rioja
- Salamanca, Segovia, Sevilla, Soria
- Tarragona, Teruel, Toledo
- Valencia, Valladolid, Vizcaya
- Zamora, Zaragoza
- Álava, Guipúzcoa
- Baleares, Las Palmas, Santa Cruz Tenerife
- Ceuta, Melilla

</details>

---

## 🐛 Solución de Problemas

### "No se encuentra el Excel"
```bash
# El sistema usa los Excel de provincias/
ls provincias/*.xlsx
```

### "Error de conexión SMTP/IMAP"
```bash
# Verifica credenciales en config.py
# Comprueba firewall/antivirus
python test_sistema_completo.py
```

### "Estado desactualizado"
```bash
# Actualiza manualmente
python actualizar_estado_completo.py

# Luego commit
git add PROGRESO.md estado_campana.json
git commit -m "Actualizar estado"
git push
```

### "Git no configurado"
```bash
git config user.email "tu@email.com"
git config user.name "Tu Nombre"
```

---

## 📚 Documentación Completa

- **[PROGRESO.md](PROGRESO.md)** - Progreso actual de la campaña
- **[GUIA_SISTEMA_COMPLETO.md](GUIA_SISTEMA_COMPLETO.md)** - Guía técnica detallada
- **[ESTADO_REAL_CAMPANA.md](ESTADO_REAL_CAMPANA.md)** - Estado verificado desde IMAP
- **[INSTRUCCIONES.md](INSTRUCCIONES.md)** - Manual de usuario

---

## 🔐 Seguridad

- Verificación previa de todos los emails
- Lista negra actualizada con dominios problemáticos
- Sistema de lock para evitar ejecuciones múltiples
- Logs completos de todas las operaciones
- Backup automático en Git cada 10 envíos

---

## 📞 Soporte

**Empresa:** TecnoHita Instrumentación
**Email:** david@tecnohita.com
**Tel:** 611 44 33 63
**Web:** https://tecnohita.com/

---

## 📄 Licencia

Uso interno de TecnoHita Instrumentación.

---

## 🎯 Próximos Pasos

1. **Ver progreso:** `python contar_enviados_real.py`
2. **Continuar campaña:** `python enviar_verificado_v2.py [Provincia] 50`
3. **Ver recomendación:** `python gestor_envios.py`

---

**Sistema operativo al 100%** ✅
**Última actualización:** 27 de enero de 2026
**Versión:** 2.0
