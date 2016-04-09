#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Directorio langs
# Fichero generado automáticamente usando __scan__.py
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Archivos totales: 3
# Generado el: 10/5/2015

# Importación de liberías
import os


# Definición de variables
__actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace("\\","/") + "/"

# Librería de /langs
LANGS = {

	#Resources/Langs
	"EN": __actualpath + "EN.lng", \
	"ES": __actualpath + "ES.lng", \
	"TEST": __actualpath + "TEST.lng"
}

# Función que retorna el elemento <index> de la librería LANGS
def getLangs(index):
    try:
        return LANGS[index]
    except:
        return -1

# Función que retorna los archivos en LANGS
def getLangsKeys():
    return LANGS.keys()

# Función que imprime los archivos en LANGS
def printLangsValues():
    print "<KEY> LANGS[<KEY>]"
    for file in LANGS.keys():
        print file +" "+str(LANGS[file])
    
