# coding=utf-8
"""
PATH
Permite la importación múltiple.
Agrega librerías al path.

Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

# Importa las librerías de sistema
import sys
# noinspection PyProtectedMember,PyUnresolvedReferences
from bindir import _DIR_BIN, _DIR_LIB  # @UnusedImport

# noinspection PyProtectedMember
# Se agregan los directorios al path del sistema
# noinspection PyCompatibility
reload(sys)
sys.path.append(_DIR_BIN)
sys.path.append(_DIR_BIN + "/external/")
sys.path.append(_DIR_BIN + "/external/mechanize/")
sys.path.append(_DIR_BIN + "/external/pil/")
sys.path.append(_DIR_BIN + "/external/pyperclip/")
sys.path.append(_DIR_BIN + "/external/wconio/")
sys.path.append(_DIR_BIN + "/internal/")
