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
# noinspection PyProtectedMember
from bindir import _DIR_BIN, _DIR_LIB

# Se agregan los directorios al path del sistema
reload(sys)
sys.path.append(_DIR_BIN)
sys.path.append(_DIR_BIN + "/external/")
sys.path.append(_DIR_BIN + "/external/mechanize/")
sys.path.append(_DIR_BIN + "/external/pil/")
sys.path.append(_DIR_BIN + "/external/pyperclip/")
sys.path.append(_DIR_BIN + "/external/wconio/")
sys.path.append(_DIR_BIN + "/internal/")
