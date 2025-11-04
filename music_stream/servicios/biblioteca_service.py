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
