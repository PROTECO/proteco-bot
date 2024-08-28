import polars as pl
import os
from utils.naming_conventions import NamingConventions

# Lista de lenguajes de programación ofrecidos
temas_asesoria = set()

# Leer el archivo CSV
data = pl.read_csv('data/becarios_raw.csv')

print(data)

# Set de temas de asesoría
temas_asesoria = set()

# Crear un directorio para cada becario con sus datos y uno para cada tema de asesoría
for becario in data.to_dicts():
    try:
        id = becario['No']
        nombre = becario['Nombre']
        nombre_pascal = NamingConventions.to_pascal_case(nombre)
        temas_asesoria_becario = [NamingConventions.to_snake_case(tema) for tema in becario['Temas de asesorías'].split(',')]
        horarios = becario['Horario'].split(';')
        user_telegram = becario['Usuario Telegram']
        

        # Crear directorio para el becario
        os.makedirs(f'data/becarios/{nombre_pascal}', exist_ok=True)

        # Crear archivo de descripción
        with open(f'data/becarios/{nombre_pascal}/descripcion.txt', 'w') as file:
            file.write(f'Nombre: {nombre}\n')
            file.write(f'Usuario Telegram: {user_telegram}\n')
        
        # Insertar horarios en un archivo
        for horario in horarios:
            with open(f'data/becarios/{nombre_pascal}/horarios.csv', 'a') as file:
                file.write(f'{horario}\n')
        
        # Insertar temas de asesoría en un archivo
        for tema in temas_asesoria_becario:
            temas_asesoria.add(tema)
            with open(f'data/becarios/{nombre_pascal}/temas_asesoria.csv', 'a') as file:
                file.write(f'{tema}\n')
    
    except Exception as e:
        print(f'Error insertando becario {nombre}: {e}')


# Crear archivos para los temas de asesoría
os.makedirs('data/temas_asesoria', exist_ok=True)
for tema in temas_asesoria:
    with open(f'data/temas_asesoria/{tema}.csv', 'w') as file:
        # Obtener becarios que asesoran en el tema convirtiendo a snake case
        for becario in data.to_dicts():
            temas_asesoria_becario = [NamingConventions.to_snake_case(tema) for tema in becario['Temas de asesorías'].split(',')]
            if tema in temas_asesoria_becario:
                file.write(f'{NamingConventions.to_pascal_case(becario["Nombre"])}\n')