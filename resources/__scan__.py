#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Programa que escanea todos los recursos de cada tipo y construye
# el __init__ respectivo
#
# Uso
#    $ __scan__.py -arg1 -arg2 -arg3
#    -folder
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías de sistema
from datetime import date
import math  # @UnusedImport
import os
import sys

from bin import configLoader


reload(sys)
sys.setdefaultencoding('UTF8')
sys.dont_write_bytecode = True

# Se obtiene el directorio actual
__actualpath = str(os.path.abspath(os.path.dirname(__file__))) + "/"
sys.path.append(__actualpath.replace("\\resources", "\\bin"))
sys.path.append(__actualpath.replace("\\resources", ""))

# Importación de librerías internas

# Se cargan las configuraciones
config = configLoader(".config/filetype.ini")
folderformats = {}
for folder in config.getParameters():
    if folder != "FORMAT":
        _fileformats = config.getValue(folder).strip(config.getValue("FORMAT"))
        folderformats[folder] = _fileformats
scanconfig = configLoader(".config/scan.ini")

# Constantes del programa
HASH_LEN = int(scanconfig.getValue("SIZE"))
HEADER = """#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Directorio {0}
# Fichero generado automáticamente usando __scan__.py
#
# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Archivos totales: {3}
# Generado el: {2}

# Importación de liberías
import os

# Definición de variables
__actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace("\\\\","/") + "/"

# Librería de /{0}
{1} = {{"""
HEADER_LAST = """}}

# Función que retorna el elemento <index> de la librería {0}
def get{1}(index):
    try:
        return {0}[index]
    except:
        return -1

# Función que retorna los archivos en {0}
def get{1}Keys():
    return {0}.keys()

# Función que imprime los archivos en {0}
def print{1}Values():
    print "<KEY> {0}[<KEY>]"
    for file in {0}.keys():
        print file +" "+str({0}[file])
    """
LOG_FOLDER = __actualpath.replace("\\resources", "\\data\\log")

# Función que retorna el nombre del archivo dado el string completo de su dirección estatica
def getFilename(fullpath):
    fullpath = fullpath.split("\\")
    filename = str(fullpath[len(fullpath) - 1]).split(".")
    return filename[0]

# Obtiene la fecha del dia actual
def getDate():
    fecha = date.today()
    return str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)

# Función que retorna la carpeta contenedora dado un archivo
def getFolder(filename):
    fullpath = filename.split("\\")
    return fullpath[len(fullpath) - 2]

# Función que retorna un identificador para cada elemento
def getHash(filename):
    filename = filename.split("\\")
    filename = filename[len(filename) - 1]
    return abs(hash(filename)) % (10 ** HASH_LEN)

# Función que retorna si no se tienen colisiones en el hash
def hashValid(listhash):
    size = len(listhash)
    colisions = 0
    for i in range(0, size - 1):
        if listhash[i][0] == listhash[i + 1][0]:
            colisions += 1
    if colisions:
        return (False, colisions)
    else:
        return (True, 0)

# Función que comprueba si un nombre es una carpeta
def isfolder(filename):
    for char in config.getValue("NOTFILE"):
        if char in filename:
            return False
    return True

# Función recursiva que añade todos los ficheros que se encuentren en parentfolder
def look(parentfolder, folder, folderlist):
    for file in os.listdir(folder):
        if isfolder(file):
            look(parentfolder, folder + "\\" + file, folderlist)
        else:
            if validfile(parentfolder, file):
                folderlist.append(folder + "\\" + file)

# Función que comprueba si un archivo tiene un formato valido
def validfile(folder, filename):
    filename = filename.split(".")
    return filename[1] in folderformats[folder.upper()]

# Si se ejecuta el programa
if __name__ == '__main__':

    # Se obtiene la hora
    SCAN_DATE = getDate()

    def _run(folder):
        print scanconfig.getValue("ARGUMENT_LOADING").format(folder),
        if folder in os.listdir(__actualpath):
            # Se cargan los archivos
            filelist = []
            look(folder, __actualpath + folder, filelist)
            if scanconfig.isTrue("HASH"):
                hashedlist = []
                for i in filelist: hashedlist.append([getHash(i), i])
                hashedlist.sort()
                initfile = open(__actualpath + folder + "/__init__.py", "w")
                c = 0; totalelements = len(hashedlist)
                for line in HEADER.split("\n"): initfile.write(line.format(folder, folder.upper(), SCAN_DATE, totalelements) + "\n")
                for line in hashedlist:
                    if c < totalelements - 1:
                        initfile.write("\t" + str(line[0]).rjust(HASH_LEN) + ": " + line[1].replace(__actualpath, '__actualpath + "').replace("\\", "/").replace(folder + "/", "") + '", \\\n')
                    else:
                        initfile.write("\t" + str(line[0]).rjust(HASH_LEN) + ": " + line[1].replace(__actualpath, '__actualpath + "').replace("\\", "/").replace(folder + "/", "") + '"\n')
                    c += 1
                for line in HEADER_LAST.split("\n"): initfile.write(line.format(folder.upper(), folder.title()) + "\n")
                initfile.close()
                # Se verifican colisiones de la hashlist
                validate_hash = hashValid(hashedlist)
                if validate_hash[0]:
                    print scanconfig.getValue("FOLDER_LOADED").format(len(filelist))
                else:
                    print scanconfig.getValue("FOLDER_LOADED_HASHNOTVALID").format(validate_hash[1], len(filelist), scanconfig.getValue("SIZE"))
                del(hashedlist)
            else:
                filelist.sort()
                initfile = open(__actualpath + folder + "/__init__.py", "w")
                c = 0; totalelements = len(filelist)
                prev_folder = ""
                for line in HEADER.split("\n"): initfile.write(line.format(folder, folder.upper(), SCAN_DATE, totalelements) + "\n")
                for line in filelist:
                    linefolder = getFolder(line)
                    if prev_folder != linefolder:
                        prev_folder = linefolder
                        initfile.write("\n\t#" + linefolder.title() + "\n")
                    if c < totalelements - 1:
                        initfile.write('\t"' + getFilename(line) + '": ' + line.replace(__actualpath, '__actualpath + "').replace("\\", "/").replace(folder + "/", "") + '", \\\n')
                    else:
                        initfile.write('\t"' + getFilename(line) + '": ' + line.replace(__actualpath, '__actualpath + "').replace("\\", "/").replace(folder + "/", "") + '"\n')
                    c += 1
                for line in HEADER_LAST.split("\n"): initfile.write(line.format(folder.upper(), folder.title()) + "\n")
                initfile.close()
                print scanconfig.getValue("FOLDER_LOADED").format(len(filelist))
            del(filelist)
        else:
            print scanconfig.getValue("FOLDER_NOT_EXIST").format(folder)

    # Se recorren los argumentos
    for i in range(1, len(sys.argv)):
        if "-" not in sys.argv[i]:
            print scanconfig.getValue("ARGUMENT_NOTVALID").format(sys.argv[i])
        else:
            folder = str(sys.argv[i]).replace("-", "").lower()
            _run(folder)
    if len(sys.argv) == 1:
        print str(scanconfig.getValue("DEFAULT_RUNNING")).format(scanconfig.getValue("DEFAULT_FOLDERS"))
        for folder in scanconfig.getValue("DEFAULT_FOLDERS").split(","):
            _run(folder.strip())
