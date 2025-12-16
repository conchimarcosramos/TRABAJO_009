#JOIN en SQL y análisis de datos con pandas

# Un JOIN en SQL se utiliza para combinar filas de dos o más tablas basándose en una columna relacionada entre ellas.
# Existen varios tipos de JOIN, siendo los más comunes:
# INNER JOIN: Devuelve filas cuando hay una coincidencia en ambas tablas.
# LEFT JOIN (o LEFT OUTER JOIN): Devuelve todas las filas de la tabla izquierda 
# y las filas coincidentes de la tabla derecha. Si no hay coincidencia, 
# los resultados de la tabla derecha serán NULL.
# RIGHT JOIN (o RIGHT OUTER JOIN): Devuelve todas las filas de la tabla derecha 
# y las filas coincidentes de la tabla izquierda. Si no hay coincidencia, 
# los resultados de la tabla izquierda serán NULL.
# FULL JOIN (o FULL OUTER JOIN): Devuelve filas cuando hay una coincidencia en una 
# de las tablas. Si no hay coincidencia, las filas de ambas tablas serán NULL.
# CROSS JOIN: Devuelve el producto cartesiano de ambas tablas, es decir, todas las combinaciones posibles de filas entre las dos tablas.    

# Creamos tablas relacionadas en SQLITE, hacemos un JOIN  y analizamos los resultados con pandas
import sqlite3
import pandas as pd

# Crear una conexión a la base de datos SQLite que ya existe o crear una nueva
conexion1 = sqlite3.connect('alumnos_cursos.db')
cursor1 = conexion1.cursor()

# Crear tabla 'cursos' que estará relacionada con la tabla 'alumnos' a través de 'curso_id'
cursor1.execute('''
CREATE TABLE IF NOT EXISTS cursos (
    id_curso INTEGER PRIMARY KEY,
    nombre_curso TEXT NOT NULL,
    horas INTEGER NOT NULL
)
''')
# Insertar datos en la tabla 'cursos'
cursos_data = [
    (1, 'Python', 40),
    (2, 'JavaScript', 35)
]
cursor1.executemany('INSERT OR IGNORE INTO cursos (id_curso, nombre_curso, horas) VALUES (?, ?, ?)', 
                   cursos_data)    
#cursor.executemany realiza múltiples inserciones en una sola llamada

# Creamos la tabla de alumnos relacionada con cursos, 
# con id_curso como clave foránea
cursor1.execute('''
CREATE TABLE IF NOT EXISTS alumnos (
    id_alumno INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL,
    id_curso INTEGER,
    nota REAL,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
)
''')
# Insertar datos en la tabla 'alumnos' con id_curso relacionado
alumnos_data = [
    (1, 'Ana', 22, 1, 8.5),
    (2, 'Carlos', 25, 1, 9.0),
    (3, 'Elena', 19, 2, 7.8),
    (4, 'Diego', 23, 2, 7.5)
]
cursor1.executemany('INSERT OR IGNORE INTO alumnos (id_alumno, nombre, edad, id_curso, nota) VALUES (?, ?, ?, ?, ?)', alumnos_data)




# Guardar los cambios y cerrar la conexión
print("Base de datos y tablas creadas e insertadas correctamente.")

# Realizar un INNER JOIN entre las tablas 'alumnos' y 'cursos' de la
# base de datos 'alumnos_cursos.db'
consulta_join = '''
SELECT 
    a.nombre, 
    a.edad, 
    b.nombre_curso, 
    a.nota, 
    b.horas
FROM alumnos a
INNER JOIN cursos b ON a.id_curso = b.id_curso
ORDER BY b.nombre_curso, a.nota DESC
'''
# Ejecutar la consulta y cargar los resultados en un DataFrame de pandas
df_join = pd.read_sql_query(consulta_join, conexion1)
print("\nResultados del INNER JOIN entre 'alumnos' y 'cursos':")
print(df_join)

# Calcular nota media por curso
print("\nNota media por curso:")
nota_por_curso = df_join.groupby('nombre_curso')['nota'].mean()
print(nota_por_curso)

# Calcular número de alumnos por curso
print("\nNúmero de alumnos por curso:")
alumnos_por_curso = df_join.groupby('nombre_curso').size()
print(alumnos_por_curso)

# Cerrar la conexión a la base de datos
# conexion.commit() guarda los cambios realizados en la base de datos
# en caso de no hacerlo los cambios no se guardan

print("Conexión a la base de datos cerrada.")
conexion1.commit()
conexion1.close()

