"""Persistencia del blog: carga y guardado de los posts en posts.json."""

import json
from pathlib import Path

from blog.modelos import Autor, Post

# posts.json se busca en la carpeta raíz del proyecto, sin importar desde dónde se ejecute
RUTA_POSTS = Path(__file__).resolve().parent.parent / "posts.json"

# Datos del autor principal (los mismos de los módulos anteriores)
perfil_autor = {
    "nombre": "Lucas Cook",
    "bio": "Desarrollo de automatización y backend",
    "especialidad": "Docker, n8n, Botpress y JavaScript",
    "redes_sociales": {
        "Instagram": "@Lulu_a_cook",
        "GitHub": "@CocinaVeneno"
    }
}

# Posts de ejemplo: se escriben en posts.json solo si el archivo no existe
POSTS_EJEMPLO = [
    {
        "id": 1,
        "titulo": "Workflows con n8n y Webhooks",
        "contenido": "Cómo recibir datos con un Webhook y procesarlos paso a paso en un workflow de n8n.",
        "autor": perfil_autor,
        "categoria": "Automatización",
        "tags": ["n8n", "Backend", "JavaScript"],
        "estado": "publicado"
    },
    {
        "id": 2,
        "titulo": "Contenedorización de microservicios con Docker",
        "contenido": "Cómo empaquetar cada microservicio en su propio contenedor y desplegarlo en un VPS.",
        "autor": perfil_autor,
        "categoria": "VPS",
        "tags": ["Docker", "Backend"],
        "estado": "borrador"
    },
    {
        "id": 3,
        "titulo": "Creación de Chatbots avanzados con Botpress",
        "contenido": "Cómo diseñar flujos de conversación en Botpress y sumarles lógica con JavaScript.",
        "autor": perfil_autor,
        "categoria": "Asistentes Virtuales",
        "tags": ["Botpress", "JavaScript"],
        "estado": "archivado"
    },
    {
        "id": 4,
        "titulo": "Automatizando tareas repetitivas con Python",
        "contenido": "Scripts simples en Python para renombrar archivos, leer datos y ahorrar tiempo todos los días.",
        "autor": perfil_autor,
        "categoria": "Python",
        "tags": ["Python", "Backend"],
        "estado": "publicado"
    },
    {
        "id": 5,
        "titulo": "Agentes de IA conectados a n8n",
        "contenido": "Cómo sumar un modelo de IA a un workflow para que responda mensajes y tome decisiones.",
        "autor": perfil_autor,
        "categoria": "Inteligencia Artificial",
        "tags": ["IA", "n8n"],
        "estado": "publicado"
    },
    {
        "id": 6,
        "titulo": "Cómo estoy construyendo este blog",
        "contenido": "El recorrido del proyecto: de estructuras de datos en Python a una aplicación web con Django.",
        "autor": perfil_autor,
        "categoria": "Blog",
        "tags": ["Python", "Django"],
        "estado": "borrador"
    },
    # Posts con errores a propósito, para probar la carga y la validación
    {
        "id": 7,
        "titulo": "Primeros pasos con Django",
        # falta la clave "contenido": no se puede reconstruir como objeto
        "autor": perfil_autor,
        "categoria": "Django",
        "tags": ["Python", "Django"],
        "estado": "borrador"
    },
    {
        "id": 8,
        "titulo": "",  # título vacío: lo detecta la validación
        "contenido": "Post de prueba que quedó sin título.",
        "autor": perfil_autor,
        "categoria": "Pruebas",
        "tags": ["Backend"],
        "estado": "publicado"
    },
    {
        "id": 9,
        "titulo": "Ideas para próximos posts sobre IA",
        "contenido": "Temas que quiero escribir más adelante.",
        "autor": perfil_autor,
        "categoria": "Inteligencia Artificial",
        "tags": "IA, Python",  # debería ser una lista: lo detecta la validación
        "estado": "pendiente"
    }
]


def autor_principal():
    """Retorna el autor principal del blog como objeto Autor."""
    return Autor.desde_dict(perfil_autor)


def reconstruir_posts(lista_dicts):
    """Convierte diccionarios en objetos Post. Retorna (posts, avisos) y saltea los incompletos."""
    posts = []
    avisos = []
    for numero, datos in enumerate(lista_dicts, start=1):
        try:
            posts.append(Post.desde_dict(datos))
        except (ValueError, TypeError) as error:
            avisos.append(f"Aviso: se ignoró el post {numero} de posts.json porque {error}.")
    return posts, avisos


def crear_archivo_ejemplo(ruta):
    """Escribe los posts de ejemplo en posts.json. Retorna un mensaje con el resultado."""
    try:
        ruta.write_text(json.dumps(POSTS_EJEMPLO, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")
    except OSError as error:
        return f"No se pudo crear {ruta.name}: {error}"
    return f"Se creó {ruta.name} con los posts de ejemplo."


def cargar_posts(ruta=RUTA_POSTS):
    """
    Lee posts.json y reconstruye los objetos Post.
    Retorna (lista de Post, lista de avisos). Nunca corta el programa.
    """
    ruta = Path(ruta)

    try:
        texto = ruta.read_text(encoding="utf-8")
    except FileNotFoundError:
        aviso_creacion = crear_archivo_ejemplo(ruta)
        posts, avisos = reconstruir_posts(POSTS_EJEMPLO)
        return posts, [f"No se encontró {ruta.name}. {aviso_creacion}"] + avisos
    except OSError as error:
        return [], [f"No se pudo leer {ruta.name} ({error}). El blog arranca sin posts."]

    if not texto.strip():
        return [], [f"{ruta.name} está vacío. El blog arranca sin posts."]

    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as error:
        return [], [
            f"{ruta.name} tiene contenido inválido (línea {error.lineno}, columna {error.colno}). "
            "El blog arranca sin posts. Si guardás, el archivo se va a reemplazar."
        ]

    if not isinstance(datos, list):
        return [], [f"{ruta.name} debería tener una lista de posts, pero tiene otro formato. El blog arranca sin posts."]

    return reconstruir_posts(datos)


def guardar_posts(posts, ruta=RUTA_POSTS):
    """
    Convierte cada Post en diccionario y guarda la lista en posts.json.
    Retorna (True/False, mensaje).
    """
    ruta = Path(ruta)

    # JSON no sabe guardar objetos: primero se convierten a diccionarios
    try:
        lista_dicts = [post.a_dict() for post in posts]
    except AttributeError:
        return False, "No se guardó nada: hay un elemento que no es un Post y no se puede convertir a diccionario."

    # Se arma todo el texto antes de escribir, así un error no deja el archivo a medias
    try:
        texto = json.dumps(lista_dicts, ensure_ascii=False, indent=4)
    except TypeError as error:
        return False, f"No se guardó nada: hay un dato que JSON no puede guardar ({error})."

    try:
        ruta.write_text(texto + "\n", encoding="utf-8")
    except OSError as error:
        return False, f"No se pudo escribir {ruta.name}: {error}"

    return True, f"Se guardaron {len(lista_dicts)} posts en {ruta.name}."
