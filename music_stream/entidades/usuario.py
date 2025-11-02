from datetime import datetime

class Usuario:
    def __init__(self, username, email, plan, pais):
        self.username = username
        self.email = email
        self.plan = plan
        self.pais = pais
        self.fecha_registro = datetime.now()
        self.perfil = None

    def set_username(self, new_username):
        self.username = new_username

    def __str__(self):
        return f"Usuario: {self.username}, Email: {self.email}, Plan: {self.plan}, País: {self.pais}"
