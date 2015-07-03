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

    # Función constructura
    def __init__(self, texture, type, pos):
        self.texture = texture
        self.type = type  # 1: pista, 2: decoracion, 3: obstaculo
        self.pos = pos
        self.rect = self.texture.get_rect()
        self.width, self.height = self.texture.get_size()

    # Dibujar el objeto en la superficie
    def draw(self, surface, window, cameraPos):
        drawx = cameraPos[0] - self.pos[0] + (window.getWindowWidth() - 1000) / 2
        drawy = cameraPos[1] - self.pos[1] + (window.getWindowHeight() - 600) / 2
        if (-self.width <= drawx <= window.getWindowWidth()) and (-self.height <= drawy <= window.getWindowHeight()):
            surface.blit(self.texture, (drawx, drawy))

    # Retorna las dimensiones del objeto
    def getDimension(self):
        return self.width, self.height

    # Retorna la posición
    def getPos(self):
        return self.pos

    # Retorna el rectangulo de la imagen
    def getRect(self):
        return self.rect

    # Retorna el tipo de objeto
    def getType(self):
        return self.type
