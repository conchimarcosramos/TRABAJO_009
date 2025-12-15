# crear, explorar y filtrar dataframes sencillos con pandas
import pandas as pd

# Crear un DataFrame sencillo
datos = {
    'Nombre': ['Ana', 'Carlos', 'Elena', 'Diego'],
    'Edad': [22, 25, 19, 23],
    'Cursos': ['Python', 'Python', 'JavaScript', 'JavaScript']
}
# Crear un DataFrame a partir del diccionario
df = pd.DataFrame(datos)

# Mostrar primeras filas del DataFrame
print("=== Primeras filas del DataFrame ===")
print(df.head())

# Mostrar información general del DataFrame
print("\n=== Información del DataFrame ===")
print(df.info())

# Mostrar estadísticas descriptivas del DataFrame
# sólo para columnas numéricas
print("\n=== Estadísticas descriptivas del DataFrame ===")
print(df.describe())    

# Filtrar filas donde la edad es mayor a 20
# usamos condición booleana df['Edad'] > 20
print("\n=== Filas donde la edad es mayor a 20 ===")
# Crear un nuevo DataFrame con los alumnos mayores de 20 años
alumnos_mas_20 = df[df['Edad'] > 20]
# mostrar el DataFrame filtrado
print(alumnos_mas_20)

# Filtrar filas donde el curso es 'Python'
print("\n=== Filas donde el curso es 'Python' ===")
# Crear un nuevo DataFrame con los alumnos que cursan Python
alumnos_python = df[df['Cursos'] == 'Python']
# mostrar el DataFrame filtrado
# utilizamos == para comparar igualdad
print("\n=== Alumnos de 'Python' ===")
print(alumnos_python)
