from music_stream.entidades.colecciones.playlist import Playlist
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.usuario import Usuario
from music_stream.patrones.contenido_service_registry import ContenidoServiceRegistry

class PlaylistService:
    def crear_playlist(self, nombre: str, usuario: Usuario, descripcion: str = "", publica: bool = False) -> Playlist:
        """Crea una nueva playlist y la agrega a la biblioteca del usuario."""
        if not hasattr(usuario, 'perfil') or not usuario.perfil:
            raise Exception("El usuario no tiene un perfil y biblioteca asociados.")
        
        playlist = Playlist(nombre, usuario, descripcion, publica)
        usuario.perfil.biblioteca.agregar_playlist(playlist)
        print(f"Playlist '{nombre}' creada para el usuario {usuario.username}.")
        return playlist

    def agregar_cancion(self, playlist: Playlist, cancion: Cancion):
        """Agrega una canción a una playlist existente."""
        playlist.agregar_cancion(cancion)
        print(f"'{cancion.titulo}' agregada a la playlist '{playlist.nombre}'.")

    def mostrar_playlist(self, playlist: Playlist):
        """Muestra los detalles de una playlist usando el Registry."""
        registry = ContenidoServiceRegistry.get_instance()
        registry.mostrar_datos(playlist)
