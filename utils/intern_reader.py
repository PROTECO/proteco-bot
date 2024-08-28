import polars as pl
import re

class InternReader:
    """
    Esta clase se encarga de leer los archivos csv que contienen la información de los becarios y de las asesorías.

    ...

    Methods:
    --------
    get_horarios_becario(becario) -> list:
        Regresa un DataFrame con los horarios del becario.

    getTemasAsesoria(becario) -> pl.DataFrame:
        Regresa un DataFrame con los temas de asesoría del becario.

    getCalendlyLink(becario) -> pl.DataFrame:
        Regresa un DataFrame con los links de Calendly del becario.

    getBecarioDescripcion(becario) -> str:
        Regresa un string con la descripción del becario.

    getHorarioAsesoriaPresencial(tema) -> pl.DataFrame:
        Regresa un DataFrame con los horarios presenciales de la asesoría.

    getHorarioAsesoriaEnLinea(tema) -> pl.DataFrame:
        Regresa un DataFrame con los horarios en línea de la asesoría.

    getBecarios(tema) -> pl.DataFrame:
        Regresa un DataFrame con los becarios que están inscritos en la asesoría.
    """


    # INFORMACIÓN DE LOS BECARIOS
    def get_horarios_becario(self, becario: str) -> pl.DataFrame:
        """
        Regresa una lista con los horarios del becario.
        
        Parameters:
        -----------
        becario : str
            Nombre del becario.

        Returns:
        --------
        list
            Lista con los horarios del becario.
        """
        ls = []
        with open(f'data/becarios/{becario}/horarios.csv', 'r') as file:
            # Leer los horarios del becario
            for line in file:
                ls.append(line.strip())
        return ls
    
    
    
    def get_temas_asesoria(becario: str) -> list:
        """
        Regresa un DataFrame con los temas de asesoría del becario.

        Parameters:
        -----------
        becario : str
            Nombre del becario.

        Returns:
        --------
        list
            Lista con los temas de asesoría del becario.
        """
        temas = []
        with open(f'data/becarios/{becario}/temas_asesoria.txt', 'r') as file:
            # Leer los temas de asesoría del becario
            for line in file:
                temas.append(line.strip())
        return temas
    
    
    def get_telegram_username(self, becario: str) -> str:
        """
        Regresa un DataFrame con los links de Calendly del becario.
        
        Parameters:
        -----------
        becario : str
            Nombre del becario.

        Returns:
        --------
        str
            String con el username de Telegram del becario.
        """
        with open(f'data/becarios/{becario}/descripcion.txt', 'r') as file:
            
            # Leer segunda línea del archivo
            line = file.readlines()[1]
            
            # Cortar string para obtener el username de Telegram
            telegram_username = line[17:]
            
        return telegram_username


    def get_becario_descripcion(becario: str) -> str:
        """
        Regresa un string con la descripción del becario.
        
        Parameters:
        -----------
        becario : str
            Nombre del becario.
            
        Returns:
        --------
        str
            String con la descripción del becario.
        """
        with open(f'data/becarios/{becario}/descripcion.txt', 'r') as file:
            becario_info = file.read()
        return becario_info
    
    
    def get_becarios(self, tema: str) -> list:
        """
        Regresa un DataFrame con los becarios que están inscritos en la asesoría.

        Parameters:
        -----------
        tema : str
            Nombre del tema de la asesoría.

        Returns:
        --------
        list
            Lista con los becarios asignados a la asesoría.
        """
        with open(f'data/temas_asesoria/{tema}.csv', 'r') as file:
            # Leer los becarios asignados a la asesoría y quitar los saltos de línea
            becarios = [becario.strip() for becario in file.readlines()]
            
        return becarios
    
    
    def get_horarios(self, tema_asesoria: str) -> str:
        """
        Regresa un string con los horarios de la asesoría.

        Parameters:
        -----------
        tema_asesoria : str
            Nombre del tema de la asesoría.

        Returns:
        --------
        str
            String con los horarios de la asesoría.
        """
        # String que se regresará
        result = ''
        
        # Leer becarios que asesoran en el tema
        becarios = self.get_becarios(tema_asesoria)
        
        for becario in becarios:
            usuario_telegram = self.get_telegram_username(becario)
            
            # Convertir el nombre a un formato más legible y agregarlo junto con el username de Telegram
            result += "--------------------------------\n"
            nombre_becario = ' '.join(re.findall('[A-Z][^A-Z]*', becario))
            result += f'{nombre_becario}:\n'
            result += f'{usuario_telegram}'
            result += "--------------------------------\n"
            
            # Leer horarios del becario
            horarios = self.get_horarios_becario(becario)
            
            for horario in horarios:
                result += f'- {horario}\n'
            result += '\n'

            
        return result