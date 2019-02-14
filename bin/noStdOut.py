# coding=utf-8
"""
NOSTDOUT
Desactiva el standard output de Python.

Autor: PABLO PIZARRO @ppizarror
Fecha: ABRIL 2015
"""


# noinspection PyMissingOrEmptyDocstring,PyPep8Naming
class noStdOut(object):
    """Desactiva print"""

    def __init__(self): pass

    def write(self, data): pass

    def read(self, data): pass

    def flush(self): pass

    def close(self): pass
