from datetime import datetime

class Perfil:
    def __init__(self, usuario, plan, biblioteca, historial):
        self.usuario = usuario
        self.plan = plan
        self.biblioteca = biblioteca
        self.historial = historial
        self.estadisticas = {
            "canciones_escuchadas": 0,
            "tiempo_total": 0
        }

    def mostrar(self):
        print("PERFIL DE USUARIO")
        print("=================")
        print(f"Username: {self.usuario.username}")
        print(f"Email: {self.usuario.email}")
        print(f"Plan: {self.plan.tipo} (${self.plan.precio}/mes)")
        print(f"Calidad: {self.plan.calidad_audio}")
        print(f"País: {self.usuario.pais}")
        print(f"Canciones escuchadas: {self.estadisticas['canciones_escuchadas']}")
        print(f"Tiempo total: {self.estadisticas['tiempo_total']} minutos")
        print(f"Playlists: {len(self.biblioteca.playlists)}")
        print(f"Favoritos: {len(self.biblioteca.favoritos)}")
