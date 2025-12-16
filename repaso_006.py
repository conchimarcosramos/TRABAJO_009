# Comparamos dos enfoques para agrupar y agregar datos sql nativo y pandas
import sqlite3
import pandas as pd
import time

#import time para medir tiempos de ejecución

# Crear una conexión a la base de datos SQLite alumnos_cursos.db
conexion = sqlite3.connect('alumnos_cursos.db')

# ============== OPCION A. GROUP BY y agregaciones en SQL nativo ==============
print("=== OPCION A: GROUP BY y agregaciones en SQL nativo ===")
inicio_a_sql = time.time()

#OPCION SQL NATIVO
consulta_sql = '''
SELECT 
    b.nombre_curso,
    COUNT(a.nombre) AS total_alumnos,
    ROUND(AVG(a.nota), 2) AS nota_media
FROM cursos b
LEFT JOIN alumnos a ON b.id_curso = a.id_curso
GROUP BY b.nombre_curso
ORDER BY nota_media DESC
'''
#OPCION NOMBRANDO TABLAS Y CAMPOS CON FULL NAMES
consulta_sql = '''
SELECT 
    cursos.nombre_curso,
    COUNT(alumnos.nombre) AS total_alumnos,
    ROUND(AVG(alumnos.nota), 2) AS nota_media
FROM cursos
LEFT JOIN alumnos ON cursos.id_curso = alumnos.id_curso
GROUP BY cursos.nombre_curso
ORDER BY nota_media DESC
'''

df_sql = pd.read_sql_query(consulta_sql, conexion)
tiempo_a_sql = time.time() - inicio_a_sql
print("Resultados SQL nativo:")
print(df_sql)
print(f"Tiempo de ejecución SQL nativo: {tiempo_a_sql:.6f} segundos\n")

# ============== OPCION B. GROUP BY y agregaciones en pandas ==============
print("=== OPCION B: GROUP BY y agregaciones en pandas ===")
inicio_b_pandas = time.time()

# OPCION PANDAS
# Cargar datos de las tablas en DataFrames de pandas

# Leer tablas en DataFrames
consulta_completa ="""
SELECT 
    alumnos.nombre,
    cursos.nombre_curso,
    alumnos.nota
FROM alumnos
INNER JOIN cursos ON alumnos.id_curso = cursos.id_curso
"""
# AGRUPAMOS Y AGREGAMOS CON PANDAS
df_datos = pd.read_sql_query(consulta_completa, conexion)

df_pandas = df_datos.groupby('nombre_curso').agg(
    total_alumnos=('nombre', 'count'),
    nota_media=('nota', 'mean')
).reset_index()
df_pandas['nota_media'] = df_pandas['nota_media'].round(2)
df_pandas = df_pandas.sort_values(by='nota_media', ascending=False)

tiempo_b_pandas = time.time() - inicio_b_pandas
print("Resultados con pandas:")
print(df_pandas)
print(f"Tiempo de ejecución con pandas: {tiempo_b_pandas:.6f} segundos\n")

# ============= COMPARACIÓN==============
print("=== COMPARACIÓN ===")
print(f"=Opción A (SQL nativo) fué {tiempo_b_pandas/tiempo_a_sql:.2f}x más rápida que Opción B (pandas)")
print("\nNota: En bases de datos pequeñas, las diferencias de tiempo pueden ser mínimas. En bases de datos grandes, SQL suele ser más eficiente para operaciones de agregación.")
print("En grandes volumentes de datos, es recomendable realizar agregaciones directamente en la base de datos para optimizar el rendimiento.")

conexion.close()