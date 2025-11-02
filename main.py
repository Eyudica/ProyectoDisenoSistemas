from datetime import date

# --- Importación de Entidades ---
from music_stream.entidades.album import Album
from music_stream.entidades.artista import Artista
from music_stream.entidades.reproductor import Reproductor
from music_stream.entidades.cola_reproduccion import ColaReproduccion

# --- Importación de Servicios ---
from music_stream.servicios.usuario_service import UsuarioService
from music_stream.servicios.perfil_service import PerfilService
from music_stream.servicios.artista_service import ArtistaService
from music_stream.servicios.cancion_service import CancionService
from music_stream.servicios.reproductor_service import ReproductorService
from music_stream.servicios.suscripcion_service import SuscripcionService
from music_stream.servicios.biblioteca_service import BibliotecaService
from music_stream.servicios.colecciones.playlist_service import PlaylistService
from music_stream.servicios.observers import LoggerObserver, HistorialObserver, AnalyticsObserver, AnuncioObserver

# --- Importación de Patrones ---
from music_stream.patrones.contenido_service_registry import ContenidoServiceRegistry


def main():
    print("=============== INICIALIZANDO SISTEMA DE MÚSICA ===============")

    # 1. Inyección de Dependencias y Creación de Servicios
    print("\n--- 1. Creando servicios...")
    perfil_service = PerfilService()
    usuario_service = UsuarioService(perfil_service=perfil_service)
    artista_service = ArtistaService()
    cancion_service = CancionService()
    reproductor_service = ReproductorService()
    suscripcion_service = SuscripcionService()
    playlist_service = PlaylistService()
    registry = ContenidoServiceRegistry.get_instance()

    # 2. Creación de Contenido (Administrador)
    print("\n--- 2. Creando contenido musical (Artistas, Álbumes, Canciones)...")
    artista = artista_service.crear_artista("Coldplay", "Rock Alternativo", "Reino Unido", "Una banda...", True)
    album = Album("A Head Full of Dreams", artista, date(2015, 12, 4), "Rock Alternativo")
    
    cancion1 = cancion_service.crear_cancion(
        titulo="Adventure of a Lifetime", artista=artista, album=album, duracion=263,
        genero="Rock Alternativo", archivo_audio="music/coldplay/adventure_of_a_lifetime.mp3"
    )
    cancion2 = cancion_service.crear_cancion(
        titulo="Hymn for the Weekend", artista=artista, album=album, duracion=258,
        genero="Pop", archivo_audio="music/coldplay/hymn_for_the_weekend.mp3"
    )

    # 3. Creación de Usuario (US-001)
    print("\n--- 3. Registrando un nuevo usuario con plan 'Free'...")
    usuario = usuario_service.crear_usuario("john_doe", "john@email.com", "Free", "Argentina")
    print(f"Usuario creado: {usuario.username} con plan {usuario.plan.tipo}")
    print(f"El usuario tiene perfil: {usuario.perfil is not None}")

    # 4. Configuración del Reproductor (State, Observer, Iterator)
    print("\n--- 4. Configurando el reproductor...")
    cola = ColaReproduccion()
    cola.agregar_cancion(cancion1)
    cola.agregar_cancion(cancion2)
    cola.agregar_cancion(cancion1) # Agregamos de nuevo para probar anuncios

    reproductor = Reproductor(usuario=usuario, cola=cola)

    print("Agregando observadores (Logger, Historial, Analytics, Anuncios)...")
    reproductor.agregar_observador(LoggerObserver())
    reproductor.agregar_observador(HistorialObserver(usuario.perfil))
    reproductor.agregar_observador(AnalyticsObserver())
    reproductor.agregar_observador(AnuncioObserver(usuario.perfil))

    # 5. Simulación de Reproducción (Strategy, State, Observer en acción)
    print("\n--- 5. Simulando reproducción para usuario 'Free'...")
    reproductor_service.reproducir(reproductor, cancion1, usuario)
    reproductor.siguiente() # Salto 1
    reproductor.siguiente() # Salto 2
    reproductor.pause()
    reproductor.play()

    # 6. Demostración del Registry (US-008)
    print("\n--- 6. Mostrando datos con el Registry...")
    registry.mostrar_datos(cancion1)
    registry.mostrar_datos(album)

    # 7. Demostración de Cambio de Plan (US-014)
    print("\n--- 7. Actualizando plan del usuario a 'Premium'...")
    suscripcion_service.cambiar_plan(usuario, "Premium")
    print(f"Plan actual del usuario: {usuario.plan.tipo}")

    # Se necesita un nuevo reproductor o actualizar la estrategia del existente
    # para que el cambio de restricción tenga efecto.
    reproductor_premium = Reproductor(usuario=usuario, cola=cola)
    print("Intentando saltar de nuevo con plan Premium...")
    reproductor_premium.siguiente()
    reproductor_premium.siguiente()
    reproductor_premium.siguiente()
    print("Saltos ilimitados en modo Premium!")

    # 8. Demostración de Persistencia (US-016, US-017)
    print("\n--- 8. Probando la persistencia de la biblioteca...")
    # Agregamos una playlist para que haya algo que guardar
    pl = playlist_service.crear_playlist("Mis temazos", usuario)
    playlist_service.agregar_cancion(pl, cancion1)
    
    BibliotecaService.persistir(usuario.perfil.biblioteca, usuario.username)
    biblioteca_cargada = BibliotecaService.leer_biblioteca(usuario.username)
    print(f"Biblioteca cargada para '{biblioteca_cargada.usuario.username}'.")
    print(f"Playlists en biblioteca cargada: {len(biblioteca_cargada.playlists_creadas)}")

    