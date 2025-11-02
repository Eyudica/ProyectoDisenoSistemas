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