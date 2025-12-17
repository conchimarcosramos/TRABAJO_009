# IMPLEMENTAR UN FLUJO DE DATOS EXTREMO A EXTREMO: CARGAR CSV A SQLITE, 
# CONSULTAR Y ANALIZAR DATOS CON SQL Y PANDAS. GENERAR INFORME.

import sqlite3
import pandas as pd
import time #import time para medir tiempos de ejecución    
# Crear una conexión a la base de datos SQLite alumnos_cursos.db

from io import StringIO

# creamos datos de ejemplo en formato CSV
# StringIO permite simular un archivo en memoria
datos_csv= StringIO("""vendedor,fecha,importe,zona
Juan,2024-01-15,1500,Norte
María,2024-01-16,2000,Sur
Juan,2024-01-17,1800,Norte
Pedro,,950.25,Este
,2024-01-19,3200.00,Sur
María,2024-01-20,2150.00,Sur
""")

# cargar y limpiar datos con pandas
# read_csv puede leer desde un archivo 
# o desde un objeto similar a un archivo como StringIO
df_ventas = pd.read_csv(datos_csv) 
print("Datos originales:")
print(df_ventas)
print(f"\nValores faltantes por columna:\n{df_ventas.isnull().sum()}\n")

#Eliminar filas con valores faltantes
#dropna elimina las filas que contienen valores NaN en cualquier columna
df_ventas= df_ventas.dropna()
print("Datos después de eliminar filas con valores faltantes:")
print(df_ventas) 

#Convertimos fechas a tipo datetime
#datetime convierte cadenas de texto a objetos datetime
df_ventas['fecha'] = pd.to_datetime(df_ventas['fecha'])   

#Convertimo importe a tipo float
df_ventas['importe'] = pd.to_numeric(df_ventas['importe'], errors='coerce').astype(float)    
#errors='coerce' convierte valores no convertibles a NaN
#astype(float) convierte la columna a tipo float

print("\nTipos de datos después de la conversión:")
print(df_ventas.dtypes)



