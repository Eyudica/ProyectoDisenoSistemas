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