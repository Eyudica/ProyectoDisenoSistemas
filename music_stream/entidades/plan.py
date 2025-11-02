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