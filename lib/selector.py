# coding=utf-8
"""
SELECTOR
Clase selector, permite manejar elementos y funciones para una entrada del menú.

Autor: PABLO PIZARRO @ppizarror
Fecha: ABRIL 2015
"""

if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    from path import *


class Selector(object):
    """Selector del menú"""

    # Función constructora
    def __init__(self, title, elements, onchange=None, onreturn=None, *args):
        """
        Función constructora.
        :param title: Título del selector
        :param elements: Elementos de selector
        :param onchange: Función a ejecutar una vez cambiado un ítem
        :param onreturn: Función a ejecutar una vez seleccionado un ítem
        :param args: Argumentos de la función
        :return: void
        """

        # Elementos en el selector
        self.args = args  # argumentos de las funciones
        self.elements = elements  # elementos del selector
        self.index = 0  # indice seleccionado
        self.onchange = onchange  # evento al cambiar el selector
        self.onreturn = onreturn  # evento al presionar return
        self.title = title  # titulo del selector
        self.total_elements = len(elements)  # total de elementos

    def apply(self):
        """
        Aplica el item seleccionado al retornar.
        :return: void
        """
        if self.onreturn is not None:
            if len(self.args) > 0:
                self.onreturn(self.elements[self.index][1], *self.args)
            else:
                self.onreturn(self.elements[self.index][1])

    def change(self):
        """
        Aplica el item seleccionado al cambiarlo.
        :return: void
        """
        if self.onchange is not None:
            if len(self.args) > 0:
                self.onchange(self.elements[self.index][1], *self.args)
            else:
                self.onchange(self.elements[self.index][1])

    def get(self):
        """
        Retorna el texto del elemento actual.
        :return: String
        """
        return "{0} < {1} >".format(self.title, self.elements[self.index][0])

    def left(self):
        """
        Mueve el selector hacia la izquierda.
        :return: void
        """
        self.index = (self.index - 1) % self.total_elements
        self.change()

    def right(self):
        """
        Mueve el selector hacia la derecha.
        :return: void
        """
        self.index = (self.index + 1) % self.total_elements
        self.change()
