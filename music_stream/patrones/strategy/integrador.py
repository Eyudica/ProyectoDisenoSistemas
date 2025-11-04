"""
Archivo integrador generado automaticamente
Directorio: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/strategy
Fecha: 2025-11-04 20:22:42
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: calidad_audio_strategy.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/strategy/calidad_audio_strategy.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 2/2: restriccion_strategy.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/strategy/restriccion_strategy.py
# ================================================================================

from abc import ABC, abstractmethod
from music_stream.entidades.usuario import Usuario
from music_stream.entidades.exceptions import LimiteSkipsException, DescargaNoPermitidaException

class RestriccionStrategy(ABC):
    @abstractmethod
    def puede_saltar(self, usuario: Usuario):
        pass

    @abstractmethod
    def puede_descargar(self, usuario: Usuario):
        pass

class RestriccionPremiumStrategy(RestriccionStrategy):
    def puede_saltar(self, usuario: Usuario):
        # Siempre permitido en Premium
        return True

    def puede_descargar(self, usuario: Usuario):
        # Siempre permitido en Premium
        return True

class RestriccionFreeStrategy(RestriccionStrategy):
    def __init__(self, max_saltos=6):
        self.max_saltos = max_saltos
        # En una app real, el contador de saltos y su timestamp se persistirían
        self.contador_saltos = 0

    def puede_saltar(self, usuario: Usuario):
        if self.contador_saltos >= self.max_saltos:
            raise LimiteSkipsException(f"Has alcanzado el límite de {self.max_saltos} saltos por hora.")
        self.contador_saltos += 1
        print(f"[Restricción] Salto {self.contador_saltos}/{self.max_saltos} utilizado.")
        return True

    def puede_descargar(self, usuario: Usuario):
        raise DescargaNoPermitidaException("Las descargas no están permitidas en el plan Free.")


