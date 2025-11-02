from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Observer(ABC):
    @abstractmethod
    def actualizar(self, evento: Dict[str, Any]):
        pass

class Observable:
    def __init__(self):
        self._observadores: List[Observer] = []

    def agregar_observador(self, observador: Observer):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar_observador(self, observador: Observer):
        self._observadores.remove(observador)

    def notificar_observadores(self, evento: Dict[str, Any]):
        for observador in self._observadores:
            observador.actualizar(evento)
