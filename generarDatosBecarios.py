import pandas as pd
import os
from unidecode import unidecode

# Lista de lenguajes de programación ofrecidos
temas_asesoria = set()

# Leer el archivo CSV
data = pd.read_csv('data/horarios_origin.csv')

def to_snake_case(code):
    # Eliminar espacios al inicio y al final
    code = code.strip()
    # Reemplazar espacios y guiones por guiones bajos
    code = code.replace(" ", "_").replace("-", "_")
    # Pasar a minúsculas
    code = code.lower()
    return unidecode(code)


# Crear un directorio para cada becario con sus datos y uno para cada tema de asesoría
for becario in data['No']:


    nombre = data[data['No'] == becario]['Nombre'].values[0]
    nombre_pascal = "".join(nombre.split(' '))
    liga_calendly = data[data['No'] == becario]['Liga de Calendly'].values[0]

    # Escribir la descripcion del becario en un archivo de texto    
    os.makedirs(f'data/becarios/{nombre_pascal}', exist_ok=True)
    file = open(f'data/becarios/{nombre_pascal}/descripcion.txt', 'w')
    file.write(f'Nombre: {nombre}\n')
    file.write(f'No: {becario}\n')


    # Horarios en linea
    file.write(f'Horarios en línea:\n')
    horarios_en_linea = data[data['No'] == becario]['Horario en Linea'].values[0]
    if not pd.isna(horarios_en_linea):
        file_horario_en_linea = open(f'data/becarios/{nombre_pascal}/horario_en_linea.csv', 'w')
        file_horario_en_linea.write(f'Horario\n')

        horarios_en_linea = str.lower(unidecode(horarios_en_linea).replace(' ', '')).split(',')
        for horario in horarios_en_linea:
            file.write(f'>{horario}\n')
            file_horario_en_linea.write(f'{horario}\n')
        
        file_horario_en_linea.close()

    # Horarios presenciales
    file.write(f'Horarios presenciales:\n')
    horarios_presencial = data[data['No'] == becario]['Horario Presencial'].values[0]

    if not pd.isna(horarios_presencial):
        file_horario_presencial = open(f'data/becarios/{nombre_pascal}/horario_presencial.csv', 'w')
        file_horario_presencial.write(f'Horario\n')

        horarios_presencial = str.lower(unidecode(horarios_presencial).replace(' ', '')).split(',')
        for horario in horarios_presencial:
            file.write(f'<{horario}\n')
            file_horario_presencial.write(f'{horario}\n')

        file_horario_presencial.close()
    
    # Temas de asesorias
    file.write(f'Temas de asesorías:\n')
    temas_asesoria_becario = data[data['No'] == becario]['Temas de asesorías'].values[0]
    if not pd.isna(temas_asesoria_becario):
        temas_asesoria_becario = temas_asesoria_becario.split(',')
        temas_asesoria_becario = [to_snake_case(tema) for tema in temas_asesoria_becario]
        for tema in temas_asesoria_becario:
            file.write(f'-{tema}\n')
            if tema not in temas_asesoria:
                temas_asesoria.add(tema)
                os.makedirs(f'data/asesorias/{tema}', exist_ok=True)
                file_asesoria = open(f'data/asesorias/{tema}/becarios.csv', 'w')
                file_asesoria.write(f'Nombre\n')
            else:
                file_asesoria = open(f'data/asesorias/{tema}/becarios.csv', 'a')
            file_asesoria.write(f'{nombre_pascal}\n')

    
    
    file.write(f"Liga de calendly:" )
    file.write(f"{liga_calendly}\n")
    file.close()

# Crear archivos para los temas de asesoría
for tema in temas_asesoria:
    
    df_presencial = pd.DataFrame(columns=['Nombre', 'Dia', 'Horario'])
    df_en_linea = pd.DataFrame(columns=['Nombre', 'Dia', 'Horario'])
    nombres = pd.read_csv(f'data/asesorias/{tema}/becarios.csv')

    # Iterar a traves de cada becario
    for becario in nombres['Nombre']:
        nombre = becario

        # Horarios en linea
        try:
            horarios_en_linea = pd.read_csv(f'data/becarios/{nombre}/horario_en_linea.csv')
            for horario in horarios_en_linea['Horario']:
                dia = horario.split(':',1)[0]
                horario = horario.split(':',1)[1]
                df_en_linea = pd.concat([df_en_linea, pd.DataFrame([[nombre, dia, horario]], columns=['Nombre', 'Dia', 'Horario'])])
        except:
            pass

        # Horarios presenciales
        try:
            horarios_presencial = pd.read_csv(f'data/becarios/{nombre}/horario_presencial.csv')
            for horario in horarios_presencial['Horario']:
                dia = horario.split(':',1)[0]
                horario = horario.split(':',1)[1]
                df_presencial = pd.concat([df_presencial, pd.DataFrame([[nombre, dia, horario]], columns=['Nombre', 'Dia', 'Horario'])])
            
        except:
            pass

    # Guardar los archivos
    df_en_linea.to_csv(f'data/asesorias/{tema}/en_linea.csv', index=False)
    df_presencial.to_csv(f'data/asesorias/{tema}/presencial.csv', index=False)
