#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# En data se almacena lo relacionado a la estructura lógica del
# juego, eso es estadisticas, partidas guardadas, cache, eventos, etc
# Al importar data se adquieren las direcciones de
# todos los directorios dentro de data/

# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
import os


__actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace("\\","/") + "/"

# Definición de directorios
DIR_CACHE = __actualpath + "cache/"
DIR_DATA = __actualpath
DIR_LOG = __actualpath + "log/"
DIR_SAVES = __actualpath + "saves/"
DIR_STATICS = __actualpath + "statics/"

# Test
if __name__ == '__main__':
    print DIR_CACHE
    print DIR_LOG
    print DIR_SAVES
    print DIR_STATICS
    print DIR_DATA