# Blog por consola (Preentrega 6: POO y persistencia JSON)

Sistema de blog que se usa desde la terminal. Permite listar posts, buscarlos por título, filtrarlos por etiqueta, crear posts nuevos, validar que estén bien cargados y guardarlos en `posts.json`, así no se pierden al cerrar el programa.

En esta versión el blog está modelado con **clases** (`Autor`, `Post` y `Blog`) y los datos se **cargan y guardan en JSON**.

## Requisitos

- Python 3.8 o superior.
- No usa librerías externas, así que no hace falta instalar nada.

## Cómo ejecutarlo

1. Abrí una terminal en la carpeta del proyecto (donde está `main.py`).
2. (Opcional) Creá y activá un entorno virtual:
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # Mac / Linux
   ```
3. Ejecutá:
   ```
   python main.py
   ```

`posts.json` siempre se lee y se guarda en la carpeta del proyecto, aunque ejecutes `main.py` desde otra carpeta.

## Estructura del proyecto

```
├── main.py               # Punto de entrada: carga posts.json, crea el Blog y conecta el menú
├── posts.json            # Datos persistentes del blog (se crea solo si no existe)
├── README.md
│
└── blog/                 # Paquete con la lógica del blog
    ├── __init__.py
    ├── modelos.py        # Clases Autor, Post y Blog
    ├── datos.py          # Carga y guardado de posts.json (persistencia)
    ├── menu.py           # Menú y todos los input()
    ├── operaciones.py    # Muestra en consola los resultados del Blog
    └── validaciones.py   # Reglas que debe cumplir un post
```

## Clases principales (`blog/modelos.py`)

| Clase | Qué representa | Atributos | Métodos principales |
|---|---|---|---|
| `Autor` | La persona que escribe | `nombre`, `bio`, `especialidad`, `redes_sociales` | `a_dict()`, `Autor.desde_dict(datos)` |
| `Post` | Una publicación | `id`, `titulo`, `contenido`, `autor` (**objeto `Autor`**), `tags`, `estado`, `categoria` | `coincide_con_titulo()`, `tiene_tag()`, `validar()`, `a_dict()`, `Post.desde_dict(datos)` |
| `Blog` | El blog completo | `nombre`, `autor`, `posts` (**lista de objetos `Post`**), `hay_cambios` | `listar_posts()`, `buscar_por_titulo()`, `filtrar_por_tag()`, `crear_post()`, `validar_posts()`, `obtener_posts()`, `obtener_tags()` |

- **Composición:** cada `Post` tiene como autor un objeto `Autor`. Si se intenta crear un `Post` con el autor como texto (`"Lucas Cook"`), se lanza un `TypeError`.
- **`Blog` centraliza la lógica:** el menú no recorre listas ni compara textos. Le pide todo al objeto `blog` (`blog.buscar_por_titulo("python")`, `blog.crear_post(...)`, etc.).
- La búsqueda y el filtro no distinguen mayúsculas porque comparan con `.lower()`.

## Cómo interactúan las clases con `posts.json`

JSON no puede guardar objetos de Python, así que los datos se convierten en los dos sentidos:

```
GUARDAR (opción 6)                                   CARGAR (al iniciar)

objetos Post ──a_dict()──> diccionarios              posts.json ──json.loads──> diccionarios
 (con su Autor  (el Autor también se                                              │
  adentro)       convierte con a_dict())             Post.desde_dict() <──────────┘
                     │                                 (reconstruye también el objeto Autor)
              json.dumps ──> posts.json                      │
                                                             ▼
                                                     Blog(posts=[objetos Post])
```

- **Al iniciar**, `main.py` llama a `cargar_posts()` (de `blog/datos.py`), que lee `posts.json` y convierte cada diccionario en un objeto `Post` con `Post.desde_dict()`. Con esos objetos se crea la instancia de `Blog`.
- **Al guardar** (opción 6, o al salir si hay cambios), `guardar_posts()` convierte cada `Post` con `a_dict()` y escribe la lista en `posts.json` con `json.dumps`.
- **Un post nuevo** (opción 4) se crea como objeto `Post` con `blog.crear_post()` y queda en memoria. Al guardar se escribe en `posts.json`, y la próxima vez que abras el programa se vuelve a cargar.

## Opciones del menú

```
--- MENU DEL BLOG ---
1. Ver todos los posts      -> blog.listar_posts(): título, autor y estado
2. Buscar por titulo        -> blog.buscar_por_titulo(termino)
3. Filtrar por tag          -> blog.filtrar_por_tag(tag)
4. Crear nuevo post         -> pide los datos y llama a blog.crear_post(...)
5. Validar posts            -> blog.validar_posts()
6. Guardar posts en JSON    -> guardar_posts(blog.obtener_posts())
7. Salir                    -> si hay cambios sin guardar, pregunta si guardarlos
```

## Manejo de errores

| Situación | Qué hace el programa |
|---|---|
| `posts.json` no existe | Lo crea con los posts de ejemplo y los carga. |
| `posts.json` está vacío | Avisa y arranca con el blog vacío. |
| `posts.json` tiene JSON inválido o no es una lista | Avisa (indica línea y columna del error) y arranca con el blog vacío. |
| Un post del JSON está incompleto (falta una clave o el autor no tiene nombre) | `Post.desde_dict()` lanza `ValueError`; ese post se informa con un aviso y se saltea, y el resto se carga normalmente. |
| Opción del menú inválida (texto o número fuera de rango) | Avisa y vuelve a mostrar el menú. |
| Campos vacíos al crear un post | El título y el contenido se vuelven a pedir hasta que no queden vacíos. Un estado inválido también se vuelve a pedir. |
| Intentar guardar algo que no es un `Post` o que JSON no soporta | No se escribe nada (el archivo no queda a medias) y se muestra el motivo. |

## Datos de prueba

`posts.json` arranca con los mismos posts de los módulos anteriores, incluidos 3 con errores a propósito:

- **Post 7:** le falta `contenido`. No se puede reconstruir como objeto y al cargar aparece un aviso. Como no se carga, no se vuelve a guardar.
- **Post 8:** título vacío. Se carga, pero la opción 5 lo marca como error.
- **Post 9:** tags guardados como texto y estado `pendiente`. Se carga, pero la opción 5 lo marca como error.

## Qué cambió respecto a la preentrega 5

| Antes (preentrega 5) | Ahora (preentrega 6) |
|---|---|
| Los posts eran diccionarios en `datos.py` | Los posts son objetos `Post` y se guardan en `posts.json` |
| El autor era el diccionario `perfil_autor` | El autor es un objeto `Autor` (`perfil_autor` queda solo como dato inicial) |
| Funciones sueltas `listar_posts`, `buscar_por_titulo`, `filtrar_por_tag` en `operaciones.py` | Métodos de la clase `Blog`. `operaciones.py` solo muestra los resultados |
| `validar_post(post)` recibía un diccionario | `Post.validar()` usa `validar_post()` sobre el objeto |
| `estados_post` y `etiquetas_blog` en `datos.py` | `Post.ESTADOS_VALIDOS` y `blog.obtener_tags()`, que calcula los tags a partir de los posts |
| Menú de 5 opciones | Menú de 7 opciones: se agregan **Crear nuevo post** y **Guardar posts en JSON** |
| Los datos se perdían al cerrar | Se guardan en `posts.json` y se cargan al iniciar |

Los imports siguen sin ciclos: `main → datos → modelos → validaciones`, y además `main → menu` y `main → operaciones`.

## Autor

Lucas Cook
