"""
Archivo integrador generado automaticamente
Directorio: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/observer
Fecha: 2025-11-04 20:22:42
Total de archivos integrados: 1
"""

# ================================================================================
# ARCHIVO 1/1: observer.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/observer/observer.py
# ================================================================================

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


