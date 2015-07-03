#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Desactiva el standard output de python

# Game template
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

class noStdOut:
    """Desactiva print"""

    def __init__(self): pass

    def write(self, data): pass

    def read(self, data): pass

    def flush(self): pass

    def close(self): pass
