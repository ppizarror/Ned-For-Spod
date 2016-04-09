#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Directorio sounds
# Fichero generado automáticamente usando __scan__.py
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Archivos totales: 21
# Generado el: 10/5/2015

# Importación de liberías
import os


# Definición de variables
__actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace("\\","/") + "/"

# Librería de /sounds
SOUNDS = {

	#Engine
	"m1": __actualpath + "engine/m1.wav", \
	"m2": __actualpath + "engine/m2.wav", \
	"m3": __actualpath + "engine/m3.wav", \
	"m4": __actualpath + "engine/m4.wav", \
	"m5": __actualpath + "engine/m5.wav", \
	"n": __actualpath + "engine/n.wav", \
	"r1": __actualpath + "engine/r1.wav", \
	"r2": __actualpath + "engine/r2.wav", \
	"r3": __actualpath + "engine/r3.wav", \
	"r4": __actualpath + "engine/r4.wav", \
	"r5": __actualpath + "engine/r5.wav", \

	#Soundtracks
	"intro": __actualpath + "soundtracks/intro.wav", \
	"results": __actualpath + "soundtracks/results.wav", \

	#Track
	"hardbrake": __actualpath + "track/hardbrake.wav", \
	"offroad": __actualpath + "track/offroad.wav", \
	"track1": __actualpath + "track/track1.wav", \
	"track2": __actualpath + "track/track2.wav", \
	"track3": __actualpath + "track/track3.wav", \
	"wheelborder": __actualpath + "track/wheelborder.wav", \

	#Ui
	"down": __actualpath + "ui/down.wav", \
	"up": __actualpath + "ui/up.wav"
}

# Función que retorna el elemento <index> de la librería SOUNDS
def getSounds(index):
    try:
        return SOUNDS[index]
    except:
        return -1

# Función que retorna los archivos en SOUNDS
def getSoundsKeys():
    return SOUNDS.keys()

# Función que imprime los archivos en SOUNDS
def printSoundsValues():
    print "<KEY> SOUNDS[<KEY>]"
    for file in SOUNDS.keys():
        print file +" "+str(SOUNDS[file])
    
