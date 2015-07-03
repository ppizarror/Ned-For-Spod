#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Permite la importación multiple
# Agrega librerías al path
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importa las librerías de sistema
import sys
reload(sys)

# Importación de librerías internas
from libdir import DIR_LIB, DIR_BIN

# Se agregan directorios al path
sys.path.append(DIR_LIB)
sys.path.append(DIR_BIN)
sys.path.append(DIR_LIB.replace("\\lib", ""))