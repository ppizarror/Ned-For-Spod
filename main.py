# coding=utf-8
"""
MAIN
Archivo principal del juego.
Carga todas las configuraciones.
Obtiene el checksum del proyecto.

Autor: PABLO PIZARRO @ ppizarro
Fecha: ABRIL 2015 - FEBRERO 2019
"""

# Importación de librerías
from bin import *
from bin import Configloader, langs
from config import DIR_CONFIG
from lib.controller import Controller
from lib.uimenu import Createuimenu
from lib.view import View
from lib.window import Window
from lib.world import World
from resources.icons import getIcons

# Iniciación de librerías
pygame.init()

# Definición de constantes
VERBOSE = False  # Imprime el estado del juego en consola


def main():
    """
    Prepara las ventanas, define modelos, controlador y vista y corre el programa.
    :return: void
    """

    # Se obtiene el checksum del juego
    checksum = [path_checksum('lib', VERBOSE),
                '8e1fd1c03d2bfe89d7dbdab8b0c4c69a'.upper(),
                path_checksum('bin', VERBOSE)]

    # Se cargan las configuraciones
    control_config = Configloader(DIR_CONFIG + 'control.ini', verbose=VERBOSE)
    game_config = Configloader(DIR_CONFIG + 'game.ini', verbose=VERBOSE)
    map_config = Configloader(DIR_CONFIG + 'map.ini', verbose=VERBOSE)
    score_config = Configloader(DIR_CONFIG + 'scoreboard.ini', verbose=VERBOSE)
    user_config = Configloader(DIR_CONFIG + 'user.ini', verbose=VERBOSE)
    view_config = Configloader(DIR_CONFIG + 'view.ini', verbose=VERBOSE)
    window_config = Configloader(DIR_CONFIG + 'window.ini', verbose=VERBOSE)
    world_config = Configloader(DIR_CONFIG + 'world.ini', verbose=VERBOSE)

    # Se carga el idioma
    lang = langs.Langloader(game_config.getValue('LANG'))

    # Se carga la información de la pantalla del cliente
    display_info = pygame.display.Info()

    # Se comprueba que el nombre de jugador no sea Player, si no es valido se pide uno nuevo
    if not username.validate(
            user_config.getValue('NAME')):
        new_name = username.request(lang.get(111), lang.get(112))
        if new_name is not username.NO_VALID_NAME:
            user_config.setParameter('NAME', new_name)
            user_config.export()
        else:
            utils.destroy_process()

    # Creación de ventana
    window = Window(window_config, lang.get(10), pygame.image.load(getIcons('icon')), display_info)
    clock = pygame.time.Clock()  # Reloj
    fps = int(game_config.getValue('FPS'))  # FPS a dibujar

    # Se crea el mundo
    world = World(world_config, map_config, window, checksum, score_config,
                  user_config, lang, game_config, verbose=VERBOSE)
    # world.load_map(1)

    # Se crean los menús de inicio y pause
    menus = Createuimenu(lang, window, world, game_config, user_config,
                         view_config, window_config, world_config, map_config)

    # Se crea la vista
    vista = View(window, clock, world, lang, view_config, menus)
    menus.addView(vista)

    # Se crea el controlador
    control = Controller(world, clock, lang, control_config, window, menus, verbose=VERBOSE)
    menus.addController(control)
    vista.add_controller(control)

    # Se lanza el mainloop
    while True:
        clock.tick(fps)
        vista.draw(control.event_loop())


# Si se ejecuta el programa
if __name__ == '__main__':
    main()
