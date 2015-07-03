#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__': from path import *

# OBJETO
# Maneja objetos del mundo, como pistas y decoraciones
# Dibuja a los elementos en pantalla
#
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

class gameObject:
    """Objetos del juego"""

    def __init__(self, texture, type, pos):
        """
        Función constructora
        :param texture: Textura del objeto
        :param type: Tipo del objeto
        :param pos: Posición (x,y) del objeto
        :return: void
        """

        self.texture = texture
        self.type = type  # 1: pista, 2: decoracion, 3: obstaculo
        self.pos = pos
        self.rect = self.texture.get_rect()
        self.width, self.height = self.texture.get_size()

    def draw(self, surface, window, cameraPos):
        """
        Dibujar el objeto en pantalla
        :param surface: Superficie de dibujo
        :param window: Ventana de la aplicación
        :param cameraPos: Posición de la camara
        :return: void
        """
        drawx = cameraPos[0] - self.pos[0] + (window.getWindowWidth() - 1000) / 2
        drawy = cameraPos[1] - self.pos[1] + (window.getWindowHeight() - 600) / 2
        if (-self.width <= drawx <= window.getWindowWidth()) and (-self.height <= drawy <= window.getWindowHeight()):
            surface.blit(self.texture, (drawx, drawy))

    def getDimension(self):
        """
        Retorna las dimensiones del objeto
        :return: void
        """
        return self.width, self.height

    def getPos(self):
        """
        Retorna la posición
        :return: void
        """
        return self.pos

    def getRect(self):
        """
        Retorna el rectangulo de la imágen
        :return: void
        """
        return self.rect

    def getType(self):
        """
        Retorna el tipo de objeto
        :return: void
        """
        return self.type
