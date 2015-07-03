#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Maneja los idiomas, permitiendo la carga y manejo de ellos

# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías y obtención de directorios
from configLoader import configLoader
# noinspection PyProtectedMember
from bindir import _LANG_DIRCONFIG, _LANG_DIRLANGS, _DIR_CONFIG
from utils import googleTranslate
import errors
import math

# Se cargan las configuraciones
langselfconfig = configLoader(_DIR_CONFIG + "langs.ini")
langconfig = configLoader(_LANG_DIRCONFIG + "const.ini")
langavaiable = configLoader(_LANG_DIRCONFIG + "langs.txt")
langtranslateconfig = configLoader(_DIR_CONFIG + "langstransl.ini")

# Constantes del programa
_SPACE = "|"
_SPLITTER = langconfig.getValue(1).replace("*", " ")
LANG_LOADED = "El archivo de idiomas '{0}' ha sido cargado correctamente"
LANG_PRINT_ELEMENT = "\t{0}{1}=> {2}"
LANG_PRINT_TITLE = "Entradas:\n\tID     STRING"
NULL_IDENTIFIER = "NULL_LANG_ID<"
NULL_LANG = NULL_IDENTIFIER + "{0}>"

# Definicion de funciones
def _totalspaces(index):
    return int(round(math.log(index, 10), 2) + 1) * " "

# Carga un archivo de idioma y maneja sus elementos, adicionalmente traduce lineas
class langLoader:

    def __init__(self, language, **kwargs):
        language = str(language).upper()
        if language + langconfig.getValue(0) in langavaiable.getParameters():
            try:
                file = open(_LANG_DIRLANGS + language + langconfig.getValue(0), "r")
            except:
                errors.throw(errors.ERROR_NOLANGFILE, language)
            self.lang = {}
            # noinspection PyUnboundLocalVariable
            for line in file:
                line = line.strip().replace("\ufeff", "").split(_SPLITTER)
                if "\xef\xbb\xbf" in line[0]:  # elimino caracteres que no sean utf-8
                    line[0] = line[0][3:]
                if line[0] == "":
                    line[0] = "10"
                self.lang[int(line[0].replace("\ufeff", ""))] = line[1].replace(_SPACE, " ")
            file.close()
            if kwargs.get("verbose"):
                print LANG_LOADED.format(language)
            self.langname = language
        else:
            errors.throw(errors.ERROR_NOLANGDEFINED)

    # Retorna un string asociado al indice -index- en el archivo de idiomas cargado
    def get(self, index, *args, **kwargs):
        if str(index).isdigit():
            try:  # Si existe el lang en la matriz de datos
                if kwargs.get("noformat") or len(args) == 0:
                    return self.lang[index]
                else:
                    return self.lang[index].format(*args)
            except:
                errors.warning(errors.ERROR_LANGNOTEXIST, str(index), self.langname)
                return NULL_LANG.format(str(index))
        else:
            errors.warning(errors.ERROR_LANGBADINDEX, str(index))
            return NULL_LANG.format(str(index))

    # Imprime todos los elementos del idioma
    def printAll(self):
        print LANG_PRINT_TITLE
        for key in self.lang.keys():
            print LANG_PRINT_ELEMENT.format(str(key), _totalspaces(key), self.lang[key])

    # Función que traduce un texto usando el servicio de google traductor
    def translate(self, index, to):
        text = self.get(index)
        if langselfconfig.isTrue("TRANSLATIONS"):  # Si el servicio de traducciones esta activado
            if not NULL_IDENTIFIER in text:
                try:  # Se consulta por la traducción al servicio de google
                    return googleTranslate(text, to, langtranslateconfig.getValue("WEB_HEADER"), langtranslateconfig.getValue("WEB_GOOGLETRANSLATE"))
                except:  # Si ocurre algún error en la traducción
                    return text
            else:
                errors.warning(errors.ERROR_CANTTRANSLATE)
                return text
        else:
            return text

# Test
if __name__ == '__main__':
    print _LANG_DIRCONFIG
    print _LANG_DIRLANGS
    lang = langLoader("TEST", verbose=True)
    langconfig.printParameters()
    print langconfig.getParameters()
    langavaiable.printParameters()
    langtranslateconfig.printParameters()
    print langselfconfig.getParameters()
    print langselfconfig.isTrue("TRANSLATIONS")
    print lang.get(10)
    print lang.get(12)
    print lang.get("a")
    # print lang.translate(11, "eng")
    lang.printAll()
    print lang.get(14, 1, 2, 3)
    print lang.get(14, 1, 2, 3, noformat=True)
    print lang.get(12, "pablo")
    print lang.get(13, "pablo", "pizarro")
