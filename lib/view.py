# coding=utf-8
"""
VISTA
Es el encargado de dibujar sobre la pantalla todos los modelos.

Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

if __name__ == '__main__':
    from path import *  # @UnusedWildImport

# Importación de librerías
from bin import *  # @UnusedWildImport
from bin.errors import *  # @UnusedWildImport
from controller import STATE_MENU, STATE_NEXT, STATE_PLAY
from data import DIR_SAVES
from player import TRACK_NOT_DEFINED, STATE_INVALIDPOS, STATE_NULL, STATE_OFFROAD, STATE_WRONGWAY, METRICS, \
    CAMBIO_NEUTRO, CAMBIO_REVERSA
from resources.fonts import getFonts
from resources.images import getImages
from revolgraph import Revolgraph
from uimenu import MENU_INICIAL, MENU_PAUSE
from world import NEXT_TRACK, get_next_track, TRACKS

# Definición de constantes
COLOR_ALERT = (165, 0, 0, 128)
COLOR_BRONCE = (205, 127, 50)
COLOR_COMPLETED = (42, 141, 55)
COLOR_FAILED_OBJETIVE = (102, 102, 102)
COLOR_ORO = (231, 174, 24)
COLOR_PLATA = (192, 192, 192)
COLOR_RESULT_LINE = (51, 51, 51)
COLOR_VELOCIMETER = (255, 255, 255, 128)
SAVE_FILE_STATICS = False


# noinspection PyBroadException,PyUnresolvedReferences,PyShadowingNames
class View(object):
    """Vista de la aplicación"""

    def __init__(self, window, clock, world, lang, view_config, menus):
        """
        Función constructora
        :param window: Ventana de la aplicación
        :param clock: Reloj de pygame
        :param world: Mundo lógico
        :param lang: Diccionario de idiomas
        :param view_config: Configuraciones de la vista
        :param menus: Menues del juego
        :return: void
        """

        # Se guardan los parametros
        self.config = view_config  # configuracion de la vista
        self.controller = None  # controlador
        self.lang = lang  # idiomas
        self.map = world.get_actual_map()  # mapa actual
        self.menu = menus  # menus del juego
        self.window = window  # ventana
        self.world = world  # mundo
        if self.map is None:
            self.isPlaying = False
        else:
            self.isPlaying = True
        # Se cargan configuraciones
        self.mark_ground_size = int(view_config.getValue(
            "GROUND_MARK_SIZE"))  # ancho de la marca en la tierra
        self.mark_track_size = int(view_config.getValue(
            "TRACK_MARK_SIZE"))  # ancho de la marca en la pista
        self.show_fps = view_config.isTrue(
            "SHOWFPS")  # define si se dibuja el fps en el titulo de la ventana
        self.show_ghost = view_config.isTrue(
            "SHOWGHOST")  # define si se dibuja al ghost o no
        self.show_mark_ground = view_config.isTrue(
            "SHOWMARKGROUND")  # define si se muestran las marcas en la tierra
        self.show_mark_track = view_config.isTrue(
            "SHOWMARKTRACK")  # define si se muestran las marcas en el camino
        self.show_player = view_config.isTrue(
            "SHOWPLAYER")  # se define si se dibuja o no el jugador en pantalla
        self.show_ruedas = view_config.isTrue(
            "SHOWRUEDAS")  # define si se dibujan las ruedas o no
        self.show_track = view_config.isTrue(
            "SHOWTRACK")  # define si se muestra la pista o no
        self.show_ui = view_config.isTrue(
            "SHOWUI")  # se define si se dibujan los paneles
        self.viewConfig = view_config  # configuraciones de la vista
        # Se defienen variables
        self.clock = clock  # reloj del juego
        self.screen = self.window.get_surface()  # superficie de dibujo
        self.windowHeight = self.window.get_window_height()  # alto de la ventana
        self.windowWidth = self.window.get_window_width()  # ancho de la ventana
        # Se crean objetos del HUD
        self.OutOfRoadFont = pygame.font.Font(getFonts("speed"),
                                              20)  # fuente fuera de la pista
        self.buttonsResultsFont = pygame.font.Font(getFonts("menu"),
                                                   20)  # fuentes de los botones de la ventana de resultados
        self.lapFont = pygame.font.Font(getFonts("lap"),
                                        40)  # fuente del contador de vueltas
        self.lapFontL = pygame.font.Font(getFonts("lap"),
                                         38)  # fuente del contador de vueltas
        self.lapPos = (self.windowWidth * 0.90,
                       self.windowHeight * 0.05)  # posición del cuenta-vueltas
        self.lapRect = pygame.image.load(
            getImages("lap_rect")).convert_alpha()  # recuadro de las vueltas
        self.lapTimeFont = pygame.font.Font(getFonts("speed"),
                                            20)  # fuente del contador de tiempo
        self.lapTimePos = (self.windowWidth * 0.03,
                           self.windowHeight * 0.05)  # posición del tiempo total
        self.posOutOfRoad = (
            self.windowWidth * 0.5 - 100,
            self.windowHeight * 0.95)  # posición del mensaje -fuera de la pista-
        self.resultsButtonNextPos = (
            int((self.windowWidth + 680) / 2) - 15, int(
                (
                    self.windowHeight + 400) / 2) - 5)  # posicion del boton siguiente del plano de resultados
        self.resultsButtonQuitPos = (
            int((self.windowWidth - 680) / 2) + 15, int(
                (
                    self.windowHeight + 400) / 2) - 5)  # posicion del boton cerrar del plano de resultados
        self.resultsFontTitle = pygame.font.Font(getFonts("speed"),
                                                 30)  # fuente de los resultados
        self.resultsFontTitleContent = pygame.font.Font(getFonts("speed"),
                                                        14)  # fuente del contenido de la pantalla resultados
        self.resultsFontTitleSubtl = pygame.font.Font(getFonts("speed"),
                                                      20)  # fuente del subtitulo de la pantalla resultados
        self.resultsFontTitleSubtl2 = pygame.font.Font(getFonts("speed"),
                                                       17)  # fuente del subtitulo de la pantalla resultados
        self.resultsFontTitleTrack = pygame.font.Font(getFonts("speed"),
                                                      20)  # fuente del titulo de la pista de la pantalla resultados
        self.resultsScreen = pygame.image.load(
            getImages("results")).convert_alpha()  # pantalla de resultados
        self.resultsScreenPos = (int((self.windowWidth - 680) / 2),
                                 int((
                                         self.windowHeight - 400) / 2) - 25)  # posición en pantalla de los resultados
        self.revolPos = (self.windowWidth - 20,
                         self.windowHeight - 60)  # posición del cuenta-revoluciones
        self.revolRect = pygame.image.load(
            getImages(
                "revol_shadowed")).convert_alpha()  # textura del cuenta-revoluciones
        self.speedFont = pygame.font.Font(getFonts("speed"),
                                          40)  # fuente de los cambios
        self.speedPos = (
            20, self.windowHeight - 60)  # posición del velocimetro
        self.speedRect = pygame.image.load(getImages(
            "velocimeter_shadowed")).convert_alpha()  # textura del velocimetro
        # Objetos del HUD dependientes
        self.revolGraph = Revolgraph(33, (
            self.revolPos[0] - 170, self.revolPos[1] + 7), 100,
                                     40)  # gráfico de las revoluciones

    def add_controller(self, controller):
        """
        Añade un controlador
        :param controller: Objeto <controller>
        :return: void
        """
        self.controller = controller

    def draw(self, state):
        """
        Dibuja en pantalla
        :param state: Estado del controlador (string)
        :return: void
        """
        time = float(
            self.clock.get_time()) / 1000.0  # tiempo que tomo el frame en generarse
        # Si la opcion de mostrar fps esta habilitada
        if self.show_fps:
            self.window.set_window_title(self.lang.get(10) + " - FPS: " + str(
                int(self.clock.get_fps())))
        # Si se encuentra jugando
        if state == STATE_PLAY and self.isPlaying:
            # Se obtiene la posición de la cámara
            camera_pos = self.map.get_player().get_pos()
            camera_rel_pos = self.map.get_player().get_relative_pos()
            # Se redibuja el fondo
            bg_size = self.map.get_background_size()
            defaultx = self.map.get_map_limits()[0]
            max_x = self.map.get_map_limits()[2]
            max_y = self.map.get_map_limits()[3]
            y = self.map.get_map_limits()[1]
            fondo = self.map.get_background()
            while True:
                x = defaultx
                while True:
                    drawx = -camera_rel_pos[0] + x
                    drawy = -camera_rel_pos[1] + y
                    # Si se ve en la pantalla se dibuja
                    if -bg_size[0] < drawx < self.windowWidth and -bg_size[1] < drawy < self.windowHeight:
                        self.screen.blit(fondo, (drawx, drawy))
                    x += bg_size[0]
                    if x >= max_x:
                        break
                y += bg_size[1]
                if y >= max_y:
                    break
            # Se dibujan las marcas del terreno
            if self.show_mark_ground:
                for marca_tierra in self.map.get_marcas_tierra():
                    pos_ini = marca_tierra[0]
                    pos_fin = marca_tierra[1]
                    drawxini = (-self.windowWidth / 2 + camera_pos[0]) + pos_ini[0]
                    drawyini = (-self.windowHeight + camera_pos[1]) + pos_ini[
                        1] + 300
                    drawxfin = (-self.windowWidth / 2 + camera_pos[0]) + pos_fin[0]
                    drawyfin = (-self.windowHeight + camera_pos[1]) + pos_fin[
                        1] + 300
                    if (0 <= drawxini <= self.windowWidth and 0 <= drawyini <= self.windowHeight) or (
                                        0 <= drawxfin <= self.windowWidth and 0 <= drawyfin <= self.windowHeight):
                        pygame.draw.line(self.screen, marca_tierra[2],
                                         (drawxini, drawyini),
                                         (drawxfin, drawyfin),
                                         self.mark_ground_size)
            # Se dibujan las pistas
            if self.show_track:
                for track in self.map.get_track():
                    track.draw(self.screen, self.window, camera_pos)
            # Se dibujan las marcas sobre la pista
            if self.show_mark_track:
                for marca_camino in self.map.get_marcas_frenado():
                    pos_ini = marca_camino[0]
                    pos_fin = marca_camino[1]
                    drawxini = (-self.windowWidth / 2 + camera_pos[0]) + pos_ini[0]
                    drawyini = (-self.windowHeight + camera_pos[1]) + pos_ini[
                        1] + 300
                    drawxfin = (-self.windowWidth / 2 + camera_pos[0]) + pos_fin[0]
                    drawyfin = (-self.windowHeight + camera_pos[1]) + pos_fin[
                        1] + 300
                    if (0 <= drawxini <= self.windowWidth and 0 <= drawyini <= self.windowHeight) or (
                                        0 <= drawxfin <= self.windowWidth and 0 <= drawyfin <= self.windowHeight):
                        pygame.draw.line(self.screen, marca_camino[2],
                                         (drawxini, drawyini),
                                         (drawxfin, drawyfin),
                                         self.mark_track_size)
            # Si no se ha terminado la pista
            if not self.map.get_player().finished_lap():
                # Se dibuja el jugador
                if self.show_player:
                    self.map.get_player().collide(self.screen, time)
                    message = self.map.get_player().draw(self.screen, time,
                                                         True, self.window,
                                                         draw_ruedas=self.show_ruedas,
                                                         show_ghost=self.show_ghost)
                else:
                    message = STATE_NULL
                # Se dibujan las decoraciones
                for decoration in self.map.get_decorations():
                    decoration.draw(self.screen, self.window, camera_pos)
                # Se dibuja la ui
                if self.show_ui:
                    # Se dibuja la velocidad actual
                    self.screen.blit(self.speedRect, (
                        self.speedPos[0] - 300, self.speedPos[1] - 50))
                    self.screen.blit(self.speedFont.render(
                        str(self.map.get_player().get_vel_kph()), 1,
                        COLOR_VELOCIMETER),
                        (self.speedPos[0] - 10,
                         self.speedPos[1] + 10))
                    self.screen.blit(
                        self.speedFont.render(METRICS, 1, COLOR_VELOCIMETER),
                        (self.speedPos[0] + 60, self.speedPos[1] + 10))
                    # Se dibujan las revoluciones
                    self.screen.blit(self.revolRect, (
                        self.revolPos[0] - 210, self.revolPos[1] - 50))
                    self.revolGraph.draw(self.screen,
                                         self.map.player.get_revl())
                    # Se dibuja el cambio
                    cambio = self.map.player.get_cambio()
                    if cambio == 0:
                        cambio = CAMBIO_NEUTRO
                    elif cambio < 0:
                        cambio = CAMBIO_REVERSA
                    else:
                        cambio = str(cambio)
                    self.screen.blit(
                        self.speedFont.render(cambio, 1, COLOR_VELOCIMETER),
                        (self.revolPos[0] - 20, self.revolPos[1] + 10))
                    # Se dibuja la vuelta actual
                    self.screen.blit(self.lapRect, (
                        self.lapPos[0] - 120, self.lapPos[1] - 8))
                    self.screen.blit(self.lapFont.render(self.lang.get(11), 1,
                                                         COLOR_VELOCIMETER),
                                     (self.lapPos[0] - 115, self.lapPos[1]))
                    self.screen.blit(
                        self.lapFontL.render(
                            str(self.map.player.get_lap_pos()) + "/" + str(
                                self.map.get_laps()), 1,
                            COLOR_VELOCIMETER),
                        (self.lapPos[0] - 12, self.lapPos[1]))
                    # Dibuja el tiempo de vuelta
                    self.screen.blit(
                        self.lapTimeFont.render(self.lang.get(
                            12) + " " * 6 + self.map.get_player().get_lap_time(),
                                                1,
                                                COLOR_VELOCIMETER),
                        (self.lapPos[0] - 121, self.lapPos[1] + 40))
                    # Se dibujan los objetivos
                    k = 0
                    if self.map.player.get_lap_pos() == 1:
                        for obj in self.map.get_player().get_track_objetives():
                            if k == 0:
                                self.screen.blit(
                                    self.lapTimeFont.render(self.lang.get(19,
                                                                          self.map.get_player().get_lap_time(
                                                                              obj)),
                                                            1,
                                                            COLOR_ORO),
                                    (20, 20 + 29 * k))
                                if self.map.get_player().get_lap_time_no_format() > obj:
                                    pygame.draw.line(self.screen, COLOR_ALERT,
                                                     (17, 31 + 29 * k),
                                                     (155, 31 + 29 * k), 3)
                            if k == 1:
                                self.screen.blit(
                                    self.lapTimeFont.render(self.lang.get(20,
                                                                          self.map.get_player().get_lap_time(
                                                                              obj)),
                                                            1,
                                                            COLOR_PLATA),
                                    (20, 20 + 29 * k))
                                if self.map.get_player().get_lap_time_no_format() > obj:
                                    pygame.draw.line(self.screen, COLOR_ALERT,
                                                     (17, 31 + 29 * k),
                                                     (175, 31 + 29 * k), 3)
                            if k == 2:
                                self.screen.blit(
                                    self.lapTimeFont.render(self.lang.get(21,
                                                                          self.map.get_player().get_lap_time(
                                                                              obj)),
                                                            1,
                                                            COLOR_BRONCE),
                                    (20, 20 + 29 * k))
                                if self.map.get_player().get_lap_time_no_format() > obj:
                                    pygame.draw.line(self.screen, COLOR_ALERT,
                                                     (17, 31 + 29 * k),
                                                     (195, 31 + 29 * k), 3)
                            k += 1
                    else:
                        for obj in self.map.get_player().get_track_objetives():
                            if k == 0:
                                if self.map.get_player().get_fast_lap()[1] < obj:
                                    self.screen.blit(self.lapTimeFont.render(
                                        self.lang.get(19, self.lang.get(46)),
                                        1,
                                        COLOR_RESULT_LINE), (20, 20 + 29 * k))
                                else:
                                    self.screen.blit(
                                        self.lapTimeFont.render(
                                            self.lang.get(19,
                                                          self.map.get_player().get_lap_time(
                                                              obj)),
                                            1, COLOR_ORO), (20, 20 + 29 * k))
                                    if self.map.get_player().get_lap_time_no_format() > obj:
                                        pygame.draw.line(self.screen,
                                                         COLOR_ALERT,
                                                         (17, 31 + 29 * k),
                                                         (155, 31 + 29 * k), 3)
                            if k == 1:
                                if self.map.get_player().get_fast_lap()[1] < obj:
                                    self.screen.blit(self.lapTimeFont.render(
                                        self.lang.get(20, self.lang.get(46)),
                                        1,
                                        COLOR_RESULT_LINE), (20, 20 + 29 * k))
                                else:
                                    self.screen.blit(
                                        self.lapTimeFont.render(
                                            self.lang.get(20,
                                                          self.map.get_player().get_lap_time(
                                                              obj)),
                                            1, COLOR_PLATA), (20, 20 + 29 * k))
                                    if self.map.get_player().get_lap_time_no_format() > obj:
                                        pygame.draw.line(self.screen,
                                                         COLOR_ALERT,
                                                         (17, 31 + 29 * k),
                                                         (155, 31 + 29 * k), 3)
                            if k == 2:
                                if self.map.get_player().get_fast_lap()[1] < obj:
                                    self.screen.blit(self.lapTimeFont.render(
                                        self.lang.get(21, self.lang.get(46)),
                                        1,
                                        COLOR_RESULT_LINE), (20, 20 + 29 * k))
                                else:
                                    self.screen.blit(
                                        self.lapTimeFont.render(
                                            self.lang.get(21,
                                                          self.map.get_player().get_lap_time(
                                                              obj)),
                                            1, COLOR_BRONCE),
                                        (20, 20 + 29 * k))
                                    if self.map.get_player().get_lap_time_no_format() > obj:
                                        pygame.draw.line(self.screen,
                                                         COLOR_ALERT,
                                                         (17, 31 + 29 * k),
                                                         (155, 31 + 29 * k), 3)
                            k += 1
                    # Se escriben los mensajes enviados por draw
                    red = False
                    if message == STATE_OFFROAD:
                        self.screen.blit(
                            self.OutOfRoadFont.render(self.lang.get(13), 1,
                                                      COLOR_ALERT),
                            self.posOutOfRoad)
                        red = True
                    elif message == STATE_INVALIDPOS:
                        self.screen.blit(
                            self.OutOfRoadFont.render(self.lang.get(14), 1,
                                                      COLOR_ALERT),
                            (self.posOutOfRoad[0] - 67, self.posOutOfRoad[1]))
                        red = True
                    elif message == STATE_WRONGWAY:
                        self.screen.blit(
                            self.OutOfRoadFont.render(self.lang.get(15), 1,
                                                      COLOR_ALERT),
                            (self.posOutOfRoad[0] - 25, self.posOutOfRoad[1]))
                        red = True
                    # Si la vuelta es valida se escribe el tiempo en blanco
                    if not red:
                        self.screen.blit(
                            self.lapTimeFont.render(self.lang.get(
                                12) + " " * 6 + self.map.get_player().get_lap_time(),
                                                    1,
                                                    COLOR_VELOCIMETER),
                            (self.lapPos[0] - 121, self.lapPos[1] + 40))
                    else:
                        self.screen.blit(
                            self.lapTimeFont.render(self.lang.get(
                                12) + " " * 6 + self.map.get_player().get_lap_time(),
                                                    1,
                                                    COLOR_ALERT),
                            (self.lapPos[0] - 121, self.lapPos[1] + 40))
            # Si ya termino la pista se muestran los resultados
            else:
                # Se dibuja al jugador sin actualizar
                self.map.get_player().draw(self.screen, time, False,
                                           self.window, draw_ruedas=False,
                                           show_ghost=True)
                # Se dibuja el recuadro de resultados
                self.screen.blit(self.resultsScreen, self.resultsScreenPos)
                self.screen.blit(
                    self.resultsFontTitle.render(self.lang.get(16), 1,
                                                 COLOR_VELOCIMETER),
                    (self.resultsScreenPos[0] + 10,
                     self.resultsScreenPos[1] + 17))
                self.screen.blit(self.resultsFontTitleTrack.render(
                    self.lang.get(17) + self.map.get_track_title(), 1,
                    COLOR_VELOCIMETER),
                    (self.resultsScreenPos[0] + 223,
                     self.resultsScreenPos[1] + 35))
                self.screen.blit(
                    self.resultsFontTitleSubtl.render(self.lang.get(18), 1,
                                                      COLOR_VELOCIMETER),
                    (self.resultsScreenPos[0] + 49,
                     self.resultsScreenPos[1] + 70))
                pygame.draw.line(self.screen, COLOR_RESULT_LINE,
                                 (self.resultsScreenPos[0] + 191,
                                  self.resultsScreenPos[1] + 62),
                                 (self.resultsScreenPos[0] + 191,
                                  self.resultsScreenPos[1] + 399))
                pygame.draw.line(self.screen, COLOR_RESULT_LINE,
                                 (self.resultsScreenPos[0] + 191,
                                  self.resultsScreenPos[1] + 62),
                                 (self.resultsScreenPos[0] + 679,
                                  self.resultsScreenPos[1] + 62))
                pygame.draw.line(self.screen, COLOR_RESULT_LINE,
                                 (self.resultsScreenPos[0] + 191,
                                  self.resultsScreenPos[1] + 62),
                                 (self.resultsScreenPos[0] + 191,
                                  self.resultsScreenPos[1] + 399))
                pygame.draw.line(self.screen, COLOR_RESULT_LINE,
                                 (self.resultsScreenPos[0] + 433,
                                  self.resultsScreenPos[1] + 62),
                                 (self.resultsScreenPos[0] + 433,
                                  self.resultsScreenPos[1] + 399))
                # Tipo de auto
                self.screen.blit(
                    self.resultsFontTitleSubtl2.render(self.lang.get(42), 1,
                                                       COLOR_VELOCIMETER),
                    (self.resultsScreenPos[0] + 470,
                     self.resultsScreenPos[1] + 38))
                tipo = self.map.get_player().get_type()
                if tipo == 1:
                    self.screen.blit(
                        self.resultsFontTitleSubtl2.render(self.lang.get(43),
                                                           1,
                                                           COLOR_VELOCIMETER),
                        (self.resultsScreenPos[0] + 590,
                         self.resultsScreenPos[1] + 38))
                elif tipo == 2:
                    self.screen.blit(
                        self.resultsFontTitleSubtl2.render(self.lang.get(44),
                                                           1,
                                                           COLOR_VELOCIMETER),
                        (self.resultsScreenPos[0] + 590,
                         self.resultsScreenPos[1] + 38))
                elif tipo == 3:
                    self.screen.blit(
                        self.resultsFontTitleSubtl2.render(self.lang.get(45),
                                                           1,
                                                           COLOR_VELOCIMETER),
                        (self.resultsScreenPos[0] + 590,
                         self.resultsScreenPos[1] + 38))
                # Resultados
                tiempo = self.map.get_player().get_fast_lap()[1]
                oro = self.map.get_player().get_track_objetives()[0]
                plata = self.map.get_player().get_track_objetives()[1]
                bronce = self.map.get_player().get_track_objetives()[2]
                self.screen.blit(
                    self.resultsFontTitleSubtl2.render(self.lang.get(19, ""),
                                                       1, COLOR_ORO),
                    (self.resultsScreenPos[0] + 10,
                     self.resultsScreenPos[1] + 118))
                self.screen.blit(
                    self.resultsFontTitleSubtl2.render(self.lang.get(20, ""),
                                                       1, COLOR_PLATA),
                    (self.resultsScreenPos[0] + 10,
                     self.resultsScreenPos[1] + 178))
                self.screen.blit(
                    self.resultsFontTitleSubtl2.render(self.lang.get(21, ""),
                                                       1, COLOR_BRONCE),
                    (self.resultsScreenPos[0] + 10,
                     self.resultsScreenPos[1] + 238))
                if tiempo < oro:
                    self.screen.blit(
                        self.resultsFontTitleSubtl2.render(self.lang.get(46),
                                                           1, COLOR_COMPLETED),
                        (self.resultsScreenPos[0] + 50,
                         self.resultsScreenPos[1] + 118))
                    self.screen.blit(self.resultsFontTitleSubtl2.render(
                        self.lang.get(48, self.map.get_player().get_lap_time(
                            oro - tiempo)), 1, COLOR_COMPLETED),
                        (self.resultsScreenPos[0] + 50,
                         self.resultsScreenPos[1] + 138))
                else:
                    self.screen.blit(
                        self.resultsFontTitleSubtl2.render(self.lang.get(47),
                                                           1, COLOR_ALERT),
                        (self.resultsScreenPos[0] + 50,
                         self.resultsScreenPos[1] + 118))
                    self.screen.blit(self.resultsFontTitleSubtl2.render(
                        self.lang.get(49, self.map.get_player().get_lap_time(
                            tiempo - oro)), 1, COLOR_ALERT),
                        (self.resultsScreenPos[0] + 50,
                         self.resultsScreenPos[1] + 138))
                if tiempo < plata:
                    self.screen.blit(
                        self.resultsFontTitleSubtl2.render(self.lang.get(46),
                                                           1, COLOR_COMPLETED),
                        (self.resultsScreenPos[0] + 63,
                         self.resultsScreenPos[1] + 178))
                    self.screen.blit(self.resultsFontTitleSubtl2.render(
                        self.lang.get(48, self.map.get_player().get_lap_time(
                            plata - tiempo)), 1, COLOR_COMPLETED),
                        (self.resultsScreenPos[0] + 50,
                         self.resultsScreenPos[1] + 198))
                else:
                    self.screen.blit(
                        self.resultsFontTitleSubtl2.render(self.lang.get(47),
                                                           1, COLOR_ALERT),
                        (self.resultsScreenPos[0] + 63,
                         self.resultsScreenPos[1] + 178))
                    self.screen.blit(self.resultsFontTitleSubtl2.render(
                        self.lang.get(49, self.map.get_player().get_lap_time(
                            tiempo - plata)), 1, COLOR_ALERT),
                        (self.resultsScreenPos[0] + 50,
                         self.resultsScreenPos[1] + 198))
                if tiempo < bronce:
                    self.screen.blit(
                        self.resultsFontTitleSubtl2.render(self.lang.get(46),
                                                           1, COLOR_COMPLETED),
                        (self.resultsScreenPos[0] + 83,
                         self.resultsScreenPos[1] + 238))
                    self.screen.blit(self.resultsFontTitleSubtl2.render(
                        self.lang.get(48, self.map.get_player().get_lap_time(
                            bronce - tiempo)), 1, COLOR_COMPLETED),
                        (self.resultsScreenPos[0] + 50,
                         self.resultsScreenPos[1] + 258))
                else:
                    self.screen.blit(
                        self.resultsFontTitleSubtl2.render(self.lang.get(47),
                                                           1, COLOR_ALERT),
                        (self.resultsScreenPos[0] + 83,
                         self.resultsScreenPos[1] + 238))
                    self.screen.blit(self.resultsFontTitleSubtl2.render(
                        self.lang.get(49, self.map.get_player().get_lap_time(
                            tiempo - bronce)), 1, COLOR_ALERT),
                        (self.resultsScreenPos[0] + 50,
                         self.resultsScreenPos[1] + 258))
                # Estadisticas
                self.screen.blit(
                    self.resultsFontTitleSubtl.render(self.lang.get(31), 1,
                                                      COLOR_VELOCIMETER),
                    (self.resultsScreenPos[0] + 247,
                     self.resultsScreenPos[1] + 70))
                self.screen.blit(
                    self.resultsFontTitleSubtl.render(self.lang.get(28), 1,
                                                      COLOR_VELOCIMETER),
                    (self.resultsScreenPos[0] + 492,
                     self.resultsScreenPos[1] + 70))
                self.screen.blit(self.resultsFontTitleContent.render(
                    self.lang.get(22, self.map.get_player().get_lap_time(
                        sum(self.map.get_player().get_laps_time()))), 1,
                    COLOR_VELOCIMETER), (
                    self.resultsScreenPos[0] + 205,
                    self.resultsScreenPos[1] + 120))
                self.screen.blit(
                    self.resultsFontTitleContent.render(self.lang.get(23,
                                                                      self.map.get_player().get_fast_lap()[
                                                                          0]),
                                                        1,
                                                        COLOR_VELOCIMETER), (
                        self.resultsScreenPos[0] + 205,
                        self.resultsScreenPos[1] + 160))
                self.screen.blit(self.resultsFontTitleContent.render(
                    self.lang.get(24, self.map.get_player().get_lap_time(
                        self.map.get_player().get_fast_lap()[1])), 1,
                    COLOR_VELOCIMETER), (
                    self.resultsScreenPos[0] + 205,
                    self.resultsScreenPos[1] + 180))
                self.screen.blit(
                    self.resultsFontTitleContent.render(
                        self.lang.get(25, self.map.get_player().get_fast_vel()),
                        1,
                        COLOR_VELOCIMETER), (
                        self.resultsScreenPos[0] + 205,
                        self.resultsScreenPos[1] + 220))
                self.screen.blit(
                    self.resultsFontTitleContent.render(self.lang.get(26), 1,
                                                        COLOR_VELOCIMETER), (
                        self.resultsScreenPos[0] + 205,
                        self.resultsScreenPos[1] + 260))
                self.screen.blit(self.resultsFontTitleContent.render(
                    self.map.get_player().get_lap_time(
                        self.map.get_player().get_tiempo_fuera()) + "s", 1,
                    COLOR_VELOCIMETER), (
                    self.resultsScreenPos[0] + 205,
                    self.resultsScreenPos[1] + 280))
                self.screen.blit(
                    self.resultsFontTitleContent.render(
                        self.lang.get(27, self.map.get_player().get_puntaje()),
                        1,
                        COLOR_VELOCIMETER), (
                        self.resultsScreenPos[0] + 205,
                        self.resultsScreenPos[1] + 320))
                # Marcadores online
                scores = self.map.get_player().get_scoreboard_online()
                if len(scores) > 0:
                    if scores[0] == NO_ERROR:
                        self.screen.blit(self.resultsFontTitleSubtl2.render(
                            self.lang.get(32), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 453,
                             self.resultsScreenPos[1] + 118))
                        i = 0
                        for score in scores:
                            if i == 0:
                                pass
                            else:
                                try:
                                    if score[0] != STATE_NULL:
                                        self.screen.blit(
                                            self.resultsFontTitleContent.render(
                                                score[1], 1, score[0]), (
                                                self.resultsScreenPos[0] + 460,
                                                self.resultsScreenPos[
                                                    1] + 130 + 19 * i))
                                        self.screen.blit(
                                            self.resultsFontTitleContent.render(
                                                score[2], 1, score[0]), (
                                                self.resultsScreenPos[0] + 505,
                                                self.resultsScreenPos[
                                                    1] + 130 + 19 * i))
                                        self.screen.blit(
                                            self.resultsFontTitleContent.render(
                                                score[3], 1, score[0]), (
                                                self.resultsScreenPos[0] + 600,
                                                self.resultsScreenPos[
                                                    1] + 130 + 19 * i))
                                    else:
                                        self.screen.blit(
                                            self.resultsFontTitleContent.render(
                                                self.lang.get(33), 1,
                                                COLOR_VELOCIMETER),
                                            (self.resultsScreenPos[0] + 540,
                                             self.resultsScreenPos[
                                                 1] + 126 + 19 * i))
                                except:
                                    self.screen.blit(
                                        self.resultsFontTitleContent.render(
                                            self.lang.get(33), 1,
                                            COLOR_VELOCIMETER),
                                        (self.resultsScreenPos[0] + 540,
                                         self.resultsScreenPos[
                                             1] + 126 + 19 * i))
                            i += 1
                    # Se imprimen mensajes de error
                    elif scores[0] == ERROR_SCOREBOARD_NOCONECTION:
                        self.screen.blit(self.resultsFontTitleContent.render(
                            self.lang.get(35), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 451,
                             self.resultsScreenPos[1] + 120))
                    elif scores[0] == ERROR_SCOREBOARD_NOCONECTIONDB:
                        self.screen.blit(self.resultsFontTitleContent.render(
                            self.lang.get(36), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 478,
                             self.resultsScreenPos[1] + 120))
                    elif scores[0] == ERROR_SCOREBOARD_FAKEHASH:
                        self.screen.blit(self.resultsFontTitleContent.render(
                            self.lang.get(37), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 443,
                             self.resultsScreenPos[1] + 120))
                        self.screen.blit(self.resultsFontTitleContent.render(
                            self.lang.get(38), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 509,
                             self.resultsScreenPos[1] + 140))
                    elif scores[0] == ERROR_SCOREBOARD_NO_SCORES:
                        self.screen.blit(self.resultsFontTitleContent.render(
                            self.lang.get(34), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 481,
                             self.resultsScreenPos[1] + 120))
                    elif scores[0] == ERROR_SCOREBOARD_BADPARAMETERS:
                        self.screen.blit(self.resultsFontTitleContent.render(
                            self.lang.get(39), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 478,
                             self.resultsScreenPos[1] + 120))
                    elif scores[0] == ERROR_SCOREBOARD_FAKESCORE:
                        self.screen.blit(self.resultsFontTitleContent.render(
                            self.lang.get(40), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 480,
                             self.resultsScreenPos[1] + 120))
                    elif scores[0] == ERROR_SCOREBOARD_FAKETIME:
                        self.screen.blit(self.resultsFontTitleContent.render(
                            self.lang.get(41), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 453,
                             self.resultsScreenPos[1] + 120))
                    elif scores[0] == ERROR_SCOREBOARD_FAKETRACK:
                        self.screen.blit(self.resultsFontTitleContent.render(
                            self.lang.get(50), 1, COLOR_VELOCIMETER),
                            (self.resultsScreenPos[0] + 451,
                             self.resultsScreenPos[1] + 120))
                else:
                    self.screen.blit(
                        self.resultsFontTitleContent.render(self.lang.get(34), 1, COLOR_VELOCIMETER),
                        (self.resultsScreenPos[0] + 481, self.resultsScreenPos[1] + 120))
                # Se guardan los resultados y se consulta la siguiente pista
                if not self.map.results_saved() and SAVE_FILE_STATICS:
                    self.map.results = True
                    save = open(
                        DIR_SAVES + str(hash(self.map.get_track_title())) + str(
                            hash(self.map.get_player().username)) + str(
                            hash(self.map.get_player().get_type())) + ".txt", "w")
                    save.write(
                        "<player>" + self.map.get_player().username + "</player>")
                    if tiempo < oro:
                        save.write("<oro>1</oro>")
                    else:
                        save.write("<oro>0</oro>")
                    if tiempo < plata:
                        save.write("<plata>1</plata>")
                    else:
                        save.write("<plata>0</plata>")
                    if tiempo < bronce:
                        save.write("<bronce>1</bronce>")
                    else:
                        save.write("<bronce>0</bronce>")
                    save.write("<oro_t>" + str(tiempo - oro) + "</oro_t>")
                    save.write("<plata_t>" + str(tiempo - oro) + "</plata_t>")
                    save.write(
                        "<bronce_t>" + str(tiempo - oro) + "</bronce_t>")
                    save.close()
                    self.map.get_player().set_next_track(
                        TRACKS[get_next_track(self.world.get_actual_index())])
                # Se dibujan los botones debajo del recuadro
                if self.map.get_player().get_next_track() != TRACK_NOT_DEFINED:
                    quit_text = self.buttonsResultsFont.render(
                        self.lang.get(108), 1, COLOR_VELOCIMETER)
                    quit_text_width = quit_text.get_size()[0]
                    next_text = self.buttonsResultsFont.render(
                        self.lang.get(109,
                                      self.map.get_player().get_next_track()),
                        1, COLOR_VELOCIMETER)
                    next_text_width = next_text.get_size()[0]
                    pygame.gfxdraw.filled_polygon(self.screen, [
                        (self.resultsButtonQuitPos[0] - 15,
                         self.resultsButtonQuitPos[1] - 8),
                        (self.resultsButtonQuitPos[0] + quit_text_width + 15,
                         self.resultsButtonQuitPos[1] - 8),
                        (self.resultsButtonQuitPos[0] + quit_text_width + 15,
                         self.resultsButtonQuitPos[1] + 30),
                        (self.resultsButtonQuitPos[0] - 15,
                         self.resultsButtonQuitPos[1] + 30)],
                                                  (0, 0, 0, 230))
                    pygame.gfxdraw.filled_polygon(self.screen, [
                        (self.resultsButtonNextPos[0] - 15 - next_text_width,
                         self.resultsButtonNextPos[1] - 8),
                        (self.resultsButtonNextPos[0] + 14,
                         self.resultsButtonNextPos[1] - 8),
                        (self.resultsButtonNextPos[0] + 14,
                         self.resultsButtonNextPos[1] + 30),
                        (self.resultsButtonNextPos[0] - 15 - next_text_width,
                         self.resultsButtonNextPos[1] + 30)],
                                                  (0, 0, 0, 230))
                    self.screen.blit(quit_text, (self.resultsButtonQuitPos[0],
                                                 self.resultsButtonQuitPos[1]))
                    self.screen.blit(next_text,
                                     (self.resultsButtonNextPos[
                                          0] - next_text_width,
                                      self.resultsButtonNextPos[1]))

        # Si está en un menu
        elif state == STATE_MENU:
            if self.isPlaying and not self.map.get_player().finished_lap():
                self.menu.setActualMenu(MENU_PAUSE)
                self.menu.drawMenuPause()
            else:
                self.menu.setActualMenu(MENU_INICIAL)
                # Si se vuelve al menu principal se destruye
                if self.isPlaying and self.map.get_player().finished_lap():
                    self.world.clear_actual_map()
                    self.stop_playing_render()
                    self.controller.del_player()
                self.menu.drawMenuInicial(time)
        # Si el evento es avanzar de pista
        elif state == STATE_NEXT:
            self.world.clear_actual_map()
            self.world.load_map(NEXT_TRACK)
            self.controller.set_player()
            self.start_playing_render()
        # Se actualiza la pantalla
        pygame.display.flip()

    def set_map(self):
        """
        Define el mapa actual
        :return: void
        """
        self.map = self.world.get_actual_map()

    def start_playing_render(self):
        """
        Empieza el renderizado del mapa
        :return: void
        """
        self.isPlaying = True
        self.set_map()

    def stop_playing_render(self):
        """
        Detiene el renderizado del mapa
        :return: void
        """
        self.isPlaying = False
        self.map = None

    def update_show_ghost(self):
        """
        Comprueba si se cambio el parametro show_ghost
        :return: void
        """
        self.show_ghost = self.viewConfig.isTrue(
            "SHOWGHOST")  # define si se dibuja al ghost o no

    def update_show_fps(self):
        """
        Comprueba si se cambio el parametro show_fps
        :return: void
        """
        self.show_fps = self.viewConfig.isTrue(
            "SHOWFPS")  # define si se dibuja el fps en el titulo de la ventana
        if not self.show_fps:
            self.window.set_window_title(
                self.lang.get(10))  # se define el titulo por defecto

    def update_window_size(self):
        """
        Actualiza el tamaño de la ventana
        :return: void
        """
        self.windowHeight = self.window.get_window_height()  # alto de la ventana
        self.windowWidth = self.window.get_window_width()  # ancho de la ventana
