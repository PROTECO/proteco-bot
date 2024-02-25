import pandas as pd
import os

class Reader:
    """
    Esta clase se encarga de leer los archivos csv que contienen la información de los becarios y de las asesorías.

    ...

    Methods:
    --------
    getHorarioBecarioEnLinea(becario) -> pd.DataFrame:
        Regresa un DataFrame con los horarios en línea del becario.
    
    getHorarioBecarioPresencial(becario) -> pd.DataFrame:
        Regresa un DataFrame con los horarios presenciales del becario.

    getTemasAsesoria(becario) -> pd.DataFrame:
        Regresa un DataFrame con los temas de asesoría del becario.

    getCalendlyLink(becario) -> pd.DataFrame:
        Regresa un DataFrame con los links de Calendly del becario.

    getBecarioDescripcion(becario) -> str:
        Regresa un string con la descripción del becario.

    getHorarioAsesoriaPresencial(tema) -> pd.DataFrame:
        Regresa un DataFrame con los horarios presenciales de la asesoría.

    getHorarioAsesoriaEnLinea(tema) -> pd.DataFrame:
        Regresa un DataFrame con los horarios en línea de la asesoría.

    getBecarios(tema) -> pd.DataFrame:
        Regresa un DataFrame con los becarios que están inscritos en la asesoría.
    """

    # INFORMACIÓN DE LOS BECARIOS
    def getHorarioBecarioEnLinea(becario: str) -> pd.DataFrame:
        """
        Regresa un DataFrame con los horarios en línea del becario.
        
        Parameters:
        -----------
        becario : str
            Nombre del becario.

        Returns:
        --------
        pd.DataFrame
            DataFrame con los horarios en línea del becario.
        """
        horario_en_linea = pd.read_csv(f'data/becarios/{becario}/horario_en_linea.csv')
        return horario_en_linea
    
    def getHorarioBecarioPresencial(becario: str) -> pd.DataFrame:
        """
        Regresa un DataFrame con los horarios presenciales del becario.
        
        Parameters:
        -----------
        becario : str
            Nombre del becario.

        Returns:
        --------
        pd.DataFrame
            DataFrame con los horarios presenciales del becario.
        """
        horario_presencial = pd.read_csv(f'data/becarios/{becario}/horario_presencial.csv')
        return horario_presencial
    
    def getTemasAsesoria(becario: str) -> pd.DataFrame:
        """
        Regresa un DataFrame con los temas de asesoría del becario.

        Parameters:
        -----------
        becario : str
            Nombre del becario.

        Returns:
        --------
        pd.DataFrame
            DataFrame con los temas de asesoría del becario.
        """
        temas_asesoria = pd.read_csv(f'data/becarios/{becario}/temas_asesoria.csv')
        return temas_asesoria
    
    def getCalendlyLink(becario: str) -> pd.DataFrame:
        """
        Regresa un DataFrame con los links de Calendly del becario.
        
        Parameters:
        -----------
        becario : str
            Nombre del becario.

        Returns:
        --------
        pd.DataFrame
            DataFrame con los links de Calendly del becario.
        """
        calendly_link = pd.read_csv(f'data/becarios/{becario}/calendly_link.csv')
        return calendly_link

    def getBecarioDescripcion(becario: str) -> str:
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
    

    ## INFORMACIÓN DE LAS ASESORÍAS
    
    def getHorarioAsesoriaPresencial(tema: str) -> pd.DataFrame:
        """
        Regresa un DataFrame con los horarios presenciales de la asesoría.

        Parameters:
        -----------
        tema : str
            Nombre del tema de la asesoría.

        Returns:
        --------
        pd.DataFrame
            DataFrame con los horarios presenciales de la asesoría.
        """
        horario_asesoria = pd.read_csv(f'data/asesorias/{tema}/presencial.csv')
        return horario_asesoria
    
    def getHorarioAsesoriaEnLinea(tema: str) -> pd.DataFrame:
        """
        Regresa un DataFrame con los horarios en línea de la asesoría.

        Parameters:
        -----------
        tema : str
            Nombre del tema de la asesoría.

        Returns:
        --------
        pd.DataFrame
            DataFrame con los horarios en línea de la asesoría.
        """
        horario_asesoria = pd.read_csv(f'data/asesorias/{tema}/en_linea.csv')
        return horario_asesoria
    
    def getBecarios(tema: str) -> pd.DataFrame:
        """
        Regresa un DataFrame con los becarios que están inscritos en la asesoría.

        Parameters:
        -----------
        tema : str
            Nombre del tema de la asesoría.

        Returns:
        --------
        pd.DataFrame
            DataFrame con los becarios que están inscritos en la asesoría.
        """
        becarios = pd.read_csv(f'data/asesorias/{tema}/becarios.csv')
        return becarios