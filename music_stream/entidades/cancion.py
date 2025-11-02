class Cancion:
    def __init__(self, titulo, artista, album, duracion, genero, archivo_audio):
        self.titulo = titulo
        self.artista = artista
        self.album = album
        self.duracion = duracion
        self.genero = genero
        self.archivo_audio = archivo_audio
        self.reproducciones = 0

    def incrementar_reproducciones(self):
        self.reproducciones += 1

    def __str__(self):
        return f"Canción: {self.titulo}, Artista: {self.artista.nombre}, Álbum: {self.album.titulo}, Duración: {self.duracion}s, Género: {self.genero}, Reproducciones: {self.reproducciones}"
