#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Almacena todos los errores propios de bin, provee adem�s una función para retornar un
# mensaje de error dado parámetros

# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
import sys
from colors import Color


# Constantes de errores
BR_ERRORxERROR_SET_FORM = 8
BR_ERRORxERROR_SET_SUBMIT = 9
BR_ERRORxNO_ACCESS_WEB = 1
BR_ERRORxNO_FORM = 3
BR_ERRORxNO_FORMID = 2
BR_ERRORxNO_OPENED = 0
BR_ERRORxNO_SELECTED_FORM = 5
BR_ERRORxNO_VALIDID = 4
BR_ERRORxNO_VALID_SUBMIT_EMPTY = 6
BR_ERRORxNO_VALID_SUBMIT_NOT_EQUAL = 7
ERROR_BADCONFIG = "La linea '{0}' del archivo de configuraciones '{1}' no es valida"
ERROR_BADINDEXCONFIG = "El indice seleccionado <{0}> no pertenece a las configuraciones cargadas"
ERROR_BADLAUNCHBIN = "La clase debe ser importada desde bin"
ERROR_CANTTRANSLATE = "El texto no se puede traducir"
ERROR_CONFIGBADEXPORT = "No se pudo guardar el archivo de configuraciones"
ERROR_CONFIGNOTEXISTENT = "El parametro <{0}> no existe en las configuraciones"
ERROR_CREATE_MENU = "No se puede crear el menu inicial, posible error en archivo de configuraciones"
ERROR_HEADER = Color.RED + "[ERROR] " + Color.END
ERROR_IMPORTERROREXTERNAL = "Ha ocurrido un error al importar las librerias de sistema externas"
ERROR_IMPORTERRORINTERNAL = "Ha ocurrido un error al importar las librerias internas de la aplicacion"
ERROR_IMPORTERRORMECHANIZE = "Ha ocurrido un error al importar la libreria external/mechanize"
ERROR_IMPORTERRORPIL = "Ha ocurrido un error al importar la libreria PIL (Python Image Library) en external/pil"
ERROR_IMPORTERRORPYGAME = "Ha ocurrido un error al importar la libreria pygame"
ERROR_IMPORTSYSTEMERROR = "Ha ocurrido un error al importar las librerias de sistema"
ERROR_IMPORTWCONIO = "Error al importar WConio"
ERROR_LANGBADINDEX = "El indice <{0}> debe ser un numero entero mayor o igual a 10"
ERROR_LANGNOTEXIST = "ID[{0}] no existe en el archivo de idiomas <{1}>"
ERROR_NOCONFIGFILE = "No existe archivo de configuraciones '{0}'"
ERROR_NOLANGDEFINED = "El idioma no existe y/o no ha sido definido"
ERROR_NOLANGFILE = "No existe el archivo de idiomas '{0}'"
ERROR_NOTRANSLATECONECTION = "No se pudo establecer comunicacion con el servidor de traducciones"
ERROR_SCOREBOARD_BADPARAMETERS = "ERROR_BADPARAMETERS"
ERROR_SCOREBOARD_FAKEHASH = "ERROR_FAKEHASH"
ERROR_SCOREBOARD_FAKESCORE = "ERROR_FAKESCORE"
ERROR_SCOREBOARD_FAKETIME = "ERROR_FAKETIME"
ERROR_SCOREBOARD_FAKETRACK = "ERROR_FAKETRACK"
ERROR_SCOREBOARD_NOCONECTION = "ERROR_NO_CONECTION"
ERROR_SCOREBOARD_NOCONECTIONMSG = "Error al conectar con el servidor"
ERROR_SCOREBOARD_NOCONECTIONDB = "ERROR_NOCONECTION_DB"
ERROR_SCOREBOARD_NO_SCORES = "NO_SCORES"
ERROR_TAG_CANTRETRIEVEHTML = 16
ERROR_TAG_INITNOTCORRECTENDING = 14
ERROR_TAG_INITNOTFINDED = 13
ERROR_TAG_LASTNOTFINDED = 15
ERROR_TRACKNOTEXIST = "La pista ID:<{0}> no existe"
NO_ERROR = "OK"
WARNING_HEADER = Color.BLUE + "[WARNING] " + Color.END
WARNING_NOCONFIGFOUND = "No se han encontrado configuraciones en el archivo '{0}'"


def createMSG(message, *args):
    """
    Función que crea un mensaje de error dado argumentos iniciales
    :param message: Código de error
    :param args: Mensaje
    :return: void
    """
    return message.format(*args)


def throw(error, *args):
    """
    Función que termina el programa mostrando un mensaje de error
    :param error: Código de error
    :param args: Mensaje
    :return: void
    """
    print(ERROR_HEADER + createMSG(error, *args))
    try:
        exit()
    except:
        sys.exit()


def warning(error, *args):
    """
    Función que imprime en pantalla un mensaje de error
    :param error: Código de error
    :param args: Mensaje
    :return: void
    """
    print (WARNING_HEADER
           + createMSG(error, *args))
