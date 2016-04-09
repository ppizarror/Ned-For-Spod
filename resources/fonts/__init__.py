#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Directorio fonts
# Fichero generado automáticamente usando __scan__.py
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Archivos totales: 4
# Generado el: 10/5/2015

# Importación de liberías
import os


# Definición de variables
__actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace("\\","/") + "/"

# Librería de /fonts
FONTS = {

	#Resources/Fonts
	"lap": __actualpath + "lap.ttf", \
	"menu": __actualpath + "menu.ttf", \
	"nfs": __actualpath + "nfs.ttf", \
	"speed": __actualpath + "speed.ttf"
}

# Función que retorna el elemento <index> de la librería FONTS
def getFonts(index):
    try:
        return FONTS[index]
    except:
        return -1

# Función que retorna los archivos en FONTS
def getFontsKeys():
    return FONTS.keys()

# Función que imprime los archivos en FONTS
def printFontsValues():
    print "<KEY> FONTS[<KEY>]"
    for file in FONTS.keys():
        print file +" "+str(FONTS[file])
    
