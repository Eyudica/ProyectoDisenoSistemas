from music_stream.entidades.plan import Plan, PlanFree, PlanPremium, PlanFamily

class PlanFactory:
    _factories = {
        "Free": PlanFree,
        "Premium": PlanPremium,
        "Family": PlanFamily
    }

    @staticmethod
    def crear_plan(tipo: str) -> Plan:
        if tipo not in PlanFactory._factories:
            raise ValueError(f"Tipo de plan desconocido: {tipo}")
        return PlanFactory._factories[tipo]()
