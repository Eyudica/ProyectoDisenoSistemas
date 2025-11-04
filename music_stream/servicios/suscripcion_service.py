from music_stream.entidades.usuario import Usuario
from music_stream.patrones.plan_factory import PlanFactory

class SuscripcionService:
    def cambiar_plan(self, usuario: Usuario, nuevo_plan_tipo: str):
        print(f"Cambiando plan de {usuario.username} de {usuario.plan.tipo} a {nuevo_plan_tipo}...")
        try:
            nuevo_plan = PlanFactory.crear_plan(nuevo_plan_tipo)
            usuario.plan = nuevo_plan
            print(f"¡Plan actualizado! El nuevo plan de {usuario.username} es {usuario.plan.tipo}.")
            # En una aplicación real, aquí se actualizaría el estado del reproductor si está activo.
        except ValueError as e:
            print(f"Error al cambiar el plan: {e}")
