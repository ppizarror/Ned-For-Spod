# coding=utf-8
"""
CONFIGLOADER
Permite cargar configuraciones dado un archivo dado por parámetro
Formato de archivo:

    #comentario
    CONFIG_1 = VALUE
    CONFIG_2 = VALUE2

Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

# Importación de librerías
from __future__ import print_function
# noinspection PyUnresolvedReferences
import operator  # @UnusedImport
import errors
from utils import string2list

# Definición de constantes
CONFIG_COMMENT = "#"
CONFIG_LOAD = "El archivo de configuraciones '{0}' ha sido cargado correctamente"
CONFIG_PRINTNOCONFIG = "No se encontraron configuraciones"
CONFIG_PRINTPARAM = "\t${0} : {1}"
CONFIG_PRINTPARAMETER = "Parametros cargados:"
CONFIG_PRINTPARAMSIMPLE = "\t{0}"
CONFIG_SAVED = "El archivo de configuraciones '{0}' ha sido guardado exitosamente"
CONFIG_SEPARATOR = " = "
FALSE = "FALSE"
TRUE = "TRUE"


# noinspection PyBroadException,PyShadowingBuiltins,PyPep8Naming
class Configloader(object):
    """Carga configuraciones y retorna sus elementos"""

    def __init__(self, filename, **kwargs):
        """
        Función constructora
        :param filename: Nombre del archivo
        :param kwargs: Parámetros adicionales
        :return: void
        """
        # Se carga el archivo de configuraciones
        try:
            file = open(filename.replace('\\', '/'))  # @ReservedAssignment
        except:
            errors.throw(errors.ERROR_NOCONFIGFILE, filename)
        # Variables
        self.config_single = []
        self.configs = {}
        self.filename = filename
        self.totalconfigs = 0
        # Se cargan las configuraciones
        # noinspection PyUnboundLocalVariable
        for configline in file:
            if configline[0] != CONFIG_COMMENT and configline != "\n":
                config = string2list(configline, CONFIG_SEPARATOR)
                if len(config) == 1:
                    self.config_single.append(config[0])
                elif len(config) == 2:
                    self.totalconfigs += 1
                    self.configs[config[0]] = config[1]
                else:
                    errors.throw(errors.ERROR_BADCONFIG, configline, filename)
        if kwargs.get("verbose"):
            self.verbose = True
            if not (self.totalconfigs + len(self.config_single)):
                errors.warning(errors.WARNING_NOCONFIGFOUND, filename)
            else:
                print(CONFIG_LOAD.format(filename))
        else:
            self.verbose = False
        file.close()

    def export(self, replace=True, name=None):
        """
        Función que exporta las configuraciones a un directorio
        :param replace: Reemplaza el archivo anterior
        :param name: Nombre del archivo nuevo
        :return: void
        """
        try:
            if replace:
                name = self.filename
            f = open(name, "w")
            # Se escriben las configuraciones unarias
            for conf in self.config_single:
                f.write(str(conf) + "\n")
            # Se escriben las configuraciones complejas
            for key in self.configs.keys():
                f.write(str(key) + CONFIG_SEPARATOR + self.configs[key] + "\n")
            # Se cierra el archivo
            f.close()
            if self.verbose:
                print(CONFIG_SAVED.format(name))
        except:
            if self.verbose:
                errors.throw(errors.ERROR_CONFIGBADEXPORT)

    def isTrue(self, param):
        """
        Función que retorna true si el parámetro del archivo es verdadero
        :param param: Parámetro a buscar
        :return: booleano
        """
        if param in self.getParameters():
            if self.configs[param] == TRUE:
                return True
            else:
                return False
        else:
            errors.warning(errors.ERROR_CONFIGNOTEXISTENT, param)

    def getParameters(self):
        """
        Retorna una lista con todos los parametros cargados
        :return: Lista de parámetros
        """
        allconfigs = []
        for i in self.config_single:
            allconfigs.append(i)
        for j in self.configs.keys():
            allconfigs.append(j)
        return allconfigs

    def getValue(self, param):
        """
        Retorna el valor del parametro param
        :param param: Parámetro
        :return: valor
        """
        if str(param).isdigit():
            param = int(param)
            if 0 <= param < len(self.config_single):
                return self.config_single[param]
            else:
                errors.throw(errors.ERROR_BADINDEXCONFIG, str(param))
        else:
            if param in self.getParameters():
                return self.configs[param]
            else:
                errors.warning(errors.ERROR_CONFIGNOTEXISTENT, param)

    def printParameters(self):
        """
        Imprime una lista con todos los parametros cargados
        :return: void
        """
        if self.totalconfigs + len(self.config_single) > 0:
            print(CONFIG_PRINTPARAMETER)
            if self.totalconfigs > 0:
                for parameter in self.getParameters():
                    print(CONFIG_PRINTPARAM.format(parameter,
                                                   self.configs[parameter]))
            for config in self.config_single:
                print(CONFIG_PRINTPARAMSIMPLE.format(config))
        else:
            print(CONFIG_PRINTNOCONFIG)
        return

    def setParameter(self, paramName, paramValue):
        """
        Define un parametro
        :param paramName: Nombre del parámetro
        :param paramValue: Valor del parámetro
        :return: void
        """
        self.configs[paramName] = paramValue


# Test
if __name__ == '__main__':
    binconfig = Configloader(".config/bin.ini", verbose=True)
    binconfig.isTrue("DONT_WRITE_BYTECODE")
    binconfig.getParameters()
    binconfig.printParameters()
    binconfig.setParameter("PARAM1", "VALUE1")
    binconfig.setParameter("PARAM2", "VALUE2")
    binconfig.setParameter("PARAM3", "VALUE3")
    binconfig.setParameter("SET_DEFAULT_ENCODING", "W-850")
    binconfig.printParameters()
    binconfig.export(False, "hola.txt")
    print(binconfig.getValue(binconfig.getParameters()[1]))
    print(binconfig.getValue("DONT_WRITE_BYTECODE"))
    print(binconfig.getValue("SET_DEFAULT_ENCODING"))
