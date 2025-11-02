# Historias de Usuario - Sistema de Gestión Musical (Tipo Spotify)

**Proyecto**: MusicStreamApp
**Versión**: 1.0.0
**Fecha**: Octubre 2025
**Metodología**: User Story Mapping

---
# Emanuel Yudica
---
## Índice

1. [Epic 1: Gestión de Usuarios y Perfiles](#epic-1-gestion-de-usuarios-y-perfiles)
2. [Epic 2: Gestión de Contenido Musical](#epic-2-gestion-de-contenido-musical)
3. [Epic 3: Sistema de Reproducción](#epic-3-sistema-de-reproduccion)
4. [Epic 4: Playlists y Colecciones](#epic-4-playlists-y-colecciones)
5. [Epic 5: Sistema de Suscripciones](#epic-5-sistema-de-suscripciones)
6. [Epic 6: Persistencia y Cache](#epic-6-persistencia-y-cache)
7. [Historias Técnicas (Patrones de Diseño)](#historias-tecnicas-patrones-de-diseno)

---

## Epic 1: Gestión de Usuarios y Perfiles

### US-001: Registrar Usuario con Plan

**Como** nuevo usuario
**Quiero** registrarme en el sistema con un tipo de plan
**Para** acceder a contenido musical según mi suscripción

#### Criterios de Aceptación

- [x] El sistema debe permitir crear un usuario con:
  - Username único (string)
  - Email único (string)
  - Plan (Free, Premium, Family)
  - Fecha de registro
  - País de origen
- [x] El username debe ser único, si no lanzar `UsuarioExistenteException`
- [x] El plan debe asignarse vía Factory Method
- [x] El usuario debe poder modificarse posteriormente

#### Detalles Técnicos

**Clase**: `Usuario` (`music_stream/entidades/usuarios/usuario.py`)
**Servicio**: `UsuarioService` (`music_stream/servicios/usuarios/usuario_service.py`)
**Factory**: `PlanFactory` (`music_stream/patrones/factory/plan_factory.py`)

**Código de ejemplo**:
```python
from music_stream.servicios.usuarios.usuario_service import UsuarioService

usuario_service = UsuarioService()
usuario = usuario_service.crear_usuario(
    username="john_doe",
    email="john@example.com",
    plan_tipo="Premium",
    pais="Argentina"
)
```

**Validaciones**:
```python
# Username válido
usuario.set_username("new_username")  # OK

# Username duplicado
usuario_service.crear_usuario(username="john_doe", ...)  
# UsuarioExistenteException: El usuario john_doe ya existe
```

---

### US-002: Crear Plan de Suscripción

**Como** usuario
**Quiero** tener un plan de suscripción asignado
**Para** acceder a funcionalidades según mi tipo de cuenta

#### Criterios de Aceptación

- [x] Un plan debe tener:
  - Tipo (Free, Premium, Family)
  - Precio mensual
  - Calidad de audio máxima (128kbps, 320kbps, Lossless)
  - Descargas offline (True/False)
  - Anuncios (True/False)
  - Saltos ilimitados (True/False)
- [x] Los planes deben crearse vía Factory Method
- [x] Free: 128kbps, anuncios, sin descargas
- [x] Premium: 320kbps, sin anuncios, descargas ilimitadas
- [x] Family: Lossless, sin anuncios, hasta 6 cuentas

#### Detalles Técnicos

**Clase**: `Plan` (`music_stream/entidades/usuarios/plan.py`)
**Factory**: `PlanFactory` (`music_stream/patrones/factory/plan_factory.py`)

**Código de ejemplo**:
```python
from music_stream.patrones.factory.plan_factory import PlanFactory

# Factory crea el plan según tipo
plan = PlanFactory.crear_plan("Premium")

print(plan.get_calidad_audio())  # 320kbps
print(plan.tiene_anuncios())     # False
print(plan.puede_descargar())    # True
```

**Tipos de planes**:
```python
# Free
- Precio: $0
- Calidad: 128kbps
- Anuncios: Sí
- Descargas: No
- Saltos: 6 por hora

# Premium
- Precio: $999
- Calidad: 320kbps
- Anuncios: No
- Descargas: Sí
- Saltos: Ilimitados

# Family
- Precio: $1499
- Calidad: Lossless (FLAC)
- Anuncios: No
- Descargas: Sí
- Saltos: Ilimitados
- Usuarios: 6 cuentas
```

---

### US-003: Crear Perfil de Usuario Completo

**Como** administrador del sistema
**Quiero** crear un perfil completo de usuario
**Para** tener toda la información centralizada

#### Criterios de Aceptación

- [x] Un perfil debe contener:
  - Usuario (referencia)
  - Plan (referencia)
  - Biblioteca musical (playlists, favoritos)
  - Historial de reproducción
  - Estadísticas (canciones escuchadas, tiempo total)
- [x] El perfil debe poder persistirse
- [x] El perfil debe poder mostrarse en consola

#### Detalles Técnicos

**Clase**: `Perfil` (`music_stream/entidades/usuarios/perfil.py`)
**Servicio**: `PerfilService` (`music_stream/servicios/usuarios/perfil_service.py`)

**Código de ejemplo**:
```python
from music_stream.entidades.usuarios.perfil import Perfil

perfil = Perfil(
    usuario=usuario,
    plan=plan,
    biblioteca=biblioteca,
    historial=[]
)
```

**Salida de mostración**:
```
PERFIL DE USUARIO
=================
Username:    john_doe
Email:       john@example.com
Plan:        Premium ($999/mes)
Calidad:     320kbps
País:        Argentina
Canciones escuchadas: 1523
Tiempo total: 84h 32min
Playlists: 12
Favoritos: 345
```

---

## Epic 2: Gestión de Contenido Musical

### US-004: Crear Artista

**Como** administrador
**Quiero** registrar artistas musicales
**Para** organizar el catálogo por creador

#### Criterios de Aceptación

- [x] Debe poder crear artistas con:
  - Nombre único
  - Género musical principal
  - País de origen
  - Biografía
  - Verificado (True/False)
- [x] El sistema debe verificar nombre único
- [x] Si nombre duplicado, lanzar `ArtistaExistenteException`
- [x] Los artistas deben crearse vía Factory Method

#### Detalles Técnicos

**Clase**: `Artista` (`music_stream/entidades/contenido/artista.py`)
**Servicio**: `ArtistaService` (`music_stream/servicios/contenido/artista_service.py`)

**Código de ejemplo**:
```python
from music_stream.servicios.contenido.artista_service import ArtistaService

artista_service = ArtistaService()

# Crear artista
artista = artista_service.crear_artista(
    nombre="Coldplay",
    genero="Rock Alternativo",
    pais="Reino Unido",
    verificado=True
)
```

**Constantes utilizadas**:
```python
GENEROS_DISPONIBLES = [
    "Rock", "Pop", "Jazz", "Clásica", 
    "Hip Hop", "Electrónica", "Reggae", "Metal"
]
```

---

### US-005: Crear Álbum con Canciones

**Como** administrador
**Quiero** crear álbumes que contengan canciones
**Para** organizar el contenido por colección

#### Criterios de Aceptación

- [x] Debe poder crear álbumes con:
  - Título
  - Artista (referencia)
  - Fecha de lanzamiento
  - Género
  - Lista de canciones (vacía al inicio)
  - Duración total (calculada automáticamente)
- [x] El álbum debe estar asociado a un artista válido
- [x] El sistema debe calcular duración total al agregar canciones
- [x] Los álbumes deben poder tener múltiples géneros

#### Detalles Técnicos

**Clase**: `Album` (`music_stream/entidades/contenido/album.py`)
**Servicio**: `AlbumService` (`music_stream/servicios/contenido/album_service.py`)

**Código de ejemplo**:
```python
from music_stream.entidades.contenido.album import Album
from datetime import date

album = Album(
    titulo="A Head Full of Dreams",
    artista=artista,
    fecha_lanzamiento=date(2015, 12, 4),
    genero="Rock Alternativo"
)

# Obtener duración total (calculada automáticamente)
print(f"Duración: {album.get_duracion_total()} segundos")
```

**Validaciones**:
```python
# Fecha válida
album.set_fecha_lanzamiento(date(2020, 1, 1))  # OK

# Fecha futura
album.set_fecha_lanzamiento(date(2030, 1, 1))  
# ValueError: La fecha no puede ser futura
```

---

### US-006: Crear Canción con Metadata

**Como** administrador
**Quiero** agregar canciones con toda su información
**Para** tener un catálogo completo

#### Criterios de Aceptación

- [x] Debe poder crear canciones con:
  - Título
  - Artista (referencia)
  - Álbum (referencia)
  - Duración (en segundos)
  - Género
  - Letra (opcional)
  - Número de reproducciones (0 al inicio)
  - Archivo de audio (ruta)
- [x] Las canciones ocupan espacio en disco según calidad
- [x] El sistema debe verificar que el archivo existe
- [x] Las canciones deben crearse vía Factory Method

#### Detalles Técnicos

**Clase**: `Cancion` (`music_stream/entidades/contenido/cancion.py`)
**Servicio**: `CancionService` (`music_stream/servicios/contenido/cancion_service.py`)

**Código de ejemplo**:
```python
from music_stream.servicios.contenido.cancion_service import CancionService

cancion_service = CancionService()

# Crear canción
cancion = cancion_service.crear_cancion(
    titulo="Adventure of a Lifetime",
    artista=artista,
    album=album,
    duracion=263,  # 4:23
    genero="Rock Alternativo",
    archivo_audio="music/coldplay/adventure.mp3"
)
```

**Constantes utilizadas**:
```python
TAMANO_ARCHIVO_128KBPS = 4.0   # MB por minuto
TAMANO_ARCHIVO_320KBPS = 9.6   # MB por minuto
TAMANO_ARCHIVO_LOSSLESS = 30.0 # MB por minuto
```

---

### US-007: Reproducir Canción según Plan

**Como** usuario
**Quiero** reproducir canciones según mi plan
**Para** escuchar música con la calidad permitida

#### Criterios de Aceptación

- [x] El sistema debe:
  - Verificar el plan del usuario
  - Reproducir en calidad correspondiente (128kbps, 320kbps, Lossless)
  - Incrementar contador de reproducciones
  - Agregar al historial del usuario
  - Mostrar anuncios si es plan Free (cada 3 canciones)
- [x] Si no hay archivo de audio, lanzar `ArchivoNoEncontradoException`
- [x] El sistema debe usar Strategy para seleccionar calidad

#### Detalles Técnicos

**Servicio**: `ReproductorService.reproducir()`
**Estrategias**:
- `CalidadBajaStrategy` (128kbps - Free)
- `CalidadAltaStrategy` (320kbps - Premium)
- `CalidadLosslessStrategy` (FLAC - Family)

**Código de ejemplo**:
```python
from music_stream.servicios.reproductor.reproductor_service import ReproductorService

reproductor = ReproductorService()

# Reproducir canción según plan del usuario
reproductor.reproducir(cancion, usuario)

# Proceso:
# 1. Verifica plan del usuario
# 2. Selecciona estrategia de calidad
# 3. Carga archivo correspondiente
# 4. Incrementa reproducciones
# 5. Agrega a historial
# 6. Muestra anuncio si Free
```

**Calidad por plan**:
```python
# Plan Free
# - Calidad: 128kbps
# - Anuncio cada 3 canciones
# - Tamaño: ~4MB/min

# Plan Premium
# - Calidad: 320kbps
# - Sin anuncios
# - Tamaño: ~9.6MB/min

# Plan Family
# - Calidad: Lossless (FLAC)
# - Sin anuncios
# - Tamaño: ~30MB/min
```

---

### US-008: Mostrar Datos de Canción por Tipo

**Como** usuario
**Quiero** ver los datos de cada canción de forma detallada
**Para** conocer la información completa

#### Criterios de Aceptación

- [x] El sistema debe mostrar:
  - **Canción**: Título, Artista, Álbum, Duración, Género, Reproducciones
  - **Álbum**: Título, Artista, Canciones (lista), Duración total
  - **Artista**: Nombre, Género, País, Canciones totales, Álbumes
- [x] Usar el patrón Registry para dispatch polimórfico
- [x] NO usar cascadas de isinstance()

#### Detalles Técnicos

**Registry**: `ContenidoServiceRegistry.mostrar_datos()`

**Código de ejemplo**:
```python
from music_stream.servicios.contenido.contenido_service_registry import ContenidoServiceRegistry

registry = ContenidoServiceRegistry.get_instance()

for item in biblioteca.get_contenidos():
    registry.mostrar_datos(item)
    # Despacho automático al servicio correcto
```

**Salida ejemplo (Canción)**:
```
Canción: Adventure of a Lifetime
Artista: Coldplay
Álbum: A Head Full of Dreams
Duración: 4:23
Género: Rock Alternativo
Reproducciones: 15,234,567
```

---

## Epic 3: Sistema de Reproducción

### US-009: Crear Cola de Reproducción

**Como** usuario
**Quiero** tener una cola de reproducción
**Para** escuchar canciones en secuencia

#### Criterios de Aceptación

- [x] La cola debe:
  - Mantener lista de canciones ordenadas
  - Permitir agregar canciones al final
  - Permitir insertar canciones en posición específica
  - Permitir eliminar canciones
  - Mantener índice de canción actual
  - Permitir avanzar/retroceder
- [x] Implementar patrón Iterator
- [x] Soportar modos: Normal, Aleatorio, Repetir

#### Detalles Técnicos

**Clase**: `ColaReproduccion` (`music_stream/entidades/reproductor/cola_reproduccion.py`)
**Patron**: Iterator

**Código de ejemplo**:
```python
from music_stream.entidades.reproductor.cola_reproduccion import ColaReproduccion

cola = ColaReproduccion()

# Agregar canciones
cola.agregar_cancion(cancion1)
cola.agregar_cancion(cancion2)
cola.agregar_cancion(cancion3)

# Navegar
cola.siguiente()  # Avanza a canción 2
cola.anterior()   # Retrocede a canción 1

# Modos
cola.set_modo_aleatorio(True)
cola.set_modo_repetir("uno")  # "uno", "todos", "ninguno"
```

---

### US-010: Controlar Reproducción (Play/Pause/Stop)

**Como** usuario
**Quiero** controlar la reproducción
**Para** manejar la música a mi gusto

#### Criterios de Aceptación

- [x] El reproductor debe:
  - Play: iniciar reproducción
  - Pause: pausar manteniendo posición
  - Stop: detener y reiniciar posición
  - Next: siguiente canción
  - Previous: canción anterior
  - Seek: saltar a posición específica
- [x] Implementar patrón State
- [x] Estados: Detenido, Reproduciendo, Pausado

#### Detalles Técnicos

**Clase**: `Reproductor` (`music_stream/entidades/reproductor/reproductor.py`)
**Patron**: State

**Código de ejemplo**:
```python
from music_stream.entidades.reproductor.reproductor import Reproductor

reproductor = Reproductor()

# Estados
reproductor.play()    # Detenido → Reproduciendo
reproductor.pause()   # Reproduciendo → Pausado
reproductor.play()    # Pausado → Reproduciendo
reproductor.stop()    # Reproduciendo → Detenido

# Navegación
reproductor.siguiente()
reproductor.anterior()

# Posición
reproductor.seek(120)  # Saltar a 2:00
```

**Estados**:
```python
# Detenido
- Posición: 0
- Puede: play()

# Reproduciendo
- Posición: incrementándose
- Puede: pause(), stop(), siguiente(), anterior()

# Pausado
- Posición: fija
- Puede: play(), stop()
```

---

## Epic 4: Playlists y Colecciones

### US-011: Crear Playlist Personalizada

**Como** usuario
**Quiero** crear playlists personalizadas
**Para** organizar mis canciones favoritas

#### Criterios de Aceptación

- [x] Una playlist debe tener:
  - Nombre
  - Descripción (opcional)
  - Usuario creador
  - Lista de canciones
  - Pública/Privada
  - Fecha de creación
  - Duración total (calculada)
- [x] Las canciones pueden repetirse
- [x] El orden de canciones es importante
- [x] Las playlists pueden compartirse (si son públicas)

#### Detalles Técnicos

**Clase**: `Playlist` (`music_stream/entidades/colecciones/playlist.py`)
**Servicio**: `PlaylistService` (`music_stream/servicios/colecciones/playlist_service.py`)

**Código de ejemplo**:
```python
from music_stream.servicios.colecciones.playlist_service import PlaylistService

playlist_service = PlaylistService()

# Crear playlist
playlist = playlist_service.crear_playlist(
    nombre="Rock Clásico",
    descripcion="Las mejores del rock",
    usuario=usuario,
    publica=True
)

# Agregar canciones
playlist_service.agregar_cancion(playlist, cancion1)
playlist_service.agregar_cancion(playlist, cancion2)

# Mostrar
playlist_service.mostrar_playlist(playlist)
```

---

### US-012: Agregar Canciones a Favoritos

**Como** usuario
**Quiero** marcar canciones como favoritas
**Para** acceder rápidamente a mis preferidas

#### Criterios de Aceptación

- [x] El usuario debe tener una colección de favoritos
- [x] Las canciones pueden agregarse/quitarse
- [x] Los favoritos son una playlist especial
- [x] Los favoritos se sincronizan automáticamente
- [x] Las canciones favoritas tienen icono especial

#### Detalles Técnicos

**Clase**: `Favoritos` (hereda de `Playlist`)

**Código de ejemplo**:
```python
from music_stream.entidades.colecciones.favoritos import Favoritos

favoritos = Favoritos(usuario)

# Agregar/quitar
favoritos.agregar(cancion)
favoritos.quitar(cancion)

# Verificar
if favoritos.contiene(cancion):
    print("❤️ Es favorita")
```

---

### US-013: Crear Biblioteca Musical del Usuario

**Como** usuario
**Quiero** tener una biblioteca con todo mi contenido
**Para** acceder fácilmente a playlists, álbumes y artistas

#### Criterios de Aceptación

- [x] La biblioteca debe contener:
  - Playlists creadas
  - Playlists seguidas
  - Álbumes guardados
  - Artistas seguidos
  - Canciones favoritas
  - Historial de reproducción
- [x] Debe poder filtrarse por tipo
- [x] Debe poder ordenarse por: reciente, nombre, artista

#### Detalles Técnicos

**Clase**: `Biblioteca` (`music_stream/entidades/colecciones/biblioteca.py`)

**Código de ejemplo**:
```python
from music_stream.entidades.colecciones.biblioteca import Biblioteca

biblioteca = Biblioteca(usuario)

# Agregar contenido
biblioteca.agregar_playlist(playlist)
biblioteca.agregar_album(album)
biblioteca.seguir_artista(artista)

# Filtrar
playlists = biblioteca.get_playlists()
albums = biblioteca.get_albums()
artistas = biblioteca.get_artistas_seguidos()
```

---

## Epic 5: Sistema de Suscripciones

### US-014: Cambiar Plan de Suscripción

**Como** usuario
**Quiero** cambiar mi plan de suscripción
**Para** acceder a diferentes funcionalidades

#### Criterios de Aceptación

- [x] El usuario puede:
  - Upgrade: Free → Premium → Family
  - Downgrade: Family → Premium → Free
  - Ver diferencias entre planes
  - Confirmar cambio
- [x] El cambio es inmediato
- [x] Al downgrade, se pierden funcionalidades premium
- [x] Usar patrón Strategy para aplicar restricciones

#### Detalles Técnicos

**Servicio**: `SuscripcionService.cambiar_plan()`

**Código de ejemplo**:
```python
from music_stream.servicios.suscripciones.suscripcion_service import SuscripcionService

suscripcion_service = SuscripcionService()

# Cambiar plan
suscripcion_service.cambiar_plan(
    usuario=usuario,
    plan_nuevo="Premium"
)

# Verificar cambio
print(f"Plan actual: {usuario.get_plan().get_nombre()}")
print(f"Calidad: {usuario.get_plan().get_calidad_audio()}")
```

---

### US-015: Aplicar Restricciones según Plan

**Como** sistema
**Quiero** aplicar restricciones según el plan del usuario
**Para** limitar funcionalidades en planes gratuitos

#### Criterios de Aceptación

- [x] Plan Free:
  - Máximo 6 saltos por hora
  - Anuncios cada 3 canciones
  - No puede descargar
  - Calidad máxima 128kbps
  - No puede escuchar sin conexión
- [x] Plan Premium:
  - Saltos ilimitados
  - Sin anuncios
  - Descargas ilimitadas
  - Calidad máxima 320kbps
  - Escucha offline
- [x] Usar patrón Strategy para restricciones

#### Detalles Técnicos

**Estrategias**: `RestriccionFreeStrategy`, `RestriccionPremiumStrategy`

**Código de ejemplo**:
```python
# Al saltar canción
if not usuario.puede_saltar():
    raise LimiteSkipsException("Has alcanzado el límite de saltos")

# Al intentar descargar
if not usuario.puede_descargar():
    raise DescargaNoPermitidaException("Requiere plan Premium")
```

---

## Epic 6: Persistencia y Cache

### US-016: Persistir Biblioteca de Usuario

**Como** administrador del sistema
**Quiero** guardar la biblioteca del usuario en disco
**Para** mantener datos entre sesiones

#### Criterios de Aceptación

- [x] El sistema debe:
  - Serializar Biblioteca completa con Pickle
  - Guardar en directorio `data/`
  - Nombre de archivo: `{username}_biblioteca.dat`
  - Crear directorio si no existe
  - Mostrar mensaje de confirmación
- [x] Si ocurre error, lanzar `PersistenciaException`
- [x] Cerrar recursos apropiadamente

#### Detalles Técnicos

**Servicio**: `BibliotecaService.persistir()`

**Código de ejemplo**:
```python
from music_stream.servicios.colecciones.biblioteca_service import BibliotecaService

biblioteca_service = BibliotecaService()

# Persistir
biblioteca_service.persistir(biblioteca)
# Crea: data/john_doe_biblioteca.dat
```

---

### US-017: Recuperar Biblioteca desde Disco

**Como** usuario
**Quiero** recuperar mi biblioteca guardada
**Para** continuar donde lo dejé

#### Criterios de Aceptación

- [x] El sistema debe:
  - Deserializar archivo `.dat` con Pickle
  - Buscar en directorio `data/`
  - Validar que username no sea nulo/vacío
  - Retornar Biblioteca completa
  - Mostrar mensaje de confirmación
- [x] Si archivo no existe, lanzar `PersistenciaException`
- [x] Si archivo corrupto, lanzar `PersistenciaException`

#### Detalles Técnicos

**Servicio**: `BibliotecaService.leer_biblioteca()` (método estático)

**Código de ejemplo**:
```python
# Leer biblioteca
biblioteca = BibliotecaService.leer_biblioteca("john_doe")

# Mostrar contenido
biblioteca_service.mostrar_datos(biblioteca)
```

---

### US-018: Cachear Canciones Reproducidas Recientemente

**Como** sistema
**Quiero** cachear canciones reproducidas recientemente
**Para** mejorar tiempo de carga

#### Criterios de Aceptación

- [x] El sistema debe:
  - Mantener cache de últimas 50 canciones
  - Usar LRU (Least Recently Used)
  - Almacenar metadata en memoria
  - Limpiar cache al cerrar sesión
- [x] Implementar patrón Singleton para Cache
- [x] Thread-safe

#### Detalles Técnicos

**Clase**: `CacheService` (Singleton)

**Código de ejemplo**:
```python
from music_stream.servicios.cache.cache_service import CacheService

cache = CacheService.get_instance()

# Guardar en cache
cache.guardar(cancion.get_id(), cancion)

# Recuperar de cache
cancion_cached = cache.obtener(cancion_id)

if cancion_cached:
    print("✅ Canción en cache")
else:
    print("❌ Cargar desde disco")
```

---

## Historias Técnicas (Patrones de Diseño)

### US-TECH-001: Implementar Singleton para ServiceRegistry

**Como** arquitecto de software
**Quiero** garantizar una única instancia del registro de servicios
**Para** compartir estado consistente

#### Criterios de Aceptación

- [x] Implementar patrón Singleton thread-safe
- [x] Usar double-checked locking con Lock
- [x] Inicialización perezosa
- [x] Metodo `get_instance()` para acceso
- [x] NO permitir múltiples instancias

#### Detalles Técnicos

**Clase**: `ContenidoServiceRegistry`
**Patrón**: Singleton

**Implementación**:
```python
from threading import Lock

class ContenidoServiceRegistry:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._inicializar_servicios()
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance
```

---

### US-TECH-002: Implementar Factory Method para Planes

**Como** arquitecto de software
**Quiero** centralizar creación de planes vía Factory
**Para** desacoplar cliente de clases concretas

#### Criterios de Aceptación

- [x] Crear clase `PlanFactory` con método estático
- [x] Soportar: Free, Premium, Family
- [x] Usar diccionario de factories
- [x] Lanzar `ValueError` si plan desconocido
- [x] Retornar tipo base `Plan`

#### Detalles Técnicos

**Clase**: `PlanFactory`
**Patrón**: Factory Method

**Implementación**:
```python
class PlanFactory:
    @staticmethod
    def crear_plan(tipo: str) -> Plan:
        factories = {
            "Free": PlanFactory._crear_free,
            "Premium": PlanFactory._crear_premium,
            "Family": PlanFactory._crear_family
        }

        if tipo not in factories:
            raise ValueError(f"Plan desconocido: {tipo}")

        return factories[tipo]()

    @staticmethod
    def _crear_free() -> Plan:
        return PlanFree(
            precio=0,
            calidad="128kbps",
            anuncios=True,
            descargas=False
        )
```

---

### US-TECH-003: Implementar Observer para Sistema de Notificaciones

**Como** arquitecto de software
**Quiero** implementar patrón Observer
**Para** notificar eventos del reproductor

#### Criterios de Aceptación

- [x] Crear clase `Observable[T]` genérica
- [x] Crear interfaz `Observer[T]` genérica
- [x] Soportar múltiples observadores
- [x] El reproductor notifica: canción iniciada, canción finalizada, pausa, error
- [x] Los observadores pueden ser: UI, Logger, Analytics
