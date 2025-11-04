from threading import Lock
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.album import Album
from music_stream.entidades.artista import Artista
from music_stream.entidades.colecciones.playlist import Playlist

class ContenidoServiceRegistry:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._inicializar_handlers()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls() # Llama a __new__ para crear la instancia
        return cls._instance

    def _inicializar_handlers(self):
        self._mostrar_datos_handlers = {
            Cancion: self._mostrar_datos_cancion,
            Album: self._mostrar_datos_album,
            Artista: self._mostrar_datos_artista,
            Playlist: self._mostrar_datos_playlist
        }
        # Los handlers de reproducción se pueden registrar aquí también
        self._reproducir_handlers = {}

    def registrar_mostrar_datos_handler(self, tipo, handler):
        self._mostrar_datos_handlers[tipo] = handler

    def mostrar_datos(self, contenido):
        handler = self._mostrar_datos_handlers.get(type(contenido))
        if handler:
            handler(contenido)
        else:
            print(f"No se encontró un handler de visualización para el tipo {type(contenido).__name__}")

    # --- Handlers de Visualización ---

    def _mostrar_datos_cancion(self, cancion: Cancion):
        duracion_min = cancion.duracion // 60
        duracion_sec = cancion.duracion % 60
        print("--- Canción ---")
        print(f"Título:         {cancion.titulo}")
        print(f"Artista:        {cancion.artista.nombre}")
        print(f"Álbum:          {cancion.album.titulo}")
        print(f"Duración:       {duracion_min}:{duracion_sec:02d}")
        print(f"Género:         {cancion.genero}")
        print(f"Reproducciones: {cancion.reproducciones:,}")
        print()

    def _mostrar_datos_album(self, album: Album):
        duracion_total_min = album.get_duracion_total() // 60
        duracion_total_sec = album.get_duracion_total() % 60
        print("--- Álbum ---")
        print(f"Título:         {album.titulo}")
        print(f"Artista:        {album.artista.nombre}")
        print(f"Lanzamiento:    {album.fecha_lanzamiento}")
        print(f"Canciones:      {len(album.canciones)}")
        print(f"Duración Total: {duracion_total_min}:{duracion_total_sec:02d}")
        for i, cancion in enumerate(album.canciones):
            print(f"  {i+1}. {cancion.titulo}")
        print()

    def _mostrar_datos_artista(self, artista: Artista):
        print("--- Artista ---")
        print(f"Nombre:         {artista.nombre}")
        print(f"Género:         {artista.genero}")
        print(f"País:           {artista.pais}")
        print(f"Verificado:     {'Sí' if artista.verificado else 'No'}")
        print()

    def _mostrar_datos_playlist(self, playlist: Playlist):
        duracion_total_min = playlist.duracion_total // 60
        duracion_total_sec = playlist.duracion_total % 60
        print("--- Playlist ---")
        print(f"Nombre:         {playlist.nombre}")
        print(f"Creador:        {playlist.usuario_creador.username}")
        print(f"Descripción:    {playlist.descripcion}")
        print(f"Canciones:      {len(playlist.canciones)}")
        print(f"Duración Total: {duracion_total_min}:{duracion_total_sec:02d}")
        for i, cancion in enumerate(playlist.canciones):
            print(f"  {i+1}. {cancion.titulo} - {cancion.artista.nombre}")
        print()