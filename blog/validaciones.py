"""Reglas de validación del blog. No importa otros módulos del proyecto, así se evitan imports circulares."""


def claves_faltantes(datos, claves):
    """Retorna la lista de claves obligatorias que no están en el diccionario."""
    return [clave for clave in claves if clave not in datos]


def es_texto_con_contenido(valor):
    """True si el valor es un texto que no está vacío ni tiene solo espacios."""
    return isinstance(valor, str) and bool(valor.strip())


def validar_post(post, estados_validos):
    """
    Revisa los atributos de un objeto Post.
    Retorna (True, "válido") o (False, "descripción del problema").
    """
    if not es_texto_con_contenido(post.titulo):
        return False, "el título está vacío o no es texto"

    if not es_texto_con_contenido(post.contenido):
        return False, "el contenido está vacío o no es texto"

    # El autor tiene que ser un objeto con nombre (una instancia de Autor)
    if not es_texto_con_contenido(getattr(post.autor, "nombre", None)):
        return False, "el autor no tiene nombre"

    if not isinstance(post.tags, list):
        return False, "los tags tienen que ser una lista"

    if post.estado not in estados_validos:
        return False, f"el estado '{post.estado}' no es válido (usá: {', '.join(estados_validos)})"

    return True, "válido"
