# coding=utf-8
"""
BIN
Permite administrar las librerías del juego que son externas,
contienen funciones auxiliares y/o son framework
/bin no contiene las clases del juego, estas van en /lib
/bin.

Game template
Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

# Importación de librerías iniciales
from __future__ import print_function
from path import *
# noinspection PyUnresolvedReferences
import os
import bindir
from configloader import Configloader
import errors


# Configuración de entorno
# noinspection PyProtectedMember
__binconfig = Configloader(bindir._DIR_CONFIG + "bin.ini")
# noinspection PyUnresolvedReferences
sys.setdefaultencoding(__binconfig.getValue("SET_DEFAULT_ENCODING"))
if __binconfig.isTrue("DONT_WRITE_BYTECODE"):
    # noinspection PyCompatibility
    reload(sys)
    sys.dont_write_bytecode = True

# Importación de librerías externas
# noinspection PyCompatibility
try:
    # noinspection PyUnresolvedReferences
    import mechanize  # @UnresolvedImport @NoMove
except Exception, e:
    print(str(e))
    errors.throw(errors.ERROR_IMPORTERRORMECHANIZE)
# noinspection PyCompatibility,PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from pil import Image  # @UnresolvedImport
except Exception, e:
    errors.throw(errors.ERROR_IMPORTERRORPIL)

# Importación de librerías internas
# noinspection PyCompatibility
try:
    from pygame import *
    import pygame
    import pygame.gfxdraw
except Exception, e:
    print(str(e))
    errors.throw(errors.ERROR_IMPORTERRORPYGAME)
# noinspection PyCompatibility
try:
    from hashdir import md5file, path_checksum
    from noStdOut import noStdOut
    import langs
    import utils
    import username
except Exception, e:
    print(str(e))
    errors.throw(errors.ERROR_IMPORTERRORINTERNAL)

# Constantes de bin
WEB_VERSION = __binconfig.getValue("WEB_VERSIONFILE")

# Test
if __name__ == '__main__':
    print(WEB_VERSION)
    utils.clrscr()
    __binconfig.printParameters()
