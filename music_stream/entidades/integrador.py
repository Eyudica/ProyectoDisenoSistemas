"""
Archivo integrador generado automaticamente
Directorio: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades
Fecha: 2025-11-04 20:22:42
Total de archivos integrados: 9
"""

# ================================================================================
# ARCHIVO 1/9: album.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/album.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 2/9: artista.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/artista.py
# ================================================================================

class Artista:
    def __init__(self, nombre, genero, pais, biografia, verificado):
        self.nombre = nombre
        self.genero = genero
        self.pais = pais
        self.biografia = biografia
        self.verificado = verificado

    def __str__(self):
        return f"Artista: {self.nombre}, Género: {self.genero}, País: {self.pais}, Verificado: {self.verificado}"


# ================================================================================
# ARCHIVO 3/9: cancion.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/cancion.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/9: cola_reproduccion.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/cola_reproduccion.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 5/9: exceptions.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/exceptions.py
# ================================================================================

class UsuarioExistenteException(Exception):
    pass

class ArtistaExistenteException(Exception):
    pass

class ArchivoNoEncontradoException(Exception):
    pass

class LimiteSkipsException(Exception):
    pass

class DescargaNoPermitidaException(Exception):
    pass

class PersistenciaException(Exception):
    pass


# ================================================================================
# ARCHIVO 6/9: perfil.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/perfil.py
# ================================================================================

from datetime import datetime

class Perfil:
    def __init__(self, usuario, plan, biblioteca, historial):
        self.usuario = usuario
        self.plan = plan
        self.biblioteca = biblioteca
        self.historial = historial
        self.estadisticas = {
            "canciones_escuchadas": 0,
            "tiempo_total": 0
        }

    def mostrar(self):
        print("PERFIL DE USUARIO")
        print("=================")
        print(f"Username: {self.usuario.username}")
        print(f"Email: {self.usuario.email}")
        print(f"Plan: {self.plan.tipo} (${self.plan.precio}/mes)")
        print(f"Calidad: {self.plan.calidad_audio}")
        print(f"País: {self.usuario.pais}")
        print(f"Canciones escuchadas: {self.estadisticas['canciones_escuchadas']}")
        print(f"Tiempo total: {self.estadisticas['tiempo_total']} minutos")
        print(f"Playlists: {len(self.biblioteca.playlists)}")
        print(f"Favoritos: {len(self.biblioteca.favoritos)}")


# ================================================================================
# ARCHIVO 7/9: plan.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/plan.py
# ================================================================================

from abc import ABC, abstractmethod

class Plan(ABC):
    @property
    @abstractmethod
    def tipo(self) -> str:
        pass

    @property
    @abstractmethod
    def precio(self) -> float:
        pass

    @property
    @abstractmethod
    def calidad_audio(self) -> str:
        pass

    @property
    @abstractmethod
    def puede_descargar(self) -> bool:
        pass

    @property
    @abstractmethod
    def tiene_anuncios(self) -> bool:
        pass

    @property
    @abstractmethod
    def tiene_saltos_ilimitados(self) -> bool:
        pass

    def __str__(self):
        return f"Plan: {self.tipo}, Precio: ${self.precio}, Calidad: {self.calidad_audio}, Descargas: {self.puede_descargar}, Anuncios: {self.tiene_anuncios}"

class PlanFree(Plan):
    @property
    def tipo(self) -> str:
        return "Free"

    @property
    def precio(self) -> float:
        return 0

    @property
    def calidad_audio(self) -> str:
        return "128kbps"

    @property
    def puede_descargar(self) -> bool:
        return False

    @property
    def tiene_anuncios(self) -> bool:
        return True

    @property
    def tiene_saltos_ilimitados(self) -> bool:
        return False

class PlanPremium(Plan):
    @property
    def tipo(self) -> str:
        return "Premium"

    @property
    def precio(self) -> float:
        return 999

    @property
    def calidad_audio(self) -> str:
        return "320kbps"

    @property
    def puede_descargar(self) -> bool:
        return True

    @property
    def tiene_anuncios(self) -> bool:
        return False

    @property
    def tiene_saltos_ilimitados(self) -> bool:
        return True

class PlanFamily(Plan):
    @property
    def tipo(self) -> str:
        return "Family"

    @property
    def precio(self) -> float:
        return 1499

    @property
    def calidad_audio(self) -> str:
        return "Lossless"

    @property
    def puede_descargar(self) -> bool:
        return True

    @property
    def tiene_anuncios(self) -> bool:
        return False

    @property
    def tiene_saltos_ilimitados(self) -> bool:
        return True

    @property
    def max_usuarios(self) -> int:
        return 6

# ================================================================================
# ARCHIVO 8/9: reproductor.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/reproductor.py
# ================================================================================

from __future__ import annotations
from music_stream.entidades.usuario import Usuario
from music_stream.entidades.cola_reproduccion import ColaReproduccion
from music_stream.patrones.state.estado_reproductor import EstadoReproductor, EstadoDetenido, EstadoReproduciendo, EstadoPausado
from music_stream.patrones.observer.observer import Observable
from music_stream.patrones.strategy.restriccion_strategy import RestriccionFreeStrategy, RestriccionPremiumStrategy

class Reproductor(Observable):
    def __init__(self, usuario: Usuario, cola: ColaReproduccion):
        super().__init__()
        self.usuario = usuario
        self.cola = cola
        self._estado_actual: EstadoReproductor = EstadoDetenido()
        self.cancion_actual = self.cola.get_actual()
        
        self._restriccion_strategies = {
            "Free": RestriccionFreeStrategy(),
            "Premium": RestriccionPremiumStrategy(),
            "Family": RestriccionPremiumStrategy() # Family tiene las mismas (o menos) restricciones que Premium
        }
        self._restriccion_strategy = self._restriccion_strategies.get(self.usuario.plan.tipo)

    def set_estado(self, estado: EstadoReproductor):
        self._estado_actual = estado

    def play(self):
        if not self.cancion_actual:
            print("No hay ninguna canción cargada.")
            return
        self._estado_actual.handle_play(self)
        if isinstance(self._estado_actual, EstadoReproduciendo):
            self.notificar_observadores({"tipo": "REPRODUCCION_INICIADA", "cancion": self.cancion_actual})

    def pause(self):
        self._estado_actual.handle_pause(self)
        if isinstance(self._estado_actual, EstadoPausado):
            self.notificar_observadores({"tipo": "REPRODUCCION_PAUSADA", "cancion": self.cancion_actual})

    def stop(self):
        self._estado_actual.handle_stop(self)
        if isinstance(self._estado_actual, EstadoDetenido):
            self.notificar_observadores({"tipo": "REPRODUCCION_DETENIDA", "cancion": self.cancion_actual})

    def siguiente(self):
        if self._restriccion_strategy.puede_saltar(self.usuario):
            print("Saltando a la siguiente canción...")
            self.cancion_actual = self.cola.siguiente()
            self.notificar_observadores({"tipo": "CAMBIO_DE_CANCION", "cancion": self.cancion_actual})
            self.play()

    def anterior(self):
        # Asumimos que retroceder también cuenta como un salto para simplificar
        if self._restriccion_strategy.puede_saltar(self.usuario):
            print("Volviendo a la canción anterior...")
            self.cancion_actual = self.cola.anterior()
            self.notificar_observadores({"tipo": "CAMBIO_DE_CANCION", "cancion": self.cancion_actual})
            self.play()


# ================================================================================
# ARCHIVO 9/9: usuario.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/usuario.py
# ================================================================================

from datetime import datetime

class Usuario:
    def __init__(self, username, email, plan, pais):
        self.username = username
        self.email = email
        self.plan = plan
        self.pais = pais
        self.fecha_registro = datetime.now()
        self.perfil = None

    def set_username(self, new_username):
        self.username = new_username

    def __str__(self):
        return f"Usuario: {self.username}, Email: {self.email}, Plan: {self.plan}, País: {self.pais}"


