#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Maneja el checksum de los archivos

# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
import hashlib
import os

# Constantes del programa
_FOLDERSEP = "/"
_FOLDERTYPE = "_FOLDER_"
_LOOKTYPES = ["py", "txt", "ini", "data"]
_MSG = ["checksum -s -d ({0})", "md5 -f ({0})", "checksum -r ({0})"]
_NONE_ = "462CAB92B7C70601299CD65B4FDC81E6"


def count_depth(folder):
    """
    Función que cuenta la profundidad de un directorio
    :param folder: Carpeta
    :return: Integer
    """
    depth = 0
    for ch in folder:
        if ch is _FOLDERSEP: depth += 1
    return depth


def get_depth(folder):
    """
    Función que retorna la profundidad de un directorio en forma de carácter
    :param folder: Carpeta
    :return: String
    """
    return "\t" * count_depth(folder)


def get_depth_subfolder(folder):
    """
    Función que retorna la profundidad de un sub-directorio en forma de carácter
    :param folder: Carpeta
    :return: String
    """
    return "\t" * (count_depth(folder) + 1)


def get_filetype(filename):
    """
    Función que retorna el tipo de archivo de un cierto elemento de un directorio
    :param filename: Nombre de archivo
    :return: String
    """
    filename = filename.strip().split(".")
    if len(filename) < 2:
        return _FOLDERTYPE
    else:
        return filename[1]


def folder_checksum(folder, checksum, verbose):
    """
    Función que genera el md5 de una carpeta
    :param folder: Carpeta
    :param checksum: Checksum parcial
    :param verbose: Indica si imprime
    :return: void
    """
    try:
        dir_files = os.listdir(folder)
        for filename in dir_files:
            filetype = get_filetype(filename)
            if filetype in _LOOKTYPES:
                checksum.append(md5file(folder + _FOLDERSEP + filename, verbose))
            elif filetype is _FOLDERTYPE and not "~" in filename:
                if verbose: print get_depth_subfolder(filename) + _MSG[0].format(filename)
                folder_checksum(folder + _FOLDERSEP + filename, checksum, verbose)
    except:
        checksum.append(_NONE_)


def md5file(filepath, verbose=False):
    """
    Función que crea el md5 de un archivo
    :param filepath: Archivo
    :param verbose: Indica si imprime
    :return: String md5
    """
    if verbose: print get_depth(filepath) + _MSG[1].format(filepath)
    with open(filepath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data: break
            m.update(data)
        return m.hexdigest()


def md5str(string):
    """
    Función que crea el md5 de un string
    :param string: String
    :return: md5
    """
    string = str(string)
    return hashlib.md5(string).hexdigest().upper()


def path_checksum(path, verbose=False):
    """
    Genera el md5 de un directorio
    :param path: Directorio raiz
    :param verbose: Indica si imprime
    :return: String md5
    """
    if verbose: print _MSG[2].format(path)
    files_checksum = []
    folder_checksum(path, files_checksum, verbose)
    checksum = hashlib.md5()
    for f in files_checksum: checksum.update(f)
    return checksum.hexdigest().upper()
