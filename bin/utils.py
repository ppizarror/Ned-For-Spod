# coding=utf-8
"""
UTILS
Este archivo provee de funciones básicas que son globalmente usadas.

Autor: PABLO PIZARRO @ppizarror
Fecha: ABRIL 2015
"""

# Importación de librerías de entorno
from __future__ import print_function
import json
import re
import urllib2
import errors
from path import *  # @UnusedWildImport

# Importación de librerías de sistema
# noinspection PyBroadException
try:
    from datetime import date
    from random import choice
    from urllib import urlencode,urlopen
    from urllib2 import urlopen, Request
    import ctypes
    import os
    import signal
    import string
    import time
except Exception:
    errors.throw(errors.ERROR_IMPORTSYSTEMERROR)

# Importación de librerías externas
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    import WConio  # @UnresolvedImport
except:
    if os.name == "nt":
        errors.warning(errors.ERROR_IMPORTWCONIO)

# Constantes
_CMD_COLORS = {"blue": 0x10,
               "gray": 0x80,
               "green": 0x20,
               "lblue": 0x90,
               "lgray": 0x70,
               "lgreen": 0xA0,
               "lred": 0xC0,
               "purple": 0x50,
               "white": 0xF0,
               "yellow": 0x60,
               "lpurple": 0xD0,
               "lyellow": 0xE0,
               "red": 0x40
               }
_CONSOLE_WRAP = -25
_MSG_LOADINGFILE = "Cargando archivo '{0}' ..."
_MSG_OK = "[OK]"


def compare_version(ver1, ver2):
    """
    Se compara entre dos versiones y se retorna el ganador
    :param ver1: Versión actual
    :param ver2: Versión de sistema
    :return: ver1 or ver2
    """
    ver1 = ver1.split(".")
    ver2 = ver2.split(".")
    for i in range(3):
        if int(ver1[i]) > int(ver2[i]):
            return 1
        elif int(ver1[i]) < int(ver2[i]):
            return 2
    return 0


def colorcmd(cmd, color):
    """
    Función que imprime un mensaje con un color
    :param cmd: command
    :param color: Color
    :return: void
    """
    if color in _CMD_COLORS:
        color = _CMD_COLORS[color]
        # noinspection PyBroadException
        try:
            ctypes.windll.kernel32.SetConsoleTextAttribute(
                ctypes.windll.kernel32.GetStdHandle(-11),
                color)
        except:
            pass
        print(cmd)
        # noinspection PyBroadException
        try:
            ctypes.windll.kernel32.SetConsoleTextAttribute(
                ctypes.windll.kernel32.GetStdHandle(-11),
                0x07)
        except:
            pass
    else:
        print(cmd)


def del_accent(txt):
    """
    Elimina los acentos de un string
    :param txt: String
    :return: String con acentos eliminados
    """
    txt = txt.replace("Á", "A").replace("É", "E").replace("Í", "I").replace(
        "Ó", "O").replace("Ú", "U")
    return txt.replace("á", "a").replace("é", "e").replace("í", "i").replace(
        "ó", "o").replace("ú", "u")


def del_matrix(matrix):
    """
    Borrar una matriz
    :param matrix: Matriz
    :return: void
    """
    a = len(matrix)
    if a > 0:
        for k in range(a):
            matrix.pop(0)


def clrscr():
    """
    Limpia la pantalla
    :return: void
    """
    # noinspection PyBroadException
    try:
        WConio.clrscr()
    except:
        pass


# noinspection PyUnresolvedReferences
def destroy_process():
    """
    Destruye el proceso del programa
    :return: void
    """
    if os.name == "nt":
        os.system("taskkill /PID " + str(os.getpid()) + " /F")
    else:
        os.kill(os.getpid(), signal.SIGKILL)


def generate_random6():
    """
    Genera un string de 6 carácteres aleatorios
    :return: String
    """
    # noinspection PyUnusedLocal
    return ''.join(choice(string.ascii_uppercase) for i in range(6))


def generate_random12():
    """
    Genera un string de 12 carácteres aleatorios
    :return: String
    """
    # noinspection PyUnusedLocal
    return ''.join(choice(string.ascii_uppercase) for i in range(12))


def get_between_tags(html, tagi, tagf):
    """
    Función que retorna un valor entre dos tagss
    :param html: Contenido html
    :param tagi: Tag inicial
    :param tagf: Tag final
    :return: String
    """
    tagi = tagi.strip()
    tagf = tagf.strip()
    # noinspection PyBroadException
    try:
        posi = html.index(tagi)
        if ("<" in tagi) and (">" not in tagi):
            c = 1
            while True:
                # noinspection PyBroadException
                try:
                    if html[posi + c] == ">":
                        posi += (c + 1)
                        break
                    c += 1
                except:
                    return errors.ERROR_TAG_INITNOTCORRECTENDING
        else:
            posi += len(tagi)
        posf = html.index(tagf, posi)
        return html[posi:posf]
    except:
        return False


def get_hour():
    """
    Función que retorna la hora de sistema
    :return: String
    """
    return time.ctime(time.time())[11:16]


def get_date():
    """
    Obtiene la fecha del dia actual
    :return: String dd/mm/aaaa
    """
    fecha = date.today()
    return str(fecha.day) + "/" + str(fecha.month) + "/" + str(fecha.year)


def get_terminal_size():
    """
    Devuelve el tamaño de la consola
    :return: tupla
    """
    env = os.environ

    # noinspection PyShadowingNames,PyMissingOrEmptyDocstring,PyBroadException,PyUnresolvedReferences
    def ioctl_gwinsz(fd):
        try:
            import fcntl
            import termios
            import struct
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr

    cr = ioctl_gwinsz(0) or ioctl_gwinsz(1) or ioctl_gwinsz(2)
    if not cr:
        # noinspection PyBroadException
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_gwinsz(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))
    return int(cr[1]), int(cr[0])


# noinspection PyArgumentEqualDefault
def get_version(label, headers):
    """
    Obtener la versión del programa
    :param label: Label del programa
    :param headers: Headers web
    :return: String
    """
    link = 'LINK_PPPRJ'
    http_headers = {"User-Agent": headers}
    request_object = Request(link, None, http_headers)
    response = urllib2.urlopen(request_object)
    html = response.read()
    html = get_between_tags(
        get_between_tags(html, "<" + label + ">", "</" + label + ">"),
        "<version>", "</version>")
    return html.strip()


# noinspection PyArgumentEqualDefault
def google_translate(text, translate_lang, header, web, source_lang=None):
    """
    Traduce una linea usando el motor de traducciones de google
    :param text: Texto a traducir
    :param translate_lang: Idioma destino
    :param header: Header web
    :param web: Web de traduccion
    :param source_lang: Idioma origen
    :return: String traducido
    """
    if source_lang is None:
        source_lang = 'auto'
    params = urlencode(
        {'client': 't', 'tl': translate_lang, 'q': text.encode('utf-8'),
         'sl': source_lang})
    http_headers = {"User-Agent": header}
    request_object = Request(web + params, None, http_headers)
    response = urlopen(request_object)
    # noinspection PyShadowingNames
    string = re.sub(',,,|,,', ',"0",', response.read())
    n = json.loads(string)
    translate_text = n[0][0][0]
    return translate_text


def is_in(termino, matriz):
    """
    Función que comprueba si un elemento esta en una matriz (no completamente)
    :param termino: Elemento
    :param matriz: Matriz
    :return: booleano
    """
    if termino is not None:
        for elem in matriz:
            if elem in termino:
                return True
    return False


# noinspection PyBroadException
def load_file(archive, lang=_MSG_LOADINGFILE, **kwargs):
    """
    Carga un archivo y retorna una matriz
    :param archive: Archivo
    :param lang: Idioma
    :param kwargs: Parámetros adicionales
    :return: Lista
    """
    if kwargs.get("show_state"):
        print(lang.format("(...)" + archive[_CONSOLE_WRAP:].replace("//", "/")).replace("\"", ""))
    try:
        _l = list()
        archive = open(archive)
        for i in archive:
            _l.append(i.decode('utf-8').strip())
        archive.close()
        if kwargs.get("show_state"):
            print(_MSG_OK)
    except:
        if kwargs.get("show_state"):
            print("error")
        _l = []
    return _l


def print_matrix(matrix):
    """
    Función que imprime una matriz en pantalla
    :param matrix: Matriz
    :return: void
    """
    for j in matrix:
        for k in j:
            print(k)
        print("\n")


def sort_and_uniq(inp):
    """
    Función que elimina datos repetidos
    :param inp: Lista
    :return: Lista modificada
    """
    output = []
    for x in inp:
        if x not in output:
            output.append(x)
    output.sort()
    return output


# noinspection PyShadowingNames
def string2list(string, separator):
    """
    Función que divide un string en una lista usando un separador
    :param string: String inicial
    :param separator: Separador
    :return: String
    """
    return string.strip().split(separator)


def sum_matrix(matrix):
    """
    Función que suma lista de listas
    :param matrix: Matrices
    :return: Double
    """
    suma = 0
    # noinspection PyBroadException
    try:
        for j in matrix:
            for k in j:
                suma += k
        return suma
    except:
        return -1


# Test
if __name__ == '__main__':
    print(string2list("foo bar", " "))
    print(get_date())
    print(get_hour())
    colorcmd("test in purple\n", "purple")
    print(generate_random6())
    print(get_terminal_size())
    # noinspection PyTypeChecker
    print(load_file("__init__.ini"))
    print(sort_and_uniq([1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 10, 5]))
    print(get_between_tags("<player>Username<title></title></player>", "<player>",
                           "</player>"))
    print(get_between_tags("<player>Username</player><title>Altername</title>",
                           "<player>", "</player>"))
    print(get_between_tags("<player>Username</player><title>Altername</title>",
                           "<title>", "</title>"))
