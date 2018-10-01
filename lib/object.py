# coding=utf-8
"""
OBJETO
Maneja objetos del mundo, como pistas y decoraciones, dibuja a los elementos
en pantalla.

Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    from path import *


class Gameobject(object):
    """Objetos del juego"""

    def __init__(self, texture, _type, pos):  # @ReservedAssignment
        """
        Función constructora
        :param texture: Textura del objeto
        :param _type: Tipo del objeto
        :param pos: Posición (x,y) del objeto
        :return: void
        """

        self.texture = texture
        self.type = _type  # 1: pista, 2: decoracion, 3: obstaculo
        self.pos = pos
        self.rect = self.texture.get_rect()
        self.width, self.height = self.texture.get_size()

    def draw(self, surface, window, camera_pos):
        """
        Dibujar el objeto en pantalla
        :param surface: Superficie de dibujo
        :param window: Ventana de la aplicación
        :param camera_pos: Posición de la camara
        :return: void
        """
        drawx = camera_pos[0] - self.pos[0] + (window.get_window_width() - 1000) / 2
        drawy = camera_pos[1] - self.pos[1] + (window.get_window_height() - 600) / 2
        if (-self.width <= drawx <= window.get_window_width()) and (
                -self.height <= drawy <= window.get_window_height()):
            surface.blit(self.texture, (drawx, drawy))

    def get_dimension(self):
        """
        Retorna las dimensiones del objeto
        :return: void
        """
        return self.width, self.height

    def get_pos(self):
        """
        Retorna la posición
        :return: void
        """
        return self.pos

    def get_rect(self):
        """
        Retorna el rectangulo de la imágen
        :return: void
        """
        return self.rect

    def get_type(self):
        """
        Retorna el tipo de objeto
        :return: void
        """
        return self.type
