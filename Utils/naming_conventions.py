from unidecode import unidecode

class NamingConventions:
    """
    Class to apply naming conventions to strings
    
    Attributes:
    -----------
    None
    
    Methods:
    --------
    to_snake_case(code: str) -> str
        Converts a string to snake case
    to_pascal_case(code: str) -> str
        Converts a string to pascal case
    """
    @staticmethod
    def to_snake_case(code):
        """
        Converts a string to snake case
        
        Parameters:
        -----------
        code: str
            String to convert
        
        Returns:
        --------
        str
            String converted to snake case
        """
        # Eliminar espacios al inicio y al final
        code = code.strip()
        # Reemplazar espacios y guiones por guiones bajos
        code = code.replace(" ", "_").replace("-", "_")
        # Pasar a minúsculas
        code = code.lower()
        return unidecode(code)
    
    @staticmethod
    def to_pascal_case(code):
        """
        Converts a string to pascal case
        
        Parameters:
        -----------
        code: str
            String to convert
        
        Returns:
        --------
        str
            String converted to pascal case
        """
        # Eliminar espacios al inicio y al final
        code = code.strip()
        # Reemplazar espacios y guiones por guiones bajos
        code = code.replace(" ", "_").replace("-", "_")
        # Pasar a minúsculas
        code = code.lower()
        # Separar por guiones bajos
        code = code.split("_")
        # Capitalizar cada palabra
        code = [word.capitalize() for word in code]
        # Unir las palabras
        return "".join(code)