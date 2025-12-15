# PRACTICA LIMPIEZA DE DATOS CON PANDAS
# Practicar manejo de datos faltantes, conversión de tipos, 
# duplicados y tipos de datos en un DataFrame de pandas. 

import pandas as pd
import numpy as np  

# Crear un DataFrame con datos sucios
datos_sucios = {
    'Nombre': ["Ana", "Carlos", "Elena", "Diego", "Ana"],
    'Edad': ['22', '25', '19', '23', '22'],
    'Curso': ["Python", "Python", "JavaScript", "JavaScript", "Python"],
    'Nota': [8.5, 9.0, np.nan, 7.5, 8.5]
}
# np.nan es utilizado para representar valores faltantes en la
# biblioteca pandas
df = pd.DataFrame(datos_sucios)
print("DataFrame original con problemas:")
print(df)
print(df.dtypes)

# Manejo de datos faltantes: verificar datos faltantes.
print("\nDataFrame verificar los datos faltantes:")
print(df.isnull().sum())   

#convertir la columna 'Edad' a tipo numérico
df['Edad'] = pd.to_numeric(df['Edad'], errors='coerce').astype('Int64')
print("\nDataFrame después de convertir 'Edad' a numérico:")
print(df)
print(df.dtypes)

# errors='coerce' convierte valores no convertibles a NaN
# .astype('Int64') permite tener una columna de enteros que
# puede contener NaN

# Eliminar datos duplicados exactos
df_limpio = df.drop_duplicates()
print("\nDataFrame después de eliminar duplicados exactos:")
print(df_limpio)

# Calculamos la nota media por curso para rellenar los valores faltantes
nota_media_por_curso = df_limpio.groupby('Curso')['Nota'].mean()
print("\nNotas medias por curso:")
print(nota_media_por_curso)