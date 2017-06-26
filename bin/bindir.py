# coding=utf-8
"""
BINDIR
Adminsitra la direccion de directorios de la aplicación
Solamente deben incluirse directorios que sean usados por ficheros en BIN.

Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

# Importación de librerías
from __future__ import print_function
import os

# Definición de directorios
__actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace('\\',
                                                                       '/') + '/'
DIR = __actualpath.replace('/bin', '')
_DIR_BIN = __actualpath
_DIR_LIB = __actualpath.replace('/bin', '/lib')

# Directorios ocultos
_DIR_CONFIG = __actualpath + '.config/'
_LANG_DIRCONFIG = __actualpath + 'internal/langeditor/config/'
_LANG_DIRLANGS = __actualpath.replace('/bin/', '/resources/langs/')

# Test
if __name__ == '__main__':
    print(_DIR_BIN)
    print(_DIR_LIB)
    print(_LANG_DIRCONFIG)
    print(_LANG_DIRLANGS)
    print(DIR)
