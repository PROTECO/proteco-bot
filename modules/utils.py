from unidecode import unidecode

def to_snake_case(code):
    # Eliminar espacios al inicio y al final
    code = code.strip()
    # Reemplazar espacios y guiones por guiones bajos
    code = code.replace(" ", "_").replace("-", "_")
    # Pasar a minúsculas
    code = code.lower()
    return unidecode(code)