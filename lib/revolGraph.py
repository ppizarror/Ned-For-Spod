#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__': from path import *  # @UnusedWildImport

# Grafico de las revoluciones
#
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
from bin import pygame


class revolGraph:
    """Gráfico de revoluciones"""

    def __init__(self, blocks, pos, width, height, space=0):
        """
        Función constructora
        :param blocks: Bloques del gráfico horizontales
        :param pos: Posición (x,y) en pantalla
        :param width: Ancho del gráfico
        :param height: Alto del gráfico
        :param space: Espacio en pixeles entre cada barra horizontal
        :return: void
        """
        # Variables de clase
        self.delta_percentage = 100 / blocks
        self.squares = []
        # Se crean los recuadros dado los parámetros
        delta_height = height / blocks
        delta_width = float(width - space * blocks) / blocks
        delta_color = 255 / blocks
        for i in range(blocks):
            pos_a = (int(pos[0] + (delta_width + space) * i), int(pos[1] + height - delta_height * (i + 1)))
            pos_b = (
                int(pos[0] + (delta_width + space) * i + delta_width), int(pos[1] + height - delta_height * (i + 1)))
            pos_c = (int(pos[0] + (delta_width + space) * i + delta_width), int(pos[1] + height))
            pos_d = (int(pos[0] + (delta_width + space) * i), int(pos[1] + height))
            self.squares.append([(255, 255 - delta_color * i, 0), [pos_a, pos_b, pos_c, pos_d]])

    def draw(self, surface, percentage):
        """
        Dibuja el gráfico dado un cierto porcentaje
        :param surface: Superficie de dibujo
        :param percentage: Porcentaje de dibujo
        :return: void
        """
        for i in range(int(percentage) / self.delta_percentage):
            pygame.draw.polygon(surface, self.squares[i][0], self.squares[i][1])
