#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__': from path import *  # @UnusedWildImport

# Provee una función para retornar el nombre de usuario si es que el actual no es válido
#
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
# noinspection PyProtectedMember
import os
import pygame, string  # @UnusedImport
import pygame.gfxdraw
from pygame.locals import *  # @UnusedWildImport
from path import _DIR_BIN
from resources.fonts import getFonts
from resources.icons import getIcons

# Constantes del programa
COLOR_BLACK = (0, 0, 0, 200)  # color negro
COLOR_WHITE = (255, 255, 255)  # color blanco
NO_VALID_NAME = "NULL"  # evento invalido
BLACKLIST = []  # nombres de usuario invalido
NULLSTATE = "NULL"  # estado nulo
POS_INPUT = (10, 58)  # posicion a dibujar el input
SCREEN_SIZE = (350, 100)  # tamaño de la pantalla
TITLE_BG_COLOR = (170, 65, 50)  # color de fondo del titulo
VALIDUSERNAME = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"  # caracteres válidos

# Nombres de usuario invalidos
blacklist = open(_DIR_BIN + "server/blacklist.data", "r")
for line in blacklist: BLACKLIST.append(line.strip())
blacklist.close()


class Input:
    """Clase input, permite ingresar texto a un string dado los eventos asociados al programa principal"""

    def __init__(self, size, prompt):
        """
        Función constructora
        :param size: Tamaño de la ventana
        :param prompt: Mensaje
        :return: void
        """
        self.font = pygame.font.Font(getFonts("menu"), 17)
        self.maxlength = size
        self.prompt = prompt
        self.value = ''
        self.shifted = False

    def draw(self, surface):
        """
        Dibuja el input en pantalla
        :param surface: Superficie de dibujo
        :return: void
        """
        text = self.font.render(self.prompt + self.value, 1, COLOR_WHITE)
        surface.blit(text, POS_INPUT)

    def update(self, events):
        """
        Actualiza el input y reescribe el username
        :param events: Eventos
        :return: void
        """
        # Recorre los eventos
        for event in events:
            # Si se levanta una tecla
            if event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = False
            # Si se presiona una tecla
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self.value = self.value[:-1]
                elif event.key == K_RETURN and len(self.value) > 3:
                    return self.value
                elif event.key == K_LSHIFT or event.key == K_RSHIFT:
                    self.shifted = True
                # Si no esta presionado shift
                if not self.shifted:
                    if event.key == K_a:
                        self.value += 'a'
                    elif event.key == K_b:
                        self.value += 'b'
                    elif event.key == K_c:
                        self.value += 'c'
                    elif event.key == K_d:
                        self.value += 'd'
                    elif event.key == K_e:
                        self.value += 'e'
                    elif event.key == K_f:
                        self.value += 'f'
                    elif event.key == K_g:
                        self.value += 'g'
                    elif event.key == K_h:
                        self.value += 'h'
                    elif event.key == K_i:
                        self.value += 'i'
                    elif event.key == K_j:
                        self.value += 'j'
                    elif event.key == K_k:
                        self.value += 'k'
                    elif event.key == K_l:
                        self.value += 'l'
                    elif event.key == K_m:
                        self.value += 'm'
                    elif event.key == K_n:
                        self.value += 'n'
                    elif event.key == K_o:
                        self.value += 'o'
                    elif event.key == K_p:
                        self.value += 'p'
                    elif event.key == K_q:
                        self.value += 'q'
                    elif event.key == K_r:
                        self.value += 'r'
                    elif event.key == K_s:
                        self.value += 's'
                    elif event.key == K_t:
                        self.value += 't'
                    elif event.key == K_u:
                        self.value += 'u'
                    elif event.key == K_v:
                        self.value += 'v'
                    elif event.key == K_w:
                        self.value += 'w'
                    elif event.key == K_x:
                        self.value += 'x'
                    elif event.key == K_y:
                        self.value += 'y'
                    elif event.key == K_z:
                        self.value += 'z'
                    elif event.key == K_0:
                        self.value += '0'
                    elif event.key == K_1:
                        self.value += '1'
                    elif event.key == K_2:
                        self.value += '2'
                    elif event.key == K_3:
                        self.value += '3'
                    elif event.key == K_4:
                        self.value += '4'
                    elif event.key == K_5:
                        self.value += '5'
                    elif event.key == K_6:
                        self.value += '6'
                    elif event.key == K_7:
                        self.value += '7'
                    elif event.key == K_8:
                        self.value += '8'
                    elif event.key == K_9:
                        self.value += '9'
                # Si shift esta presionado
                elif self.shifted:
                    if event.key == K_a:
                        self.value += 'A'
                    elif event.key == K_b:
                        self.value += 'B'
                    elif event.key == K_c:
                        self.value += 'C'
                    elif event.key == K_d:
                        self.value += 'D'
                    elif event.key == K_e:
                        self.value += 'E'
                    elif event.key == K_f:
                        self.value += 'F'
                    elif event.key == K_g:
                        self.value += 'G'
                    elif event.key == K_h:
                        self.value += 'H'
                    elif event.key == K_i:
                        self.value += 'I'
                    elif event.key == K_j:
                        self.value += 'J'
                    elif event.key == K_k:
                        self.value += 'K'
                    elif event.key == K_l:
                        self.value += 'L'
                    elif event.key == K_m:
                        self.value += 'M'
                    elif event.key == K_n:
                        self.value += 'N'
                    elif event.key == K_o:
                        self.value += 'O'
                    elif event.key == K_p:
                        self.value += 'P'
                    elif event.key == K_q:
                        self.value += 'Q'
                    elif event.key == K_r:
                        self.value += 'R'
                    elif event.key == K_s:
                        self.value += 'S'
                    elif event.key == K_t:
                        self.value += 'T'
                    elif event.key == K_u:
                        self.value += 'U'
                    elif event.key == K_v:
                        self.value += 'V'
                    elif event.key == K_w:
                        self.value += 'W'
                    elif event.key == K_x:
                        self.value += 'X'
                    elif event.key == K_y:
                        self.value += 'Y'
                    elif event.key == K_z:
                        self.value += 'Z'
        if len(self.value) > self.maxlength >= 0: self.value = self.value[:-1]
        return NULLSTATE


def request(title, inputtext):
    """
    Función que abre una ventana para pedir un nombre de usuario
    :param title: Título de la ventana
    :param inputtext: Mensaje del prompt
    :return: String del nombre
    """
    # Se crea la ventana
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    display = pygame.display.set_mode(SCREEN_SIZE, pygame.NOFRAME)  # @UnusedVariable
    pygame.display.set_caption(title)
    pygame.display.set_icon(pygame.image.load(getIcons("icon")))
    screen = pygame.display.get_surface()
    nombre = Input(10, inputtext)

    # Reloj del juego
    clock = pygame.time.Clock()

    # Se crea el titulo de la ventana
    window_title_fontsize = 30
    window_title = pygame.font.Font(getFonts("menu"), window_title_fontsize)
    window_title_font = window_title.render(title, 1, COLOR_WHITE)
    window_title_width = window_title_font.get_size()[0]
    window_title_pos = [(0, 0), (SCREEN_SIZE[0], 0), (SCREEN_SIZE[0], int(window_title_fontsize / 2)),
                        (window_title_width + 15, int(window_title_fontsize / 2)), \
                        (window_title_width + 5, window_title_fontsize + 7), (0, window_title_fontsize + 7)]

    # Se lanza el programa
    while True:
        clock.tick(60)  # se definen los fps
        time = float(clock.get_time()) / 1000.0  # tiempo que tomo el frame en generarse @UnusedVariable
        screen.fill(COLOR_BLACK)  # se limpia la pantalla

        # Se dibuja el rectangulo rojo del titulo
        pygame.gfxdraw.filled_polygon(screen, window_title_pos, TITLE_BG_COLOR)
        screen.blit(window_title_font, (5, 0))

        # Eventos del programa principal
        events = pygame.event.get()  # se definen los eventos
        for event in events:
            if event.type == QUIT:
                return NO_VALID_NAME
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: return NO_VALID_NAME

                # Se recoge el resultado
        state = nombre.update(events)
        if state != NULLSTATE and validate(state): return state

        # Se dibuja el campo en pantalla
        nombre.draw(screen)

        # Se refresca la ventana
        pygame.display.flip()


def validate(username):
    """
    Valida un nombre de usuario
    :param username: Nombre de usuario
    :return: booleano
    """
    if username.upper() not in BLACKLIST:
        if 4 <= len(username) <= 10:
            for char in username:
                if char not in VALIDUSERNAME: return False
            return True
    return False

# Test
if __name__ == '__main__':
    pygame.init()
    print validate("Player")
    print validate("Test")
    print validate("1")
    print validate("$INVALIDNAME'")
    request("Crea un perfil", "Nombre (4-10 caracteres): ")
