# coding=utf-8
"""
MENU
Brinda distintas opciones las cuales se pueden seleccionar

Autor: PABLO PIZARRO @ ppizarro ~
Fecha: ABRIL 2015
"""

# Importación de librerías
import types
from bin import *  # @UnusedWildImport
from selector import Selector

# Configuraciones de menú
MENU_ALPHA = 90
MENU_BACK = 0
MENU_BGCOLOR = (0, 0, 0)
MENU_CENTERED_TEXT = True
MENU_DRAW_X = 50
MENU_DRAW_Y = 57
MENU_EXIT = 1
MENU_FONT_COLOR = (255, 255, 255)
MENU_FONT_SIZE = 40
MENU_FONT_SIZE_TITLE = 50
MENU_HEIGHT = 400
MENU_OPTION_MARGIN = 15
MENU_OPTION_SHADOW = True
MENU_SELECTEDCOLOR = (180, 180, 180)
MENU_SELECTED_DRAW = True
MENU_SELECTED_WIDTH = 1
MENU_TITLE_BG_COLOR = (170, 65, 50)
MENU_WIDTH = 600
SELECTOR = -1
SHADOW = (0, 0, 0)


# noinspection PyAttributeOutsideInit,PyBroadException,PyUnresolvedReferences,PyShadowingNames
class Menu(object):
    """Crea menús dinámicos"""

    def __init__(self, window, font, title, **kwargs):
        """
        Constructor
        :param window: Objeto ventana de la aplicación
        :param font: Fuente
        :param title: Titulo principal
        :param kwargs: Paramámetros del menú
        :return: void
        """

        # Se obtienen parámetros pasados por kwargs
        # Transparencia
        if kwargs.get("bgalpha") is not None:
            bgalpha = kwargs.get("bgalpha")
        else:
            bgalpha = MENU_ALPHA
        # Color de fondo a dibujar
        if kwargs.get("bgcolor") is not None:
            bgcolor = kwargs.get("bgcolor")
        else:
            bgcolor = MENU_BGCOLOR
        self.bgColor = (bgcolor[0], bgcolor[1], bgcolor[2],
                        int(255 * (1 - (100 - bgalpha) / 100.0)))
        # Color del titulo
        if kwargs.get("bgcolor_title") is not None:
            bgcolor = kwargs.get("bgcolor_title")
        else:
            bgcolor = MENU_TITLE_BG_COLOR
        self.bgColorTitle = (bgcolor[0], bgcolor[1], bgcolor[2],
                             int(255 * (1 - (100 - bgalpha) / 100.0)))
        # Menu centrado
        if kwargs.get("centered") is not None:
            self.centered_option = kwargs.get("centered")
        else:
            self.centered_option = MENU_CENTERED_TEXT
        # Define si se escribe el rectangulo en el indice seleccionado o no
        if kwargs.get("draw_selected") is not None:
            self.drawselrect = kwargs.get("draw_selected")
        else:
            self.drawselrect = MENU_SELECTED_DRAW
        # Tamaño de la fuente
        if kwargs.get("font_size") is not None:
            self.fontsize = kwargs.get("font_size")
        else:
            self.fontsize = MENU_FONT_SIZE
        # Tamaño de la fuente del titulo
        if kwargs.get("font_size_title") is not None:
            self.fontsize_title = kwargs.get("font_size_title")
        else:
            self.fontsize_title = MENU_FONT_SIZE_TITLE
        # Fuente del menú
        self.font = pygame.font.Font(font, self.fontsize)
        self.fonttitle = pygame.font.Font(font, self.fontsize_title)
        # Color de la fuente
        if kwargs.get("font_color") is not None:
            self.fontColor = kwargs.get("font_color")
        else:
            self.fontColor = MENU_FONT_COLOR
        # Alto del menu en pixeles
        if kwargs.get("height") is not None:
            self.height = kwargs.get("height")
        else:
            self.height = MENU_HEIGHT
        # Distancia entre opciones
        if kwargs.get("option_margin") is not None:
            self.optiondy = kwargs.get("option_margin")
        else:
            self.optiondy = MENU_OPTION_MARGIN
        # Ancho del rectangulo dibujado
        if kwargs.get("rect_width") is not None:
            self.rectwidth = kwargs.get("rect_width")
        else:
            self.rectwidth = MENU_SELECTED_WIDTH
        # Color del item seleccionado
        if kwargs.get("color_selected") is not None:
            self.selectedcolor = kwargs.get("color_selected")
        else:
            self.selectedcolor = MENU_SELECTEDCOLOR
        # Sombra de las opciones
        if kwargs.get("option_shadow") is not None:
            self.option_shadow = kwargs.get("option_shadow")
        else:
            self.option_shadow = MENU_OPTION_SHADOW
        # ancho del menu en pixeles
        if kwargs.get("width") is not None:
            self.width = kwargs.get("width")
        else:
            self.width = MENU_WIDTH
        # Variables independientes no configurables
        self.actual = self  # menu actual
        self.opciones = []  # entradas del menu
        self.index = 0  # indice seleccionado
        self.prev = None  # menu previo
        self.prevDraw = None  # menu previo
        self.size = 0  # numero de elementos en el menu
        # Posición del rectangulo de fondo
        self.posx = (window.get_window_width() - self.width) / 2
        self.posy = (window.get_window_height() - self.height) / 2
        # Puntos del rectangulo del fondo
        self.bgRect = [(self.posx, self.posy),
                       (self.posx + self.width, self.posy),
                       (self.posx + self.width, self.posy + self.height),
                       (self.posx, self.posy + self.height)]
        # Punto a dibujar de las opciones
        if kwargs.get("draw_region_x") is not None:
            self.drawRegionX = kwargs.get("draw_region_x")
        else:
            self.drawRegionX = MENU_DRAW_X
        if kwargs.get("draw_region_y") is not None:
            self.drawRegionY = kwargs.get("draw_region_y")
        else:
            self.drawRegionY = MENU_DRAW_Y
        self.posOptionX = int(
            self.width * (self.drawRegionX / 100.0)) + self.posx
        self.posOptionY = int(
            self.height * (self.drawRegionY / 100.0)) + self.posy
        # Se obtiene el titlo y el rectangulo
        self.title = self.fonttitle.render(title, 1, self.fontColor)
        title_width = self.title.get_size()[0]
        self.titleRect = [(self.posx, self.posy),
                          (self.posx + self.width, self.posy),
                          (self.posx + self.width,
                           self.posy + self.fontsize_title / 2),
                          (self.posx + title_width + 25,
                           self.posy + self.fontsize_title / 2),
                          (self.posx + title_width + 5,
                           self.posy + self.fontsize_title + 5),
                          (self.posx, self.posy + self.fontsize_title + 5)]
        self.titlePos = (self.posx + 5, self.posy - 3)

    # noinspection PyShadowingNames
    def add_option(self, element_name, menu, *args):
        """
        Agrega una entrada al menú
        :param element_name: Nombre del elemento
        :param menu: Dirección del elemento (del tipo menú)
        :param args: argumentos del objeto
        :return: void
        """
        self.actual.opciones.append([element_name, menu, args])
        self.actual.size += 1
        if self.actual.size > 1:
            self.actual.posOptionY += -self.actual.fontsize / 2 - self.actual.optiondy / 2

    def add_selector(self, title, values, event, *args, **kwargs):
        """
        Agrega un selector (menú de opciones lateral) como entrada al menú
        :param title: Titulo del selector
        :param values: Valores (entradas) del selector
        :param event: Evento al seleccionar
        :param args: Argumento de los eventos
        :param kwargs: Parametros de los eventos
        :return: void
        """
        if kwargs.get("index") is not None:
            self.actual.opciones.insert(kwargs.get("index"), [SELECTOR,
                                                              Selector(title,
                                                                       values,
                                                                       event,
                                                                       *args)])
        else:
            self.actual.opciones.append(
                [SELECTOR, Selector(title, values, event, *args)])
        self.actual.size += 1
        if self.actual.size > 1:
            self.actual.posOptionY += -self.actual.fontsize / 2 - self.actual.optiondy / 2

    def down(self):
        """
        Bajar opción
        :return: void
        """
        self.actual.index = (self.actual.index - 1) % self.actual.size

    def draw(self, surface):
        """
        Dibujar el menú en pantalla
        :param surface: Superficie de dibujo
        :return: void
        """
        # Se dibuja el fondo del menú
        pygame.gfxdraw.filled_polygon(surface, self.actual.bgRect,
                                      self.actual.bgColor)
        # Se dibuja el titulo
        pygame.gfxdraw.filled_polygon(surface, self.actual.titleRect,
                                      self.bgColorTitle)
        surface.blit(self.actual.title, self.titlePos)
        # Se dibujan las opciones
        dy = 0
        for option in self.actual.opciones:
            # Si el tipo es un selector
            if option[0] == SELECTOR:
                # Si el indice seleccionado es el item se cambia el color
                if dy == self.actual.index:
                    text = self.actual.font.render(option[1].get(), 1,
                                                   self.actual.selectedcolor)
                    text_bg = self.actual.font.render(option[1].get(), 1,
                                                      SHADOW)
                else:
                    text = self.actual.font.render(option[1].get(), 1,
                                                   self.actual.fontColor)
                    text_bg = self.actual.font.render(option[1].get(), 1,
                                                      SHADOW)
            else:
                # Si el indice seleccionado es el item se cambia el color
                if dy == self.actual.index:
                    text = self.actual.font.render(option[0], 1,
                                                   self.actual.selectedcolor)
                    text_bg = self.actual.font.render(option[0], 1, SHADOW)
                else:
                    text = self.actual.font.render(option[0], 1,
                                                   self.actual.fontColor)
                    text_bg = self.actual.font.render(option[0], 1, SHADOW)
            # Se obtiene el texto y su ancho
            text_width, text_height = text.get_size()
            # Si el texto está centrado se obtiene el tamaño de la fuente
            text_dy = -int(text_height / 2.0)
            if self.actual.centered_option:
                text_dx = -int(text_width / 2.0)
            else:
                text_dx = 0
            # Se dibuja la fuente
            if self.actual.option_shadow:
                surface.blit(text_bg, (self.actual.posOptionX + text_dx - 3,
                                       self.actual.posOptionY + dy * (
                                           self.actual.fontsize + self.actual.optiondy) + text_dy - 3))
            surface.blit(text, (self.actual.posOptionX + text_dx,
                                self.actual.posOptionY + dy * (
                                    self.actual.fontsize + self.actual.optiondy) + text_dy))
            # Si se tiene la seleccionada se dibuja el rectangulo
            if self.actual.drawselrect and (dy == self.actual.index):
                if not self.actual.centered_option:
                    text_dx_tl = -text_width
                else:
                    text_dx_tl = text_dx
                pygame.draw.line(surface, self.actual.selectedcolor,
                                 (self.actual.posOptionX + text_dx - 10,
                                  self.actual.posOptionY + dy * (
                                      self.actual.fontsize + self.actual.optiondy) + text_dy - 2),
                                 (self.actual.posOptionX - text_dx_tl + 10,
                                  self.actual.posOptionY + dy * (
                                      self.actual.fontsize + self.actual.optiondy) + text_dy - 2),
                                 self.actual.rectwidth)
                pygame.draw.line(surface, self.actual.selectedcolor,
                                 (self.actual.posOptionX + text_dx - 10,
                                  self.actual.posOptionY + dy * (
                                      self.actual.fontsize + self.actual.optiondy) - text_dy + 2),
                                 (self.actual.posOptionX - text_dx_tl + 10,
                                  self.actual.posOptionY + dy * (
                                      self.actual.fontsize + self.actual.optiondy) - text_dy + 2),
                                 self.actual.rectwidth)
                pygame.draw.line(surface, self.actual.selectedcolor,
                                 (self.actual.posOptionX + text_dx - 10,
                                  self.actual.posOptionY + dy * (
                                      self.actual.fontsize + self.actual.optiondy) + text_dy - 2),
                                 (self.actual.posOptionX + text_dx - 10,
                                  self.actual.posOptionY + dy * (
                                      self.actual.fontsize + self.optiondy) - text_dy + 2),
                                 self.actual.rectwidth)
                pygame.draw.line(surface, self.actual.selectedcolor,
                                 (self.actual.posOptionX - text_dx_tl + 10,
                                  self.actual.posOptionY + dy * (
                                      self.actual.fontsize + self.actual.optiondy) + text_dy - 2),
                                 (self.actual.posOptionX - text_dx_tl + 10,
                                  self.actual.posOptionY + dy * (
                                      self.actual.fontsize + self.actual.optiondy) - text_dy + 2),
                                 self.actual.rectwidth)
            dy += 1

    def left(self):
        """
        Mueve el selector activo hacia la izquierda
        :return: void
        """
        opcion = self.actual.opciones[self.actual.index][1]
        if isinstance(opcion, Selector):
            opcion.left()

    def reset(self, total=0):
        """
        Resetea el menú
        :param total: Total de reseteos recursivos
        :return: void
        """
        # Se devuelve al menú padre
        i = 0
        while True:
            if self.actual.prev is not None:
                prev = self.actual.prev
                prev_draw = self.actual.prevDraw
                self.draw = prev_draw
                self.actual.index = 0
                self.actual = prev
                self.actual.prev = None
                self.actual.prevDraw = None
                i += 1
                if total != 0 and i == total:
                    break
            else:
                break

    def right(self):
        """
        Mueve el selector (si existe) a la derecha
        :return: void
        """
        opcion = self.actual.opciones[self.actual.index][1]
        if isinstance(opcion, Selector):
            opcion.right()

    def select(self):
        """
        Selecciona la opción actual
        :return:
        """
        try:
            opcion = self.actual.opciones[self.actual.index][1]
            # Si no es una opción crítica
            if isinstance(opcion, Menu):
                actual = self
                self.actual.actual = opcion.actual
                self.actual.prev = actual
                self.actual.prevDraw = self.draw
                self.draw = opcion.draw
            # Si el tipo es un número
            elif isinstance(opcion, types.IntType):
                # Si es volver al menu anterior
                if opcion == MENU_BACK:
                    prev = self.actual.prev
                    prev_draw = self.actual.prevDraw
                    self.draw = prev_draw
                    self.actual.index = 0
                    self.actual = prev
                    self.actual.prev = None
                    self.actual.prevDraw = None
                # Si es terminar el programa
                elif opcion == MENU_EXIT:
                    pygame.quit()
                    utils.destroyProcess()
            # Si el tipo es una función
            elif isinstance(opcion, types.FunctionType) or callable(opcion):
                if len(self.actual.opciones[self.actual.index][2]) > 0:
                    opcion(*self.actual.opciones[self.actual.index][2])
                else:
                    opcion()
            # Si el tipo es Null
            elif isinstance(opcion, types.NoneType):
                pass
            # Si el tipo es Selector
            elif isinstance(opcion, Selector):
                opcion.apply()
        except:
            pass

    def up(self):
        """
        Subir la opción seleccionada
        :return: void
        """
        self.actual.index = (self.actual.index + 1) % self.actual.size
