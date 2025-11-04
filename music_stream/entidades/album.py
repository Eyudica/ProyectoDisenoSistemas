from datetime import date

class Album:
    def __init__(self, titulo, artista, fecha_lanzamiento, genero):
        self.titulo = titulo
        self.artista = artista
        self._fecha_lanzamiento = fecha_lanzamiento
        self.genero = genero
        self.canciones = []

    @property
    def fecha_lanzamiento(self):
        return self._fecha_lanzamiento

    @fecha_lanzamiento.setter
    def fecha_lanzamiento(self, fecha):
        if fecha > date.today():
            raise ValueError("La fecha no puede ser futura")
        self._fecha_lanzamiento = fecha

    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)

    def get_duracion_total(self):
        return sum(cancion.duracion for cancion in self.canciones)

    def __str__(self):
        return f"Álbum: {self.titulo}, Artista: {self.artista.nombre}, Género: {self.genero}, Canciones: {len(self.canciones)}"
