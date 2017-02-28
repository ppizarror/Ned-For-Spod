# coding=utf-8
"""
Adminsitra la direccion de directorios de la aplicación
Se pueden incluir todos los directorios salvo bin/

Game template
Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

# Importación de librerías
import os

# Definición de directorios
__actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace("\\", "/") + "/"
DIR = __actualpath.replace("/lib/", "/")
DIR_BIN = __actualpath.replace("/lib/", "/bin/")
DIR_LIB = __actualpath

# Directorios ocultos
_LIB_CONFIG = __actualpath + ".config/"

# Test
if __name__ == '__main__':
    print DIR_BIN
    print DIR_LIB
    print DIR
