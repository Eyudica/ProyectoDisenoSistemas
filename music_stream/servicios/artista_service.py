from music_stream.entidades.artista import Artista
from music_stream.entidades.exceptions import ArtistaExistenteException

class ArtistaService:
    def __init__(self):
        self.artistas = {}

    def crear_artista(self, nombre, genero, pais, biografia, verificado):
        if nombre in self.artistas:
            raise ArtistaExistenteException(f"El artista {nombre} ya existe")

        artista = Artista(nombre, genero, pais, biografia, verificado)
        self.artistas[nombre] = artista
        return artista

    def obtener_artista(self, nombre):
        return self.artistas.get(nombre)

    def mostrar_artista(self, nombre):
        artista = self.obtener_artista(nombre)
        if artista:
            print(artista)
        else:
            print(f"Artista no encontrado: {nombre}")
