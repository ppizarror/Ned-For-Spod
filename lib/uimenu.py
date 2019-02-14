# coding=utf-8
"""
CLASE USER-INTERFACE MENU
Crea los menús de interacción del juego, toma como argumento todas las variables
a las cuales el menu puede acceder, como idiomas, configuraciones y modelos.

Autor: PABLO PIZARRO @ppizarror
Fecha: ABRIL 2015
"""

# Importación de librerías
import random
from bin import errors
from bin import pygame
from menu import Menu, MENU_BACK, MENU_EXIT
from resources.fonts import getFonts
from resources.images import getImages
from resources.sounds import getSounds
from textmenu import Textmenu
from world import TRACKS

if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    from path import *  # @UnusedWildImport

# Constantes del prograMA
MENU_PAUSE = "MENU_PAUSE"
MENU_INICIAL = "MENU_INICIAL"


# noinspection PyPep8Naming,PyBroadException,PyAttributeOutsideInit,PyUnresolvedReferences
class Createuimenu(object):
    """Crea los menús del juego"""

    def __init__(self, langs, window, world, game_config, user_config,
                 view_config, window_config, world_config, map_config):
        """
        Función constructora.
        :param langs: Diccionario de idioma
        :param window: Ventana de la aplicación
        :param world: Objeto mundo
        :param game_config: Configuraciones del juego
        :param user_config: Configuraciones de usuario
        :param view_config: Configuraciones de la vista
        :param window_config: Configuraciones de la ventana
        :param world_config: Configuraciones del mundo
        :param map_config: Configuraciones del mapa
        :return: void
        """

        # Variables de clase
        self.config_game = game_config  # Configuraciones del juego
        self.config_map = map_config  # Configuracion del mapa
        self.config_user = user_config  # Configuraciones de usuario
        self.config_view = view_config  # Configuraciones de la vista
        self.config_window = window_config  # Configuraciones de la ventana
        self.config_world = world_config  # Configuraciones del mundo
        self.controller = None  # Controlador
        self.font = getFonts("menu")  # Se obtiene la fuente por defecto
        self.langs = langs  # Idiomas del juego
        self.menu_inicial_title_font = pygame.font.Font(getFonts("nfs"), 55)
        self.screen = window.get_surface()  # Se obtiene la superficie de dibujo
        self.sound_state = game_config.isTrue(
            "ENABLESOUND")  # Define si los sonidos estan activos
        self.view = None  # Vista
        self.window = window  # Ventana de visualización
        self.world = world  # Mundo

        # Canales de sonido de los menues
        self.menuSoundChannel = pygame.mixer.Channel(4)
        self.menuSoundChannel.set_volume(
            float(self.config_world.getValue("CHANNEL_4")))
        self.menuButtonChannel = pygame.mixer.Channel(5)
        self.menuSoundChannel.set_volume(
            float(self.config_world.getValue("CHANNEL_5")))

        # Sonido de fondo del menu de inicio
        self.menu_inicial_sfx = pygame.mixer.Sound(getSounds("intro"))
        self.menu_button_up = pygame.mixer.Sound(getSounds("down"))
        self.menu_button_down = pygame.mixer.Sound(getSounds("up"))

        # Se renderiza la fuente del título
        self.menu_inicial_title = self.menu_inicial_title_font.render(
            self.langs.get(10), 1, (255, 255, 255))
        self.menu_inicial_title_shadow = self.menu_inicial_title_font.render(
            self.langs.get(10), 1, (0, 0, 0))
        self.menu_inicial_title_shadow_width = \
            self.menu_inicial_title_shadow.get_size()[0]
        self.menu_inicial_title_width = self.menu_inicial_title.get_size()[0]
        self.menu_inicial_title_shadow_pos = (
            self.window.get_window_width() / 2 - self.menu_inicial_title_shadow_width / 2 - 3,
            (self.window.get_window_height() - 400) / 2 - 70)
        self.menu_inicial_title_pos = (
            self.window.get_window_width() / 2 - self.menu_inicial_title_width / 2,
            (self.window.get_window_height() - 400) / 2 - 65)

        # Menues
        self.actualmenu = None
        self.menu_inicial = None
        self.menu_jugar = None
        self.menu_pausa = None

        # Se crean los menues
        self.intializeMenuInicial()
        self.setActualMenu(MENU_INICIAL)
        self.initializeMenuPausa()

        # Se crean las imágenes de fondo
        self.splashimages = []
        for key in range(1, 11):
            image = pygame.transform.scale(
                pygame.image.load(getImages("splash" + str(key))),
                (window.get_window_width(), window.get_window_height()))
            self.splashimages.append(image)

        # Tiempos de efectos visuales de fondo
        self.splashindex = 0
        self.splashmaxtime = 0
        self.splashtime = 0

    def addController(self, controller):
        """
        Agrega un controlador.
        :param controller: Objeto <controller>
        :return: void
        """
        self.controller = controller

    def addView(self, view):
        """
        Agrega la vista del juego.
        :param view: Objeto <view>
        :return: void
        """
        self.view = view

    def down(self):
        """
        Baja el menú actual.
        :return: void
        """
        self.sound()
        self.actualmenu.down()

    def drawMenuInicial(self, t):
        """
        Dibujar en pantalla el menú inicial.
        :param t: Tiempo t
        :return: void
        """
        # Si la imagen de fondo aun no debe cambiar entonces solo se suma el tiempo
        if self.splashtime < self.splashmaxtime:
            self.splashtime += t

        # Si se debe cambiar tanto el indice como el tiempo maximo
        else:
            self.splashtime = 0
            self.splashmaxtime = random.randint(5, 10)
            self.splashindex = random.randint(0, 10)
        try:
            self.screen.blit(self.splashimages[self.splashindex], (0, 0))
        except:
            self.screen.blit(self.splashimages[0], (0, 0))
        self.menu_inicial.draw(self.screen)
        self.screen.blit(self.menu_inicial_title_shadow,
                         self.menu_inicial_title_shadow_pos)
        self.screen.blit(self.menu_inicial_title, self.menu_inicial_title_pos)

        # Se reproduce el sonido de fondo
        if not self.menuSoundChannel.get_busy() and self.sound_state:
            self.menuSoundChannel.play(self.menu_inicial_sfx)

    def drawMenuPause(self):
        """
        Dibujar en pantalla el menú de pausa.
        :return: void
        """
        self.menu_pausa.draw(self.screen)

    def getMenuInicial(self):
        """
        Retorna el menú inicial.
        :return: Objeto <menu> inicial
        """
        return self.menu_inicial

    def getMenuPausa(self):
        """
        Retorna el menú de pausa.
        :return: Objeto <menu> de pausa
        """
        return self.menu_pausa

    def intializeMenuInicial(self):
        """
        Crea el menu inicial.
        :return: void
        """
        try:
            # Colores de autos
            COLOR_CAR_1_1 = [(self.langs.get(100), "lr_classic_yellow"),
                             (self.langs.get(96), "lr_classic_blue"),
                             (self.langs.get(97), "lr_classic_cyan"),
                             (self.langs.get(99), "lr_classic_red"),
                             (self.langs.get(98), "lr_classic_pink")]
            COLOR_CAR_1_2 = [(self.langs.get(96), "lr_classic_blue"),
                             (self.langs.get(97), "lr_classic_cyan"),
                             (self.langs.get(99), "lr_classic_red"),
                             (self.langs.get(98), "lr_classic_pink"),
                             (self.langs.get(100), "lr_classic_yellow")]
            COLOR_CAR_1_3 = [(self.langs.get(97), "lr_classic_cyan"),
                             (self.langs.get(99), "lr_classic_red"),
                             (self.langs.get(98), "lr_classic_pink"),
                             (self.langs.get(100), "lr_classic_yellow"),
                             (self.langs.get(96), "lr_classic_blue")]
            COLOR_CAR_1_4 = [(self.langs.get(99), "lr_classic_red"),
                             (self.langs.get(98), "lr_classic_pink"),
                             (self.langs.get(100), "lr_classic_yellow"),
                             (self.langs.get(96), "lr_classic_blue"),
                             (self.langs.get(97), "lr_classic_cyan")]
            COLOR_CAR_1_5 = [(self.langs.get(98), "lr_classic_pink"),
                             (self.langs.get(100), "lr_classic_yellow"),
                             (self.langs.get(96), "lr_classic_blue"),
                             (self.langs.get(97), "lr_classic_cyan"),
                             (self.langs.get(99), "lr_classic_red")]
            COLOR_CAR_2_1 = [(self.langs.get(96), "lr_modern_blue"),
                             (self.langs.get(99), "lr_modern_red"),
                             (self.langs.get(98), "lr_modern_pink"),
                             (self.langs.get(101), "lr_modern_green")]
            COLOR_CAR_2_2 = [(self.langs.get(99), "lr_modern_red"),
                             (self.langs.get(98), "lr_modern_pink"),
                             (self.langs.get(101), "lr_modern_green"),
                             (self.langs.get(96), "lr_modern_blue")]
            COLOR_CAR_2_3 = [(self.langs.get(98), "lr_modern_pink"),
                             (self.langs.get(101), "lr_modern_green"),
                             (self.langs.get(96), "lr_modern_blue"),
                             (self.langs.get(99), "lr_modern_red")]
            COLOR_CAR_2_4 = [(self.langs.get(101), "lr_modern_green"),
                             (self.langs.get(96), "lr_modern_blue"),
                             (self.langs.get(99), "lr_modern_red"),
                             (self.langs.get(98), "lr_modern_pink")]
            COLOR_CAR_3_1 = [(self.langs.get(100), "lr_super_yellow"),
                             (self.langs.get(97), "lr_super_cyan"),
                             (self.langs.get(98), "lr_super_pink"),
                             (self.langs.get(101), "lr_super_green")]
            COLOR_CAR_3_2 = [(self.langs.get(97), "lr_super_cyan"),
                             (self.langs.get(98), "lr_super_pink"),
                             (self.langs.get(101), "lr_super_green"),
                             (self.langs.get(100), "lr_super_yellow")]
            COLOR_CAR_3_3 = [(self.langs.get(98), "lr_super_pink"),
                             (self.langs.get(101), "lr_super_green"),
                             (self.langs.get(100), "lr_super_yellow"),
                             (self.langs.get(97), "lr_super_cyan")]
            COLOR_CAR_3_4 = [(self.langs.get(101), "lr_super_green"),
                             (self.langs.get(100), "lr_super_yellow"),
                             (self.langs.get(97), "lr_super_cyan"),
                             (self.langs.get(98), "lr_super_pink")]

            # Tipos de auto
            TYPECAR_1 = [(self.langs.get(43), "1"), (self.langs.get(44), "2"),
                         (self.langs.get(45), "3")]
            TYPECAR_2 = [(self.langs.get(44), "2"), (self.langs.get(45), "3"),
                         (self.langs.get(43), "1")]
            TYPECAR_3 = [(self.langs.get(45), "3"), (self.langs.get(43), "1"),
                         (self.langs.get(44), "2")]

            def _launchTrack():
                """
                Lanza una pista.
                :return: void
                """
                self.reset(0)
                self.menuSoundChannel.stop()
                self.world.load_map()
                self.controller.disable_menu()
                self.controller.set_player()
                self.view.start_playing_render()

            def _saveConfig(value, *args):
                """
                Función que guarda configuraciones y las aplica.
                :param value: Valor de la configuración
                :param *args: Argumentos adicionales
                :return: void
                """
                if args[1] != "SCREENSIZE":
                    args[0].setParameter(args[1], value)
                    args[0].export()
                else:
                    value = value.split(" ")
                    args[0].setParameter("WIDTH", value[0])
                    args[0].setParameter("HEIGHT", value[1])
                    args[0].export()
                    self.menu_configuracion.actual.opciones.pop(2)
                    self.menu_configuracion.actual.posOptionY -= (
                            -self.menu_configuracion.actual.fontsize / 2 - self.menu_configuracion.actual.optiondy / 2)
                    self.menu_configuracion.add_selector(self.langs.get(110),
                                                         self.window.get_display_list(),
                                                         _saveConfig,
                                                         None,
                                                         self.config_window,
                                                         "SCREENSIZE", index=2)
                    self.menu_configuracion.actual.size -= 1
                    # self.window.update()
                    # self.view.updateWindowSize()
                # Se aplican la configuraciones
                # Si se cambio el modo de ventana
                if args[1] == "WINDOWED" and value == "FALSE":
                    self.window.set_fullscreen()
                elif args[1] == "WINDOWED" and value == "TRUE":
                    self.window.set_windowed()
                # Si se activan / desactivan los sonidos
                if args[1] == "ENABLESOUND":
                    if value == "FALSE":
                        self.menu_inicial_sfx.stop()
                    self.updateSound()
                # Si se activa / desactiva el mostrar los fps en el titulo de la ventana
                if args[1] == "SHOWFPS":
                    self.view.update_show_fps()
                # Si se cambia la pista a jugar
                if args[1] == "TYPECAR":
                    self.menu_jugar.actual.opciones.pop(2)
                    self.menu_jugar.actual.opciones.pop(2)
                    self.menu_jugar.actual.posOptionY -= 2 * (
                            -self.menu_jugar.actual.fontsize / 2 - self.menu_jugar.actual.optiondy / 2)
                    if value == "1":
                        self.menu_jugar.add_selector(self.langs.get(94),
                                                     TYPECAR_1, _saveConfig,
                                                     _launchTrack,
                                                     self.config_user,
                                                     "TYPECAR", index=2)
                        self.config_user.setParameter("TEXTURE",
                                                      "lr_classic_red")
                        self.menu_jugar.add_selector(self.langs.get(95),
                                                     COLOR_CAR_1_4,
                                                     _saveConfig,
                                                     _launchTrack,
                                                     self.config_user,
                                                     "TEXTURE", index=3)
                    elif value == "2":
                        self.menu_jugar.add_selector(self.langs.get(94),
                                                     TYPECAR_2, _saveConfig,
                                                     _launchTrack,
                                                     self.config_user,
                                                     "TYPECAR", index=2)
                        self.config_user.setParameter("TEXTURE",
                                                      "lr_modern_red")
                        self.menu_jugar.add_selector(self.langs.get(95),
                                                     COLOR_CAR_2_2,
                                                     _saveConfig,
                                                     _launchTrack,
                                                     self.config_user,
                                                     "TEXTURE", index=3)
                    elif value == "3":
                        self.menu_jugar.add_selector(self.langs.get(94),
                                                     TYPECAR_3, _saveConfig,
                                                     _launchTrack,
                                                     self.config_user,
                                                     "TYPECAR", index=2)
                        self.config_user.setParameter("TEXTURE",
                                                      "lr_super_cyan")
                        self.menu_jugar.add_selector(self.langs.get(95),
                                                     COLOR_CAR_3_2,
                                                     _saveConfig,
                                                     _launchTrack,
                                                     self.config_user,
                                                     "TEXTURE", index=3)
                    self.menu_jugar.actual.size -= 2
                    args[0].export()
                # Si se activa/ desactiva el mostrar el fantasma
                if args[1] == "SHOWGHOST":
                    self.view.update_show_ghost()

            # Menú jugar
            self.menu_jugar = Menu(self.window, self.font, self.langs.get(61),
                                   draw_region_y=55)
            self.menu_jugar.add_option(self.langs.get(104), _launchTrack)
            # Se cargan los mapas
            tracks = []
            actual_map = int(self.config_map.getValue("DEFAULTMAP"))
            tracks.append((TRACKS[actual_map], str(actual_map)))
            for track in TRACKS.keys():
                if track != actual_map:
                    tracks.append((TRACKS[track], str(track)))
            self.menu_jugar.add_selector(self.langs.get(103), tracks,
                                         _saveConfig, None, self.config_map,
                                         "DEFAULTMAP")
            if self.config_user.getValue("TYPECAR") == "1":
                typecar_values = TYPECAR_1
            elif self.config_user.getValue("TYPECAR") == "2":
                typecar_values = TYPECAR_2
            else:
                typecar_values = TYPECAR_3
            self.menu_jugar.add_selector(self.langs.get(94), typecar_values,
                                         _saveConfig, None, self.config_user,
                                         "TYPECAR")
            if self.config_user.getValue("TYPECAR") == "1":
                if self.config_user.getValue("TEXTURE") == "lr_classic_yellow":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_1_1, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_classic_blue":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_1_2, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_classic_cyan":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_1_3, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_classic_red":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_1_4, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_classic_pink":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_1_5, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                else:
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_1_4, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
            elif self.config_user.getValue("TYPECAR") == "2":
                if self.config_user.getValue("TEXTURE") == "lr_modern_blue":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_2_1, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_modern_red":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_2_2, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_modern_pink":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_2_3, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_modern_green":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_2_4, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                else:
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_2_2, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
            elif self.config_user.getValue("TYPECAR") == "3":
                if self.config_user.getValue("TEXTURE") == "lr_super_yellow":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_3_1, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_super_cyan":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_3_2, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_super_pink":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_3_3, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                elif self.config_user.getValue("TEXTURE") == "lr_super_green":
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_3_4, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
                else:
                    self.menu_jugar.add_selector(self.langs.get(95),
                                                 COLOR_CAR_3_2, _saveConfig,
                                                 _launchTrack,
                                                 self.config_user, "TEXTURE")
            self.menu_jugar.add_option(self.langs.get(102), MENU_BACK)
            # Menu de configuraciones
            self.menu_configuracion = Menu(self.window, self.font,
                                           self.langs.get(62), centered=False,
                                           draw_region_x=5,
                                           font_size=25, option_margin=20)
            if self.config_window.isTrue("WINDOWED"):
                window_values = [(self.langs.get(84), "TRUE"),
                                 (self.langs.get(85), "FALSE")]
            else:
                window_values = [(self.langs.get(85), "FALSE"),
                                 (self.langs.get(84), "TRUE")]
            if self.config_game.isTrue("ENABLESOUND"):
                sound_values = [(self.langs.get(84), "TRUE"),
                                (self.langs.get(85), "FALSE")]
            else:
                sound_values = [(self.langs.get(85), "FALSE"),
                                (self.langs.get(84), "TRUE")]
            if self.config_game.getValue("LANG") == "ES":
                lang_values = [(self.langs.get(89), "ES"),
                               (self.langs.get(90), "EN")]
            else:
                lang_values = [(self.langs.get(90), "EN"),
                               (self.langs.get(89), "ES")]
            # if self.config_game.getValue("FPS") == "60": fps_values = [("60", "60"), ("30", "30"), ("45", "45")]
            # elif self.config_game.getValue("FPS") == "30": fps_values = [("30", "30"), ("45", "45"), ("60", "60")]
            # else: fps_values = [("45", "45"), ("60", "60"), ("30", "30")]
            if self.config_view.isTrue("SHOWFPS"):
                showfps_values = [(self.langs.get(84), "TRUE"),
                                  (self.langs.get(85), "FALSE")]
            else:
                showfps_values = [(self.langs.get(85), "FALSE"),
                                  (self.langs.get(84), "TRUE")]
            if self.config_view.isTrue("SHOWGHOST"):
                showghost_values = [(self.langs.get(84), "TRUE"),
                                    (self.langs.get(85), "FALSE")]
            else:
                showghost_values = [(self.langs.get(85), "FALSE"),
                                    (self.langs.get(84), "TRUE")]
            self.menu_configuracion.add_selector(self.langs.get(88),
                                                 lang_values, _saveConfig,
                                                 None,
                                                 self.config_game,
                                                 "LANG")
            self.menu_configuracion.add_selector(self.langs.get(87),
                                                 sound_values, _saveConfig,
                                                 None, self.config_game,
                                                 "ENABLESOUND")
            self.menu_configuracion.add_selector(self.langs.get(110),
                                                 self.window.get_display_list(),
                                                 _saveConfig, None,
                                                 self.config_window,
                                                 "SCREENSIZE")
            self.menu_configuracion.add_selector(self.langs.get(83),
                                                 window_values, _saveConfig,
                                                 None,
                                                 self.config_window,
                                                 "WINDOWED")
            # self.menu_configuracion.addSelector(self.langs.get(91),fps_values,_saveConfig,None,self.config_game,"FPS")
            self.menu_configuracion.add_selector(self.langs.get(92),
                                                 showfps_values, _saveConfig,
                                                 None, self.config_view,
                                                 "SHOWFPS")
            self.menu_configuracion.add_selector(self.langs.get(93),
                                                 showghost_values, _saveConfig,
                                                 None,
                                                 self.config_view, "SHOWGHOST")
            self.menu_configuracion.add_option(self.langs.get(86), MENU_BACK)

            # Menú de ayuda
            menu_ayuda = Textmenu(self.window, self.font, self.langs.get(63),
                                  font_text_size=18, draw_text_region=2,
                                  draw_region_y=58)
            menu_ayuda.add_text(self.langs.get(66))
            menu_ayuda.add_text(self.langs.get(68))
            menu_ayuda.add_text(self.langs.get(69))
            menu_ayuda.add_text(self.langs.get(70))
            menu_ayuda.add_text(self.langs.get(71))
            menu_ayuda.add_text(self.langs.get(72))
            menu_ayuda.add_text(self.langs.get(73))
            menu_ayuda.add_text(self.langs.get(74))
            menu_ayuda.add_text(self.langs.get(75))
            menu_ayuda.add_text(self.langs.get(76))
            menu_ayuda.add_text(self.langs.get(77))
            menu_ayuda.add_text(self.langs.get(78))
            menu_ayuda.add_option(self.langs.get(67), MENU_BACK)

            # Menú acerca de
            menu_acercade = Textmenu(self.window, self.font,
                                     self.langs.get(64), text_centered=True,
                                     draw_text_region=50, draw_region_y=50)
            menu_acercade.add_text(self.langs.get(79))
            menu_acercade.add_text(self.langs.get(80))
            menu_acercade.add_text(self.langs.get(81))
            menu_acercade.add_text(self.langs.get(82))
            menu_acercade.add_option(self.langs.get(67), MENU_BACK)

            # Se crea el menú de inicio
            self.menu_inicial = Menu(self.window, self.font,
                                     self.langs.get(60), draw_region_y=56)
            self.menu_inicial.add_option(self.langs.get(61), self.menu_jugar)
            self.menu_inicial.add_option(self.langs.get(62),
                                         self.menu_configuracion)
            self.menu_inicial.add_option(self.langs.get(63), menu_ayuda)
            self.menu_inicial.add_option(self.langs.get(64), menu_acercade)
            self.menu_inicial.add_option(self.langs.get(65), MENU_EXIT)
        except:
            errors.throw(errors.ERROR_CREATE_MENU)

    def initializeMenuPausa(self):
        """
        Inicia el menú de pausa.
        :return: void
        """

        def _returnIntialMenu():
            """
            Funcion que vuelve al menú principal.
            :return: void
            """
            self.setZeroIndex()
            self.world.clear_actual_map()
            self.view.stop_playing_render()
            self.controller.del_player()

        def _back():
            """
            Retorna el juego.
            :return: void
            """
            self.setZeroIndex()
            self.controller.disable_menu()
            self.world.get_actual_map().get_player().sound_unpause()

        def _reinitiate():
            """
            Reinicia el juego.
            :return: void
            """
            _back()
            self.world.get_actual_map().get_player().clear(True)

        self.menu_pausa = Menu(self.window, self.font, self.langs.get(105),
                               height=230, width=440, font_size=30,
                               draw_region_y=60)
        self.menu_pausa.add_option(self.langs.get(107), _back)
        self.menu_pausa.add_option(self.langs.get(106), _reinitiate)
        self.menu_pausa.add_option(self.langs.get(86), _returnIntialMenu)

    def left(self):
        """
        Mueve el selector del menú actual hacia la izquierda.
        :return: void
        """
        self.sound()
        self.actualmenu.left()

    def reset(self, times):
        """
        Resetea el menú
        :param times: Número de veces (en plan recursivo).
        :return:
        """
        self.actualmenu.reset(times)

    def right(self):
        """
        Mueve el selector del menú actual hacia la derecha.
        :return: void
        """
        self.sound()
        self.actualmenu.right()

    def select(self):
        """
        Selecciona la opción actual.
        :return: void
        """
        self.actualmenu.select()

    def setActualMenu(self, menuEvent):
        """
        Define el menu actual.
        :param menuEvent: Evento del menú
        :return: void
        """
        if menuEvent == MENU_INICIAL:
            self.actualmenu = self.menu_inicial
        elif menuEvent == MENU_PAUSE:
            self.actualmenu = self.menu_pausa

    def setZeroIndex(self):
        """
        Define el índice cero.
        :return: void
        """
        self.actualmenu.index = 0

    def sound(self):
        """
        Reproduce el efecto de sonido del menú.
        :return: void
        """
        if self.sound_state and not self.menuButtonChannel.get_busy():
            self.menuButtonChannel.play(self.menu_button_down)

    def up(self):
        """
        Sube el menú actual.
        :return: void
        """
        self.sound()
        self.actualmenu.up()

    def updateSound(self):
        """
        Comprueba si los sonidos están activos.
        :return: void
        """
        self.sound_state = self.config_game.isTrue("ENABLESOUND")
