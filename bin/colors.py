# coding=utf-8
"""
COLORS
Maneja los colores en la consola.

Autor: PABLO PIZARRO @ppizarror
Fecha: JULIO 2015
"""

# Importación de librerías
import os


# noinspection PyClassHasNoInit
class Color:
    """Permite manejar colores en la terminal"""

    if os.name != "nt":
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'
    else:
        PURPLE = ''
        CYAN = ''
        DARKCYAN = ''
        BLUE = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        BOLD = ''
        UNDERLINE = ''
        END = ''
