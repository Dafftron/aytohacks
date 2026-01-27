import pandas as pd
import os
from config import DATOS_DIR, EXCEL_TOLEDO_FUSIONADO

# Leer ambos archivos (ajusta estas rutas según donde estén tus archivos fuente)
df_completo = pd.read_excel(os.path.join(DATOS_DIR, 'Direcciones_Toledo_completo.xlsx'))
df_comparativa = pd.read_excel(os.path.join(DATOS_DIR, 'comparativa_emails_toledo.xlsx'))

print(f"Archivo completo: {len(df_completo)} filas")
print(f"Archivo comparativa: {len(df_comparativa)} filas")

# Normalizar nombres de municipios para el merge (quitar espacios y mayúsculas)
df_completo['Municipio_norm'] = df_completo['NOMBRE'].str.strip().str.upper()
df_comparativa['Municipio_norm'] = df_comparativa['Municipio'].str.strip().str.upper()

# Filtrar solo Toledo en el archivo completo
df_toledo = df_completo[df_completo['PROV_nombre'].str.contains('Toledo', case=False, na=False)].copy()
print(f"Ayuntamientos de Toledo en archivo completo: {len(df_toledo)}")

# Hacer merge de los datos de comparativa con toledo
df_fusionado = df_toledo.merge(
    df_comparativa[['Municipio_norm', 'Email_Excel_Original', 'Email_Diputacion', 'Web_Diputacion']],
    on='Municipio_norm',
    how='left',
    suffixes=('', '_comp')
)

# Actualizar las columnas con los datos de comparativa (si existen)
df_fusionado['Email_Original'] = df_fusionado['Email_Excel_Original'].fillna(df_fusionado['Email_Original'])
df_fusionado['Email_Diputacion'] = df_fusionado['Email_Diputacion_comp'].fillna(df_fusionado['Email_Diputacion'])
df_fusionado['Web_Diputacion'] = df_fusionado['Web_Diputacion_comp'].fillna(df_fusionado['Web_Diputacion'])

# Limpiar columnas temporales
df_fusionado = df_fusionado.drop(columns=['Municipio_norm', 'Email_Excel_Original', 'Email_Diputacion_comp', 'Web_Diputacion_comp'])

# Agregar columna de origen para saber qué correos son oficiales vs buscados
df_fusionado['Origen_Email_1'] = 'Oficial'
df_fusionado['Origen_Email_2'] = ''
df_fusionado['Origen_Email_3'] = ''

# Guardar el archivo fusionado
df_fusionado.to_excel(EXCEL_TOLEDO_FUSIONADO, index=False)
output_path = EXCEL_TOLEDO_FUSIONADO

print(f"\nArchivo fusionado guardado en: {output_path}")
print(f"Total de filas: {len(df_fusionado)}")
print(f"\nColumnas finales: {df_fusionado.columns.tolist()}")
print(f"\nPrimeras 3 filas:")
print(df_fusionado.head(3).to_string())
