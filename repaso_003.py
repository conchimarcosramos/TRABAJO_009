import pandas as pd
import sqlite3

datos = {
    'Nombre': ["Ana", "Carlos", "Elena", "Diego"],
    'Edad': [22, 25, 19, 23],
    'Curso': ["Python", "Python", "JavaScript", "JavaScript"],
    'Nota': [8.5, 9.0, 7.8, 8.5]
}

# Pasar datos desde pandas a una base de datos SQLite usando to_sql()
df = pd.DataFrame(datos)
# Crear una conexión a la base de datos SQLite (o crearla si no existe)
conexion = sqlite3.connect('alumnos.db')
# Guardar el DataFrame en una tabla llamada 'alumnos'
df.to_sql('alumnos', conexion, if_exists='replace', index=False)
print("Dataframe guardado en la tabla alumnos en alumnos.db.")


# Verificamos que la tabla se ha creado correctamente
consulta = pd.read_sql_query("SELECT * FROM alumnos", conexion)
print(consulta) 
# Cerrar la conexión a la base de datos

cursor=conexion.cursor()
cursor.execute("SELECT * FROM alumnos")
filas = cursor.fetchall()
print("\nContenido de la tabla alumnos:")
for fila in filas:
    print(fila)
  
# pd.read_sql_query(): Cuando quieres analizar datos con pandas 
# (filtrar, agrupar, graficar, etc.)
# cursor.execute(): Cuando quieres ejecutar comandos SQL directamente 
# (crear tablas, insertar datos, etc.) 
  
cursor.execute("PRAGMA table_info(alumnos)")
columnas = cursor.fetchall()
print("\nEstructura de la tabla alumnos:")
for columna in columnas:
    print(columna)
    
        
conexion.close()
print