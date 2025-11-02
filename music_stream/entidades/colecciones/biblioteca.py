from typing import List
from music_stream.entidades.usuario import Usuario
from music_stream.entidades.colecciones.playlist import Playlist
from music_stream.entidades.album import Album
from music_stream.entidades.artista import Artista
from music_stream.entidades.cancion import Cancion

class Biblioteca:
    def __init__(self, usuario: Usuario):
        self.usuario = usuario
        self.playlists_creadas: List[Playlist] = []
        self.playlists_seguidas: List[Playlist] = []
        self.albumes_guardados: List[Album] = []
        self.artistas_seguidos: List[Artista] = []
        self.canciones_favoritas: List[Cancion] = []
        # El historial de reproducción se manejará directamente en el Perfil
        # para mantener la cohesión con la US-003

    def agregar_playlist(self, playlist: Playlist):
        self.playlists_creadas.append(playlist)

    def seguir_playlist(self, playlist: Playlist):
        self.playlists_seguidas.append(playlist)

    def guardar_album(self, album: Album):
        self.albumes_guardados.append(album)

    def seguir_artista(self, artista: Artista):
        self.artistas_seguidos.append(artista)

    def agregar_a_favoritos(self, cancion: Cancion):
        if cancion not in self.canciones_favoritas:
            self.canciones_favoritas.append(cancion)

    def quitar_de_favoritos(self, cancion: Cancion):
        self.canciones_favoritas.remove(cancion)

    def __str__(self):
        return f"Biblioteca de {self.usuario.username}"
