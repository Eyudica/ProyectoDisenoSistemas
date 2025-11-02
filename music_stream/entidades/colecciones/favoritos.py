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
