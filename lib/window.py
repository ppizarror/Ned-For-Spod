# coding=utf-8
"""
WINDOW
Ventana del juego, instancia la ventana en función de la configuración inicial
Adicionalmente maneja tamaños y superficies.

Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    from path import *  # @UnusedWildImport

# Importación de librerías
import os
from pygame.locals import *  # @UnusedWildImport
from bin import pygame

# Constantes del programa
FORMAT_16_9 = "(16:9) {0}x{1}"
FORMAT_4_3 = "(4:3) {0}x{1}"
FORMAT_VALUE = "{0} {1}"
# Resoluciones en 16:9
SCREEN16_9 = [(8192, 4608),
              (7680, 4320),
              (5120, 2880),
              (4096, 2304),
              (3840, 2160),
              (3200, 1800),
              (2560, 1440),
              (2048, 1152),
              (1920, 1080),
              (1600, 900),
              (1366, 768),
              (1280, 720),
              (1024, 600),
              (960, 540)]
# Resoluciones en 4:3
SCREEN4_3 = [(6400, 4800),
             (4096, 3072),
             (3200, 2400),
             (2800, 2100),
             (2560, 1920),
             (2304, 1728),
             (1920, 1440),
             (1856, 1392),
             (1600, 1200),
             (1440, 1080),
             (1400, 1050),
             (1280, 960),
             (1152, 900),
             (1024, 768),
             (960, 720),
             (800, 600),
             ]


# noinspection PyUnusedLocal
class Window(object):
    """Ventana de la aplicación"""

    def __init__(self, configs, title, icon, info, **kwargs):
        """
        Función constructora
        :param configs: Configuración de la ventana
        :param title: Título de la aplicación
        :param icon: �?cono de la aplicación
        :param info: Información de la ventana
        :param kwargs: Parámetros adicionales
        :return: void
        """

        # Se guarda ia informacion de la ventana
        self.info = info
        # Se guarda la informacion de las configuraciones
        self.config = configs
        self.height = int(configs.getValue("HEIGHT"))
        self.width = int(configs.getValue("WIDTH"))
        # Si esta centrada
        if configs.isTrue("CENTERED"):
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        # Se crea la pantalla
        if configs.isTrue("WINDOWED"):
            self.display = pygame.display.set_mode((self.width, self.height),
                                                   pygame.DOUBLEBUF | pygame.HWSURFACE,
                                                   32)
        else:
            self.display = pygame.display.set_mode((self.width, self.height),
                                                   FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME,
                                                   32)
        pygame.display.set_icon(icon)
        pygame.display.set_caption(title)
        # Si se desabilita el raton
        if not configs.isTrue("SHOW_MOUSE"):
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

    def get_display(self):
        """
        Retorna el display
        :return: Objeto display
        """
        return self.display

    def get_display_list(self):
        """
        Retorna una lista formateada para el selector con todas las resoluciones disponibles
        :return: Lista de opciones
        """
        actual_value = FORMAT_VALUE.format(self.config.getValue("WIDTH"),
                                           self.config.getValue("HEIGHT"))
        max_w, max_h = (self.info.current_w, self.info.current_h)
        disponible = []
        for resolution in SCREEN16_9:
            if resolution[0] <= max_w and resolution[1] <= max_h:
                disponible.append(
                    (FORMAT_16_9.format(resolution[0], resolution[1]),
                     FORMAT_VALUE.format(resolution[0], resolution[1])))
        for resolution in SCREEN4_3:
            if resolution[0] <= max_w and resolution[1] <= max_h:
                disponible.append(
                    (FORMAT_4_3.format(resolution[0], resolution[1]),
                     FORMAT_VALUE.format(resolution[0], resolution[1])))
        while True:
            if disponible[0][1] == actual_value:
                break
            else:
                disponible.append(disponible.pop(0))
        return disponible

    @staticmethod
    def get_surface():
        """
        Retorna la superficie de dibujo
        :return: Superficie de dibujo pygame
        """
        return pygame.display.get_surface()

    def get_window_height(self):
        """
        Retorna el alto de la pantalla
        :return: Integer
        """
        return self.height

    def get_window_size(self):
        """
        Retorna una tupla con el tamaño de la pantalla
        :return: Tupla (w,h)
        """
        return self.width, self.height

    def get_window_width(self):
        """
        Retorna el ancho de la pantalla
        :return: Integer
        """
        return self.width

    def set_fullscreen(self):
        """
        Cambia a pantalla completa
        :return: void
        """
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.display = pygame.display.set_mode((self.width, self.height),
                                               FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME,
                                               32)

    def set_windowed(self):
        """
        Cambia a pantalla reducida
        :return: void
        """
        self.display = pygame.display.set_mode((self.width, self.height),
                                               pygame.DOUBLEBUF | pygame.HWSURFACE,
                                               32)

    @staticmethod
    def set_window_title(title):
        """
        Cambia el título de la ventana
        :param title: Título
        :return: void
        """
        pygame.display.set_caption(title)

    def update(self):
        """
        Actualiza la ventana
        :return: void
        """
        self.width = int(self.config.getValue("WIDTH"))
        self.height = int(self.config.getValue("HEIGHT"))
        if self.config.isTrue("WINDOWED"):
            self.display = pygame.display.set_mode((self.width, self.height),
                                                   pygame.DOUBLEBUF | pygame.HWSURFACE,
                                                   32)
        else:
            self.display = pygame.display.set_mode((self.width, self.height),
                                                   FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME,
                                                   32)
