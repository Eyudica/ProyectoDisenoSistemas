from typing import List
import random
from music_stream.entidades.cancion import Cancion

class ColaReproduccion:
    def __init__(self):
        self._canciones: List[Cancion] = []
        self._indice_actual: int = -1
        self._modo_aleatorio: bool = False
        self._modo_repetir: str = "ninguno"  # "ninguno", "uno", "todos"

    def agregar_cancion(self, cancion: Cancion):
        self._canciones.append(cancion)
        if self._indice_actual == -1:
            self._indice_actual = 0

    def insertar_cancion(self, cancion: Cancion, posicion: int):
        self._canciones.insert(posicion, cancion)

    def eliminar_cancion(self, posicion: int):
        del self._canciones[posicion]

    def limpiar(self):
        self._canciones = []
        self._indice_actual = -1

    def get_actual(self) -> Cancion | None:
        if 0 <= self._indice_actual < len(self._canciones):
            return self._canciones[self._indice_actual]
        return None

    def siguiente(self) -> Cancion | None:
        if not self._canciones:
            return None

        if self._modo_repetir == "uno":
            return self.get_actual()

        if self._modo_aleatorio:
            self._indice_actual = random.randint(0, len(self._canciones) - 1)
            return self.get_actual()

        if self._indice_actual < len(self._canciones) - 1:
            self._indice_actual += 1
        elif self._modo_repetir == "todos":
            self._indice_actual = 0
        else:
            return None # Fin de la cola

        return self.get_actual()

    def anterior(self) -> Cancion | None:
        if not self._canciones or self._indice_actual <= 0:
            return None
        
        self._indice_actual -= 1
        return self.get_actual()

    def set_modo_aleatorio(self, activado: bool):
        self._modo_aleatorio = activado

    def set_modo_repetir(self, modo: str):
        if modo not in ["ninguno", "uno", "todos"]:
            raise ValueError("Modo de repetición no válido")
        self._modo_repetir = modo
