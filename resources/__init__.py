#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Directorio resources, dentro del directorio irán todos los recursos
# audiovisuales del juego, además de los recursos escritos, como documentacion
# etc.
# Al importar resources se adquieren las direcciones de
# todos los directorios dentro de resources/

# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
import os


__actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace("\\", "/") + "/"

# Definición de directorios
# \
DIR_DOC = __actualpath + "doc/"
DIR_FONTS = __actualpath + "fonts/"
DIR_ICONS = __actualpath + "icons/"
DIR_IMAGES = __actualpath + "images/"
DIR_LANGS = __actualpath + "langs/"
DIR_RESOURCES = __actualpath
DIR_SOUNDS = __actualpath + "sounds/"

# \..\
DIR_CHANGELOG = DIR_DOC + "changelog/"
DIR_DEV = DIR_DOC + "dev/"
DIR_DOCUMENTATION = DIR_DOC + "documentation"
DIR_HELP = DIR_DOC + "help"
DIR_LICENCE = DIR_DOC + "licence"

# Test
if __name__ == '__main__':
    print DIR_CHANGELOG
    print DIR_DEV
    print DIR_DOC
    print DIR_DOCUMENTATION
    print DIR_FONTS
    print DIR_HELP
    print DIR_ICONS
    print DIR_IMAGES
    print DIR_RESOURCES
    print DIR_SOUNDS
