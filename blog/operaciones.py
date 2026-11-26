"""Muestra en consola los resultados de las operaciones del Blog."""


def mostrar_posts(posts, mensaje_vacio="No hay posts para mostrar."):
    """Muestra un post por línea. Sirve para objetos Post o para las líneas de Blog.listar_posts()."""
    if not posts:
        print(mensaje_vacio)
        return
    for post in posts:
        print(f"- {post}")


def mostrar_validaciones(resultados):
    """Muestra el resultado de Blog.validar_posts(): una línea por post y un resumen."""
    if not resultados:
        print("No hay posts para validar.")
        return

    validos = 0
    for post, es_valido, mensaje in resultados:
        if es_valido:
            validos += 1
            print(f"Post {post.id}: válido")
        else:
            print(f"Post {post.id}: error - {mensaje}")
    print(f"\nResultado: {validos} válidos y {len(resultados) - validos} con errores.")


def mostrar_mensajes(mensajes):
    """Muestra una lista de avisos, uno por línea."""
    for mensaje in mensajes:
        print(mensaje)
