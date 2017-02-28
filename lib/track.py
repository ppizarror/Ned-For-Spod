# coding=utf-8
"""
TRACK
Permite crear una pista, posee tanto decoraciones como coches

Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    from path import *  # @UnusedWildImport

# Importación de librerías
from bin import pygame
from object import Gameobject
from player import Player
from resources.images import getImages


# noinspection PyBroadException,PyUnresolvedReferences
class Maptrack(object):
    """Pista de carreras"""

    def __init__(self, config, window):
        """
        Función constructora
        :param config: Configuraciones de las pistas
        :param window: Ventana de la aplicación
        :return: void
        """

        # Se guardan parametros
        self.config = config
        self.window = window
        # Variables de modelo
        self.background = None  # fondo de las pistas
        self.backgroundSize = ()  # tamaño del fondo
        self.decorations = []  # decoraciones del juego
        self.enemies = []  # autos de los enemigos
        self.images = {}  # Imágenes propias de cada pista
        self.laps = 0  # define el numero de vueltas maximas a ganar
        self.mapLimits = []  # coordenadas maximas del mapa
        self.marcas_frenado = []  # marcas del frenado en la pista
        self.marcas_tierra = []  # marcas de la tierra en la pista
        self.obstacles = []  # obstaculos de la pista
        self.objetives = []  # objetivos por cada tipo de jugador
        self.player = None  # jugador
        self.results = False  # Si se han mostrado los resultados de la pista
        self.title = ""  # titulo de la pista
        self.track = []  # pista misma (imagen)
        self.track_coords = []  # coordenadas de la pista

    def add_car(self, _type, texture, automatic, angle, player, logic_track,
                sounds, sound_channels, checksum,
                scoreconfig, username, tracktitle, game_config, browser,
                **kwargs):
        """
        Función que añade un auto al modelo
        :param _type: Tipo de auto
        :param texture: Textura del auto
        :param automatic: Define si la transmisión es automático/manual
        :param angle: �?ngulo inicial del auto
        :param player: Indica si es jugable o AI
        :param logic_track: Entidades lógicas de la pista
        :param sounds: Sonidos de la pista
        :param sound_channels: Canales de sonido
        :param checksum: Checksum (hash) de la aplicación
        :param scoreconfig: Configuraciones del scoreboard
        :param username: Username del usuario
        :param tracktitle: Título de la pista
        :param game_config: Configuraciones del juego
        :param browser: Navegador web
        :param kwargs: Parámetros adicionales
        :return: void
        """
        # Se obtiene la sombra de la imagen
        if "classic" in texture:
            ghost = "lr_classic_ghost"
            shadow = "lr_classic_shadow"
        elif "modern" in texture:
            ghost = "lr_modern_ghost"
            shadow = "lr_modern_shadow"
        else:
            ghost = "lr_super_ghost"
            shadow = "lr_super_shadow"
        # Se define la posición por defecto
        pos = (0, 0)
        # Se instancia el objeto
        if player:
            del self.player
            pos = self.window.get_window_size()
            image = self.load_image(texture, **kwargs)
            image_width, image_height = image.get_size()
            self.player = Player(_type, image,
                                 self.load_image(shadow, alpha=True),
                                 (pos[0] / 2 - image_width / 2,
                                  pos[1] / 2 - image_height / 2),
                                 angle, True, self.get_marcas_frenado(),
                                 self.get_marcas_tierra(), logic_track,
                                 self.laps,
                                 sounds, sound_channels,
                                 self.load_image(ghost, alpha=True), checksum,
                                 scoreconfig,
                                 username, tracktitle,
                                 self.objetives, automatic,
                                 self.get_map_limits(), self.window,
                                 game_config,
                                 browser,
                                 **kwargs)
        else:
            self.enemies.append(
                Player(_type, self.load_image(texture, **kwargs),
                       self.load_image(shadow, alpha=True),
                       pos, angle, False,
                       self.get_marcas_frenado(),
                       self.get_marcas_tierra(), logic_track,
                       self.laps, sounds, sound_channels,
                       self.load_image(ghost, alpha=True),
                       checksum,
                       scoreconfig, username, tracktitle,
                       self.objetives, automatic,
                       self.get_map_limits(), self.window,
                       game_config, browser, **kwargs))

    def add_decoration(self, texture, pos):
        """
        Función que agrega una decoración
        :param texture: Textura del objeto
        :param pos: Posición (x,y) en el mundo
        :return: void
        """
        self.decorations.append(Gameobject(texture, 2, pos))

    def add_marcas_frenado(self, linea):
        """
        Función que agrega una marca de frenado
        :param linea: Línea a agregar
        :return: void
        """
        self.marcas_frenado.append(linea)

    def add_marcas_tierra(self, linea):
        """
        Función que agrega una marca en la tierra
        :param linea: Línea a agregar
        :return: void
        """
        self.marcas_tierra.append(linea)

    def add_track(self, texture, pos):
        """
        Función que agrega una pista al circuito
        :param texture: Textura de la pista
        :param pos: Posición (x,y) en el mundo
        :return: void
        """
        image = texture
        width, height = image.get_size()
        self.track.append(Gameobject(image, 1, pos))
        self.track_coords.append(
            [(self.window.get_window_width() / 2 - pos[0],
              self.window.get_window_height() / 2 - pos[1]),
             (self.window.get_window_width() / 2 - pos[0] + width,
              self.window.get_window_height() / 2 - pos[1] + height)])

    def clean(self):
        """
        Función que elimina todos los datos
        :return: void
        """
        try:
            # Se borran los datos
            del self.background, self.backgroundSize, self.decorations, self.mapLimits, \
                self.marcas_frenado, self.marcas_tierra, self.obstacles, self.title, self.track, self.track_coords
            # Se limpia el jugador y se borra
            self.player.clear()
            try:
                del self.player
            except:
                pass
        except:
            pass
        # Se borra
        del self

    def get_background(self):
        """
        Función que retorna el fondo de la pista
        :return: void
        """
        return self.background

    def get_background_size(self):
        """
        Función que retorna el tamaño del fondo
        :return: Tupla (w,h)
        """
        return self.backgroundSize

    def get_background_teselation(self):
        """
        Función que retorna las veces que hay que dibujar en ambos ejes
        :return: Integer
        """
        return self.backgroundTesel

    def get_decorations(self):
        """
        Función que retorna las decoraciones
        :return: Lista de <object>
        """
        return self.decorations

    def get_laps(self):
        """
        Retorna el numero de vueltas del circuito
        :return: Integer
        """
        return self.laps

    def get_player(self):
        """
        Función que retorna al jugador
        :return: Objeto <player>
        """
        return self.player

    def get_marcas_frenado(self):
        """
        Función que retorna las marcas de frenado en la pista
        :return: Lista
        """
        return self.marcas_frenado

    def get_marcas_tierra(self):
        """
        Función que retorna las marcas de la tierra
        :return: Lista
        """
        return self.marcas_tierra

    def get_map_limits(self):
        """
        Función que retorna los limites del mapa
        :return: Tupla (w,h)
        """
        return self.mapLimits

    def get_track_title(self):
        """
        Retorna el título del mapa
        :return: String
        """
        return self.title

    def get_track(self):
        """
        Función que retorna la pista
        :return: Objeto <track>
        """
        return self.track

    def get_track_logic(self):
        """
        Función que retorna la pista lógica
        :return: Retorna las coordenadas de cada elemento de la pista
        """
        return self.track_coords

    def load_image(self, texture_name, color_key=(0, 0, 0), **kwargs):
        """
        Función que carga una imagen
        :param texture_name: Dirección física de la textura
        :param color_key: Índice de color
        :param kwargs: Parámetros adicionales
        :return: Objeto imagen
        """
        # Si la imagen no ha sido cargada entonces se carga y se guarda
        if texture_name not in self.images.keys():
            if kwargs.get("alpha"):
                image = pygame.image.load(
                    getImages(texture_name)).convert_alpha()
            else:
                image = pygame.image.load(getImages(texture_name)).convert(32)
                image.set_colorkey(color_key)
            self.images[texture_name] = image
        return self.images[texture_name]

    def results_saved(self):
        """
        Función que retorna si se han calculado los resultados de la pista o no
        :return: booleano
        """
        return self.results

    def set_background(self, texture):
        """
        Función que define el fondo a dibujar
        :param texture: Textura
        :return: void
        """
        self.background = texture
        self.backgroundSize = texture.get_size()

    def set_map_limits(self, x1, y1, x2, y2):
        """
        Función que define las coordenadas máximas del mapa
        :param x1: Posición x mínima
        :param y1: Posición y mínima
        :param x2: Posición x máxima
        :param y2: Posición y máxima
        :return: void
        """
        self.mapLimits = [x1, y1, x2, y2]

    def set_laps(self, laps):
        """
        Función que define la cantidad de vueltas del mapa
        :param laps: Número de vueltas
        :return: void
        """
        self.laps = laps

    def set_objetives(self, objetives):
        """
        Función que define los objetivos del mapa
        :param objetives: Lista de objetivos
        :return: void
        """
        self.objetives = objetives

    def set_title(self, title):
        """
        Función que establece el nombre del mapa
        :param title: Título del mapa
        :return: void
        """
        self.title = title
