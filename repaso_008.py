# CONSOLIDAR TODO EN UN SCRIPT CON MENÚ INTERACTIVO QUE GESTIONE DATOS SQLITE Y GENERE INFORMES CON PANDAS

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# matplotlib.pyplot  # Para entornos sin interfaz gráfica

# INICIAMOS LA BASE DE DATOS
def init_db():
    conn = sqlite3.connect('alumnos_cursos.db')
    cursor = conn.cursor()
    
    # crear tabla cursos_2
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos_2 (
            id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_curso TEXT UNIQUE NOT NULL
        )
    ''')

    # crear tabla alumnos_2
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos_2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            id_curso INTEGER,
            nota REAL,
            FOREIGN KEY (id_curso) REFERENCES cursos_2(id_curso)
        )
    ''')
 
 # INTRODUCIMOS DATOS DE PRUEBA
 # EN NUESTRO CASO LA BD YA ESTA CREADA Y LOS DATOS YA ESTAN EN LA BD
 
    cursor.execute("SELECT COUNT(*) FROM cursos_2")
    # execute para ejecutar una consulta
    if cursor.fetchone()[0] == 0:
        cursos_2_data = [
            (1,'Python'),
            (2,'JavaScript'),
            (3,'Big Data')
        ]
        cursor.executemany('INSERT INTO cursos_2 VALUES (?, ?)', cursos_2_data)
        # executemany para insertar multiples filas a la vez
        alumnos_2_data = [
            (1,'Ana', 22, 1, 8.5),
            (2,'Carlos', 25, 1, 9.0),
            (3,'Elena', 19, 2, 7.8),
            (4,'Diego', 23, 2, 8.2),
            (5,'Laura', 21, 1, 8.9),
            (6,'Marta', 24, 3, 9.5)
        ]
        cursor.executemany('INSERT INTO alumnos_2 (id, nombre, edad, id_curso, nota) VALUES (?, ?, ?, ?, ?)', alumnos_2_data)
        print("Datos de prueba insertados en la base de datos.")
        conn.commit()
        conn.close()

# FUNCIONES PARA CONSULTAS Y REPORTES
def listar_alumnos_por_curso():
    conn = sqlite3.connect('alumnos_cursos.db')
    # Realizar consulta para listar alumnos por curso
    conexion = sqlite3.connect('alumnos_cursos.db')
    # Obtener y mostrar los cursos disponibles 
    df_cursos = pd.read_sql_query('SELECT id_curso, nombre_curso FROM cursos_2', conexion)
    print("Cursos disponibles:")
    print(df_cursos.to_string(index=False))
    id_curso = input("Ingrese el ID del curso para listar sus alumnos: ")   
      
    consulta = '''
        SELECT 
            cursos_2.nombre_curso,
            alumnos_2.nombre,
            alumnos_2.edad,
            alumnos_2.nota
        FROM alumnos_2
        INNER JOIN cursos_2 ON alumnos_2.id_curso = cursos_2.id_curso
        WHERE alumnos_2.id_curso = ?
        ORDER BY alumnos_2.nota DESC
    '''
    
    df = pd.read_sql_query(consulta, conn, params=(id_curso,))
    #pd.read_sql_query para leer el resultado de una consulta SQL en un DataFrame de pandas
    print("\nResultados de alumnos por curso:")
    print(df.to_string(index=False))
    
    conn.close()   
    
def estadisticas_por_curso():
         #Mostrar estadísticas de notas por curso
        conn = sqlite3.connect('alumnos_cursos.db')
        consulta = '''
            SELECT 
                cursos_2.nombre_curso,
                COUNT(alumnos_2.nombre) AS cantidad_alumnos,
                ROUND(AVG(alumnos_2.nota), 2) AS nota_media,
                ROUND(MAX(alumnos_2.nota), 2) AS nota_maxima,
                ROUND(MIN(alumnos_2.nota), 2) AS nota_minima
            FROM alumnos_2
            inner JOIN cursos_2 ON alumnos_2.id_curso = cursos_2.id_curso
            GROUP BY cursos_2.nombre_curso
        '''
        
        df = pd.read_sql_query(consulta, conn)
        #pd.read_sql_query para leer el resultado de una consulta SQL en un DataFrame de pandas
        print("\nEstadísticas de notas por curso:")
        print(df.to_string(index=False))
        conn.close()
        
def buscar_alumno():    
        #Buscar alumno por nombre
        conn = sqlite3.connect('alumnos_cursos.db')
        nombre_alumno = input("Ingrese el nombre del alumno a buscar: ")
        
        consulta = '''
            SELECT 
                alumnos_2.nombre,
                alumnos_2.edad,
                cursos_2.nombre_curso,
                alumnos_2.nota
            FROM alumnos_2
            INNER JOIN cursos_2 ON alumnos_2.id_curso = cursos_2.id_curso
            WHERE LOWER(alumnos_2.nombre) LIKE LOWER(?)
        '''
        #LOWER para hacer la búsqueda case-insensitive
        #case-insensitive para que no importe mayúsculas o minúsculas
        
        df = pd.read_sql_query(consulta, conn, params=(f'%{nombre_alumno}%',))
        #pd.read_sql_query para leer el resultado de una consulta SQL en un DataFrame de pandas
        if len(df) == 0:
            print("No se encontraron alumnos con ese nombre.")
        else:
            print("\n=== Resultados de la búsqueda ===")
            print(df.to_string(index=False)
                  )
        
        conn.close()
# EXPORTAMOS INFOMRE COMPLETO A CSV
def exportar_informe_csv():
    conn = sqlite3.connect('alumnos_cursos.db')
    consulta = '''
        SELECT 
            alumnos_2.nombre AS nombre_alumno,
            alumnos_2.edad,
            cursos_2.nombre_curso,
            alumnos_2.nota
        FROM alumnos_2
        INNER JOIN cursos_2 ON alumnos_2.id_curso = cursos_2.id_curso
        ORDER BY cursos_2.nombre_curso, alumnos_2.nota DESC
    '''
    
    df = pd.read_sql_query(consulta, conn)
    df.to_csv('informe_alumnos_cursos.csv', index=False)
    print("Informe exportado a informe_alumnos_cursos.csv")
    conn.close()   
    
    # MENÚ INTERACTIVO PRINCIPAL
    
def menu_principal():
    init_db()
    while True:
        print("\n=== Menú Principal ===")
        print("1. Listar alumnos por curso")
        print("2. Mostrar estadísticas de notas por curso")
        print("3. Buscar alumno por nombre")
        print("4. Exportar informe completo a CSV")
        print("5. Salir")
        
        opcion = input("Seleccione una opción (1-5): ")
        
        if opcion == '1':
            listar_alumnos_por_curso()
        elif opcion == '2':
            estadisticas_por_curso()
        elif opcion == '3':
            buscar_alumno()
        elif opcion == '4':
            exportar_informe_csv()
        elif opcion == '5':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 5.") 
if __name__ == "__main__":
    init_db()
    menu_principal()
                