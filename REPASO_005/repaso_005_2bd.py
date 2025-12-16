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
conexion1 = sqlite3.connect('alumnos_2.db')
conexion2 = sqlite3.connect('cursos_2.db')
cursor1 = conexion1.cursor()
cursor2 = conexion2.cursor()

# Crear tabla 'cursos_2' que estará relacionada con la tabla 'alumnos_2' a través de 'curso_id'
cursor2.execute('''
CREATE TABLE cursos_2 (
    id_curso INTEGER PRIMARY KEY,
    nombre_curso TEXT NOT NULL,
    horas INTEGER NOT NULL
)
''')
# Insertar datos en la tabla 'cursos_2'
cursos_2_data = [
    (1, 'Python', 40),
    (2, 'JavaScript', 35)
]
cursor2.executemany('INSERT INTO cursos_2 (id_curso, nombre_curso, horas) VALUES (?, ?, ?)', 
                   cursos_2_data)    
#cursor.executemany realiza múltiples inserciones en una sola llamada

# Creamos la tabla de alumnos_2 relacionada con cursos_2, 
# con id_curso como clave foránea
cursor1.execute('''
CREATE TABLE alumnos_2 (
    id_alumno INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL,
    id_curso INTEGER,
    nota REAL,
    FOREIGN KEY (id_curso) REFERENCES cursos_2(id_curso)
)
''')
# Insertar datos en la tabla 'alumnos_2' con id_curso relacionado
alumnos_2_data = [
    (1, 'Ana', 22, 1, 8.5),
    (2, 'Carlos', 25, 1, 9.0),
    (3, 'Elena', 19, 2, 7.8),
    (4, 'Diego', 23, 2, 7.5)
]
cursor1.executemany('INSERT INTO alumnos_2 (id_alumno, nombre, edad, id_curso, nota) VALUES (?, ?, ?, ?, ?)', alumnos_2_data)

# Guardar los cambios y cerrar la conexión
conexion1.commit()
conexion2.commit()
print("Tablas creadas e insertados los datos correctamente.")
conexion1.close()
conexion2.close()
