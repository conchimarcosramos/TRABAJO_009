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

#Guardar datos limpios en SQLite
conn = sqlite3.connect('ventas.db')
#sqlite3.connect crea una conexión a la base de datos SQLite
df_ventas.to_sql('ventas', conn, if_exists='replace', index=False)
print("\nDatos guardados en la base de datos SQLite 'ventas.db' en la tabla 'ventas'.\n")

# Consultar datos con SQL
consulta_zona ="""
SELECT 
    zona, 
    COUNT(*) as num_ventas,
    ROUND (SUM(importe), 2) as ventas_totales,
    ROUND (AVG(importe), 2) as venta_promedio   
FROM ventas
GROUP BY zona
ORDER BY ventas_totales DESC;
"""

df_por_zona = pd.read_sql_query(consulta_zona, conn)
#read_sql_query ejecuta la consulta SQL y devuelve un DataFrame de pandas
print("Resumen de ventas por zona:")
print(df_por_zona)

# Consulta de ventas por vendedor
consulta_vendedor ="""
SELECT 
    vendedor, 
    COUNT(*) as num_ventas,
    ROUND (SUM(importe), 2) as ventas_totales,
    ROUND (AVG(importe), 2) as venta_promedio   
FROM ventas
GROUP BY vendedor
ORDER BY ventas_totales DESC;
"""
df_por_vendedor = pd.read_sql_query(consulta_vendedor, conn)
#read_sql_query ejecuta la consulta SQL y devuelve un DataFrame de pandas
print("\nResumen de ventas por vendedor:")
print(df_por_vendedor)

# Exportar informes a CSV
df_por_zona.to_csv('informe_ventas_por_zona.csv', index=False)
#index=False evita que se exporte la columna de índices
df_por_vendedor.to_csv('informe_ventas_por_vendedor.csv', index=False)
#index=False evita que se exporte la columna de índices
print("\nInformes exportados:")
print("Informe_ventas_por_zona.csv")
print("Informe_ventas_por_vendedor.csv")
# Cerrar la conexión a la base de datos
conn.close()
print("\nConexión a la base de datos cerrada.")
print("\nProceso completado.")
