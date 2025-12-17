#CONSOLIDAR TODO EN UN SCRIPT CON MENÚ INTERACTIVO QUE GESTIONE DATOS SQLITE Y GENERE INFORMES CON PANDAS

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

#matplotlib.pyplot  # Para entornos sin interfaz gráfica

# INICIAMOS LA BASE DE DATOS
def init_db():
    conn = sqlite3.connect('alumnos_cursos.db')
    cursor = conn.cursor()
    
    #crear tabla cursos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            id_curso INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_curso TEXT UNIQUE NOT NULL
        )
    ''')

    #crear tabla alumnos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            edad INTEGER,
            id_curso INTEGER,
            nota REAL,
            FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
        )
    ''')
 