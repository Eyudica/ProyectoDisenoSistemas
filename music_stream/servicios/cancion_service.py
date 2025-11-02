import os
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.exceptions import ArchivoNoEncontradoException

class CancionService:
    def __init__(self):
        self.canciones = {}

    def crear_cancion(self, titulo, artista, album, duracion, genero, archivo_audio):
        if not os.path.exists(archivo_audio):
            raise ArchivoNoEncontradoException(f"El archivo de audio no se encuentra en la ruta: {archivo_audio}")

        cancion = Cancion(
            titulo=titulo,
            artista=artista,
            album=album,
            duracion=duracion,
            genero=genero,
            archivo_audio=archivo_audio
        )
        
        album.agregar_cancion(cancion)
        self.canciones[cancion.titulo] = cancion
        return cancion
