#leer sqlite y pasar a pandas
#Consultar una base de datos SQLite y cargar los resultados en un Dataframe de pandas usando pd.read_sql_query().
import pandas as pd
import sqlite3

#Conectar a la base de datos SQLite
conexion = sqlite3.connect('alumnos.db') 

# Crear la consulta SQL
# select : traer las columnas especificadas
# WHERE: notas > 8.0
# ORDER BY nota DESC: ordenar por la columna Edad de forma DESCENDENTE

#""" indica que es un string multilínea
consulta ="""
SELECT Nombre, Edad, Curso, Nota
FROM alumnos
WHERE Nota > 8.0
ORDER BY Nota DESC
"""
 
# Ejecutar la consulta y cargar los resultados en un DataFrame de pandas
# pd.read_sql_query(): Cuando quieres analizar datos con pandas
# combina la consulta SQL con pandas para obtener un DataFrame directamente
df_filtrado = pd.read_sql_query(consulta, conexion)
print("=== Alumnos con nota superior a 8 ordenados por nota descendente ===")
print(df_filtrado)  

# Calculamos la nota media de los alumnos en el DataFrame filtrado
nota_media = df_filtrado['Nota'].mean()
# recordamos que mean() calcula el promedio de una serie numérica en pandas
print(f"\nNota media de los alumnos con nota superior a 8: {nota_media:.2f}")

# Información adiciónal, como el número de alumnos que cumplen la condición
print(f"Total de alumnos con nota superior a 8: {len(df_filtrado)}")

# Cerrar la conexión a la base de datos
conexion.close()
print("Conexión cerrada.")  

