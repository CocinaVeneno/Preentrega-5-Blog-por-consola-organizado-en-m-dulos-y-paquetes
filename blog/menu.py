"""Menú del blog y manejo de la entrada del usuario (input)."""

OPCIONES = {
    1: "Ver todos los posts",
    2: "Buscar por titulo",
    3: "Filtrar por tag",
    4: "Crear nuevo post",
    5: "Validar posts",
    6: "Guardar posts en JSON",
    7: "Salir",
}


def mostrar_menu():
    """Muestra el menú y retorna la opción elegida, o None si no es válida."""
    print("\n--- MENU DEL BLOG ---")
    for numero, texto in OPCIONES.items():
        print(f"{numero}. {texto}")

    try:
        opcion = int(input("Elegí una opción: "))
    except ValueError:
        print("Opción inválida: tenés que escribir un número.")
        return None

    if opcion not in OPCIONES:
        print(f"Opción inválida, elegí un número del 1 al {len(OPCIONES)}.")
        return None

    return opcion


def pedir_texto(mensaje, obligatorio=False):
    """Pide un texto. Si es obligatorio, lo vuelve a pedir hasta que no quede vacío."""
    texto = input(mensaje).strip()
    while obligatorio and not texto:
        print("Este campo es obligatorio, no puede quedar vacío.")
        texto = input(mensaje).strip()
    return texto


def pedir_termino(mensaje):
    """Pide un término de búsqueda. Si queda vacío, avisa y retorna un texto vacío."""
    termino = pedir_texto(mensaje)
    if not termino:
        print("No escribiste nada, volvé a intentarlo.")
    return termino


def pedir_tag(tags_disponibles):
    """Muestra los tags que existen en el blog y pide uno."""
    print("Tags disponibles:", ", ".join(tags_disponibles) or "(todavía no hay tags)")
    return pedir_termino("Ingresá un tag: ")


def pedir_estado(estados, por_defecto="borrador"):
    """Pide un estado válido. Con Enter se usa el estado por defecto."""
    while True:
        estado = input(f"Estado ({'/'.join(estados)}) [Enter = {por_defecto}]: ").strip().lower()
        if not estado:
            return por_defecto
        if estado in estados:
            return estado
        print(f"Estado inválido. Elegí uno de estos: {', '.join(estados)}.")


def pedir_datos_post(estados):
    """Pide los datos de un post nuevo y los retorna en un diccionario."""
    print("\nNuevo post (el título y el contenido son obligatorios)")
    titulo = pedir_texto("Título: ", obligatorio=True)
    contenido = pedir_texto("Contenido: ", obligatorio=True)
    tags_texto = pedir_texto("Tags separados por coma (ej: Python, IA): ")
    tags = [tag.strip() for tag in tags_texto.split(",") if tag.strip()]
    estado = pedir_estado(estados)
    return {"titulo": titulo, "contenido": contenido, "tags": tags, "estado": estado}


def confirmar(pregunta):
    """Retorna True si el usuario responde que sí (s / si / sí)."""
    return input(pregunta).strip().lower() in ("s", "si", "sí")
