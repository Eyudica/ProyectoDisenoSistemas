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
