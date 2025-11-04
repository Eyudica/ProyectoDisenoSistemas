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
