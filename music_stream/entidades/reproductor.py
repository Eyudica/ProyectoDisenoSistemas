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
