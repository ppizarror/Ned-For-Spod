#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__': from path import *  # @UnusedWildImport

# WORLD
# maneja distintos mapas
#
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
from bin import pygame
from bin.browser import Browser, HREF_HEADERS
from bin.errors import ERROR_HEADER, throw, ERROR_TRACKNOTEXIST  # @UnusedImport
from player import Player  # @UnusedImport
from resources.images import getImages
from resources.sounds import getSounds
from track import mapTrack

# Definición de constantes
NEXT_TRACK = -1
TRACKS = {
    1: "El origen",
    2: "Serona rw",
    3: "Riverside intl",
    4: "Santiago intl"
}


def getNextTrack(index):
    """
    Retorna el siguiente elemento de la lista de pistas
    :param index: Indice del diccionario
    :return: Llave o -1
    """
    keys = TRACKS.keys()
    if index in keys:
        return keys[(keys.index(index) + 1) % len(keys)]
    else:
        return -1


class World:
    """Mundo lógico"""

    def __init__(self, configWorld, configMap, window, checksum, scoreConfig, userConfig, lang, gameConfig, **kwargs):
        """
        Función constructora
        :param configWorld: Configuraciones del mundo
        :param configMap: Configuraciones del mapa
        :param window: Ventana de la aplicación
        :param checksum: Checksum de la aplicación
        :param scoreConfig: Configuraciones del scoreboard
        :param userConfig: Configuraciones del usuario
        :param lang: Diccionario de idioma
        :param gameConfig: Configuraciones del juego
        :param kwargs: Parámetros adicionales
        :return: void
        """

        # Se define si se imprime o no en consola
        if kwargs.get("verbose"):
            self.verbose = True
        else:
            self.verbose = False
        # Variables de clase
        self.actualMap = None  # mapa actual
        self.actualMapIndex = -1  # indice del mapa actual
        self.checksum = checksum  # checksum del juego
        self.configMap = configMap  # configuraciones de los mapas
        self.configWorld = configWorld  # configuración del mundo
        self.gameConfig = gameConfig  # configuraciones del juego
        self.images = {}  # Imagenes del juego
        self.langs = lang  # Idioma del juego
        self.playerName = userConfig.getValue("NAME")  # nombre del jugador
        self.scoreConfig = scoreConfig  # configuraciones del scoreboard
        self.userConfig = userConfig  # configuraciones del usuario
        self.window = window  # ventana del programa
        # Se cargan los sonidos
        self.sound_state = gameConfig.isTrue("ENABLESOUND")  # define si se activan los sonidos o no
        self.sounds = [[self.loadSound("m1"), self.loadSound("n"), self.loadSound("m1"), self.loadSound("m2"),
                        self.loadSound("m3"), \
                        self.loadSound("m4"), self.loadSound("m5")], \
                       [self.loadSound("r1"), self.loadSound("n"), self.loadSound("r1"), self.loadSound("r2"),
                        self.loadSound("r3"), self.loadSound("r4"), \
                        self.loadSound("r5")], \
                       self.loadSound("offroad"), \
                       [self.loadSound("track1"), self.loadSound("track2"), self.loadSound("track3")], \
                       self.loadSound("results"), \
                       self.loadSound("intro"), \
                       self.loadSound("wheelborder")
                       ]
        self.soundsChannel = [pygame.mixer.Channel(0), pygame.mixer.Channel(1), pygame.mixer.Channel(2),
                              pygame.mixer.Channel(3)]
        # Se configuran los canales de sonido
        for i in range(len(self.soundsChannel)):
            self.soundsChannel[i].set_volume(float(self.configWorld.getValue("CHANNEL_" + str(i))))
        # Se crea el navegador web
        self.browser = Browser()
        self.browser.addHeaders(HREF_HEADERS)

    def clearActualMap(self):
        """
        Borra el mapa actual
        :return: void
        """
        if self.actualMap is not None:
            self.actualMap.clean()

    def getActualIndex(self):
        """
        Retorna el índice del mapa actual
        :return: void
        """
        return self.actualMapIndex

    def getActualMap(self):
        """
        Retorna el mapa actual
        :return: Objeto <track>
        """
        return self.actualMap

    def loadImage(self, texture_name, color_key=(0, 0, 0), **kwargs):
        """
        Función que carga una imagen
        :param texture_name: Path de la textura
        :param color_key: Tono de color
        :param kwargs: Parámetros adicionales
        :return: Imagen
        """
        # Si la imagen no ha sido cargada entonces se carga y se guarda
        # Si se rota
        if kwargs.get("rotate"):
            texture_name_rot = texture_name + "_r" + str(kwargs.get("rotate"))
            if texture_name_rot not in self.images.keys():
                if self.verbose: print self.langs.get(55, texture_name)
                texture_path = getImages(texture_name)
                if texture_path != -1:
                    # Se obtiene el alpha
                    if kwargs.get("alpha"):
                        image = pygame.image.load(texture_path).convert_alpha()
                    else:
                        image = pygame.image.load(texture_path).convert(32)
                        image.set_colorkey(color_key)
                    image = pygame.transform.rotate(image, int(kwargs.get("rotate")))
                    self.images[texture_name_rot] = image
                else:
                    self.images[texture_name_rot] = pygame.image.load(getImages("missing")).convert_alpha()
                    if self.verbose: print self.lang.get(53, self.langs.get(51, texture_name))
            return self.images[texture_name_rot]
        # Si no se rota
        else:
            if texture_name not in self.images.keys():
                if self.verbose: print self.langs.get(55, texture_name)
                texture_path = getImages(texture_name)
                if texture_path != -1:
                    # Se obtiene el alpha
                    if kwargs.get("alpha"):
                        image = pygame.image.load(texture_path).convert_alpha()
                    else:
                        image = pygame.image.load(texture_path).convert(32)
                        image.set_colorkey(color_key)
                    self.images[texture_name] = image
                else:
                    self.images[texture_name] = pygame.image.load(getImages("missing")).convert_alpha()
                    if self.verbose: print self.lang.get(53, self.langs.get(51, texture_name))
            return self.images[texture_name]

    def loadMap(self, index=None):
        """
        Crea un mapa
        :param index: Indice de la pista a cargar
        :return: void
        """
        if index is None:
            index = int(self.configMap.getValue("DEFAULTMAP"))
        else:
            if index == NEXT_TRACK: index = getNextTrack(self.actualMapIndex)
        # Si el indice no existe
        if index not in TRACKS.keys(): throw(ERROR_TRACKNOTEXIST, index)
        self.actualMapIndex = index
        # Se crea el objeto
        self.actualMap = mapTrack(self.configMap, self.window)
        # Se define el titulo del mapa
        self.actualMap.setTitle(TRACKS[index])
        if self.verbose: print self.langs.get(56, self.actualMap.getTrackTitle())

        # Pista 1 - El origen
        if index == 1:
            try:
                # Se definen los límites del mapas
                self.actualMap.setMapLimits(-2500, -2200, 3200, 3200)
                # Se definen las vueltas máximas
                self.actualMap.setLaps(3)
                # Se definen los objetivos del mapa
                self.actualMap.setObjetives([(17.5, 19.5, 23.5), (17.0, 19.2, 22.5), (15.5, 17.1, 20.0)])
                # Se define el fondo del mundo
                self.actualMap.setBackground(self.loadImage("grass", alpha=False))
                # Se agrega al jugador
                self.actualMap.addCar(int(self.userConfig.getValue("TYPECAR")), self.userConfig.getValue("TEXTURE"),
                                      True, 0, True, self.actualMap.getTrackLogic(), \
                                      self.sounds, self.soundsChannel, self.checksum, self.scoreConfig, self.playerName,
                                      self.actualMap.getTrackTitle(), self.gameConfig, self.browser, rotate=-270,
                                      verbose=self.verbose)
                # Se agregan decoraciones
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1650, 0))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1400, -250))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1440, 300))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (800, 100))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (750, -300))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (650, -600))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-600, -600))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-600, -1200))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-400, -1400))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-180, -150))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1350, -1250))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (180, -800))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (180, 500))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (180, 500))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-450, 550))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1300, 750))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1200, 0))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (0, 1300))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (700, 1280))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1400, 1080))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (793, -1607))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1603, -677))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1483, 523))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (283, 1453))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (913, 1363))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1397, 943))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1067, -167))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-1037, 1363))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-1577, 343))
                # Se agregan los caminos
                self.actualMap.addTrack(self.loadImage("goal_w", alpha=True, rotate=180), (100, 200))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (500, 200))
                self.actualMap.addTrack(self.loadImage("c2_1", alpha=True), (500, -200))
                self.actualMap.addTrack(self.loadImage("c4_4", alpha=True), (100, -300))
                self.actualMap.addTrack(self.loadImage("c3_2", alpha=True), (-100, -1000))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (200, -1185))
                self.actualMap.addTrack(self.loadImage("rect_w_2", alpha=True), (500, -1185))
                self.actualMap.addTrack(self.loadImage("c2_3", alpha=True), (1100, -900))
                self.actualMap.addTrack(self.loadImage("rect_h_4", alpha=True), (1100, -600))
                self.actualMap.addTrack(self.loadImage("rect_h", alpha=True), (1100, -300))
                self.actualMap.addTrack(self.loadImage("rect_h", alpha=True), (1100, 0))
                self.actualMap.addTrack(self.loadImage("rect_h", alpha=True), (1100, 300))
                self.actualMap.addTrack(self.loadImage("rect_h_1", alpha=True), (1100, 600))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (1100, 1000))
                self.actualMap.addTrack(self.loadImage("rect_w_3", alpha=True), (700, 1000))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (400, 1000))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (200, 1000))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-100, 1000))
                self.actualMap.addTrack(self.loadImage("rect_w_4", alpha=True), (-400, 1000))
                self.actualMap.addTrack(self.loadImage("c4_2", alpha=True), (-700, 1000))
                self.actualMap.addTrack(self.loadImage("c3_3", alpha=True), (-600, 500))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (-300, 215))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-100, 200))
                # Se define la posición inicial del jugador
                self.actualMap.player.setDefaultPos((400, 350))
            except:
                print self.langs.get(53, self.langs.get(57, self.actualMap.getTrackTitle()))
                self.clearActualMap()
        # Pista 2 - Adelaide raceway
        elif index == 2:
            try:
                # Se definen los límites del mapas
                self.actualMap.setMapLimits(-3500, -2700, 5000, 1400)
                # Se definen las vueltas máximas
                self.actualMap.setLaps(3)
                # Se definen los objetivos del mapa
                self.actualMap.setObjetives([(28.8, 30.5, 32.9), (23.5, 25.0, 27.9), (21.3, 23.0, 24.5)])
                # Se define el fondo del mundo
                self.actualMap.setBackground(self.loadImage("sand3", alpha=False))
                # Se agrega al jugador
                self.actualMap.addCar(int(self.userConfig.getValue("TYPECAR")), self.userConfig.getValue("TEXTURE"),
                                      True, 180, True, self.actualMap.getTrackLogic(), \
                                      self.sounds, self.soundsChannel, self.checksum, self.scoreConfig, self.playerName,
                                      self.actualMap.getTrackTitle(), self.gameConfig, self.browser, rotate=-270,
                                      verbose=self.verbose)
                # Se agregan decoraciones
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (1400, 1000))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-2200, 1000))
                self.actualMap.addDecoration(self.loadImage("tree5", alpha=True), (-3000, 500))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (0, -150))
                self.actualMap.addDecoration(self.loadImage("tree5", alpha=True), (-2000, -140))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (1600, 100))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (600, 500))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-1500, 480))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-3000, 1200))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-1600, 2000))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-350, 950))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (1000, 1600))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (2600, 1000))
                self.actualMap.addDecoration(self.loadImage("tree5", alpha=True), (1693, 1573))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-767, -227))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-1667, -257))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-3227, 643))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-2627, 1993))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (2203, 403))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-737, 1303))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (-1007, 583))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (523, 913))
                self.actualMap.addDecoration(self.loadImage("tree3", alpha=True), (223, 1573))
                self.actualMap.addDecoration(self.loadImage("tree5", alpha=True), (-2687, -47))
                self.actualMap.addDecoration(self.loadImage("tree5", alpha=True), (2323, 1393))
                self.actualMap.addDecoration(self.loadImage("tree5", alpha=True), (-1367, 1363))
                self.actualMap.addDecoration(self.loadImage("tree5", alpha=True), (163, 433))
                # Se agregan los caminos
                self.actualMap.addTrack(self.loadImage("goal_w", alpha=True, rotate=0), (100, 200))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-200, 200))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-500, 200))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-800, 200))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-1100, 200))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-1300, 200))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-1600, 200))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (-1900, 215))
                self.actualMap.addTrack(self.loadImage("c3_4", alpha=True), (-2200, 600))
                self.actualMap.addTrack(self.loadImage("rect_h_3", alpha=True), (-2585, 900))
                self.actualMap.addTrack(self.loadImage("rect_h_2", alpha=True), (-2585, 1200))
                self.actualMap.addTrack(self.loadImage("c4_4", alpha=True), (-2200, 1900))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (-1800, 1900))
                self.actualMap.addTrack(self.loadImage("rect_h_1", alpha=True), (-1800, 1500))
                self.actualMap.addTrack(self.loadImage("c3_2", alpha=True), (-1600, 1200))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (-1300, 1015))
                self.actualMap.addTrack(self.loadImage("rect_w_3", alpha=True), (-1000, 1000))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (-600, 1000))
                self.actualMap.addTrack(self.loadImage("c3_1", alpha=True), (-500, 600))
                self.actualMap.addTrack(self.loadImage("c2_2", alpha=True), (0, 700))
                self.actualMap.addTrack(self.loadImage("c4_3", alpha=True), (300, 1300))
                self.actualMap.addTrack(self.loadImage("rect_w_4", alpha=True), (600, 1300))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (900, 1300))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (1200, 1300))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (1500, 1300))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (1800, 1300))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (2200, 1300))
                self.actualMap.addTrack(self.loadImage("c2_1", alpha=True), (2200, 900))
                self.actualMap.addTrack(self.loadImage("rect_w_2", alpha=True), (1800, 815))
                self.actualMap.addTrack(self.loadImage("c4_1", alpha=True), (1500, 800))
                self.actualMap.addTrack(self.loadImage("c2_2", alpha=True), (1400, 400))
                self.actualMap.addTrack(self.loadImage("rect_w_2", alpha=True), (900, 215))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (600, 200))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (300, 200))
                # Se define la posición inicial del jugador
                self.actualMap.player.setDefaultPos((490, 350))
            except:
                print self.langs.get(53, self.langs.get(57, self.actualMap.getTrackTitle()))
                self.clearActualMap()
        # Pista 3 - Riverside intl
        elif index == 3:
            try:
                # Se definen los límites del mapas
                self.actualMap.setMapLimits(-3500, -2700, 5300, 2000)
                # Se definen las vueltas máximas
                self.actualMap.setLaps(3)
                # Se definen los objetivos del mapa
                self.actualMap.setObjetives([(37.2, 38.6, 40.0), (33.2, 35.6, 38.9), (31.4, 32.9, 34.6)])
                # Se define el fondo del mundo
                self.actualMap.setBackground(self.loadImage("grass5", alpha=False))
                # Se agrega al jugador
                self.actualMap.addCar(int(self.userConfig.getValue("TYPECAR")), self.userConfig.getValue("TEXTURE"),
                                      True, 180, True, self.actualMap.getTrackLogic(), \
                                      self.sounds, self.soundsChannel, self.checksum, self.scoreConfig, self.playerName,
                                      self.actualMap.getTrackTitle(), self.gameConfig, self.browser, rotate=-270,
                                      verbose=self.verbose)
                # Se agregan decoraciones
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (0, -300))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1500, -300))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-300, 300))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (1300, -320))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-2800, -200))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-2340, -700))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-3300, -700))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-3200, 470))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1200, -1163))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-3270, 1100))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-3000, 1883))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1950, 2000))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-690, 1850))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (180, 1490))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (1050, 1883))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1560, 1520))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (2670, 1343))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1080, 683))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-2220, 1193))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (570, 893))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-300, 833))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (2700, -127))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (2900, 653))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1230, 1193))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1560, 773))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (2130, 533))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1110, 233))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-1200, 233))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-2850, 683))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (480, 2213))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (1620, 383))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-3660, -517))
                # Se agregan los caminos
                self.actualMap.addTrack(self.loadImage("goal_w", alpha=True), (0, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-300, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-600, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-900, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-1200, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-1500, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-1800, 0))
                self.actualMap.addTrack(self.loadImage("rect_w_4", alpha=True), (-2100, 0))
                self.actualMap.addTrack(self.loadImage("c4_1", alpha=True), (-2400, 0))
                self.actualMap.addTrack(self.loadImage("c2_1", alpha=True), (-2500, -400))
                self.actualMap.addTrack(self.loadImage("c3_2", alpha=True), (-2900, -300))
                self.actualMap.addTrack(self.loadImage("c4_4", alpha=True), (-2700, 400))
                self.actualMap.addTrack(self.loadImage("rect_w_4", alpha=True), (-2400, 400))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-2100, 400))
                self.actualMap.addTrack(self.loadImage("rect_w_2", alpha=True), (-1800, 415))
                self.actualMap.addTrack(self.loadImage("c2_1", alpha=True), (-1400, 500))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (-1400, 900))
                self.actualMap.addTrack(self.loadImage("rect_w_3", alpha=True), (-1800, 900))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (-2100, 915))
                self.actualMap.addTrack(self.loadImage("c3_4", alpha=True), (-2400, 1300))
                self.actualMap.addTrack(self.loadImage("c4_1", alpha=True), (-2700, 1700))
                self.actualMap.addTrack(self.loadImage("rect_w_4", alpha=True), (-2400, 1700))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-2100, 1700))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-1800, 1700))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-1500, 1700))
                self.actualMap.addTrack(self.loadImage("rect_w_3", alpha=True), (-1200, 1700))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (-800, 1700))
                self.actualMap.addTrack(self.loadImage("c3_1", alpha=True), (-700, 1300))
                self.actualMap.addTrack(self.loadImage("c2_1", alpha=True), (-300, 1300))
                self.actualMap.addTrack(self.loadImage("c4_4", alpha=True), (100, 2000))
                self.actualMap.addTrack(self.loadImage("c1_4", alpha=True), (800, 2000))
                self.actualMap.addTrack(self.loadImage("c3_1", alpha=True), (900, 1300))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (1200, 1215))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (1500, 1200))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (1800, 1200))
                self.actualMap.addTrack(self.loadImage("rect_w_3", alpha=True), (2100, 1200))
                self.actualMap.addTrack(self.loadImage("c1_2", alpha=True), (2600, 1200))
                self.actualMap.addTrack(self.loadImage("rect_h", alpha=True), (2600, 700))
                self.actualMap.addTrack(self.loadImage("c2_4", alpha=True), (2600, 400))
                self.actualMap.addTrack(self.loadImage("rect_w_2", alpha=True), (1900, 15))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (1600, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (1300, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (1000, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (700, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (500, 0))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (300, 0))
                # Se define la posición inicial del jugador
                self.actualMap.player.setDefaultPos((387, 150))
            except:
                print self.langs.get(53, self.langs.get(57, self.actualMap.getTrackTitle()))
                self.clearActualMap()
        # Santiago intl
        elif index == 4:
            try:
                # Se definen los límites del mapas
                self.actualMap.setMapLimits(-4400, -3500, 5500, 2500)
                # Se definen las vueltas máximas
                self.actualMap.setLaps(3)
                # Se definen los objetivos del mapa
                self.actualMap.setObjetives([(49.3, 51.0, 53.0), (50.0, 53.5, 58.6), (49.0, 50.5, 52.0)])
                # Se define el fondo del mundo
                self.actualMap.setBackground(self.loadImage("grass", alpha=False))
                # Se agrega al jugador
                self.actualMap.addCar(int(self.userConfig.getValue("TYPECAR")), self.userConfig.getValue("TEXTURE"),
                                      True, 270, True, self.actualMap.getTrackLogic(), \
                                      self.sounds, self.soundsChannel, self.checksum, self.scoreConfig, self.playerName,
                                      self.actualMap.getTrackTitle(), self.gameConfig, self.browser, rotate=-270,
                                      verbose=self.verbose)
                # Se agregan decoraciones
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-457, 433))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-1147, 493))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-997, -317))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1297, -407))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-2977, 643))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1717, -1067))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-427, -1187))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (503, -917))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (2603, -317))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (713, 793))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1253, 1213))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (2003, 2083))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (2123, 1123))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1853, 493))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-637, 703))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1987, 463))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-2647, 553))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-2257, 1153))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-2257, 1843))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1987, 2083))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-2677, 2683))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-1537, 2713))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1117, 1993))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-337, 1423))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (293, 313))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (1253, -347))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (2003, -467))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (3233, 253))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (3593, -467))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (3083, -1187))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-1207, 1153))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1987, 583))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-1327, -167))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-2077, -300))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-2677, 853))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-3037, 1513))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-3667, 1153))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-3847, 583))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1643, -1067))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (683, -857))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-2437, -197))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-3097, 2173))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-1867, 1423))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (323, 1603))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (803, 2353))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (2153, 1513))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (773, 283))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1703, -287))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (2903, 493))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-157, -1397))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-787, -1127))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (-3607, 73))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (443, 493))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-37, 1573))
                self.actualMap.addDecoration(self.loadImage("tree0", alpha=True), (1673, 2563))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (983, 973))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (3383, -257))
                self.actualMap.addDecoration(self.loadImage("tree1", alpha=True), (-247, -1067))
                # Se agregan los caminos
                self.actualMap.addTrack(self.loadImage("goal_h", alpha=True), (0, 0))
                self.actualMap.addTrack(self.loadImage("rect_h", alpha=True), (0, 300))
                self.actualMap.addTrack(self.loadImage("rect_h", alpha=True), (0, 600))
                self.actualMap.addTrack(self.loadImage("c4_4", alpha=True), (400, 1300))
                self.actualMap.addTrack(self.loadImage("c2_4", alpha=True), (1100, 1700))
                self.actualMap.addTrack(self.loadImage("c4_2", alpha=True), (1300, 2200))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (1700, 2200))
                self.actualMap.addTrack(self.loadImage("rect_h_1", alpha=True), (1700, 1800))
                self.actualMap.addTrack(self.loadImage("rect_h", alpha=True), (1700, 1500))
                self.actualMap.addTrack(self.loadImage("rect_h_4", alpha=True), (1700, 1200))
                self.actualMap.addTrack(self.loadImage("c2_1", alpha=True), (1700, 900))
                self.actualMap.addTrack(self.loadImage("c4_1", alpha=True), (1300, 800))
                self.actualMap.addTrack(self.loadImage("c3_3", alpha=True), (1500, 400))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (1800, 115))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (2100, 100))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (2400, 100))
                self.actualMap.addTrack(self.loadImage("rect_w_3", alpha=True), (2700, 100))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (3100, 100))
                self.actualMap.addTrack(self.loadImage("rect_h", alpha=True), (3100, -300))
                self.actualMap.addTrack(self.loadImage("c2_1", alpha=True), (3100, -600))
                self.actualMap.addTrack(self.loadImage("rect_w_2", alpha=True), (2700, -685))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (2400, -700))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (2100, -700))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (1800, -700))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (1500, -685))
                self.actualMap.addTrack(self.loadImage("c3_3", alpha=True), (1200, -400))
                self.actualMap.addTrack(self.loadImage("c1_1", alpha=True), (900, 0))
                self.actualMap.addTrack(self.loadImage("c4_1", alpha=True), (500, 0))
                self.actualMap.addTrack(self.loadImage("c2_3", alpha=True), (400, -400))
                self.actualMap.addTrack(self.loadImage("rect_w_2", alpha=True), (-200, -685))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-500, -700))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-800, -700))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (-1100, -685))
                self.actualMap.addTrack(self.loadImage("c3_3", alpha=True), (-1400, -400))
                self.actualMap.addTrack(self.loadImage("c1_3", alpha=True), (-1700, 200))
                self.actualMap.addTrack(self.loadImage("rect_w_3", alpha=True), (-2300, 200))
                self.actualMap.addTrack(self.loadImage("rect_w_1", alpha=True), (-2600, 215))
                self.actualMap.addTrack(self.loadImage("c3_4", alpha=True), (-2900, 600))
                self.actualMap.addTrack(self.loadImage("c4_3", alpha=True), (-3000, 1200))
                self.actualMap.addTrack(self.loadImage("c2_2", alpha=True), (-2500, 1400))
                self.actualMap.addTrack(self.loadImage("rect_h_4", alpha=True), (-2500, 1700))
                self.actualMap.addTrack(self.loadImage("rect_h_2", alpha=True), (-2485, 2000))
                self.actualMap.addTrack(self.loadImage("c4_3", alpha=True), (-2200, 2600))
                self.actualMap.addTrack(self.loadImage("c1_3", alpha=True), (-1600, 2600))
                self.actualMap.addTrack(self.loadImage("c3_4", alpha=True), (-1200, 2000))
                self.actualMap.addTrack(self.loadImage("c1_2", alpha=True), (-700, 1600))
                self.actualMap.addTrack(self.loadImage("c2_2", alpha=True), (-700, 1100))
                self.actualMap.addTrack(self.loadImage("c4_3", alpha=True), (-1200, 900))
                self.actualMap.addTrack(self.loadImage("c3_1", alpha=True), (-1400, 300))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-1100, 200))
                self.actualMap.addTrack(self.loadImage("rect_w", alpha=True), (-900, 200))
                self.actualMap.addTrack(self.loadImage("c1_2", alpha=True), (-500, 200))
                self.actualMap.addTrack(self.loadImage("c3_1", alpha=True), (-400, -300))
                self.actualMap.addTrack(self.loadImage("c2_1", alpha=True), (0, -300))
                # Se define la posición inicial del jugador
                self.actualMap.player.setDefaultPos((350, 110))
            except:
                print self.langs.get(53, self.langs.get(57, self.actualMap.getTrackTitle()))
                self.clearActualMap()

    def loadSound(self, sound_file):
        """
        Carga un sonido
        :param sound_file: Archivo de sonido
        :return: Sonido
        """
        try:
            if self.verbose: print self.langs.get(52, sound_file)
            return pygame.mixer.Sound(getSounds(sound_file))
        except:
            if self.verbose: print self.langs.get(53, self.langs.get(54, sound_file))
            return pygame.mixer.Sound()
