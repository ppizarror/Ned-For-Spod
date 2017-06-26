# coding=utf-8
"""
CONTROL
Maneja los eventos.

Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

from __future__ import print_function
if __name__ == '__main__':
    from path import *  # @UnusedWildImport

# Importación de librerías
# noinspection PyFromFutureImport
from bin import *  # @UnusedWildImport
from data import DIR_SAVES

# Definición de constantes
STATE_MENU = "MENU"  # indica que se encuentra en un menú
STATE_NEXT = "NEXT"  # indica que se avanza a la siguiente pista
STATE_PLAY = "PLAY"  # indica que se está jugando


# Funciones del programa
def pygame_to_pil_img(pg_surface):
    """
    Convierte una imagen de PIL a PYGAME
    :param pg_surface:
    :return:
    """
    imgstr = pygame.image.tostring(pg_surface, 'RGB')  # @UndefinedVariable
    # noinspection PyDeprecation,PyUnresolvedReferences
    return Image.fromstring('RGB', pg_surface.get_size(), imgstr)


# noinspection PyBroadException,PyUnresolvedReferences,PyShadowingNames
class Controller(object):
    """Clase que maneja eventos"""

    # noinspection PyShadowingNames
    def __init__(self, world, clock, langs, config, window, menu, **kwargs):
        """
        Función constructora
        :param world: Objeto mundo el cual posee todos los elementos lógicos del juego
        :param clock: Objeto del tipo pygame.Clock()
        :param langs: Diccionario de idioma
        :param config: Configuraciones del controlador
        :param window: Objeto ventana
        :param menu: Menúes del juego
        :param kwargs: Parámetros
        :return: void
        """

        # Se define si se imprime o no en consola
        if kwargs.get("verbose"):
            self.verbose = True
        else:
            self.verbose = False
        # Modelos del juego
        if world.get_actual_map() is not None:
            self.player = world.get_actual_map().get_player()
        else:
            self.player = None
        # Variables del controlador
        self.clock = clock  # reloj del juego
        self.configs = config  # configuraciones del controlador
        self.inmenu = True  # define si se tiene la ventana de menu abierta o no
        self.lang = langs  # idiomas
        self.menu = menu  # menú del juego
        self.window = window  # ventana
        self.world = world  # mundo del juego

    def del_player(self):
        """
        Elimina al jugador
        :return: void
        """
        self.player = None

    def disable_menu(self):
        """
        Desactiva el menú
        :return: void
        """
        self.inmenu = False

    def enable_menu(self):
        """
        Activa el menú
        :return: void
        """
        self.inmenu = True

    def event_loop(self):
        """
        Función que verifica los eventos de entrada
        :return: void
        """
        time = float(
            self.clock.get_time()) / 1000.0  # tiempo que tomo el frame en generarse
        # Se obtienen los eventos base
        for event in pygame.event.get():
            # Si se cierra la ventana (con evento QUIT o ALT-F4)
            try:
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_F4 and (key[K_LALT] or key[K_LALT])):
                    utils.destroyProcess()  # @UndefinedVariable
            except:
                utils.destroyProcess()
            # Si se presiona una tecla
            if event.type == KEYDOWN:
                # Se activa el menu de pausa
                if event.key == K_ESCAPE:
                    # Cerrar menu
                    if self.inmenu:
                        self.inmenu = False
                        if self.player is not None:
                            if not self.player.finished_lap():
                                self.player.sound_unpause()
                    # Abrir menu
                    else:
                        if self.player is not None:
                            if not self.player.finished_lap():
                                self.player.sound_pause()
                        self.inmenu = True
                # Si se esta jugando
                if self.player is not None and not self.inmenu:
                    if not self.player.finished_lap():
                        # Limpiar la vuelta
                        # elif event.key == K_F10:
                        #    self.player.clear()
                        # Captura de pantalla
                        if event.key == K_F3:
                            try:
                                fileimg = 'screenshot_' + str(abs(
                                    hash(utils.generateRandom6()))) + '.png'
                                surfimg = pygame_to_pil_img(
                                    pygame.display.get_surface())
                                surfimg.save(DIR_SAVES + fileimg)
                                if self.verbose:
                                    print(self.lang.get(58, fileimg))
                            except:
                                if self.verbose:
                                    print(self.lang.get(59))
                    else:
                        if event.key == K_RETURN:
                            return STATE_NEXT
                # Si no se esta jugando -> menu inicial
                else:
                    # Subir opción en menú
                    if event.key == K_UP:
                        self.menu.down()
                    # Bajar opción en menu
                    elif event.key == K_DOWN:
                        self.menu.up()
                    # Ingresar opción en menú
                    elif event.key == K_RETURN:
                        self.menu.select()
                    # Mover selector a la izquierda
                    elif event.key == K_LEFT:
                        self.menu.left()
                    # Mover selector a la derecha
                    elif event.key == K_RIGHT:
                        self.menu.right()
                    # Retroceder
                    elif event.key == K_BACKSPACE or event.key == K_ESCAPE:
                        self.menu.reset(1)
                        self.menu.setZeroIndex()
        # Se comprueban las teclas presionadas
        key_pressed = pygame.key.get_pressed()
        # Si existe un jugador
        if self.player is not None and not self.inmenu:
            # Si no ha terminado el circuito se puede conducir
            if not self.player.finished_lap():
                # Acelerar
                if key_pressed[K_UP] or key_pressed[K_w]:
                    self.player.acelerate(time)
                else:
                    self.player.stop_acelerating()
                # Frenar
                if key_pressed[K_DOWN] or key_pressed[K_s] or key_pressed[K_SPACE]:
                    self.player.desacelerate(self.player.get_desacel(), time,
                                             True)
                else:
                    self.player.stop_track_marking()
                # Doblar a la izquierda
                if key_pressed[K_LEFT] or key_pressed[K_a]:
                    self.player.rotate(1, time)
                # Doblar a la derecha
                if key_pressed[K_RIGHT] or key_pressed[K_d]:
                    self.player.rotate(-1, time)
                # Freno de mano
                # if key_pressed[K_SPACE]:
                #    self.player.handBrake(time)
                # else:
                #    self.player.stopTrackMarkingHB()
                # Devolver a la pista
                if key_pressed[K_BACKSPACE]:
                    self.player.return_to_track()
                    # Mover la camara para map-testing
                    #   if key_pressed[K_l]:
                    #       self.player.posx -= 30
                    #   if key_pressed[K_j]:
                    #       self.player.posx += 30
                    #   if key_pressed[K_i]:
                    #       self.player.posy += 30
                    #   if key_pressed[K_k]:
                    #       self.player.posy -= 30
        # Si no existe un jugador se fuerza el menu
        else:
            self.enable_menu()
            return STATE_MENU
        # Se retorna el estado del controlador
        if self.inmenu:
            return STATE_MENU
        else:
            return STATE_PLAY

    def set_player(self):
        """
        Define el jugador
        :return: void
        """
        self.player = self.world.get_actual_map().get_player()
