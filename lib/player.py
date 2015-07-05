#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__': from path import *

# PLAYER
# Maneja lo que es un auto, sus texturas, propiedades y manejo lógico
# Maneja la comunicación con el servidor para el caso de los marcadores
#
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
from bin import pygame
from bin.browser import unescape
from bin.errors import *
from bin.utils import urlencode, Request, urlopen, getBetweenTags
from bin.hashdir import md5str
from math import sqrt
from operator import pos
import math
import random
import string

# Definición de constantes
ACELCONST = 300  # aceleracion por dt
AGARRECONST = 1  # agarre por defecto
BGREEN = (0, 200, 0)  # color verde claro
BLACK = (0, 0, 0, 100)  # color negro
BLUE = (0, 0, 255)  # color azul
BROWN = (139, 69, 19, 100)  # color cafe
CAMBIO = [-0.4, 1.15, 0.97, 0.84, 0.71, 0.59]  # taza de aceleración por cada cambio
CAMBIO_NEUTRO = "N"  # cambio neutro
CAMBIO_REVERSA = "R"  # cambio en reversa
DEFAULT_NAME_PLAYER = "Player"  # nombre por defecto del jugador
DESACELCONST = 200  # desaceleración por dt
DGREY = (25, 25, 25)  # color gris
D_BROWN = (117, 58, 16, 100)  # color cafe oscuro
GREEN = (0, 160, 0)  # color verde claro
HIGH = 1.5  # parámetro -alto- de los tipos de auto
LBLACK = (25, 25, 25, 100)  # color negro mas claro (para las frenadas)
LBLUE = (0, 200, 255)  # color azul claro
LGREY = (75, 75, 75)  # color azul oscuro
LLBLACK = (47, 47, 47, 100)  # color negro aún mas claro para las frenadas
LOW = 0.5  # parámetro -bajo- de los tipos de auto
LOWEST_VALUE_VEL_DESACEL = 1  # valor minimo de velocidad aceptado para las desaceleraciones
L_BROWN = (162, 80, 22, 100)  # clor cafe claro
MARK_DELETE_RANDOM = False  # Se borra de forma random
MAXANGVEL = [1.15, 1.10, 1.0]  # máxima velocidad angular
MAXROTVEL = [80, 140, 100]  # máxima velocidad de rotación
MAXVELCONST = 1000  # constante de velocidad máxima
MAX_GROUND_MARKS = 700  # número de marcas en la tierra
MAX_TRACK_MARKS = 800  # número de marcas en el asfalto
MAX_VEL_KMH = 250  # velocidad máxima en kilómetros por hora
MEDIUM = 1  # parámetro -medio- en los tipos de auto
METRICS = "km/h"  # indica el sistema metrico de unidad de medida para la velocidad
MID_LOW = 0.8  # coeficiente medio-bajo
MINROTVEL = 5  # mínima velocidad para rotar el auto
MIN_LENGTH_FRENADO = 10  # mínima distancia para mostrar las marcas en el asfalto
MIN_LENGTH_MARCA = 6  # mínima distancia para mostrar las marcas en la tierra
MIN_VEL_MARK_FRENADO = 50  # mínima velocidad para mostrar marcas en el asfalto
RED = (255, 0, 0)  # color rojo
ROCE = 120  # coeficiente de roce en el asfalto
ROCE_PASTO = 190  # coeficiente de roce en el pasto
ROTVEL = 80  # velocidad de rotación
SCOREBOARD_RED = (165, 0, 0, 128)  # color rojo del scoreboard
SCOREBOARD_WHITE = (255, 255, 255, 128)  # color blanco del scoreboard
SHADOW_PERCENTAGE = [0.06, 0.03]  # porcentaje de sombra
SOUND_TRACK_WHEEL = 0  # sonido a reproducir cuando se frena
SOUND_TRACK_WHEEL_HB = 1  # sonido del freno de mano
STATE_CORRECT = "SIG"  # indica que el jugador avanzó correctamente en la pista
STATE_INVALIDPOS = "INVALIDPOS"  # indica si se salió de la pista
STATE_NEWLAP = "NEWLAP"  # indica que el jugador completó la vuelta anterior
STATE_NULL = "NONE"  # indica ausencia de estado
STATE_OFFROAD = "OFFROAD"  # indica si el auto se salio de la pista
STATE_WRONGWAY = "WRONGWAY"  # indica que el jugador conduce en sentido inverso a la orientación de la pista
TIMETO_SHOW_FRENADO = 0.3  # tiempo que se debe presionar continuamente el botón de frenado para mostrar las marcas en el asfalto
TRACK_NOT_DEFINED = "$notdefined$"  # pista no definida
VALIDUSERNAME = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # caracteres válidos para un nombre de jugador online
VEL_PASTO = 60  # velocidad máxima en el pasto
WEB_BROWSER = True  # indica si se usa el navegador web pasado por argumento o no
WHITE = (255, 255, 255)  # color blanco


def absTrig(x):
    """
    Retorna 0 si el valor trigonometrico es muy pequeño
    :param x: Valor trigonométrico
    :return: double
    """
    if -0.001 < x < 0.001:
        return 0
    else:
        return abs(x)


def cos(x):
    """
    Función coseno en grados
    :param x: Grado sexagesimal
    :return: Coseno del grado x
    """
    return math.cos(math.radians(x))


def ecos(x):
    """
    Retorna el coseno con dirección especial
    :param x: Angulo x
    :return: Coseno de x modificado
    """
    return sgnCos(x) * absTrig(cos(x))


def esin(x):
    """
    Retorna el seno con direccion especial
    :param x: Angulo x
    :return: Seno de x modificado
    """
    return sgnSin(x) * absTrig(sin(x))


def hour(seg):
    """
    Retorna el tiempo en minutos y segundos para cada vuelta
    :param seg: Segundos
    :return: Tupla (min, seg)
    """
    return int(seg / 60), round(seg % 60, 1)


def minAng(ang):
    """
    Retorna el mínimo angulo de su cuadrante
    :param ang: Angulo
    :return: Angulo minimo del cuadrante
    """
    min = 360
    for i in range(5):
        if abs(90 * i - ang) < min:
            min = abs(90 * i - ang)
    return min


def rotatePoint(point, origin, theta):
    """
    Rota un punto con respecto a otro mediante un ángulo theta
    :param point: Punto a rotar
    :param origin: Origen de rotación
    :param theta: Desplazamiento angular de rotación
    :return: Punto (x,y) rotado en theta grados con respecto a origin
    """
    newx = cos(theta) * (point[0] - origin[0]) - sin(theta) * (point[1] - origin[1])
    newy = sin(theta) * (point[0] - origin[0]) + cos(theta) * (point[1] - origin[1])
    return int(newx + origin[0]), int(newy + origin[1])


def sin(x):
    """
    Función seno en grados sexagesimales
    :param x: Grado
    :return: Seno de x
    """
    return math.sin(math.radians(x))


def sgn(x):
    """
    Retorna el signo de x
    :param x: Valor numérico
    :return: Función sgn de x
    """
    if x > 0:
        return 1
    elif x == 0:
        return 0
    else:
        return -1


def sgnCos(angle):
    """
    Retorna la dirección del coseno
    :param angle: Angulo
    :return: valores -1, 0, 1
    """
    if 270 < angle <= 360 or 0 <= angle < 90:
        return 1
    elif 90 < angle < 270:
        return -1
    else:
        return 0


def sgnSin(angle):
    """
    Retorna la dirección del seno
    :param angle: Angulo
    :return: valores -1, 0, 1
    """
    if 0 < angle < 180:
        return -1
    elif 180 < angle < 360:
        return 1
    else:
        return 0


def stringCleaner(s):
    """
    Elimina todos los caracteres inválidos de un strig
    :param string: String a limpiar
    :return: String
    """
    return filter(lambda x: x in string.printable, s)


def validUsername(username):
    """
    Retorna un nombre de jugador válido para el scoreboard online
    :param username: Nombre de usuario
    :return: Nombre de usuario modificado
    """
    name = ""
    for caracter in username:
        if caracter in VALIDUSERNAME:
            name += caracter
    # Si no cumple con los requisitos minimos
    if 0 <= len(name) < 4:
        return DEFAULT_NAME_PLAYER
    else:
        return name[0:10]


class Player:
    """Objeto player, que representa cualquier entidad en el mapa"""

    # noinspection PyShadowingNames
    def __init__(self, type, texture, shadow_texture, pos, angle, playable, mark_track, mark_ground, logic_track,
                 totalLaps, sounds, sounds_channels, ghost, hash, scoreConfig, username, trackname, trackobjetives,
                 automatic, mapLimits, window, gameConfig, browser, **kwargs):
        """
        Función constructora
        :param type: Tipo de auto
        :param texture: Textura del auto
        :param shadow_texture: Textura de la sombra del auto
        :param pos: Posición (x,y) en el mapa
        :param angle: Angulo inicial del auto
        :param playable: Indica si es jugable por el usuario (caso contrario seria AI, aún no implementada)
        :param mark_track: Lista de marcas de frenado en la pista
        :param mark_ground: Lista de marcas de frenado en la tierra
        :param logic_track: Lista de entidades lógicas en la pista
        :param totalLaps: Vueltas totales
        :param sounds: Lista de sonidos
        :param sounds_channels: Lista de canales de sonido
        :param ghost: Lista de fantasma
        :param hash: Hash del programa
        :param scoreConfig: Configuraciones de la plataforma de scoreboard
        :param username: Nombre de usuario del jugador
        :param trackname: Nombre de la pista
        :param trackobjetives: Objetivos de la pista
        :param automatic: Indica si los cambios son automáticos o manuales
        :param mapLimits: Límites (xi,yi,xf,yf) de la pista
        :param window: Ventana del programa
        :param gameConfig: Configuraciones del juego
        :param browser: Navegador web
        :param kwargs: Argumentos adicionales
        :return: void
        """

        # Se define si se imprime o no en consola
        if kwargs.get("verbose"):
            self.verbose = True
        else:
            self.verbose = False
        # se definen variables independientes
        self.acel = []  # aceleracion del auto
        self.agarre = 0  # agarre del auto al suelo (para las curvas)
        self.angle = angle % 360  # angulo de rotacion del auto en radianes
        self.automatic = automatic  # transmision del auto automatica/manual
        self.browser = browser  # navegador web
        self.cambio = 0  # cambio del vehiculo
        self.defaultAngle = angle % 360  # ángulo por defecto
        self.desacel = 0  # frenado del auto
        self.drawablepos = (pos[0], pos[1])  # define la posicion inicial
        self.fastlap = [0, 0.0]  # vuelta rapida
        self.finished = False  # indica si ya se acabo el juego
        self.gameConfig = gameConfig  # se guarda la configuración del usuario
        self.ghost = None  # fantasma de la vuelta más rápida
        self.ghost_actual = []  # fantasma de la vuelta actual
        self.ghost_i = 0  # indice de dibujo del fantasma actual más rápido
        self.hash = hash  # hash del programa
        self.highVelocity = 0  # velocidad maxima alcanzada en toda la carrera
        self.initPos = (0, 0)  # posicion por default al partir un mapa
        self.lapCount = 1  # conteo de vueltas en la pista
        self.lapTime = 0  # tiempo de vuelta
        self.lastIndexTrack = 0  # ultimo indice visitado en la pista
        self.lastIndexTrackAng = angle % 360  # ultimo angulo visitado en la pista
        self.lastIndexTrackPos = pos  # posición del jugador
        self.lastcambio = 0  # último cambio efectuado
        self.lastdirangle = 0  # última dirección angular de rotación
        self.logic_track = logic_track  # lista de coordenadas de la pista actual
        self.mapLimits = mapLimits  # limites del mapa
        self.marcasFrenado = [None, None]  # frenados rueda 3, 4
        self.marcasFrenadoHB = [None, None]  # frenado de mano rueda 3,4
        self.marcasTierra = [None, None, None, None]  # marcas rueda 1, 2 ,3, 4
        self.maxangvel = 0  # máxima velocidad angular
        self.maxcambio = 0  # cambio máximo del auto
        self.maxrotvel = 0  # máxima velocidad de rotación
        self.maxvel = 0  # velocidad maxima del auto
        self.maxvelkmh = 0  # velocidad máxima en kilómetros por hora
        self.nextTrack = TRACK_NOT_DEFINED  # nombre de la siguiente pista a jugar
        self.playable = playable  # define si se puede controlar al auto o no
        self.pos_center = (0, 0)  # posición del centro
        self.posrueda_1 = (0, 0)  # posición rueda superior derecha
        self.posrueda_2 = (0, 0)  # posición rueda superior izquierda
        self.posrueda_3 = (0, 0)  # posición rueda inferior izquierda
        self.posrueda_4 = (0, 0)  # posición rueda inferior derecha
        self.posx = pos[0]  # posicion en x
        self.posy = pos[1]  # posicion en y
        self.roce = 0  # roce de las ruedas
        self.score = 0  # puntaje de la pista
        self.scoreBoardOnline = []  # scoreboard online
        self.scoreConfig = scoreConfig  # configuraciones de los puntajes
        self.scoreLink = scoreConfig.getValue("WEB_I")  # link del scoreboard
        self.soundGear = sounds[0]  # sonido del motor al acelerar
        self.soundGearChannel = sounds_channels[0]  # canal de sonido del motor
        self.soundGearPlaying = 0
        self.soundGearR = sounds[1]  # sonido del motor al frenar
        self.soundGroundChannel = sounds_channels[2]  # canal de los sonidos de la tierra
        self.soundMusicChannel = sounds_channels[3]  # canal de sonidos de fondo
        self.soundResults = sounds[4]  # sonido al terminar la carrera
        self.soundTrack = sounds[3]  # sonidos de llanta
        self.soundTrackOffroad = sounds[2]  # sonido en la tierra
        self.soundWheelsChannel = sounds_channels[1]  # canal de sonido de las ruedas en frenado
        self.sound_state = gameConfig.isTrue("ENABLESOUND")  # define si los sonidos estan activos
        self.texture = texture  # textura del auto
        self.texture_ghost = ghost  # textura del fantasma
        self.tiempoAcelerando = 0  # tiempo continuo de aceleración
        self.tiempoFrenado = 0  # tiempo continuo de frenado
        self.tiempoFrenoDeMano = 0  # freno continuo con freno de mano
        self.tiempoFuera = 0  # tiempo total fuera de la pista
        self.totalLaps = totalLaps  # vueltas totales del circuito
        self.totalTime = []  # tiempo por cada vuelta
        self.trackCheckPoint = 0  # indice de la pista que es checkpoint
        self.trackName = trackname  # nombre de la pista
        self.trackObjetives = trackobjetives  # objetivos de tiempo de la pista actual
        self.trackSize = 0  # largo del circuito
        self.type = type  # tipo de auto
        self.username = username  # nombre del usuario
        self.velcambios = []  # velocidades para cada cambio
        self.velx = 0  # velocidad en x
        self.vely = 0  # velocidad en y
        self.window = window  # ventana del juego
        # Se carga el tipo
        self.loadType(type)
        # Se obtiene el rectangulo de la imagen
        self.rect = self.texture.get_rect()
        # Se obtiene el tamaño de la imagen
        shadow_texture = pygame.transform.scale(shadow_texture,
                                                (int(shadow_texture.get_size()[0] * (1 + SHADOW_PERCENTAGE[0])), \
                                                 int(shadow_texture.get_size()[1] * (1 + SHADOW_PERCENTAGE[1]))))
        self.imagenRotada = self.texture  # textura de la imagen rotada
        self.imagenRotadaSize = self.texture.get_size()  # tamaño de la imagen rotada
        self.shadow_texture = shadow_texture  # textura de la sombra
        self.shadow_texture_rotada = shadow_texture  # textura de la sombra rotada
        self.shadow_texture_size = shadow_texture.get_size()  # tamaño de la sombra rotada
        self.width, self.height = self.texture.get_size()  # dimensiones de la imagen
        # Se obtienen las variables de la pista
        self.marks_track = mark_track  # marcas en la pista
        self.marks_ground = mark_ground  # marcas en la tierra
        # Si se pasa como parametro rotate se rota la imagen
        if kwargs.get("rotate"):
            self.shadow_texture = pygame.transform.rotate(self.shadow_texture, kwargs.get("rotate"))
            self.texture = pygame.transform.rotate(self.texture, kwargs.get("rotate"))
            self.texture_ghost = pygame.transform.rotate(self.texture_ghost, kwargs.get("rotate"))
        self.rotate(0, 0, False)
        # Se activa el sonido idle
        if self.sound_state:
            self.soundGearChannel.play(self.soundGear[1], -1)

    def acelerate(self, t):
        """
        Acelera el auto (modifica la aceleracion)
        :param t: Tiempo t
        :return: void
        """
        if self.getVel() < self.maxvel:
            if self.automatic:
                cambio = self.getCambio()
                if cambio == 0: cambio = 1
                self.velx += self.acel[cambio] * ecos(self.angle) * t
                self.vely += self.acel[cambio] * esin(self.angle) * t
                self.tiempoAcelerando += t
                self.highVelocity = max(self.highVelocity, self.getVel())
            else:
                cambio = self.cambio
                if cambio > 0 and 0 < self.getRevl() < 99:
                    if self.getVelKph() > self.velcambios[self.cambio]:
                        print "<TODO>FRENO:MOTOR"
                    self.velx += self.acel[cambio] * ecos(self.angle) * t
                    self.vely += self.acel[cambio] * esin(self.angle) * t
                    self.tiempoAcelerando += t
                    self.highVelocity = max(self.highVelocity, self.getVel())

    def bajarCambio(self):
        """
        Baja el cambio
        :return: void
        """
        if not self.automatic:
            self.cambio = max(0, self.cambio - 1)

    def checkTrack(self):
        """
        Comprueba que el auto esté en una cierta pista del mapa y retorna el indice de la pista colisionada
        :return: indice entre -1 y inf+
        """
        # Posición relativa en el mapa
        (pos_x, pos_y) = self.getRelativePos()
        # Se recorre toda la pista buscando la pista a la cual el auto está dentro
        index = 0
        for track in self.logic_track:
            if track[0][0] <= pos_x <= track[1][0] and track[0][1] <= pos_y <= track[1][1]: return index
            index += 1
        else:
            return -1  # codigo de error

    def checkTrackIndex(self, index):
        """
        Compreba que el auto esté en una región en particular del cirguito
        :param index: Indice que representa la posición en la pista
        :return: booleano True/False
        """
        # Posición relativa en el mapa
        (pos_x, pos_y) = self.getRelativePos()
        # Se recorre toda la pista buscando la pista a la cual el auto está dentro
        if index < self.trackSize:
            track = self.logic_track[index]
            if track[0][0] <= pos_x <= track[1][0] and track[0][1] <= pos_y <= track[1][1]:
                return True
            else:
                return False

    def clear(self, soundIdle=False):
        """
        Limpia todas las variables y deja el auto en la posición y angulos originales
        :param soundIdle: Indica si se deja el sonido del motor en indle
        :return: void
        """
        for i in range(len(self.marks_ground)):
            self.marks_ground.pop()
        for j in range(len(self.marks_track)):
            self.marks_track.pop()
        self.loadType(self.type)
        self.angle = self.defaultAngle
        self.marcasFrenado = [None, None]
        self.marcasFrenadoHB = [None, None]
        self.marcasTierra = [None, None, None, None]
        self.posx = self.initPos[0]
        self.posy = self.initPos[1]
        self.rotate(0, 0, False)
        self.velx = 0
        self.vely = 0
        self.lastcambio = 0
        self.tiempoAcelerando = 0
        self.tiempoFrenado = 0
        self.tiempoFrenoDeMano = 0
        self.lastdirangle = 0
        self.stopAcelerating()
        self.stopTrackMarking()
        self.stopTrackMarkingHB()
        self.tiempoFuera = 0
        self.lapCount = 1
        self.lapTime = 0
        self.soundMute()
        del self.ghost
        self.ghost = None
        del self.ghost_actual
        self.ghost_actual = []
        del self.totalTime
        self.totalTime = []
        self.trackCheckPoint = self.checkTrack()
        self.lastIndexTrack = self.trackCheckPoint  # se define el indice actual como el primero de la pista
        self.lastIndexTrackPos = self.initPos
        if self.sound_state and soundIdle:  # Si los sonidos estan activados se deja el sonido de motor en idle
            self.soundGearChannel.play(self.soundGear[1], -1)

    def collide(self, surface, t, **kwargs):
        """
        Comprueba colisiones con objetos
        :param surface: Superficie de dibujo
        :param t: Tiempo t
        :param kwargs: Parámetros adicionales
        :return: void
        """
        # Se obtiene el color del suelo bajo cada rueda
        ground_rueda1 = surface.get_at(self.pos_rueda1)
        ground_rueda2 = surface.get_at(self.pos_rueda2)
        ground_rueda3 = surface.get_at(self.pos_rueda3)
        ground_rueda4 = surface.get_at(self.pos_rueda4)
        p1 = self.groundTouch(self.rocePasto / 1.0, ground_rueda1, self.pos_rueda1, 0, t)
        p2 = self.groundTouch(self.rocePasto / 1.0, ground_rueda2, self.pos_rueda2, 1, t)
        p3 = self.groundTouch(self.rocePasto / 0.9, ground_rueda3, self.pos_rueda3, 2, t)
        p4 = self.groundTouch(self.rocePasto / 0.9, ground_rueda4, self.pos_rueda4, 3, t)
        if ((p1 or p2) or p3) or p4: self.tiempoFuera += t

    def desacelerate(self, acel, t, marks):
        """
        Frena el auto
        :param acel: Constante de desaceleración
        :param t: Tiempo t
        :param marks: Lista de marcas
        :return: void
        """
        prev_vel = self.getVel()
        if self.velx != 0: self.velx -= acel * ecos(self.angle) * t
        if self.vely != 0: self.vely -= acel * esin(self.angle) * t
        if abs(self.velx) < LOWEST_VALUE_VEL_DESACEL: self.velx = 0
        if abs(self.vely) < LOWEST_VALUE_VEL_DESACEL: self.vely = 0
        if self.getVel() > prev_vel:  # se comprueba que no se este acelerando
            self.velx = 0
            self.vely = 0
        else:  # si se desacelero
            if marks:
                self.tiempoFrenado += t
                if self.tiempoFrenado > TIMETO_SHOW_FRENADO and self.getVel() > MIN_VEL_MARK_FRENADO:
                    self.marcarFrenado(self.pos_rueda1, 0)
                    self.marcarFrenado(self.pos_rueda2, 1)
                else:
                    self.marcasFrenado = [None, None]

    def draw(self, surface, t, update, window, **kwargs):
        """
        Dibuja el auto
        :param surface: Superficie de dibujo
        :param t: Tiempo t
        :param update: Indica si actualizar los parámetros fisicos del auto
        :param window: Ventana de la aplicación
        :param kwargs: Parámetros adicionales
        :return: String con mensaje de estado
        """
        if update:
            msg = self.update(t)
        else:
            msg = STATE_NULL
        # Se dibuja el fantasma
        if self.ghost is not None and kwargs.get("show_ghost"):
            if self.ghost_i < len(self.ghost):
                ghost = self.ghost[self.ghost_i]
                ang = ghost[1]
                image = pygame.transform.rotate(self.texture_ghost, ang)
                width, height = image.get_size()
                # noinspection PyShadowingNames
                pos = (int((-window.getWindowWidth() / 2 + self.posx) + ghost[0][0] - (width - self.width) / 2), \
                       int((-window.getWindowHeight() / 2 + self.posy) + ghost[0][1] - (height - self.height) / 2))
                surface.blit(image, pos)
                self.ghost_i += 1
        # Se dibuja al jugador
        if self.playable:
            surface.blit(self.shadow_texture_rotada,
                         [int(self.drawablepos[0] - (self.shadow_texture_size[0] - self.width) / 2), \
                          int(self.drawablepos[1] - (self.shadow_texture_size[1] - self.height) / 2)])
            surface.blit(self.imagenRotada, [int(self.drawablepos[0] - (self.imagenRotadaSize[0] - self.width) / 2), \
                                             int(self.drawablepos[1] - (self.imagenRotadaSize[1] - self.height) / 2)])
        else:
            surface.blit(self.shadow_texture_rotada, [int(self.posx - (self.shadow_texture_size[0] - self.width) / 2), \
                                                      int(self.posy - (self.shadow_texture_size[1] - self.height) / 2)])
            surface.blit(self.imagenRotada, [int(self.posx - (self.imagenRotadaSize[0] - self.width) / 2), \
                                             int(self.posy - (self.imagenRotadaSize[1] - self.height) / 2)])
        # Si se dibujan las ruedas
        if kwargs.get("draw_ruedas"):
            pygame.draw.line(surface, (255, 255, 255), self.pos_center, (self.pos_center[0], self.pos_center[1] + 5), 5)
            pygame.draw.line(surface, (255, 255, 255), self.pos_rueda1, (self.pos_rueda1[0], self.pos_rueda1[1] + 5), 5)
            pygame.draw.line(surface, (255, 255, 255), self.pos_rueda2, (self.pos_rueda2[0], self.pos_rueda2[1] + 5), 5)
            pygame.draw.line(surface, (255, 255, 255), self.pos_rueda3, (self.pos_rueda3[0], self.pos_rueda3[1] + 5), 5)
            pygame.draw.line(surface, (255, 255, 255), self.pos_rueda4, (self.pos_rueda4[0], self.pos_rueda4[1] + 5), 5)
        # Si se dibuja el poligono lógico del auto
        if kwargs.get("draw_car"):
            pygame.draw.polygon(surface, (0, 0, 0),
                                [self.pos_rueda1, self.pos_rueda2, self.pos_rueda3, self.pos_rueda4])
        # Se añade el fantasma a la lista del fantasma actual
        if update:
            w1 = self.width / 2
            h1 = self.height / 2
            pos_x = int(-self.posx + 2 * self.drawablepos[0] + 2 * w1)
            pos_y = int(-self.posy + 3 * self.drawablepos[1] + 0.1 * h1) - self.width
            self.ghost_actual.append([(pos_x, pos_y), self.angle])
        return msg

    def finishedLap(self):
        """
        Determina si se termino la pista o no
        :return: booleano True/False
        """
        if self.lapCount > self.totalLaps:
            if not self.finished:
                self.soundGearChannel.stop()
                self.soundGroundChannel.stop()
                self.soundWheelsChannel.stop()
                if self.sound_state:
                    self.soundMusicChannel.play(self.soundResults, -1)
            self.finished = True
            return True
        else:
            return False

    def getAngle(self):
        """
        Retorna el angulo de rotación del auto
        :return: Angulo en grados sexagesimales
        """
        return self.angle

    def getCambio(self, v=None):
        """
        Retorna la marcha del auto
        :param v: Indica si la velocidad es en kph o la interna
        :return: Integer entre 0 1 inf+
        """
        if v is None:
            vel = self.getVelKph()
        else:
            vel = v
        if vel == 0:
            new_cambio = 0
        else:
            cambio = 1
            for velc in self.velcambios:
                if vel >= velc:
                    cambio += 1
                else:
                    break
            new_cambio = min(cambio, self.maxcambio - 1)
        # Se cambia el sonido si se modificó el cambio
        if new_cambio != self.lastcambio:
            # Se detiene el sonido anterior
            self.soundGearChannel.stop()
            # Si se acelera
            if self.tiempoAcelerando > 0:
                if self.sound_state:
                    self.soundGearChannel.play(self.soundGear[new_cambio + 1], -1)
                self.soundGearPlaying = 1
            # Si se desacelera
            else:
                if self.sound_state:
                    self.soundGearChannel.play(self.soundGearR[new_cambio + 1], -1)
                self.soundGearPlaying = -1
            self.lastcambio = new_cambio
        # Si no ha pasado el cambio
        else:
            # Si se está acelerando pero se tiene el sonido de bajar marcha se cambia
            if self.tiempoAcelerando > 0 and self.soundGearPlaying == -1:
                self.soundGearChannel.stop()
                if self.sound_state:
                    self.soundGearChannel.play(self.soundGear[self.lastcambio + 1], -1)
                self.soundGearPlaying = 1
            elif self.tiempoAcelerando == 0 and self.soundGearPlaying == 1:
                self.soundGearChannel.stop()
                if self.sound_state:
                    self.soundGearChannel.play(self.soundGearR[self.lastcambio + 1], -1)
                self.soundGearPlaying = -1
        if self.automatic:
            return new_cambio
        else:
            return self.cambio

    def getDesacel(self):
        """
        Retorna la desaceleración del auto
        :return: Double
        """
        return self.desacel

    def getFastLap(self):
        """
        Retorna la vuelta rápida del circuito
        :return: Tiempo de vuelta de la pista
        """
        return self.fastlap

    def getFastVel(self):
        """
        Retorna la velocidad máxima alcanzada
        :return: Double
        """
        return self.getVelKph(self.highVelocity)

    def getNextTrack(self):
        """
        Retorna la siguiente psita
        :return: Double
        """
        return self.nextTrack

    def getLapPos(self):
        """
        Retorna la vuelta actual en el circuito
        :return: Integer
        """
        return self.lapCount

    def getLapTime(self, t=None):
        """
        Retorna el tiempo de vuelta en un string imprimible
        :param t: Tiempo t
        :return: String con el formato xx:yy
        """
        if t is not None:
            tiempo = hour(t)
        else:
            tiempo = hour(self.lapTime)
        t = ""
        if tiempo[0] < 10: t += "0"
        t += str(tiempo[0])
        t += " :"
        if tiempo[1] < 10: t += "0"
        t += str(tiempo[1])
        return t

    def getLapTimeNoFormat(self):
        """
        Retorna el tiempo de vuelta sin formato
        :return: Double de tiempo en segundos
        """
        return self.lapTime

    def getScoreboardOnline(self):
        """
        Retorna el scoreboard online
        :return: Retorna una lista de puntajes imprimibles
        """
        return self.scoreBoardOnline

    def getPos(self):
        """
        Retorna la posición del auto
        :return: Tupla (x,y)
        """
        return self.posx, self.posy

    def getPuntaje(self):
        """
        Retorna el puntaje del jugador
        :return: Double
        """
        return self.score

    def getRelativePos(self):
        """
        Retorna la posición relativa al mundo
        :return: Tupla (x,y)
        """
        w1 = self.width / 2
        h1 = self.height / 2
        pos_x = int(-self.posx + 2 * self.drawablepos[0] + 2 * w1) - (self.window.getWindowWidth() - 1000) / 2
        pos_y = int(-self.posy + 3 * self.drawablepos[1] + 0.1 * h1) - (self.window.getWindowHeight() - 600) / 2
        return pos_x, pos_y

    def getRevl(self):
        """
        Retorna las revoluciones del motor
        :return: Integer entre 0 y 100
        """
        if self.automatic:
            cambio = self.getCambio()
            # Si está en neutro
            if cambio == 0:
                return 15
            else:
                if cambio == 1:
                    prev_vel = 0
                else:
                    prev_vel = self.velcambios[cambio - 2]
                if cambio < self.maxcambio:
                    next_vel = self.velcambios[cambio - 1]
                else:
                    next_vel = self.maxvelkmh
                if self.getVelKph() == self.maxvelkmh:
                    return 95
                prev_revl = (float(cambio - 1) / (self.maxcambio - 1)) * 100
                revl_cambio = float(self.getVelKph() - prev_vel) / (next_vel - prev_vel)
                return min(prev_revl + revl_cambio * (100 - prev_revl), 100)
        else:
            cambio = self.cambio
            # Si está en neutro
            if cambio == 0:
                return 15
            else:
                if cambio == 1:
                    prev_vel = 0
                else:
                    prev_vel = self.velcambios[cambio - 2]
                if cambio < self.maxcambio:
                    next_vel = self.velcambios[cambio - 1]
                else:
                    next_vel = self.maxvelkmh
                if self.getVelKph() == self.maxvelkmh:
                    return 95
                prev_revl = (float(cambio - 1) / (self.maxcambio - 1)) * 100
                revl_cambio = float(self.getVelKph() - prev_vel) / (next_vel - prev_vel)
                if cambio == 1:
                    return max(15, min(prev_revl + revl_cambio * (100 - prev_revl), 100))
                else:
                    return min(prev_revl + revl_cambio * (100 - prev_revl), 100)

    def getLapsTime(self):
        """
        Retorna los tiempos de vuelta
        :return: Lista de tiempos de vuelta en segundos
        """
        return self.totalTime

    def getTiempoFuera(self):
        """
        Retorna el tiempo fuera de la pista
        :return: Tiempo en segundos
        """
        return self.tiempoFuera

    def getTrackObjetives(self):
        """
        Retorna el objetivo de la pista
        :return: Retorna el objetivo en segundos del tipo actual
        """
        return self.trackObjetives[self.type - 1]

    def getType(self):
        """
        Retorna el tipo de auto
        :return: Integer entre 0 y inf+
        """
        return self.type

    def getVelKph(self, v=None):
        """
        Retorna la velocidad en kilómetros por hora
        :param v: Permite definir la velocidad
        :return: Integer entre 0 y inf+
        """
        if v is not None:
            vel = v
        else:
            vel = self.getVel()
        return int(vel * self.maxvelkmh / self.maxvel)

    def getVel(self):
        """
        Obtiene el módulo de la velocidad
        :return: Double
        """
        return math.sqrt(self.velx ** 2 + self.vely ** 2)

    # noinspection PyShadowingNames
    def groundTouch(self, roce, color, pos, index, t):
        """
        Comprueba toques con el suelo
        :param roce: Constante de roce
        :param color: Color esperado
        :param pos: Posición de comprobación
        :param index: Indice de la lista de marcas
        :param t: Tiempo t
        :return: booleano True/False indicando la colisión
        """
        if color[0] not in [88, 89, 90, 91, BLACK[0], LBLACK[0], LLBLACK[0], WHITE[0], 165]:
            if self.getVel() > VEL_PASTO:
                self.desacelerate(roce, t, False)
            dy = pos[1] - self.pos_center[1]
            dx = pos[0] - self.pos_center[0]
            w1 = self.width / 2
            h1 = self.height / 2
            new_x = -self.posx + 2 * self.drawablepos[0] + dx + 2 * w1
            new_y = -self.posy + 3 * self.drawablepos[1] + dy + 0.1 * h1
            if self.marcasTierra[index] is None:
                self.marcasTierra[index] = (new_x, new_y)
            else:
                if math.sqrt((new_x - self.marcasTierra[index][0]) ** 2 + (
                            new_y - self.marcasTierra[index][1]) ** 2) > MIN_LENGTH_MARCA:
                    # Se elige el color de dibujado
                    color_choice = random.randint(-10, 2)
                    if color_choice < 0:
                        color = BROWN
                    elif color_choice == 1:
                        color = L_BROWN
                    else:
                        color = D_BROWN
                    # Se agrega la linea a las marcas_tierra
                    self.marks_ground.append(
                        [(int(self.marcasTierra[index][0]), int(self.marcasTierra[index][1])), (int(new_x), int(new_y)),
                         color])
                    self.marcasTierra[index] = (new_x, new_y)
                    if len(self.marks_ground) > MAX_GROUND_MARKS:
                        if MARK_DELETE_RANDOM:
                            self.marks_ground.pop(random.randint(0, MAX_GROUND_MARKS))
                        else:
                            self.marks_ground.pop(0)
                    # Se reproduce un sonido mientras el canal no se esté usando
                    if not self.soundGroundChannel.get_busy():
                        if self.sound_state: self.soundGroundChannel.play(self.soundTrackOffroad)
            return True
        else:
            self.marcasTierra[index] = None
            return False

    def handBrake(self, t):
        """
        Aplica freno de mano
        :param t: Tiempo t
        :return: void
        """
        prev_vel = self.getVel()
        acel = 4 * self.desacel
        if self.velx != 0: self.velx -= acel * ecos(self.angle) * t
        if self.vely != 0: self.vely -= acel * esin(self.angle) * t
        if abs(self.velx) < LOWEST_VALUE_VEL_DESACEL: self.velx = 0
        if abs(self.vely) < LOWEST_VALUE_VEL_DESACEL: self.vely = 0
        # Se calcula el desplazamiento angular
        angleDespl = True
        for i in range(5):
            if abs(90 * i - self.angle) < 2:
                angleDespl = False
        if angleDespl:
            angl = minAng(self.angle) * sin((self.getVel() * 90) / self.maxvelkmh) * t * self.lastdirangle
            self.angle += angl
            self.rotate(self.lastdirangle, t, True)
        if self.getVel() > prev_vel:  # se comprueba que no se este acelerando
            self.velx = 0
            self.vely = 0
        else:  # si se desacelero
            self.tiempoFrenoDeMano += t
            if self.getVel() > 0 and self.tiempoFrenoDeMano > 0:
                self.marcarFrenadoHB(self.pos_rueda1, 0)
                self.marcarFrenadoHB(self.pos_rueda2, 1)
            else:
                self.marcasFrenadoHB = [None, None]

    def loadType(self, type):
        """
        Cargar tipo de auto
        :param type: Tipo de auto
        :return: void
        """
        # Classic: media velocidad, gran frenado, gran agarre y baja aceleracion
        if type == 1:
            acel = MID_LOW * ACELCONST
            self.acel = [CAMBIO[0] * acel, CAMBIO[1] * acel, CAMBIO[2] * acel, CAMBIO[3] * acel, CAMBIO[4] * acel,
                         CAMBIO[5] * acel]
            self.agarre = 2 * HIGH * AGARRECONST
            self.desacel = HIGH * DESACELCONST
            self.maxangvel = MAXANGVEL[0]
            self.maxrotvel = MAXROTVEL[0]
            self.maxvel = LOW * MAXVELCONST
            self.maxvelkmh = MAX_VEL_KMH * MID_LOW
            self.roce = LOW * ROCE
            self.rocePasto = MEDIUM * ROCE_PASTO
            self.velcambios = [50, 72, 100, 115, self.maxvelkmh, 2 * self.maxvelkmh]
            self.maxcambio = 5
        # Modern: media velocidad, medio frenado, medio agarre y media aceleracion
        elif type == 2:
            acel = MEDIUM * ACELCONST
            self.acel = [CAMBIO[0] * acel, CAMBIO[1] * acel, CAMBIO[2] * acel, CAMBIO[3] * acel, CAMBIO[4] * acel,
                         CAMBIO[5] * acel]
            self.agarre = MEDIUM * AGARRECONST
            self.desacel = MEDIUM * DESACELCONST
            self.maxangvel = MAXANGVEL[1]
            self.maxrotvel = MAXROTVEL[1]
            self.maxvel = MEDIUM * MAXVELCONST
            self.maxvelkmh = MAX_VEL_KMH * MEDIUM
            self.roce = MEDIUM * ROCE
            self.rocePasto = MEDIUM * ROCE_PASTO
            self.velcambios = [80, 130, 170, 220, 240, self.maxvelkmh]
            self.maxcambio = 6
        # Super: alta velocidad, mal frenado, mal agarre, alta aceleracion
        elif type == 3:
            acel = HIGH * ACELCONST
            self.acel = [CAMBIO[0] * acel, CAMBIO[1] * acel, CAMBIO[2] * acel, CAMBIO[3] * acel, CAMBIO[4] * acel,
                         CAMBIO[5] * acel]
            self.agarre = MID_LOW * AGARRECONST
            self.desacel = MEDIUM * DESACELCONST
            self.maxangvel = MAXANGVEL[2]
            self.maxrotvel = MAXROTVEL[2]
            self.maxvel = HIGH * MAXVELCONST
            self.maxvelkmh = HIGH * MAX_VEL_KMH
            self.roce = MEDIUM * ROCE
            self.rocePasto = HIGH * ROCE_PASTO
            self.velcambios = [120, 190, 260, 340, 400, self.maxvelkmh]
            self.maxcambio = 6

    def marcarFrenado(self, pos_rueda, index):
        """
        Marca el frenado en la pista
        :param pos_rueda: Posición de marcado
        :param index: Indice de la marca
        :return: void
        """
        dy = pos_rueda[1] - self.pos_center[1]
        dx = pos_rueda[0] - self.pos_center[0]
        w1 = self.width / 2
        h1 = self.height / 2
        new_x = -self.posx + 2 * self.drawablepos[0] + dx + 2 * w1
        new_y = -self.posy + 3 * self.drawablepos[1] + dy + 0.1 * h1
        if self.marcasFrenado[index] is None:
            self.marcasFrenado[index] = (new_x, new_y)
        else:
            if math.sqrt((new_x - self.marcasFrenado[index][0]) ** 2 + (
                        new_y - self.marcasFrenado[index][1]) ** 2) > MIN_LENGTH_FRENADO:
                # Se elige el color de dibujado
                color_choice = random.randint(-10, 2)
                if color_choice < 0:
                    color = BLACK
                elif color_choice == 1:
                    color = LBLACK
                else:
                    color = LLBLACK
                # Se agrega la linea a las marcas_frenado
                self.marks_track.append(
                    [(int(self.marcasFrenado[index][0]), int(self.marcasFrenado[index][1])), (int(new_x), int(new_y)),
                     color])
                self.marcasFrenado[index] = (new_x, new_y)
                if len(self.marks_track) > MAX_TRACK_MARKS:
                    self.marks_track.pop(random.randint(0, MAX_TRACK_MARKS))
                # sound_choice = random.randint(0,2) modo azar
                # Se reproduce un sonido mientras el canal no se esté usando
                if not self.soundWheelsChannel.get_busy():
                    if self.sound_state: self.soundWheelsChannel.play(self.soundTrack[SOUND_TRACK_WHEEL])

    def marcarFrenadoHB(self, pos_rueda, index):
        """
        Marca el frenado en la pista usando el freno de mano
        :param pos_rueda: Posición de marcado
        :param index: Indice de la marca
        :return: void
        """
        dy = pos_rueda[1] - self.pos_center[1]
        dx = pos_rueda[0] - self.pos_center[0]
        w1 = self.width / 2
        h1 = self.height / 2
        new_x = -self.posx + 2 * self.drawablepos[0] + dx + 2 * w1
        new_y = -self.posy + 3 * self.drawablepos[1] + dy + 0.1 * h1
        if self.marcasFrenadoHB[index] is None:
            self.marcasFrenadoHB[index] = (new_x, new_y)
        else:
            if math.sqrt((new_x - self.marcasFrenadoHB[index][0]) ** 2 + (
                        new_y - self.marcasFrenadoHB[index][1]) ** 2) > MIN_LENGTH_FRENADO:
                # Se elige el color de dibujado
                color_choice = random.randint(-10, 2)
                if color_choice < 0:
                    color = BLACK
                elif color_choice == 1:
                    color = LBLACK
                else:
                    color = LLBLACK
                # Se agrega la linea a las marcas_frenado
                self.marks_track.append([(int(self.marcasFrenadoHB[index][0]), int(self.marcasFrenadoHB[index][1])),
                                         (int(new_x), int(new_y)), color])
                self.marcasFrenadoHB[index] = (new_x, new_y)
                if len(self.marks_track) > MAX_TRACK_MARKS:
                    if MARK_DELETE_RANDOM:
                        self.marks_track.pop(random.randint(0, MAX_TRACK_MARKS))
                    else:
                        self.marks_track.pop(0)
                # sound_choice = random.randint(0,2) modo azar
                # Se reproduce un sonido mientras el canal no se esté usando
                if not self.soundWheelsChannel.get_busy():
                    if self.sound_state: self.soundWheelsChannel.play(self.soundTrack[SOUND_TRACK_WHEEL_HB])

    def returnToTrack(self):
        """
        Retornar el auto a la pista
        :return: void
        """
        self.angle = self.lastIndexTrackAng
        self.posx = self.lastIndexTrackPos[0]
        self.posy = self.lastIndexTrackPos[1]
        self.velx = 0
        self.vely = 0
        self.rotate(0, 0, False)

    def rotate(self, direction, t, controller=True):
        """
        Rota el auto
        :param direction: Dirección de rotación
        :param t: Tiempo t
        :param controller: Controlador del programa
        :return: void
        """
        if controller:  # si se mueve el auto mediante el controlador
            actual_vel = self.getVel()
            if MINROTVEL < actual_vel < self.maxrotvel * self.agarre:  # si se esta bajo la maxima velocidad de rotacion ->creciente
                self.angle = (self.angle + max(
                    min(ROTVEL * t * direction * 1 * cos((actual_vel * 90) / (2 * self.maxrotvel * self.agarre)),
                        self.maxangvel), \
                    - self.maxangvel)) % 360
            elif self.maxrotvel * self.agarre <= actual_vel:  # Si se esta sobre la velocidad de rotacion -> decreciente
                self.angle = (self.angle + max(min(ROTVEL * t * direction * max(
                    cos((actual_vel * 90) / (1.3 * self.agarre * (self.maxvel - 2 * self.maxrotvel))), 0.4), \
                                                   self.maxangvel), -self.maxangvel)) % 360
            else:
                return
            self.desacelerate(self.roce, t, False)
            self.velx = actual_vel * ecos(self.angle)
            self.vely = actual_vel * esin(self.angle)
            self.lastdirangle = direction
        # Se modifican las texturas
        self.imagenRotada = pygame.transform.rotate(self.texture, self.angle)
        self.imagenRotadaSize = self.imagenRotada.get_size()
        self.shadow_texture_rotada = pygame.transform.rotate(self.shadow_texture, self.angle)
        self.shadow_texture_size = self.shadow_texture_rotada.get_size()
        # Modifica la posición de las ruedas
        #  _  ____  _
        # | R3    R2 |
        # B    CE    F
        # |_R4____R1_|
        #
        w1 = self.width / 2
        h1 = self.height / 2
        center_image = self.imagenRotada.get_rect()
        self.pos_center = (self.drawablepos[0] + w1, self.drawablepos[1] + h1)
        largo = math.sqrt(((self.imagenRotadaSize[0] / 2) * 0.75) ** 2 + ((self.imagenRotadaSize[1] / 2) * 0.7) ** 2)
        pos_rueda1 = (self.pos_center[0] + 2 * w1 * 0.75, self.pos_center[1] + h1 / 2 * 0.8)
        pos_rueda2 = (self.pos_center[0] + 2 * w1 * 0.75, self.pos_center[1] - h1 / 2 * 0.8)
        pos_rueda3 = (self.pos_center[0] - 2 * w1 * 0.75, self.pos_center[1] - h1 / 2 * 0.8)
        pos_rueda4 = (self.pos_center[0] - 2 * w1 * 0.75, self.pos_center[1] + h1 / 2 * 0.8)
        self.pos_rueda1 = rotatePoint(pos_rueda1, self.pos_center, 360 - self.angle)
        self.pos_rueda2 = rotatePoint(pos_rueda2, self.pos_center, 360 - self.angle)
        self.pos_rueda3 = rotatePoint(pos_rueda3, self.pos_center, 360 - self.angle)
        self.pos_rueda4 = rotatePoint(pos_rueda4, self.pos_center, 360 - self.angle)

    # noinspection PyShadowingNames
    def setDefaultPos(self, pos):
        """
        Definir la posición inicial del auto en la pista
        :param pos: Posición (x,y) en la pista
        :return: void
        """
        # se modifica la posición
        self.posx = pos[0]
        self.posy = pos[1]
        self.initPos = (self.posx, self.posy)
        # se modifican las variables de movimiento
        self.lastcambio = 0
        self.tiempoAcelerando = 0
        self.tiempoFrenado = 0
        self.tiempoFrenoDeMano = 0
        self.lastdirangle = 0
        # se detienene los sonidos y se deja en idle
        if self.sound_state:
            self.soundGearChannel.play(self.soundGear[1], -1)
        self.soundGroundChannel.stop()
        self.soundWheelsChannel.stop()
        # se obtiene la posición de la pista inicial (que sera la meta para cada vuelta)
        self.trackCheckPoint = self.checkTrack()
        self.lastIndexTrack = self.trackCheckPoint  # se define el indice actual como el primero de la pista
        self.lastIndexTrackPos = pos
        # Se obtiene el largo de la pista
        self.trackSize = len(self.logic_track)

    def setNextTrack(self, track):
        """
        Define la sigiente pista
        :param track: String con el nombre de la pista
        :return: void
        """
        self.nextTrack = track

    def setLogicTrack(self, track):
        """
        Redefine la pista lógica
        :param track: Objeto track
        :return: void
        """
        self.logic_track = track

    def soundMute(self):
        """
        Detiene todos los sonidos del auto
        :return: void
        """
        self.soundGearChannel.stop()
        self.soundGroundChannel.stop()
        self.soundMusicChannel.stop()
        self.soundWheelsChannel.stop()

    def soundPause(self):
        """
        Pausa todos los sonidos del auto
        :return: void
        """
        self.soundGearChannel.pause()
        self.soundGroundChannel.pause()
        self.soundMusicChannel.pause()
        self.soundWheelsChannel.pause()

    def soundUnpause(self):
        """
        Reanuda todos los sonidos del auto
        :return: void
        """
        self.soundGearChannel.unpause()
        self.soundGroundChannel.unpause()
        self.soundMusicChannel.unpause()
        self.soundWheelsChannel.unpause()

    def stopAcelerating(self):
        """
        Detiene el evento de aceleración
        :return: void
        """
        self.tiempoAcelerando = 0
        self.getCambio()

    def stopTrackMarking(self):
        """
        Detiene las marcas en el asfalto
        :return: void
        """
        self.marcasFrenado = [None, None]
        self.tiempoFrenado = 0
        self.getCambio()

    def stopTrackMarkingHB(self):
        """
        Detiene las marcas en el asfalto por el freno de mano
        :return: void
        """
        self.tiempoFrenoDeMano = 0
        self.marcasFrenadoHB = [None, None]
        self.getCambio()

    def subirCambio(self):
        """
        Sube el cambio del vehiculo
        :return: void
        """
        if not self.automatic:
            if self.cambio < self.maxcambio:
                self.cambio += 1

    def update(self, t):
        """
        Actualiza la posicion usando el tiempo y retorna un mensaje para que view la represente en pantalla
        :param t: Tiempo t
        :return: Mensaje de estado
        """
        self.posx += self.velx * t
        self.posy += self.vely * t
        self.desacelerate(self.roce, t, False)
        self.lapTime += t
        # Si se sale del mapa se resetea
        rel_pos = self.getRelativePos()
        if (rel_pos[1] - 1.25 * self.window.getWindowHeight()) < self.mapLimits[1] or (
                    rel_pos[1] + 1.0 * self.window.getWindowHeight()) > self.mapLimits[3] or \
                        (rel_pos[0] - 1.25 * self.window.getWindowWidth()) < self.mapLimits[0] or (
                    rel_pos[0] + 1.0 * self.window.getWindowWidth()) > self.mapLimits[2]:
            self.returnToTrack()
        # Se comprueba el avance en la pista
        if self.checkTrackIndex(self.lastIndexTrack):  # si no se ha avanzado
            return STATE_NULL
        else:
            next_index = (self.lastIndexTrack + 1) % self.trackSize
            if self.checkTrackIndex(next_index):  # si se avanzo correctamente
                self.lastIndexTrack = next_index  # se avanza en la pista
                self.lastIndexTrackAng = self.angle  # se guarda el angulo asociado al ultimo sector valido de la pista
                self.lastIndexTrackPos = self.getPos()  # se guarda la posición asociada al ultimo sector valido de la pista
                if self.lastIndexTrack == 0:  # si se volvió al punto de origen entonces aumenta la pista
                    self.lapCount += 1
                    self.totalTime.append(self.lapTime)
                    fast_index = 0
                    current_min = 3600
                    self.lapTime = 0
                    for i in self.totalTime:
                        if i < current_min:
                            current_min = i
                        fast_index += 1
                    sumtime = sum(self.totalTime)
                    self.fastlap = [fast_index, round(current_min, 1)]
                    # si se acabo la carrera se escoge la vuelta mas rapida y se calcula el puntaje total
                    if self.finishedLap():
                        self.score = int(
                            100000 * ((0.3 / (self.tiempoFuera + 1) + 0.4 / math.sqrt(float(sumtime / current_min) + \
                                                                                      1 - self.totalLaps)) + 0.3 / (
                                          current_min ** 1.5)))
                        # Se sube el puntaje a la web
                        scoreboard_insert_url = self.scoreLink.format(self.hash[0], self.hash[1], self.hash[2],
                                                                      md5str(self.trackName),
                                                                      validUsername(self.username),
                                                                      self.score, round(current_min, 1), self.type)
                        if WEB_BROWSER:
                            self.browser.abrirLink(scoreboard_insert_url)
                        else:
                            http_header = {"User-Agent": self.scoreConfig.getValue("HEADER")}
                            request_object = Request(scoreboard_insert_url, None, http_header)
                        # Si existe comunicación con el servidor
                        try:
                            if self.verbose:
                                print "Conectando con el servidor ...",
                            if WEB_BROWSER:
                                scoreboard = unescape(self.browser.getHtml())
                            else:
                                response = urlopen(request_object)
                                scoreboard = response.read()
                            # Se obtiene el scoreboard
                            scoreboard_list = str(scoreboard).strip().split("<br>")
                            status = stringCleaner(scoreboard_list[0])
                            self.scoreBoardOnline.append(status)
                            for i in range(1, len(scoreboard_list) - 1):
                                line = stringCleaner(scoreboard_list[i])
                                if line != "NULL":
                                    color = getBetweenTags(line, "<color>", "</color>")
                                    player = getBetweenTags(line, "<player>", "</player>")[0:10]
                                    score = getBetweenTags(line, "<score>", "</score>")
                                    indexp = getBetweenTags(line, "<index>", "</index>")
                                    if color == "red":
                                        color = SCOREBOARD_RED
                                    elif color == "white":
                                        color = SCOREBOARD_WHITE
                                    self.scoreBoardOnline.append([color, indexp, player, score])
                                else:
                                    self.scoreBoardOnline.append([line])
                            if self.verbose:
                                print "ok"
                        # Error de conexión
                        except:
                            if self.verbose:
                                print "fail"
                                warning(ERROR_SCOREBOARD_NOCONECTIONMSG)
                            self.scoreBoardOnline = [ERROR_SCOREBOARD_NOCONECTION]
                    # si no se acabo la carrera se reemplaza el fantasma
                    else:
                        # Se volca un ghost en otro si es que se disminuye el tiempo
                        if self.ghost is None:
                            self.ghost = []
                            for elem in self.ghost_actual:
                                self.ghost.append(elem)
                            del self.ghost_actual
                            self.ghost_actual = []
                        else:
                            if len(self.ghost_actual) < len(self.ghost):
                                del self.ghost
                                self.ghost = []
                                for elem in self.ghost_actual:
                                    self.ghost.append(elem)
                            del self.ghost_actual
                            self.ghost_actual = []
                        self.ghost_i = 0
                    return STATE_NEWLAP
                else:
                    return STATE_CORRECT
            else:  # si no esta avanzado entonces
                self.tiempoFuera += t
                actual_index_trk = self.checkTrack()
                if actual_index_trk == -1:
                    return STATE_OFFROAD
                else:
                    if actual_index_trk < self.lastIndexTrack:
                        return STATE_WRONGWAY
                    else:
                        return STATE_INVALIDPOS

    def updateSound(self):
        """
        Comprueba si los sonidos están activos
        :return: void
        """
        self.sound_state = self.gameConfig.isTrue("ENABLESOUND")
