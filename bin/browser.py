#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__': from path import *

# Sencillo navegador web
#
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
import cookielib
import errors
import htmlentitydefs
import mechanize
import re

# Constantes
HREF_HEADERS = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1"

# Funciones de clase
def unescape(text):
    """
    Reemplaza los caracteres html
    :param text: HTML
    :return: HTML sin caracteres
    """

    # noinspection PyShadowingNames
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text

    return re.sub("&#?\w+;", fixup, text)


class Browser:
    """Navegador web"""

    def __init__(self):
        """
        Función constuctora
        :return: void
        """
        self.br = mechanize.Browser()  # navegador
        self.cookies = cookielib.LWPCookieJar()  # cookies
        self.br.set_cookiejar(self.cookies)
        self.opened = False  # define si una páginas se ha cargado
        self.selectedForm = False  # define si se ha definido un formulario

        # Opciones del navegador
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_refresh(False)
        self.br.set_handle_robots(False)
        # noinspection PyProtectedMember
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    def playBrowser(self):
        """
        Obtener el browser
        :return: Browser
        """
        return self.br

    def addHeaders(self, header):
        """
        Agregar headers al navegador
        :param header: String de browser header
        :return: void
        """
        self.br.addheaders = [('User-agent', header)]

    def abrirLink(self, web):
        """
        Ingresar a una dirección web
        :param web: Link a web
        :return: Integer en caso de error
        """
        try:  # Intento cargar la web
            self.br.open(web)
            self.opened = True
            self.selectedForm = False
        except:
            return errors.BR_ERRORxNO_ACCESS_WEB

    def getHtml(self):
        """
        Obtener el código html
        :return: String
        """
        if self.opened:
            return self.br.response().read()
        else:
            return errors.BR_ERRORxNO_OPENED

    def getTitle(self):
        """
        Obtener el título
        :return: String
        """
        if self.opened:
            return self.br.title()
        else:
            return errors.BR_ERRORxNO_OPENED

    def getHeaders(self):
        """
        Obtener los headers
        :return: String
        """
        if self.opened:
            return self.br.response().info()
        else:
            return errors.BR_ERRORxNO_OPENED

    def getForms(self):
        """
        Obtener los forms
        :return: String
        """
        if self.opened:
            return self.br.forms()
        else:
            return errors.BR_ERRORxNO_OPENED

    def selectFormById(self, formid):
        """
        Definir un formulario como activo mediante un id
        :param formid: String
        :return: Integer en caso de error
        """
        formid = str(formid)
        if formid != "":  # Si el id no está vacío
            if formid.isdigit():  # Si es un dígito
                try:
                    self.selectedForm = True
                    return self.br.select_form(nr=int(formid))
                except:
                    return errors.BR_ERRORxERROR_SET_FORM
            else:
                return errors.BR_ERRORxNO_VALIDID
        else:
            return errors.BR_ERRORxNO_FORMID

    def selectFormByName(self, formname):
        """
        Definir un formulario como activo mediante un id
        :param formname: Nombre del formulario
        :return: Integer en caso de error
        """
        if formname != "":  # Si el id no está vacío
            try:
                self.selectedForm = True
                return self.br.select_form(name=formname)
            except:
                return errors.BR_ERRORxERROR_SET_FORM
        else:
            return errors.BR_ERRORxNO_FORMID

    def submitForm(self, form, values):
        """
        Enviar un formulario
        :param form: Formulario
        :param values: Valores
        :return: Integer en caso de error
        """
        if self.selectedForm:
            if len(form) > 0 and len(values) > 0:
                if len(form) == len(values):
                    try:
                        for i in range(len(form)): self.br.form[form[i]] = values[i]
                        self.br.submit()
                    except:
                        return errors.BR_ERRORxERROR_SET_SUBMIT
                else:
                    return errors.BR_ERRORxNO_VALID_SUBMIT_NOT_EQUAL
            else:
                return errors.BR_ERRORxNO_VALID_SUBMIT_EMPTY
        else:
            return errors.BR_ERRORxNO_SELECTED_FORM

    def clearCookies(self):
        """
        Elimina las cookies
        :return: void
        """
        self.cookies.clear_session_cookies()
