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
