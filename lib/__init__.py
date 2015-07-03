#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Clases del juego
# Permite administrar las clases lógicas del juego
# Las librerías auxiliares o que no pertenecen a la lógica van en /bin

# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Configuración de entorno
from path import *
from bin import configLoader
import libdir

# noinspection PyProtectedMember
__binconfig = configLoader(libdir._LIB_CONFIG + "lib.ini")
