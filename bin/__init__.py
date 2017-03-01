#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Permite administrar las librerías del juego que son externas,
# contienen funciones auxiliares y/o son framework
# /bin no contiene las clases del juego, estas van en /lib
# /bin.
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías iniciales
from path import *
import os
import bindir
from configLoader import configLoader
import errors


# Configuración de entorno
# noinspection PyProtectedMember
__binconfig = configLoader(bindir._DIR_CONFIG + "bin.ini")
sys.setdefaultencoding(__binconfig.getValue("SET_DEFAULT_ENCODING"))
if __binconfig.isTrue("DONT_WRITE_BYTECODE"):
    reload(sys)
    sys.dont_write_bytecode = True

# Importación de librerías externas
try:
    import mechanize  # @UnresolvedImport @NoMove
except Exception, e:
    print str(e)
    errors.throw(errors.ERROR_IMPORTERRORMECHANIZE)
try:
    from pil import Image  # @UnresolvedImport
except Exception, e:
    errors.throw(errors.ERROR_IMPORTERRORPIL)

# Importación de librerías internas
try:
    from pygame import *
    import pygame
    import pygame.gfxdraw
except Exception, e:
    print str(e)
    errors.throw(errors.ERROR_IMPORTERRORPYGAME)
try:
    from hashdir import md5file, path_checksum
    from noStdOut import noStdOut
    import langs
    import utils
    import username
except Exception, e:
    print str(e)
    errors.throw(errors.ERROR_IMPORTERRORINTERNAL)

# Constantes de bin
WEB_VERSION = __binconfig.getValue("WEB_VERSIONFILE")

# Test
if __name__ == '__main__':
    print WEB_VERSION
    utils.clrscr()
    __binconfig.printParameters()
