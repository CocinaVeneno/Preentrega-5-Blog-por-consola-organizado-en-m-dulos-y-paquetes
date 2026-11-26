"""Punto de entrada del blog por consola: carga posts.json, crea el Blog y conecta el menú con sus métodos."""

from blog.datos import autor_principal, cargar_posts, guardar_posts
from blog.menu import confirmar, mostrar_menu, pedir_datos_post, pedir_tag, pedir_termino
from blog.modelos import Blog, Post
from blog.operaciones import mostrar_mensajes, mostrar_posts, mostrar_validaciones


def guardar(blog):
    """Guarda los posts del blog en posts.json y muestra el resultado."""
    ok, mensaje = guardar_posts(blog.obtener_posts())
    print(mensaje)
    if ok:
        blog.marcar_guardado()


def main():
    # 1. Cargar posts.json (los diccionarios vuelven a ser objetos Post)
    posts, avisos = cargar_posts()
    mostrar_mensajes(avisos)

    # 2. Crear la instancia de Blog que maneja toda la colección
    blog = Blog("Blog de Lucas Cook", autor_principal(), posts)
    print(f"Blog listo: {len(blog)} posts cargados.")

    # 3. Menú: cada opción llama a un método del objeto blog
    while True:
        opcion = mostrar_menu()
        # Si la opción no es válida, mostrar_menu() ya avisó y retorna None: se vuelve al menú

        if opcion == 1:
            print("\nPosts disponibles:")
            mostrar_posts(blog.listar_posts(), "El blog todavía no tiene posts.")

        elif opcion == 2:
            termino = pedir_termino("Buscar por titulo: ")
            if termino:
                print(f"\nResultados para '{termino}':")
                mostrar_posts(blog.buscar_por_titulo(termino), "No se encontraron posts con ese título.")

        elif opcion == 3:
            tag = pedir_tag(blog.obtener_tags())
            if tag:
                print(f"\nPosts con el tag '{tag}':")
                mostrar_posts(blog.filtrar_por_tag(tag), "No hay posts con ese tag.")

        elif opcion == 4:
            datos = pedir_datos_post(Post.ESTADOS_VALIDOS)
            try:
                post = blog.crear_post(**datos)
            except ValueError as error:
                print(f"No se pudo crear el post: {error}")
            else:
                print(f"\nPost creado con id {post.id}: {post}")
                print("Para que no se pierda al cerrar, guardalo con la opción 6.")

        elif opcion == 5:
            print("\nValidación de posts:")
            mostrar_validaciones(blog.validar_posts())

        elif opcion == 6:
            guardar(blog)

        elif opcion == 7:
            if blog.hay_cambios and confirmar("Hay cambios sin guardar. ¿Guardarlos antes de salir? (s/n): "):
                guardar(blog)
            print("Gracias por usar el sistema del blog. ¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
