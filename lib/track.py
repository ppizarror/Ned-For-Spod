#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__': from path import *

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

    # Función constructora
    def __init__(self, config, window, **kwargs):
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

    # Función que añade un auto al modelo
    def addCar(self, type, texture, automatic, angle, player, logic_track, sounds, sound_channels, checksum, scoreconfig, username, tracktitle, gameConfig, **kwargs):
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
            self.player = Player(type, image, self.loadImage(shadow, alpha=True), (pos[0] / 2 - imageWidth / 2, pos[1] / 2 - imageHeight / 2), \
                              angle, True, self.getMarcasFrenado(), self.getMarcasTierra(), logic_track, self.laps, sounds, sound_channels, \
                              self.loadImage(ghost, alpha=True), checksum, scoreconfig, username, tracktitle, self.objetives, automatic, self.getMapLimits(), \
                              self.window, gameConfig, ** kwargs)
        else:
            self.enemies.append(Player(type, self.loadImage(texture, **kwargs), self.loadImage(shadow, alpha=True), \
                                    pos, angle, False, self.getMarcasFrenado(), self.getMarcasTierra(), logic_track, self.laps, sounds, sound_channels, \
                                    self.loadImage(ghost, alpha=True), checksum, scoreconfig, username, tracktitle, self.objetives, automatic, self.getMapLimits(), \
                                    self.window, gameConfig, ** kwargs))

    # Función que agrega una decoración
    def addDecoration(self, texture, pos, **kwargs):
        self.decorations.append(gameObject(texture, 2, pos))

    # Función que agrega una marca de frenado
    def addMarcasFrenado(self, linea):
        self.marcas_frenado.append(linea)

    # Función que agrega una marca en la tierra
    def addMarcasTierra(self, linea):
        self.marcas_tierra.append(linea)

    # Función que agrega una pista al circuito
    def addTrack(self, texture, pos, **kwargs):
        image = texture
        width, height = image.get_size()
        self.track.append(gameObject(image, 1, pos))
        self.track_coords.append([(self.window.getWindowWidth() / 2 - pos[0], self.window.getWindowHeight() / 2 - pos[1]), \
                                  (self.window.getWindowWidth() / 2 - pos[0] + width, self.window.getWindowHeight() / 2 - pos[1] + height)])

    # Función que elimina todos los datos
    def clean(self):
        try:
            # Se borran los datos
            del self.background, self.backgroundSize, self.decorations, self.mapLimits, \
            self.marcas_frenado, self.marcas_tierra, self.obstacles, self.title, self.track, self.track_coords
            # Se limpia el jugador y se borra
            self.player.clear()
            try: del self.player
            except: pass
        except: pass
        # Se borra
        del self

    # Función que retorna el fondo
    def getBackground(self):
        return self.background

    # Función que retorna el tamaño del fondo
    def getBackgroundSize(self):
        return self.backgroundSize

    # Función que retorna las veces que hay que dibujar en ambos ejes
    def getBackgroundTeselation(self):
        return self.backgroundTesel

    # Función que retorna las decoraciones
    def getDecorations(self):
        return self.decorations

    # Retorna el numero de vueltas del circuito
    def getLaps(self):
        return self.laps

    # Función que retorna al jugador
    def getPlayer(self):
        return self.player

    # Función que retorna las marcas de frenado en la pista
    def getMarcasFrenado(self):
        return self.marcas_frenado

    # Función que retorna las marcas de la tierra
    def getMarcasTierra(self):
        return self.marcas_tierra

    # Función que retorna los limites del mapa
    def getMapLimits(self):
        return self.mapLimits

    # Retorna el título del mapa
    def getTrackTitle(self):
        return self.title

    # Función que retorna la pista
    def getTrack(self):
        return self.track

    # Función que retorna la pista lógica
    def getTrackLogic(self):
        return self.track_coords

    # Función que carga una imagen
    def loadImage(self, texture_name, color_key=(0, 0, 0), **kwargs):
        # Si la imagen no ha sido cargada entonces se carga y se guarda
        if texture_name not in self.images.keys():
            if kwargs.get("alpha"):
                image = pygame.image.load(getImages(texture_name)).convert_alpha()
            else:
                image = pygame.image.load(getImages(texture_name)).convert(32)
                image.set_colorkey(color_key)
            self.images[texture_name] = image
        return self.images[texture_name]

    # Función que retorna si se han calculado los resultados de la pista o no
    def resultsSaved(self):
        return self.results

    # Función que define el fondo a dibujar
    def setBackground(self, texture):
        self.background = texture
        self.backgroundSize = texture.get_size()

    # Función que define las coordenadas máximas del mapa
    def setMapLimits(self, x1, y1, x2, y2):
        self.mapLimits = [x1, y1, x2, y2]

    # Función que define la cantidad de vueltas del mapa
    def setLaps(self, laps):
        self.laps = laps

    # Función que define los objetivos del mapa
    def setObjetives(self, objetives):
        self.objetives = objetives

    # Función que establece el nombre del mapa
    def setTitle(self, title):
        self.title = title
