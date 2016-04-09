#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__': from path import *  # @UnusedWildImport

# TRACK
# Permite crear una pista, posee tanto decoraciones como coches
#
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
from bin import pygame
from object import gameObject
from player import Player
from resources.images import getImages


class mapTrack:
    """Pista de carreras"""

    def __init__(self, config, window, **kwargs):
        """
        Función constructora
        :param config: Configuraciones de las pistas
        :param window: Ventana de la aplicación
        :param kwargs: Parámetros adicionales
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

    def addCar(self, type, texture, automatic, angle, player, logic_track, sounds, sound_channels, checksum,
               scoreconfig, username, tracktitle, gameConfig, browser, **kwargs):
        """
        Función que añade un auto al modelo
        :param type: Tipo de auto
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
        :param gameConfig: Configuraciones del juego
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
            pos = self.window.getWindowSize()
            image = self.loadImage(texture, **kwargs)
            imageWidth, imageHeight = image.get_size()
            self.player = Player(type, image, self.loadImage(shadow, alpha=True),
                                 (pos[0] / 2 - imageWidth / 2, pos[1] / 2 - imageHeight / 2), \
                                 angle, True, self.getMarcasFrenado(), self.getMarcasTierra(), logic_track, self.laps,
                                 sounds, sound_channels, self.loadImage(ghost, alpha=True), checksum, scoreconfig,
                                 username, tracktitle,
                                 self.objetives, automatic, self.getMapLimits(), self.window, gameConfig, browser,
                                 **kwargs)
        else:
            self.enemies.append(Player(type, self.loadImage(texture, **kwargs), self.loadImage(shadow, alpha=True), \
                                       pos, angle, False, self.getMarcasFrenado(), self.getMarcasTierra(), logic_track,
                                       self.laps, sounds, sound_channels, self.loadImage(ghost, alpha=True), checksum,
                                       scoreconfig, username, tracktitle, self.objetives, automatic,
                                       self.getMapLimits(), self.window, gameConfig, browser, **kwargs))

    def addDecoration(self, texture, pos, **kwargs):
        """
        Función que agrega una decoración
        :param texture: Textura del objeto
        :param pos: Posición (x,y) en el mundo
        :param kwargs: Parámetros adicionales
        :return: void
        """
        self.decorations.append(gameObject(texture, 2, pos))

    def addMarcasFrenado(self, linea):
        """
        Función que agrega una marca de frenado
        :param linea: Línea a agregar
        :return: void
        """
        self.marcas_frenado.append(linea)

    def addMarcasTierra(self, linea):
        """
        Función que agrega una marca en la tierra
        :param linea: Línea a agregar
        :return: void
        """
        self.marcas_tierra.append(linea)

    def addTrack(self, texture, pos, **kwargs):
        """
        Función que agrega una pista al circuito
        :param texture: Textura de la pista
        :param pos: Posición (x,y) en el mundo
        :param kwargs: Parámetros adicionales
        :return: void
        """
        image = texture
        width, height = image.get_size()
        self.track.append(gameObject(image, 1, pos))
        self.track_coords.append(
            [(self.window.getWindowWidth() / 2 - pos[0], self.window.getWindowHeight() / 2 - pos[1]), \
             (self.window.getWindowWidth() / 2 - pos[0] + width, self.window.getWindowHeight() / 2 - pos[1] + height)])

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

    def getBackground(self):
        """
        Función que retorna el fondo de la pista
        :return: void
        """
        return self.background

    def getBackgroundSize(self):
        """
        Función que retorna el tamaño del fondo
        :return: Tupla (w,h)
        """
        return self.backgroundSize

    def getBackgroundTeselation(self):
        """
        Función que retorna las veces que hay que dibujar en ambos ejes
        :return: Integer
        """
        return self.backgroundTesel

    def getDecorations(self):
        """
        Función que retorna las decoraciones
        :return: Lista de <object>
        """
        return self.decorations

    def getLaps(self):
        """
        Retorna el numero de vueltas del circuito
        :return: Integer
        """
        return self.laps

    def getPlayer(self):
        """
        Función que retorna al jugador
        :return: Objeto <player>
        """
        return self.player

    def getMarcasFrenado(self):
        """
        Función que retorna las marcas de frenado en la pista
        :return: Lista
        """
        return self.marcas_frenado

    def getMarcasTierra(self):
        """
        Función que retorna las marcas de la tierra
        :return: Lista
        """
        return self.marcas_tierra

    def getMapLimits(self):
        """
        Función que retorna los limites del mapa
        :return: Tupla (w,h)
        """
        return self.mapLimits

    def getTrackTitle(self):
        """
        Retorna el título del mapa
        :return: String
        """
        return self.title

    def getTrack(self):
        """
        Función que retorna la pista
        :return: Objeto <track>
        """
        return self.track

    def getTrackLogic(self):
        """
        Función que retorna la pista lógica
        :return: Retorna las coordenadas de cada elemento de la pista
        """
        return self.track_coords

    def loadImage(self, texture_name, color_key=(0, 0, 0), **kwargs):
        """
        Función que carga una imagen
        :param texture_name: Dirección física de la textura
        :param color_key: �?ndice de color
        :param kwargs: Parámetros adicionales
        :return: Objeto imagen
        """
        # Si la imagen no ha sido cargada entonces se carga y se guarda
        if texture_name not in self.images.keys():
            if kwargs.get("alpha"):
                image = pygame.image.load(getImages(texture_name)).convert_alpha()
            else:
                image = pygame.image.load(getImages(texture_name)).convert(32)
                image.set_colorkey(color_key)
            self.images[texture_name] = image
        return self.images[texture_name]

    def resultsSaved(self):
        """
        Función que retorna si se han calculado los resultados de la pista o no
        :return: booleano
        """
        return self.results

    def setBackground(self, texture):
        """
        Función que define el fondo a dibujar
        :param texture: Textura
        :return: void
        """
        self.background = texture
        self.backgroundSize = texture.get_size()

    def setMapLimits(self, x1, y1, x2, y2):
        """
        Función que define las coordenadas máximas del mapa
        :param x1: Posición x mínima
        :param y1: Posición y mínima
        :param x2: Posición x máxima
        :param y2: Posición y máxima
        :return: void
        """
        self.mapLimits = [x1, y1, x2, y2]

    def setLaps(self, laps):
        """
        Función que define la cantidad de vueltas del mapa
        :param laps: Número de vueltas
        :return: void
        """
        self.laps = laps

    def setObjetives(self, objetives):
        """
        Función que define los objetivos del mapa
        :param objetives: Lista de objetivos
        :return: void
        """
        self.objetives = objetives

    def setTitle(self, title):
        """
        Función que establece el nombre del mapa
        :param title: Título del mapa
        :return: void
        """
        self.title = title
