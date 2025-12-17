# IMPLEMENTAR UN FLUJO DE DATOS EXTREMO A EXTREMO: CARGAR CSV A SQLITE, 
# CONSULTAR Y ANALIZAR DATOS CON SQL Y PANDAS. GENERAR INFORME.

import sqlite3
import pandas as pd
import time #import time para medir tiempos de ejecución    
# Crear una conexión a la base de datos SQLite alumnos_cursos.db

from io import StringIO

# creamos datos de ejemplo en formato CSV
datos_csv= StringIO("""vendedor, fecha, importe, zona
Juan, 2024-01-15, 1500, Norte
María, 2024-01-16, 2000, Sur
Juan, 2024-01-17, 1800, Norte
Pedro,, 950.25, Este
,2024-01-19, 3200.00, Sur
María, 2024-01-20, 2150.00, Sur
""")

