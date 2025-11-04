"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream
Fecha de generacion: 2025-11-04 20:22:42
Total de archivos integrados: 28
Total de directorios procesados: 8
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: entidades
#   1. album.py
#   2. artista.py
#   3. cancion.py
#   4. cola_reproduccion.py
#   5. exceptions.py
#   6. perfil.py
#   7. plan.py
#   8. reproductor.py
#   9. usuario.py
#
# DIRECTORIO: entidades/colecciones
#   10. biblioteca.py
#   11. favoritos.py
#   12. playlist.py
#
# DIRECTORIO: patrones
#   13. contenido_service_registry.py
#   14. plan_factory.py
#
# DIRECTORIO: patrones/observer
#   15. observer.py
#
# DIRECTORIO: patrones/state
#   16. estado_reproductor.py
#
# DIRECTORIO: patrones/strategy
#   17. calidad_audio_strategy.py
#   18. restriccion_strategy.py
#
# DIRECTORIO: servicios
#   19. artista_service.py
#   20. biblioteca_service.py
#   21. cache_service.py
#   22. cancion_service.py
#   23. observers.py
#   24. perfil_service.py
#   25. reproductor_service.py
#   26. suscripcion_service.py
#   27. usuario_service.py
#
# DIRECTORIO: servicios/colecciones
#   28. playlist_service.py
#



################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 1/28: album.py
# Directorio: entidades
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/album.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 2/28: artista.py
# Directorio: entidades
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/artista.py
# ==============================================================================

class Artista:
    def __init__(self, nombre, genero, pais, biografia, verificado):
        self.nombre = nombre
        self.genero = genero
        self.pais = pais
        self.biografia = biografia
        self.verificado = verificado

    def __str__(self):
        return f"Artista: {self.nombre}, Género: {self.genero}, País: {self.pais}, Verificado: {self.verificado}"


# ==============================================================================
# ARCHIVO 3/28: cancion.py
# Directorio: entidades
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/cancion.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 4/28: cola_reproduccion.py
# Directorio: entidades
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/cola_reproduccion.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 5/28: exceptions.py
# Directorio: entidades
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/exceptions.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 6/28: perfil.py
# Directorio: entidades
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/perfil.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 7/28: plan.py
# Directorio: entidades
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/plan.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 8/28: reproductor.py
# Directorio: entidades
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/reproductor.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 9/28: usuario.py
# Directorio: entidades
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/usuario.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: entidades/colecciones
################################################################################

# ==============================================================================
# ARCHIVO 10/28: biblioteca.py
# Directorio: entidades/colecciones
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/colecciones/biblioteca.py
# ==============================================================================

from typing import List
from music_stream.entidades.usuario import Usuario
from music_stream.entidades.colecciones.playlist import Playlist
from music_stream.entidades.album import Album
from music_stream.entidades.artista import Artista
from music_stream.entidades.cancion import Cancion

class Biblioteca:
    def __init__(self, usuario: Usuario):
        self.usuario = usuario
        self.playlists_creadas: List[Playlist] = []
        self.playlists_seguidas: List[Playlist] = []
        self.albumes_guardados: List[Album] = []
        self.artistas_seguidos: List[Artista] = []
        self.canciones_favoritas: List[Cancion] = []
        # El historial de reproducción se manejará directamente en el Perfil
        # para mantener la cohesión con la US-003

    def agregar_playlist(self, playlist: Playlist):
        self.playlists_creadas.append(playlist)

    def seguir_playlist(self, playlist: Playlist):
        self.playlists_seguidas.append(playlist)

    def guardar_album(self, album: Album):
        self.albumes_guardados.append(album)

    def seguir_artista(self, artista: Artista):
        self.artistas_seguidos.append(artista)

    def agregar_a_favoritos(self, cancion: Cancion):
        if cancion not in self.canciones_favoritas:
            self.canciones_favoritas.append(cancion)

    def quitar_de_favoritos(self, cancion: Cancion):
        self.canciones_favoritas.remove(cancion)

    def __str__(self):
        return f"Biblioteca de {self.usuario.username}"


# ==============================================================================
# ARCHIVO 11/28: favoritos.py
# Directorio: entidades/colecciones
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/colecciones/favoritos.py
# ==============================================================================

from music_stream.entidades.usuario import Usuario
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.colecciones.playlist import Playlist

class Favoritos(Playlist):
    def __init__(self, usuario_creador: Usuario):
        super().__init__(
            nombre="Canciones Favoritas",
            usuario_creador=usuario_creador,
            descripcion="Tus canciones favoritas en un solo lugar",
            publica=False
        )

    def agregar(self, cancion: Cancion):
        """Agrega una canción a favoritos si no está ya."""
        if not self.contiene(cancion):
            self.agregar_cancion(cancion)
            print(f"❤️ '{cancion.titulo}' agregada a tus favoritos.")

    def quitar(self, cancion: Cancion):
        """Quita una canción de favoritos."""
        self.remover_cancion(cancion)
        print(f"💔 '{cancion.titulo}' quitada de tus favoritos.")

    def contiene(self, cancion: Cancion) -> bool:
        """Verifica si una canción está en favoritos."""
        return cancion in self.canciones


# ==============================================================================
# ARCHIVO 12/28: playlist.py
# Directorio: entidades/colecciones
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/entidades/colecciones/playlist.py
# ==============================================================================

from datetime import datetime
from typing import List
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.usuario import Usuario

class Playlist:
    def __init__(self, nombre: str, usuario_creador: Usuario, descripcion: str = "", publica: bool = False):
        self.nombre = nombre
        self.usuario_creador = usuario_creador
        self.descripcion = descripcion
        self.publica = publica
        self.canciones: List[Cancion] = []
        self.fecha_creacion = datetime.now()

    @property
    def duracion_total(self) -> int:
        """Calcula la duración total de la playlist en segundos."""
        return sum(cancion.duracion for cancion in self.canciones)

    def agregar_cancion(self, cancion: Cancion):
        """Agrega una canción a la playlist."""
        self.canciones.append(cancion)

    def remover_cancion(self, cancion: Cancion):
        """Remueve una canción de la playlist."""
        if cancion in self.canciones:
            self.canciones.remove(cancion)

    def __str__(self):
        return f"Playlist: {self.nombre} (Creador: {self.usuario_creador.username}, Canciones: {len(self.canciones)})"



################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 13/28: contenido_service_registry.py
# Directorio: patrones
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/contenido_service_registry.py
# ==============================================================================

from threading import Lock
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.album import Album
from music_stream.entidades.artista import Artista
from music_stream.entidades.colecciones.playlist import Playlist

class ContenidoServiceRegistry:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._inicializar_handlers()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls() # Llama a __new__ para crear la instancia
        return cls._instance

    def _inicializar_handlers(self):
        self._mostrar_datos_handlers = {
            Cancion: self._mostrar_datos_cancion,
            Album: self._mostrar_datos_album,
            Artista: self._mostrar_datos_artista,
            Playlist: self._mostrar_datos_playlist
        }
        # Los handlers de reproducción se pueden registrar aquí también
        self._reproducir_handlers = {}

    def registrar_mostrar_datos_handler(self, tipo, handler):
        self._mostrar_datos_handlers[tipo] = handler

    def mostrar_datos(self, contenido):
        handler = self._mostrar_datos_handlers.get(type(contenido))
        if handler:
            handler(contenido)
        else:
            print(f"No se encontró un handler de visualización para el tipo {type(contenido).__name__}")

    # --- Handlers de Visualización ---

    def _mostrar_datos_cancion(self, cancion: Cancion):
        duracion_min = cancion.duracion // 60
        duracion_sec = cancion.duracion % 60
        print("--- Canción ---")
        print(f"Título:         {cancion.titulo}")
        print(f"Artista:        {cancion.artista.nombre}")
        print(f"Álbum:          {cancion.album.titulo}")
        print(f"Duración:       {duracion_min}:{duracion_sec:02d}")
        print(f"Género:         {cancion.genero}")
        print(f"Reproducciones: {cancion.reproducciones:,}")
        print()

    def _mostrar_datos_album(self, album: Album):
        duracion_total_min = album.get_duracion_total() // 60
        duracion_total_sec = album.get_duracion_total() % 60
        print("--- Álbum ---")
        print(f"Título:         {album.titulo}")
        print(f"Artista:        {album.artista.nombre}")
        print(f"Lanzamiento:    {album.fecha_lanzamiento}")
        print(f"Canciones:      {len(album.canciones)}")
        print(f"Duración Total: {duracion_total_min}:{duracion_total_sec:02d}")
        for i, cancion in enumerate(album.canciones):
            print(f"  {i+1}. {cancion.titulo}")
        print()

    def _mostrar_datos_artista(self, artista: Artista):
        print("--- Artista ---")
        print(f"Nombre:         {artista.nombre}")
        print(f"Género:         {artista.genero}")
        print(f"País:           {artista.pais}")
        print(f"Verificado:     {'Sí' if artista.verificado else 'No'}")
        print()

    def _mostrar_datos_playlist(self, playlist: Playlist):
        duracion_total_min = playlist.duracion_total // 60
        duracion_total_sec = playlist.duracion_total % 60
        print("--- Playlist ---")
        print(f"Nombre:         {playlist.nombre}")
        print(f"Creador:        {playlist.usuario_creador.username}")
        print(f"Descripción:    {playlist.descripcion}")
        print(f"Canciones:      {len(playlist.canciones)}")
        print(f"Duración Total: {duracion_total_min}:{duracion_total_sec:02d}")
        for i, cancion in enumerate(playlist.canciones):
            print(f"  {i+1}. {cancion.titulo} - {cancion.artista.nombre}")
        print()

# ==============================================================================
# ARCHIVO 14/28: plan_factory.py
# Directorio: patrones
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/plan_factory.py
# ==============================================================================

from music_stream.entidades.plan import Plan, PlanFree, PlanPremium, PlanFamily

class PlanFactory:
    _factories = {
        "Free": PlanFree,
        "Premium": PlanPremium,
        "Family": PlanFamily
    }

    @staticmethod
    def crear_plan(tipo: str) -> Plan:
        if tipo not in PlanFactory._factories:
            raise ValueError(f"Tipo de plan desconocido: {tipo}")
        return PlanFactory._factories[tipo]()



################################################################################
# DIRECTORIO: patrones/observer
################################################################################

# ==============================================================================
# ARCHIVO 15/28: observer.py
# Directorio: patrones/observer
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/observer/observer.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: patrones/state
################################################################################

# ==============================================================================
# ARCHIVO 16/28: estado_reproductor.py
# Directorio: patrones/state
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/state/estado_reproductor.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: patrones/strategy
################################################################################

# ==============================================================================
# ARCHIVO 17/28: calidad_audio_strategy.py
# Directorio: patrones/strategy
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/strategy/calidad_audio_strategy.py
# ==============================================================================

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


# ==============================================================================
# ARCHIVO 18/28: restriccion_strategy.py
# Directorio: patrones/strategy
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/patrones/strategy/restriccion_strategy.py
# ==============================================================================

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



################################################################################
# DIRECTORIO: servicios
################################################################################

# ==============================================================================
# ARCHIVO 19/28: artista_service.py
# Directorio: servicios
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/artista_service.py
# ==============================================================================

from music_stream.entidades.artista import Artista
from music_stream.entidades.exceptions import ArtistaExistenteException

class ArtistaService:
    def __init__(self):
        self.artistas = {}

    def crear_artista(self, nombre, genero, pais, biografia, verificado):
        if nombre in self.artistas:
            raise ArtistaExistenteException(f"El artista {nombre} ya existe")

        artista = Artista(nombre, genero, pais, biografia, verificado)
        self.artistas[nombre] = artista
        return artista

    def obtener_artista(self, nombre):
        return self.artistas.get(nombre)

    def mostrar_artista(self, nombre):
        artista = self.obtener_artista(nombre)
        if artista:
            print(artista)
        else:
            print(f"Artista no encontrado: {nombre}")


# ==============================================================================
# ARCHIVO 20/28: biblioteca_service.py
# Directorio: servicios
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/biblioteca_service.py
# ==============================================================================

import pickle
import os

class BibliotecaService:
    @staticmethod
    def persistir(biblioteca, username):
        try:
            os.makedirs("music_stream/data", exist_ok=True)
            filepath = f"music_stream/data/{username}_biblioteca.dat"
            with open(filepath, "wb") as file:
                pickle.dump(biblioteca, file)
            print(f"Biblioteca persistida correctamente en {filepath}")
        except Exception as e:
            raise Exception(f"PersistenciaException: {str(e)}")

    @staticmethod
    def leer_biblioteca(username):
        try:
            filepath = f"music_stream/data/{username}_biblioteca.dat"
            if not os.path.exists(filepath):
                raise Exception("PersistenciaException: Archivo no encontrado")

            with open(filepath, "rb") as file:
                biblioteca = pickle.load(file)
            print(f"Biblioteca cargada correctamente desde {filepath}")
            return biblioteca
        except Exception as e:
            raise Exception(f"PersistenciaException: {str(e)}")


# ==============================================================================
# ARCHIVO 21/28: cache_service.py
# Directorio: servicios
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/cache_service.py
# ==============================================================================

from threading import Lock
from collections import OrderedDict

class CacheService:
    _instance = None
    _lock = Lock()

    def __new__(cls, max_size=50):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.cache = OrderedDict()
                    cls._instance.max_size = max_size
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    def guardar(self, key, value):
        with self._lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False) # Elimina el más antiguo (LRU)
            print(f"[Cache] Objeto con clave '{key}' guardado en caché.")

    def obtener(self, key):
        with self._lock:
            if key not in self.cache:
                print(f"[Cache] Objeto con clave '{key}' no encontrado en caché.")
                return None
            
            self.cache.move_to_end(key)
            print(f"[Cache] Objeto con clave '{key}' obtenido de la caché.")
            return self.cache[key]

    def limpiar(self):
        with self._lock:
            self.cache.clear()
            print("[Cache] La caché ha sido limpiada.")


# ==============================================================================
# ARCHIVO 22/28: cancion_service.py
# Directorio: servicios
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/cancion_service.py
# ==============================================================================

import os
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.exceptions import ArchivoNoEncontradoException

class CancionService:
    def __init__(self):
        self.canciones = {}

    def crear_cancion(self, titulo, artista, album, duracion, genero, archivo_audio):
        if not os.path.exists(archivo_audio):
            raise ArchivoNoEncontradoException(f"El archivo de audio no se encuentra en la ruta: {archivo_audio}")

        cancion = Cancion(
            titulo=titulo,
            artista=artista,
            album=album,
            duracion=duracion,
            genero=genero,
            archivo_audio=archivo_audio
        )
        
        album.agregar_cancion(cancion)
        self.canciones[cancion.titulo] = cancion
        return cancion


# ==============================================================================
# ARCHIVO 23/28: observers.py
# Directorio: servicios
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/observers.py
# ==============================================================================

from typing import Dict, Any
from music_stream.patrones.observer.observer import Observer
from music_stream.entidades.perfil import Perfil

class LoggerObserver(Observer):
    def actualizar(self, evento: Dict[str, Any]):
        print(f"[LOG] Evento recibido: {evento.get('tipo')}, Canción: {evento.get('cancion')}")

class HistorialObserver(Observer):
    def __init__(self, perfil: Perfil):
        self.perfil = perfil

    def actualizar(self, evento: Dict[str, Any]):
        if evento.get('tipo') == "REPRODUCCION_INICIADA":
            cancion = evento.get('cancion')
            if cancion and cancion not in self.perfil.historial:
                self.perfil.historial.append(cancion)
                print(f"[Historial] '{cancion.titulo}' agregada al historial.")

class AnalyticsObserver(Observer):
    def actualizar(self, evento: Dict[str, Any]):
        if evento.get('tipo') == "REPRODUCCION_INICIADA":
            cancion = evento.get('cancion')
            if cancion:
                cancion.incrementar_reproducciones()
                print(f"[Analytics] Se incrementó el contador de '{cancion.titulo}'.")

class AnuncioObserver(Observer):
    def __init__(self, perfil: Perfil):
        self.perfil = perfil

    def actualizar(self, evento: Dict[str, Any]):
        if self.perfil.plan.tipo == "Free" and evento.get('tipo') == "REPRODUCCION_INICIADA":
            # La lógica de "cada 3 canciones" se simplifica aquí
            # Una implementación más robusta podría contar las canciones desde la última vez que se mostró un anuncio
            if len(self.perfil.historial) % 3 == 0 and len(self.perfil.historial) > 0:
                print("\n--- Mostrando anuncio de 15 segundos ---\n")


# ==============================================================================
# ARCHIVO 24/28: perfil_service.py
# Directorio: servicios
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/perfil_service.py
# ==============================================================================

from music_stream.entidades.perfil import Perfil

class PerfilService:
    def __init__(self):
        self.perfiles = {}

    def crear_perfil(self, usuario, plan, biblioteca):
        perfil = Perfil(usuario, plan, biblioteca, historial=[])
        self.perfiles[usuario.username] = perfil
        usuario.perfil = perfil  # Vincular perfil al usuario
        return perfil

    def obtener_perfil(self, username):
        return self.perfiles.get(username)

    def mostrar_perfil(self, username):
        perfil = self.obtener_perfil(username)
        if perfil:
            perfil.mostrar()
        else:
            print(f"Perfil no encontrado para el usuario: {username}")


# ==============================================================================
# ARCHIVO 25/28: reproductor_service.py
# Directorio: servicios
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/reproductor_service.py
# ==============================================================================

import os
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.usuario import Usuario
from music_stream.entidades.reproductor import Reproductor
from music_stream.entidades.exceptions import ArchivoNoEncontradoException
from music_stream.patrones.strategy.calidad_audio_strategy import (
    CalidadBajaStrategy, CalidadAltaStrategy, CalidadLosslessStrategy
)

class ReproductorService:
    def __init__(self):
        self._estrategias_calidad = {
            "Free": CalidadBajaStrategy(),
            "Premium": CalidadAltaStrategy(),
            "Family": CalidadLosslessStrategy()
        }

    def reproducir(self, reproductor: Reproductor, cancion: Cancion, usuario: Usuario):
        """Orquesta la reproducción: selecciona calidad, prepara el reproductor y lo inicia."""
        plan = usuario.plan

        # 1. Seleccionar estrategia de calidad
        estrategia = self._estrategias_calidad.get(plan.tipo)
        if not estrategia:
            raise ValueError(f"No se encontró una estrategia de calidad para el plan {plan.tipo}")

        # 2. Obtener archivo de audio y verificar existencia
        archivo_a_reproducir = estrategia.obtener_archivo(cancion.archivo_audio)
        if not os.path.exists(archivo_a_reproducir):
            # Aquí podrías intentar con el archivo base como fallback
            if not os.path.exists(cancion.archivo_audio):
                raise ArchivoNoEncontradoException(f"No se encontró ninguna versión del archivo de audio: {cancion.archivo_audio}")
            else:
                print(f"Advertencia: No se encontró la versión de calidad {plan.calidad_audio}. Usando archivo base.")
        
        print(f"Cargando '{cancion.titulo}' en el reproductor...")
        reproductor.cancion_actual = cancion
        
        # 3. Iniciar el reproductor (que notificará a los observers)
        reproductor.play()

# ==============================================================================
# ARCHIVO 26/28: suscripcion_service.py
# Directorio: servicios
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/suscripcion_service.py
# ==============================================================================

from music_stream.entidades.usuario import Usuario
from music_stream.patrones.plan_factory import PlanFactory

class SuscripcionService:
    def cambiar_plan(self, usuario: Usuario, nuevo_plan_tipo: str):
        print(f"Cambiando plan de {usuario.username} de {usuario.plan.tipo} a {nuevo_plan_tipo}...")
        try:
            nuevo_plan = PlanFactory.crear_plan(nuevo_plan_tipo)
            usuario.plan = nuevo_plan
            print(f"¡Plan actualizado! El nuevo plan de {usuario.username} es {usuario.plan.tipo}.")
            # En una aplicación real, aquí se actualizaría el estado del reproductor si está activo.
        except ValueError as e:
            print(f"Error al cambiar el plan: {e}")


# ==============================================================================
# ARCHIVO 27/28: usuario_service.py
# Directorio: servicios
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/usuario_service.py
# ==============================================================================

from music_stream.entidades.usuario import Usuario
from music_stream.patrones.plan_factory import PlanFactory
from music_stream.entidades.exceptions import UsuarioExistenteException
from music_stream.servicios.perfil_service import PerfilService
from music_stream.entidades.colecciones.biblioteca import Biblioteca

class UsuarioService:
    def __init__(self, perfil_service: PerfilService):
        self.usuarios = {}
        self.perfil_service = perfil_service

    def crear_usuario(self, username, email, plan_tipo, pais):
        if username in self.usuarios:
            raise UsuarioExistenteException(f"El usuario {username} ya existe")

        # Crear entidades principales
        plan = PlanFactory.crear_plan(plan_tipo)
        usuario = Usuario(username, email, plan, pais)
        biblioteca = Biblioteca(usuario)

        # Crear y vincular el perfil
        self.perfil_service.crear_perfil(usuario, plan, biblioteca)

        self.usuarios[username] = usuario
        return usuario

    def obtener_usuario(self, username):
        return self.usuarios.get(username)

    def __str__(self):
        return "\n".join([str(usuario) for usuario in self.usuarios.values()])


################################################################################
# DIRECTORIO: servicios/colecciones
################################################################################

# ==============================================================================
# ARCHIVO 28/28: playlist_service.py
# Directorio: servicios/colecciones
# Ruta completa: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/colecciones/playlist_service.py
# ==============================================================================

from music_stream.entidades.colecciones.playlist import Playlist
from music_stream.entidades.cancion import Cancion
from music_stream.entidades.usuario import Usuario
from music_stream.patrones.contenido_service_registry import ContenidoServiceRegistry

class PlaylistService:
    def crear_playlist(self, nombre: str, usuario: Usuario, descripcion: str = "", publica: bool = False) -> Playlist:
        """Crea una nueva playlist y la agrega a la biblioteca del usuario."""
        if not hasattr(usuario, 'perfil') or not usuario.perfil:
            raise Exception("El usuario no tiene un perfil y biblioteca asociados.")
        
        playlist = Playlist(nombre, usuario, descripcion, publica)
        usuario.perfil.biblioteca.agregar_playlist(playlist)
        print(f"Playlist '{nombre}' creada para el usuario {usuario.username}.")
        return playlist

    def agregar_cancion(self, playlist: Playlist, cancion: Cancion):
        """Agrega una canción a una playlist existente."""
        playlist.agregar_cancion(cancion)
        print(f"'{cancion.titulo}' agregada a la playlist '{playlist.nombre}'.")

    def mostrar_playlist(self, playlist: Playlist):
        """Muestra los detalles de una playlist usando el Registry."""
        registry = ContenidoServiceRegistry.get_instance()
        registry.mostrar_datos(playlist)



################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 28
# Generado: 2025-11-04 20:22:42
################################################################################
