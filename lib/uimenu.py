#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__': from path import *

# CLASE USER-INTERFACE MENU
# Crea los menús de interacción del juego, toma como argumento todas las variables
# a las cuales el menu puede acceder, como idiomas, configuraciones y modelos

# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
from bin import errors
from bin import pygame
from menu import Menu, MENU_BACK, MENU_EXIT
from resources.fonts import getFonts
from resources.images import getImages
from resources.sounds import getSounds
from textmenu import textMenu, TEXT_NEWLINE
from world import TRACKS
import math
import random

# Constantes del prograMA
MENU_PAUSE = "MENU_PAUSE"
MENU_INICIAL = "MENU_INICIAL"

class createUImenu:

    # Función constructora
    def __init__(self, langs, window, world, gameConfig, userConfig, viewConfig, windowConfig, worldConfig, mapConfig):
        # Variables de clase
        self.config_game = gameConfig  # configuraciones del juego
        self.config_map = mapConfig  # configuracion del mapa
        self.config_user = userConfig  # configuraciones de usuario
        self.config_view = viewConfig  # configuraciones de la vista
        self.config_window = windowConfig  # configuraciones de la ventana
        self.config_world = worldConfig  # configuraciones del mundo
        self.controller = None  # controlador
        self.font = getFonts("menu")  # se obtiene la fuente por defecto
        self.langs = langs  # idiomas del juego
        self.menu_inicial_title_font = pygame.font.Font(getFonts("nfs"), 55)
        self.screen = window.getSurface()  # se obtiene la superficie de dibujo
        self.sound_state = gameConfig.isTrue("ENABLESOUND")  # define si los sonidos estan activos
        self.view = None  # vista
        self.window = window  # ventana de visualización
        self.world = world  # mundo
        # Canales de sonido de los menues
        self.menuSoundChannel = pygame.mixer.Channel(4)
        self.menuSoundChannel.set_volume(float(self.config_world.getValue("CHANNEL_4")))
        self.menuButtonChannel = pygame.mixer.Channel(5)
        self.menuSoundChannel.set_volume(float(self.config_world.getValue("CHANNEL_5")))
        # Sonido de fondo del menu de inicio
        self.menu_inicial_sfx = pygame.mixer.Sound(getSounds("intro"))
        self.menu_button_up = pygame.mixer.Sound(getSounds("down"))
        self.menu_button_down = pygame.mixer.Sound(getSounds("up"))
        # Se renderiza la fuente del titulo
        self.menu_inicial_title = self.menu_inicial_title_font.render(self.langs.get(10), 1, (255, 255, 255))
        self.menu_inicial_title_shadow = self.menu_inicial_title_font.render(self.langs.get(10), 1, (0, 0, 0))
        self.menu_inicial_title_shadow_width = self.menu_inicial_title_shadow.get_size()[0]
        self.menu_inicial_title_width = self.menu_inicial_title.get_size()[0]
        self.menu_inicial_title_shadow_pos = (self.window.getWindowWidth() / 2 - self.menu_inicial_title_shadow_width / 2 - 3, (self.window.getWindowHeight() - 400) / 2 - 70)
        self.menu_inicial_title_pos = (self.window.getWindowWidth() / 2 - self.menu_inicial_title_width / 2, (self.window.getWindowHeight() - 400) / 2 - 65)
        # Menues
        self.actualmenu = None
        self.menu_inicial = None
        self.menu_jugar = None
        self.menu_pausa = None
        # Se crean los menues
        self.intializeMenuInicial()
        self.setActualMenu(MENU_INICIAL)
        self.initializeMenuPausa()
        # Se crean las imagenes de fondo
        self.splashimages = []
        for key in range(1, 11):
            image = pygame.transform.scale(pygame.image.load(getImages("splash" + str(key))), (window.getWindowWidth(), window.getWindowHeight()))
            self.splashimages.append(image)
        # Tiempos de efectos visuales de fondo
        self.splashindex = 0
        self.splashmaxtime = 0
        self.splashtime = 0

    # Agrega un controlador
    def addController(self, controller):
        self.controller = controller

    # Agrega la vista del juego
    def addView(self, view):
        self.view = view

    # Baja el menu actual
    def down(self):
        self.sound()
        self.actualmenu.down()

    # Dibujar en pantalla el menú inicial
    def drawMenuInicial(self, t):
        # Si la imagen de fondo aun no debe cambiar entonces solo se suma el tiempo
        if self.splashtime < self.splashmaxtime:
            self.splashtime += t
        # Si se debe cambiar tanto el indice como el tiempo maximo
        else:
            self.splashtime = 0
            self.splashmaxtime = random.randint(5, 10)
            self.splashindex = random.randint(0, 10)
        try: self.screen.blit(self.splashimages[self.splashindex], (0, 0))
        except: self.screen.blit(self.splashimages[0], (0, 0))
        self.menu_inicial.draw(self.screen)
        self.screen.blit(self.menu_inicial_title_shadow, self.menu_inicial_title_shadow_pos)
        self.screen.blit(self.menu_inicial_title, self.menu_inicial_title_pos)
        # Se reproduce el sonido de fondo
        if not self.menuSoundChannel.get_busy() and self.sound_state:
            self.menuSoundChannel.play(self.menu_inicial_sfx)

    # Dibujar en pantalla el menú de pausa
    def drawMenuPause(self):
        self.menu_pausa.draw(self.screen)

    # Retorna el menú inicial
    def getMenuInicial(self):
        return self.menu_inicial

    # Retorna el menú de pausa
    def getMenuPausa(self):
        return self.menu_pausa

    # Crea el menu inicial
    def intializeMenuInicial(self):
        try:
            # Colores de autos
            COLOR_CAR_1_1 = [(self.langs.get(100), "lr_classic_yellow"), (self.langs.get(96), "lr_classic_blue"), (self.langs.get(97), "lr_classic_cyan"), (self.langs.get(99), "lr_classic_red"), (self.langs.get(98), "lr_classic_pink")]
            COLOR_CAR_1_2 = [(self.langs.get(96), "lr_classic_blue"), (self.langs.get(97), "lr_classic_cyan"), (self.langs.get(99), "lr_classic_red"), (self.langs.get(98), "lr_classic_pink"), (self.langs.get(100), "lr_classic_yellow")]
            COLOR_CAR_1_3 = [(self.langs.get(97), "lr_classic_cyan"), (self.langs.get(99), "lr_classic_red"), (self.langs.get(98), "lr_classic_pink"), (self.langs.get(100), "lr_classic_yellow"), (self.langs.get(96), "lr_classic_blue")]
            COLOR_CAR_1_4 = [(self.langs.get(99), "lr_classic_red"), (self.langs.get(98), "lr_classic_pink"), (self.langs.get(100), "lr_classic_yellow"), (self.langs.get(96), "lr_classic_blue"), (self.langs.get(97), "lr_classic_cyan")]
            COLOR_CAR_1_5 = [(self.langs.get(98), "lr_classic_pink"), (self.langs.get(100), "lr_classic_yellow"), (self.langs.get(96), "lr_classic_blue"), (self.langs.get(97), "lr_classic_cyan"), (self.langs.get(99), "lr_classic_red")]
            COLOR_CAR_2_1 = [(self.langs.get(96), "lr_modern_blue"), (self.langs.get(99), "lr_modern_red"), (self.langs.get(98), "lr_modern_pink"), (self.langs.get(101), "lr_modern_green")]
            COLOR_CAR_2_2 = [(self.langs.get(99), "lr_modern_red"), (self.langs.get(98), "lr_modern_pink"), (self.langs.get(101), "lr_modern_green"), (self.langs.get(96), "lr_modern_blue")]
            COLOR_CAR_2_3 = [(self.langs.get(98), "lr_modern_pink"), (self.langs.get(101), "lr_modern_green"), (self.langs.get(96), "lr_modern_blue"), (self.langs.get(99), "lr_modern_red")]
            COLOR_CAR_2_4 = [(self.langs.get(101), "lr_modern_green"), (self.langs.get(96), "lr_modern_blue"), (self.langs.get(99), "lr_modern_red"), (self.langs.get(98), "lr_modern_pink")]
            COLOR_CAR_3_1 = [(self.langs.get(100), "lr_super_yellow"), (self.langs.get(97), "lr_super_cyan"), (self.langs.get(98), "lr_super_pink"), (self.langs.get(101), "lr_super_green")]
            COLOR_CAR_3_2 = [(self.langs.get(97), "lr_super_cyan"), (self.langs.get(98), "lr_super_pink"), (self.langs.get(101), "lr_super_green"), (self.langs.get(100), "lr_super_yellow")]
            COLOR_CAR_3_3 = [(self.langs.get(98), "lr_super_pink"), (self.langs.get(101), "lr_super_green"), (self.langs.get(100), "lr_super_yellow"), (self.langs.get(97), "lr_super_cyan")]
            COLOR_CAR_3_4 = [(self.langs.get(101), "lr_super_green"), (self.langs.get(100), "lr_super_yellow"), (self.langs.get(97), "lr_super_cyan"), (self.langs.get(98), "lr_super_pink")]
            # Tipos de auto
            TYPECAR_1 = [(self.langs.get(43), "1"), (self.langs.get(44), "2"), (self.langs.get(45), "3")]
            TYPECAR_2 = [(self.langs.get(44), "2"), (self.langs.get(45), "3"), (self.langs.get(43), "1")]
            TYPECAR_3 = [(self.langs.get(45), "3"), (self.langs.get(43), "1"), (self.langs.get(44), "2")]
            # Lanzar la carrera
            def _launchTrack(*args):
                self.reset(0)
                self.menuSoundChannel.stop()
                self.world.loadMap()
                self.controller.disableMenu()
                self.controller.setPlayer()
                self.view.startPlayingRender()
            # Funcion que guarda configuraciones y las aplica
            def _saveConfig(value, *args):
                if args[1] != "SCREENSIZE":
                    args[0].setParameter(args[1], value)
                    args[0].export()
                else:
                    value = value.split(" ")
                    args[0].setParameter("WIDTH", value[0])
                    args[0].setParameter("HEIGHT", value[1])
                    args[0].export()
                    self.menu_configuracion.actual.opciones.pop(2)
                    self.menu_configuracion.actual.posOptionY -= (-self.menu_configuracion.actual.fontsize / 2 - self.menu_configuracion.actual.optiondy / 2)
                    self.menu_configuracion.addSelector(self.langs.get(110), self.window.getDisplayList(), _saveConfig, None, self.config_window, "SCREENSIZE", index=2)
                    self.menu_configuracion.actual.size -= 1
                    # self.window.update()
                    # self.view.updateWindowSize()
                # Se aplican la configuraciones
                # Si se cambio el modo de ventana
                if args[1] == "WINDOWED" and value == "FALSE":self.window.setFullscreen()
                elif args[1] == "WINDOWED" and value == "TRUE": self.window.setWindowed()
                # Si se activan / desactivan los sonidos
                if args[1] == "ENABLESOUND":
                    if value == "FALSE": self.menu_inicial_sfx.stop()
                    self.updateSound()
                # Si se activa / desactiva el mostrar los fps en el titulo de la ventana
                if args[1] == "SHOWFPS":
                    self.view.updateShowFPS()
                # Si se cambia la pista a jugar
                if args[1] == "TYPECAR":
                    self.menu_jugar.actual.opciones.pop(2)
                    self.menu_jugar.actual.opciones.pop(2)
                    self.menu_jugar.actual.posOptionY -= 2 * (-self.menu_jugar.actual.fontsize / 2 - self.menu_jugar.actual.optiondy / 2)
                    if value == "1":
                        self.menu_jugar.addSelector(self.langs.get(94), TYPECAR_1, _saveConfig, _launchTrack, self.config_user, "TYPECAR", index=2)
                        self.config_user.setParameter("TEXTURE", "lr_classic_red")
                        self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_1_4, _saveConfig, _launchTrack, self.config_user, "TEXTURE", index=3)
                    elif value == "2":
                        self.menu_jugar.addSelector(self.langs.get(94), TYPECAR_2, _saveConfig, _launchTrack, self.config_user, "TYPECAR", index=2)
                        self.config_user.setParameter("TEXTURE", "lr_modern_red")
                        self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_2_2, _saveConfig, _launchTrack, self.config_user, "TEXTURE", index=3)
                    elif value == "3":
                        self.menu_jugar.addSelector(self.langs.get(94), TYPECAR_3, _saveConfig, _launchTrack, self.config_user, "TYPECAR", index=2)
                        self.config_user.setParameter("TEXTURE", "lr_super_cyan")
                        self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_3_2, _saveConfig, _launchTrack, self.config_user, "TEXTURE", index=3)
                    self.menu_jugar.actual.size -= 2
                    args[0].export()
                # Si se activa/ desactiva el mostrar el fantasma
                if args[1] == "SHOWGHOST":
                    self.view.updateShowGhost()
            # Menu jugar
            self.menu_jugar = Menu(self.window, self.font, self.langs.get(61), draw_region_y=55)
            self.menu_jugar.addOption(self.langs.get(104), _launchTrack, "a")
            # Se cargan los mapas
            tracks = []
            actual_map = int(self.config_map.getValue("DEFAULTMAP"))
            tracks.append((TRACKS[actual_map], str(actual_map)))
            for track in TRACKS.keys():
                if track != actual_map:
                    tracks.append((TRACKS[track], str(track)))
            self.menu_jugar.addSelector(self.langs.get(103), tracks, _saveConfig, None, self.config_map, "DEFAULTMAP")
            if self.config_user.getValue("TYPECAR") == "1": typecar_values = TYPECAR_1
            elif self.config_user.getValue("TYPECAR") == "2": typecar_values = TYPECAR_2
            else: typecar_values = TYPECAR_3
            self.menu_jugar.addSelector(self.langs.get(94), typecar_values, _saveConfig, None, self.config_user, "TYPECAR")
            if self.config_user.getValue("TYPECAR") == "1":
                if self.config_user.getValue("TEXTURE") == "lr_classic_yellow":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_1_1, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_classic_blue":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_1_2, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_classic_cyan":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_1_3, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_classic_red":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_1_4, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_classic_pink":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_1_5, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                else:
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_1_4, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
            elif self.config_user.getValue("TYPECAR") == "2":
                if self.config_user.getValue("TEXTURE") == "lr_modern_blue":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_2_1, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_modern_red":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_2_2, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_modern_pink":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_2_3, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_modern_green":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_2_4, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                else:
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_2_2, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
            elif self.config_user.getValue("TYPECAR") == "3":
                if self.config_user.getValue("TEXTURE") == "lr_super_yellow":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_3_1, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_super_cyan":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_3_2, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_super_pink":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_3_3, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_super_green":
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_3_4, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
                else:
                    self.menu_jugar.addSelector(self.langs.get(95), COLOR_CAR_3_2, _saveConfig, _launchTrack, self.config_user, "TEXTURE")
            self.menu_jugar.addOption(self.langs.get(102), MENU_BACK)
            # Menu de configuraciones
            self.menu_configuracion = Menu(self.window, self.font, self.langs.get(62), centered=False, draw_region_x=5, font_size=25, option_margin=20)
            if self.config_window.isTrue("WINDOWED"): window_values = [(self.langs.get(84), "TRUE"), (self.langs.get(85), "FALSE")]
            else: window_values = [(self.langs.get(85), "FALSE"), (self.langs.get(84), "TRUE")]
            if self.config_game.isTrue("ENABLESOUND"): sound_values = [(self.langs.get(84), "TRUE"), (self.langs.get(85), "FALSE")]
            else: sound_values = [(self.langs.get(85), "FALSE"), (self.langs.get(84), "TRUE")]
            if self.config_game.getValue("LANG") == "ES": lang_values = [(self.langs.get(89), "ES"), (self.langs.get(90), "EN")]
            else: lang_values = [(self.langs.get(90), "EN"), (self.langs.get(89), "ES")]
            # if self.config_game.getValue("FPS") == "60": fps_values = [("60", "60"), ("30", "30"), ("45", "45")]
            # elif self.config_game.getValue("FPS") == "30": fps_values = [("30", "30"), ("45", "45"), ("60", "60")]
            # else: fps_values = [("45", "45"), ("60", "60"), ("30", "30")]
            if self.config_view.isTrue("SHOWFPS"): showfps_values = [(self.langs.get(84), "TRUE"), (self.langs.get(85), "FALSE")]
            else: showfps_values = [(self.langs.get(85), "FALSE"), (self.langs.get(84), "TRUE")]
            if self.config_view.isTrue("SHOWGHOST"): showghost_values = [(self.langs.get(84), "TRUE"), (self.langs.get(85), "FALSE")]
            else: showghost_values = [(self.langs.get(85), "FALSE"), (self.langs.get(84), "TRUE")]
            self.menu_configuracion.addSelector(self.langs.get(88), lang_values, _saveConfig, None, self.config_game, "LANG")
            self.menu_configuracion.addSelector(self.langs.get(87), sound_values, _saveConfig, None, self.config_game, "ENABLESOUND")
            self.menu_configuracion.addSelector(self.langs.get(110), self.window.getDisplayList(), _saveConfig, None, self.config_window, "SCREENSIZE")
            self.menu_configuracion.addSelector(self.langs.get(83), window_values, _saveConfig, None, self.config_window, "WINDOWED")
            # self.menu_configuracion.addSelector(self.langs.get(91), fps_values, _saveConfig, None, self.config_game, "FPS")
            self.menu_configuracion.addSelector(self.langs.get(92), showfps_values, _saveConfig, None, self.config_view, "SHOWFPS")
            self.menu_configuracion.addSelector(self.langs.get(93), showghost_values, _saveConfig, None, self.config_view, "SHOWGHOST")
            self.menu_configuracion.addOption(self.langs.get(86), MENU_BACK)
            # Menu de ayuda
            menu_ayuda = textMenu(self.window, self.font, self.langs.get(63), font_text_size=18, draw_text_region=2, draw_region_y=58)
            menu_ayuda.addText(self.langs.get(66))
            menu_ayuda.addText(self.langs.get(68))
            menu_ayuda.addText(self.langs.get(69))
            menu_ayuda.addText(self.langs.get(70))
            menu_ayuda.addText(self.langs.get(71))
            menu_ayuda.addText(self.langs.get(72))
            menu_ayuda.addText(self.langs.get(73))
            menu_ayuda.addText(self.langs.get(74))
            menu_ayuda.addText(self.langs.get(75))
            menu_ayuda.addText(self.langs.get(76))
            menu_ayuda.addText(self.langs.get(77))
            menu_ayuda.addText(self.langs.get(78))
            menu_ayuda.addOption(self.langs.get(67), MENU_BACK)
            # Menu acerca de
            menu_acercade = textMenu(self.window, self.font, self.langs.get(64), text_centered=True, draw_text_region=50, draw_region_y=50)
            menu_acercade.addText(self.langs.get(79))
            menu_acercade.addText(self.langs.get(80))
            menu_acercade.addText(self.langs.get(81))
            menu_acercade.addText(self.langs.get(82))
            menu_acercade.addOption(self.langs.get(67), MENU_BACK)
            # Se crea el menú de inicio
            self.menu_inicial = Menu(self.window, self.font, self.langs.get(60), draw_region_y=56)
            self.menu_inicial.addOption(self.langs.get(61), self.menu_jugar)
            self.menu_inicial.addOption(self.langs.get(62), self.menu_configuracion)
            self.menu_inicial.addOption(self.langs.get(63), menu_ayuda)
            self.menu_inicial.addOption(self.langs.get(64), menu_acercade)
            self.menu_inicial.addOption(self.langs.get(65), MENU_EXIT)
        except:
            errors.throw(errors.ERROR_CREATE_MENU)

    # Inicia el menu de pausa
    def initializeMenuPausa(self):
        # Funcion que vuelve al menu principal
        def _returnIntialMenu():
            self.setZeroIndex()
            self.world.clearActualMap()
            self.view.stopPlayingRender()
            self.controller.delPlayer()
        # Retorna el juego
        def _back():
            self.setZeroIndex()
            self.controller.disableMenu()
            self.world.getActualMap().getPlayer().soundUnpause()
         # Reinicia el juego
        def _reinitiate():
            _back()
            self.world.getActualMap().getPlayer().clear(True)
        self.menu_pausa = Menu(self.window, self.font, self.langs.get(105), height=230, width=440, font_size=30, draw_region_y=60)
        self.menu_pausa.addOption(self.langs.get(107), _back)
        self.menu_pausa.addOption(self.langs.get(106), _reinitiate)
        self.menu_pausa.addOption(self.langs.get(86), _returnIntialMenu)

    # Mueve el selector del menú actual hacia la izqueirda
    def left(self):
        self.sound()
        self.actualmenu.left()

    # Resetea el menu
    def reset(self, times):
        self.actualmenu.reset(times)

    # Mueve el selector del menú actual hacia la derecha
    def right(self):
        self.sound()
        self.actualmenu.right()

    # Selecciona la opción actual
    def select(self):
        self.actualmenu.select()

    # Define el menu actual
    def setActualMenu(self, menuEvent):
        if menuEvent == MENU_INICIAL:
            self.actualmenu = self.menu_inicial
        elif menuEvent == MENU_PAUSE:
            self.actualmenu = self.menu_pausa

    # Define el indice cero
    def setZeroIndex(self):
        self.actualmenu.index = 0

    # Reproduce el efecto de sonido del menu
    def sound(self):
        if self.sound_state and not self.menuButtonChannel.get_busy():
            self.menuButtonChannel.play(self.menu_button_down)

    # Sube el menu actual
    def up(self):
        self.sound()
        self.actualmenu.up()

    # Comprueba si los sondios estan activos
    def updateSound(self):
        self.sound_state = self.config_game.isTrue("ENABLESOUND")
