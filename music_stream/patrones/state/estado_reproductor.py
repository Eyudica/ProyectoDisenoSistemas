from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from music_stream.entidades.reproductor import Reproductor

class EstadoReproductor(ABC):
    @abstractmethod
    def handle_play(self, reproductor: Reproductor):
        pass

    @abstractmethod
    def handle_pause(self, reproductor: Reproductor):
        pass

    @abstractmethod
    def handle_stop(self, reproductor: Reproductor):
        pass

class EstadoDetenido(EstadoReproductor):
    def handle_play(self, reproductor: Reproductor):
        print("Iniciando reproducción.")
        reproductor.set_estado(EstadoReproduciendo())

    def handle_pause(self, reproductor: Reproductor):
        print("No se puede pausar. El reproductor está detenido.")

    def handle_stop(self, reproductor: Reproductor):
        print("El reproductor ya está detenido.")

class EstadoReproduciendo(EstadoReproductor):
    def handle_play(self, reproductor: Reproductor):
        print("El reproductor ya está en modo reproducción.")

    def handle_pause(self, reproductor: Reproductor):
        print("Reproducción pausada.")
        reproductor.set_estado(EstadoPausado())

    def handle_stop(self, reproductor: Reproductor):
        print("Reproducción detenida.")
        reproductor.set_estado(EstadoDetenido())

class EstadoPausado(EstadoReproductor):
    def handle_play(self, reproductor: Reproductor):
        print("Reanudando reproducción.")
        reproductor.set_estado(EstadoReproduciendo())

    def handle_pause(self, reproductor: Reproductor):
        print("El reproductor ya está pausado.")

    def handle_stop(self, reproductor: Reproductor):
        print("Reproducción detenida desde pausa.")
        reproductor.set_estado(EstadoDetenido())
