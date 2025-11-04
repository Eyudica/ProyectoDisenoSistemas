"""
Archivo integrador generado automaticamente
Directorio: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios
Fecha: 2025-11-04 20:22:42
Total de archivos integrados: 9
"""

# ================================================================================
# ARCHIVO 1/9: artista_service.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/artista_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 2/9: biblioteca_service.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/biblioteca_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 3/9: cache_service.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/cache_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 4/9: cancion_service.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/cancion_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 5/9: observers.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/observers.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 6/9: perfil_service.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/perfil_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 7/9: reproductor_service.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/reproductor_service.py
# ================================================================================

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

# ================================================================================
# ARCHIVO 8/9: suscripcion_service.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/suscripcion_service.py
# ================================================================================

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


# ================================================================================
# ARCHIVO 9/9: usuario_service.py
# Ruta: /home/manu/Proyectos/Sistemas/2/Ds/ProyectoDisenoSistemas/music_stream/servicios/usuario_service.py
# ================================================================================

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

