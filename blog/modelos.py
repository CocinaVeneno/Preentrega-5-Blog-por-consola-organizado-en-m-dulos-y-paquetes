"""Clases del blog: Autor, Post y Blog."""

from blog.validaciones import claves_faltantes, validar_post


class Autor:
    """Persona que escribe en el blog."""

    def __init__(self, nombre, bio="", especialidad="", redes_sociales=None):
        self.nombre = nombre
        self.bio = bio
        self.especialidad = especialidad
        self.redes_sociales = redes_sociales if redes_sociales is not None else {}

    def a_dict(self):
        """Convierte el autor en un diccionario que se puede guardar en JSON."""
        return {
            "nombre": self.nombre,
            "bio": self.bio,
            "especialidad": self.especialidad,
            "redes_sociales": self.redes_sociales,
        }

    @classmethod
    def desde_dict(cls, datos):
        """Crea un Autor a partir de un diccionario. Lanza ValueError si los datos no alcanzan."""
        if not isinstance(datos, dict):
            raise ValueError("el autor tiene que ser un diccionario")
        if "nombre" not in datos:
            raise ValueError("al autor le falta la clave 'nombre'")
        return cls(
            nombre=datos["nombre"],
            bio=datos.get("bio", ""),
            especialidad=datos.get("especialidad", ""),
            redes_sociales=datos.get("redes_sociales", {}),
        )

    def __str__(self):
        return self.nombre


class Post:
    """Publicación del blog. Su autor es un objeto Autor (composición)."""

    ESTADOS_VALIDOS = ("borrador", "publicado", "archivado")
    CLAVES_OBLIGATORIAS = ("id", "titulo", "contenido", "autor", "tags", "estado")

    def __init__(self, id_post, titulo, contenido, autor, tags=None, estado="borrador", categoria=""):
        if not isinstance(autor, Autor):
            raise TypeError("el autor de un post tiene que ser un objeto Autor, no un texto")
        self.id = id_post
        self.titulo = titulo
        self.contenido = contenido
        self.autor = autor
        self.tags = tags if tags is not None else []
        self.estado = estado
        self.categoria = categoria

    def coincide_con_titulo(self, termino):
        """True si el término aparece en el título, sin importar mayúsculas."""
        return termino.lower() in str(self.titulo).lower()

    def tiene_tag(self, tag):
        """True si el post tiene ese tag, sin importar mayúsculas."""
        if not isinstance(self.tags, list):
            return False
        return tag.lower() in [str(t).lower() for t in self.tags]

    def validar(self):
        """Retorna (True, "válido") o (False, mensaje) según las reglas de validaciones.py."""
        return validar_post(self, self.ESTADOS_VALIDOS)

    def a_dict(self):
        """Convierte el post (y su autor) en un diccionario que se puede guardar en JSON."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "autor": self.autor.a_dict(),
            "categoria": self.categoria,
            "tags": list(self.tags) if isinstance(self.tags, list) else self.tags,
            "estado": self.estado,
        }

    @classmethod
    def desde_dict(cls, datos):
        """Reconstruye un Post (y su Autor) desde un diccionario. Lanza ValueError si está incompleto."""
        if not isinstance(datos, dict):
            raise ValueError("el post no es un diccionario")

        faltantes = claves_faltantes(datos, cls.CLAVES_OBLIGATORIAS)
        if faltantes:
            raise ValueError(f"le faltan las claves: {', '.join(faltantes)}")

        return cls(
            id_post=datos["id"],
            titulo=datos["titulo"],
            contenido=datos["contenido"],
            autor=Autor.desde_dict(datos["autor"]),
            tags=datos["tags"],
            estado=datos["estado"],
            categoria=datos.get("categoria", ""),
        )

    def __str__(self):
        titulo = str(self.titulo).strip() or "(sin título)"
        return f"{titulo} | Autor: {self.autor.nombre} | Estado: {self.estado}"


class Blog:
    """El blog completo: tiene un autor principal y una lista de objetos Post."""

    def __init__(self, nombre, autor, posts=None):
        self.nombre = nombre
        self.autor = autor
        self.posts = list(posts) if posts else []
        self.hay_cambios = False

    def __len__(self):
        return len(self.posts)

    def obtener_posts(self):
        """Retorna una copia de la lista de posts cargados."""
        return list(self.posts)

    def listar_posts(self):
        """Retorna una línea de texto por post: título, autor y estado."""
        return [str(post) for post in self.posts]

    def buscar_por_titulo(self, termino):
        """Retorna los posts cuyo título contiene el término (coincidencia total o parcial)."""
        termino = termino.strip()
        if not termino:
            return []
        return [post for post in self.posts if post.coincide_con_titulo(termino)]

    def filtrar_por_tag(self, tag):
        """Retorna los posts que tienen ese tag."""
        tag = tag.strip()
        if not tag:
            return []
        return [post for post in self.posts if post.tiene_tag(tag)]

    def obtener_tags(self):
        """Retorna los tags usados en el blog, sin repetir (ni por mayúsculas) y ordenados."""
        tags = {}
        for post in self.posts:
            if isinstance(post.tags, list):
                for tag in post.tags:
                    # La clave en minúsculas evita que "Backend" y "backend" aparezcan dos veces
                    tags.setdefault(str(tag).lower(), str(tag))
        return sorted(tags.values(), key=str.lower)

    def siguiente_id(self):
        """Retorna el próximo id libre."""
        ids = [post.id for post in self.posts if isinstance(post.id, int)]
        return max(ids, default=0) + 1

    def crear_post(self, titulo, contenido, tags=None, estado="borrador", autor=None):
        """Crea un Post, lo agrega al blog y lo retorna. Lanza ValueError si faltan datos."""
        titulo = titulo.strip()
        contenido = contenido.strip()
        if not titulo or not contenido:
            raise ValueError("el título y el contenido no pueden quedar vacíos")
        if estado not in Post.ESTADOS_VALIDOS:
            raise ValueError(f"el estado '{estado}' no es válido")

        post = Post(self.siguiente_id(), titulo, contenido, autor or self.autor, tags or [], estado)
        self.posts.append(post)
        self.hay_cambios = True
        return post

    def validar_posts(self):
        """Valida cada post. Retorna una lista de tuplas (post, es_valido, mensaje)."""
        resultados = []
        for post in self.posts:
            es_valido, mensaje = post.validar()
            resultados.append((post, es_valido, mensaje))
        return resultados

    def marcar_guardado(self):
        """Indica que los cambios ya se guardaron en posts.json."""
        self.hay_cambios = False
