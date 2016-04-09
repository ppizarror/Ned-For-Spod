#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Directorio icons
# Fichero generado automáticamente usando __scan__.py
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Archivos totales: 2
# Generado el: 10/5/2015

# Importación de liberías
import os


# Definición de variables
__actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace("\\","/") + "/"

# Librería de /icons
ICONS = {

	#Resources/Icons
	"icon": __actualpath + "icon.png", \
	"launcher": __actualpath + "launcher.ico"
}

# Función que retorna el elemento <index> de la librería ICONS
def getIcons(index):
    try:
        return ICONS[index]
    except:
        return -1

# Función que retorna los archivos en ICONS
def getIconsKeys():
    return ICONS.keys()

# Función que imprime los archivos en ICONS
def printIconsValues():
    print "<KEY> ICONS[<KEY>]"
    for file in ICONS.keys():
        print file +" "+str(ICONS[file])
    
