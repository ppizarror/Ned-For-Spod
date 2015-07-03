#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Clase selector, permite manejar elementos y funciones para una entrada del menu
#
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

class Selector:

    # Función constructora
    def __init__(self, title, elements, onchange=None, onreturn=None, *args):

        # Elementos en el selector
        self.args = args  # argumentos de las funciones
        self.elements = elements  # elementos del selector
        self.index = 0  # indice seleccionado
        self.onchange = onchange  # evento al cambiar el selector
        self.onreturn = onreturn  # evento al presionar return
        self.title = title  # titulo del selector
        self.total_elements = len(elements)  # total de elementos

    # Aplica el item seleccionado al retornar
    def apply(self):
        if self.onreturn is not None:
            if len(self.args) > 0:
                self.onreturn(self.elements[self.index][1], *self.args)
            else:
                self.onreturn(self.elements[self.index][1])

    # Aplica el item seleccionado al cambiarlo
    def change(self):
        if self.onchange is not None:
            if len(self.args) > 0:
                self.onchange(self.elements[self.index][1], *self.args)
            else:
                self.onchange(self.elements[self.index][1])

    # Retorna el texto del elemento actual
    def get(self):
        return "{0} < {1} >".format(self.title, self.elements[self.index][0])

    # Mueve el selector hacia la izquierda
    def left(self):
        self.index = (self.index - 1) % self.total_elements
        self.change()

    # Mueve el selector hacia la derecha
    def right(self):
        self.index = (self.index + 1) % self.total_elements
        self.change()
