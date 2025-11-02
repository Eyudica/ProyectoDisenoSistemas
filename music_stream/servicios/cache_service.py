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
