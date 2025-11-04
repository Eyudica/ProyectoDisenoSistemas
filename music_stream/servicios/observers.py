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
