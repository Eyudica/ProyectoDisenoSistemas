from abc import ABC, abstractmethod
import os

class CalidadAudioStrategy(ABC):
    @abstractmethod
    def obtener_archivo(self, archivo_base: str) -> str:
        pass

class CalidadBajaStrategy(CalidadAudioStrategy):
    def obtener_archivo(self, archivo_base: str) -> str:
        directorio, nombre_archivo = os.path.split(archivo_base)
        nombre, extension = os.path.splitext(nombre_archivo)
        return os.path.join(directorio, f"{nombre}_128kbps.mp3")

class CalidadAltaStrategy(CalidadAudioStrategy):
    def obtener_archivo(self, archivo_base: str) -> str:
        directorio, nombre_archivo = os.path.split(archivo_base)
        nombre, extension = os.path.splitext(nombre_archivo)
        return os.path.join(directorio, f"{nombre}_320kbps.mp3")

class CalidadLosslessStrategy(CalidadAudioStrategy):
    def obtener_archivo(self, archivo_base: str) -> str:
        directorio, nombre_archivo = os.path.split(archivo_base)
        nombre, extension = os.path.splitext(nombre_archivo)
        return os.path.join(directorio, f"{nombre}.flac")
