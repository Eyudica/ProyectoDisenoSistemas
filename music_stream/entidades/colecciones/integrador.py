"""
Archivo integrador generado automaticamente
Directorio: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/colecciones
Fecha: 2025-11-04 20:22:42
Total de archivos integrados: 3
"""

# ================================================================================
# ARCHIVO 1/3: biblioteca.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/colecciones/biblioteca.py
# ================================================================================

from typing import List
from music_stream.entidades.usuario import Usuario
from music_stream.entidades.colecciones.playlist import Playlist
from music_stream.entidades.album import Album
from music_stream.entidades.artista import Artista
from music_stream.entidades.cancion import Cancion

class Biblioteca:
    def __init__(self, usuario: Usuario):
        self.usuario = usuario
        self.playlists_creadas: List[Playlist] = []
        self.playlists_seguidas: List[Playlist] = []
        self.albumes_guardados: List[Album] = []
        self.artistas_seguidos: List[Artista] = []
        self.canciones_favoritas: List[Cancion] = []
        # El historial de reproducción se manejará directamente en el Perfil
        # para mantener la cohesión con la US-003

    def agregar_playlist(self, playlist: Playlist):
        self.playlists_creadas.append(playlist)

    def seguir_playlist(self, playlist: Playlist):
        self.playlists_seguidas.append(playlist)

    def guardar_album(self, album: Album):
        self.albumes_guardados.append(album)

    def seguir_artista(self, artista: Artista):
        self.artistas_seguidos.append(artista)

    def agregar_a_favoritos(self, cancion: Cancion):
        if cancion not in self.canciones_favoritas:
            self.canciones_favoritas.append(cancion)

    def quitar_de_favoritos(self, cancion: Cancion):
        self.canciones_favoritas.remove(cancion)

    def __str__(self):
        return f"Biblioteca de {self.usuario.username}"


# ================================================================================
# ARCHIVO 2/3: favoritos.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/colecciones/favoritos.py
# ================================================================================

from music_stream.entidades.usuario import Usuario
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.colecciones.playlist import Playlist

class Favoritos(Playlist):
    def __init__(self, usuario_creador: Usuario):
        super().__init__(
            nombre="Canciones Favoritas",
            usuario_creador=usuario_creador,
            descripcion="Tus canciones favoritas en un solo lugar",
            publica=False
        )

    def agregar(self, cancion: Cancion):
        """Agrega una canción a favoritos si no está ya."""
        if not self.contiene(cancion):
            self.agregar_cancion(cancion)
            print(f"❤️ '{cancion.titulo}' agregada a tus favoritos.")

    def quitar(self, cancion: Cancion):
        """Quita una canción de favoritos."""
        self.remover_cancion(cancion)
        print(f"💔 '{cancion.titulo}' quitada de tus favoritos.")

    def contiene(self, cancion: Cancion) -> bool:
        """Verifica si una canción está en favoritos."""
        return cancion in self.canciones


# ================================================================================
# ARCHIVO 3/3: playlist.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/colecciones/playlist.py
# ================================================================================

from datetime import datetime
from typing import List
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.usuario import Usuario

class Playlist:
    def __init__(self, nombre: str, usuario_creador: Usuario, descripcion: str = "", publica: bool = False):
        self.nombre = nombre
        self.usuario_creador = usuario_creador
        self.descripcion = descripcion
        self.publica = publica
        self.canciones: List[Cancion] = []
        self.fecha_creacion = datetime.now()

    @property
    def duracion_total(self) -> int:
        """Calcula la duración total de la playlist en segundos."""
        return sum(cancion.duracion for cancion in self.canciones)

    def agregar_cancion(self, cancion: Cancion):
        """Agrega una canción a la playlist."""
        self.canciones.append(cancion)

    def remover_cancion(self, cancion: Cancion):
        """Remueve una canción de la playlist."""
        if cancion in self.canciones:
            self.canciones.remove(cancion)

    def __str__(self):
        return f"Playlist: {self.nombre} (Creador: {self.usuario_creador.username}, Canciones: {len(self.canciones)})"


