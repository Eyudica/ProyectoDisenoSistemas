class Artista:
    def __init__(self, nombre, genero, pais, biografia, verificado):
        self.nombre = nombre
        self.genero = genero
        self.pais = pais
        self.biografia = biografia
        self.verificado = verificado

    def __str__(self):
        return f"Artista: {self.nombre}, Género: {self.genero}, País: {self.pais}, Verificado: {self.verificado}"
