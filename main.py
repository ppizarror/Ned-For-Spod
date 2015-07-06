#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Archivo principal del juego.
# Carga todas las configuraciones.
# Obtiene el checksum del proyecto.

# Ned for Spod
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
from bin import *
from config import DIR_CONFIG
from lib.controller import Controller
from lib.uimenu import createUImenu
from lib.view import View
from lib.window import Window
from lib.world import World
from resources.icons import getIcons

# Iniciación de librerías
pygame.init()

# Definición de constantes
VERBOSE = False  # imprime el estado del juego en consola


def main():
    """
    Prepara las ventanas, define modelos, controlador y vista y corre el programa
    :return: void
    """

    # Se obtiene el checksum del juego
    checksum = [path_checksum('lib', VERBOSE), md5file('main.py', VERBOSE).upper(), path_checksum('bin', VERBOSE)]

    # Se cargan las configuraciones
    controlConfig = configLoader(DIR_CONFIG + "control.ini", verbose=VERBOSE)
    gameConfig = configLoader(DIR_CONFIG + "game.ini", verbose=VERBOSE)
    mapConfig = configLoader(DIR_CONFIG + "map.ini", verbose=VERBOSE)
    scoreConfig = configLoader(DIR_CONFIG + "scoreboard.ini", verbose=VERBOSE)
    userConfig = configLoader(DIR_CONFIG + "user.ini", verbose=VERBOSE)
    viewConfig = configLoader(DIR_CONFIG + "view.ini", verbose=VERBOSE)
    windowConfig = configLoader(DIR_CONFIG + "window.ini", verbose=VERBOSE)
    worldConfig = configLoader(DIR_CONFIG + "world.ini", verbose=VERBOSE)

    # Se carga el idioma
    lang = langs.langLoader(gameConfig.getValue("LANG"))

    # Se carga la información de la pantalla del cliente
    display_info = pygame.display.Info()

    # Se comprueba que el nombre de jugador no sea Player, si no es valido se pide uno nuevo
    if not username.validate(userConfig.getValue("NAME")):
        new_name = username.request(lang.get(111), lang.get(112))
        if new_name is not username.NO_VALID_NAME:
            userConfig.setParameter("NAME", new_name);
            userConfig.export()
        else:
            utils.destroyProcess()

    # Creación de ventana
    window = Window(windowConfig, lang.get(10), pygame.image.load(getIcons("icon")), display_info)  # ventana
    clock = pygame.time.Clock()  # reloj
    fps = int(gameConfig.getValue("FPS"))  # fps a dibujar

    # Se crea el mundo
    world = World(worldConfig, mapConfig, window, checksum, scoreConfig, userConfig, lang, gameConfig, verbose=VERBOSE)
    # TEST: world.loadMap(1)

    # Se crean los menús de inicio y pause
    menus = createUImenu(lang, window, world, gameConfig, userConfig, viewConfig, windowConfig, worldConfig, mapConfig)

    # Se crea la vista
    vista = View(window, clock, world, lang, viewConfig, menus)
    menus.addView(vista)

    # Se crea el controlador
    control = Controller(world, clock, lang, controlConfig, window, menus, verbose=VERBOSE)
    menus.addController(control)
    vista.addController(control)

    # Se lanza el mainloop
    while True:
        clock.tick(fps)
        vista.draw(control.event_loop())

# Si se ejecuta el programa
if __name__ == '__main__':
    main()
