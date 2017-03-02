#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# En la carpeta config iran las configuraciones del juego, eso es
# configuraciones de la ventana, titulos, argumentos, etc
# Al importar config se adquieren las direcciones de
# todos los directorios dentro de config/

# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
import os
import sys

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

# Definición de directorios
__actualpath = application_path.replace("\\", "/") + "/"
DIR_CONFIG = __actualpath
# DIR_CONFIG = __actualpath + 'config/'  # compilacion

# Test
if __name__ == '__main__':
    print DIR_CONFIG
