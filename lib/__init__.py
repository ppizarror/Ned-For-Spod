# coding=utf-8
"""
LIB
Permite administrar las clases lógicas del juego
Las librerías auxiliares o que no pertenecen a la lógica van en /bin.

Autor: PABLO PIZARRO @ppizarror
Fecha: ABRIL 2015
"""

# Configuración de entorno
from bin import Configloader
import libdir
# noinspection PyUnresolvedReferences
from path import *

# noinspection PyProtectedMember
__binconfig = Configloader(libdir._LIB_CONFIG + "lib.ini")
