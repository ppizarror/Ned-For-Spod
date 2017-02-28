#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Lang editor
# Pablo Pizarro, 2013

# Importación de librerias
from Tkinter import *  # @UnusedWildImport
import datetime  # @UnusedImport
import os
import sys  # @UnusedImport @Reimport
from tkFileDialog import *  # @UnusedWildImport
import tkFont
import ttk

try:
    import winsound
except:
    pass

# Configuración de librerías
reload(sys)
sys.setdefaultencoding('UTF8')
_PATH = str(os.path.abspath(os.path.dirname(__file__))).replace('\\', '/')

# Constantes del programa
AUTOR = "Pablo Pizarro"
C_DATA = [650, 450, False, False, False, "*//*", False]
DATADOCUMENTS = "doc/"
DATAICONS = "icons/"
DATACONFIG = "config/"
DATALANGS = _PATH.replace("bin/internal/langeditor", "resources/langs/")
print DATALANGS
DATARECOVER = "recover/"
DEFAULT_FONT_TITLE = "Arial", 10
EMAIL = "ppizarror@ing.uchile.cl"
LANGFILE = DATACONFIG + "langs.txt"
CONFIGURATIONFILE = DATACONFIG + "config.ini"
ICONPROGRAM = DATAICONS + "icon.ico"
CONSTANTFILE = DATACONFIG + "const.ini"
ALERTICON = DATAICONS + "alert.ico"
TITLE = "Langs"
VERSION = 1.8
LANGEND = ".lng"
ml_columns = ("   ID   ", \
              "                               String            " + \
              "                                                  ")


# Genera una matriz dado un archivo


def loadFromArchive(archive):
    l = list()
    archive = open(archive, "r")
    for i in archive:
        l.append(i.strip())
    archive.close()
    return l


# Genera un archivo dado una matriz
def save_from_list(archive, lista):
    archive = open(archive, "w")
    k = 0
    l = len(lista)
    for i in lista:
        if k != l - 1:
            archive.write(i + "\n")
        else:
            archive.write(i)
    archive.close()


# Borrar una matriz
def delMatrix(matrix):
    a = len(matrix)
    if a > 0:
        for k in range(a): matrix.pop(0)  # @UnusedVariable


# Función que reemplaza los caracteres restrictivos
def replaceStrict(a):
    return a.replace(",", "%XCOM%").replace(";", "%XPYC%").replace(":", "%XDP%").replace("-", "%XGUI%").replace("\\",
                                                                                                                "").replace(
        "'", "%XII%")


# Función que retorna los caracteres restrictivos
def putStrict(a):
    return a.replace("%XCOM%", ",").replace("%XPYC%", ";").replace("%XDP%", ":").replace("%XGUI%", "-").replace("%XII%",
                                                                                                                "'")


# Función que comprueba si un texto es digito
def isNumerable(x):
    if x.strip().isdigit():
        return True
    else:
        return False


# Función que ordena las columnas segun orden
def sortby(tree, col, descending):
    data = [(tree.set(child, col), child) for child in tree.get_children('')]  # Obtiene los datos para ordenar
    data.sort(reverse=descending)  # Se reonrdenan y modifican
    for indx, item in enumerate(data): tree.move(item[1], '', indx)
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))


# Se cargan la lista de idiomas disponibles
try:
    LANGLIST = loadFromArchive(LANGFILE)
except:
    archive = open(LANGFILE, "w")
    archive.close()
    LANGLIST = ""


# Clase pop
class pop:
    # Función constructora
    def __init__(self, properties):
        title = properties[0]
        icon = properties[1]
        typeObject = properties[2]
        size = properties[4], properties[3]
        if title == "Error" or title == "Precaucion":
            self.w = Toplevel()
        else:
            self.w = Tk()
        self.w.protocol("WM_DELETE_WINDOW", self.kill)
        self.values = []
        if size[0] != 0 and size[1] != 0: self.w.minsize(width=size[0], height=size[
            1])  # Alineación de la ventana a la mitad de la pantalla
        self.w.resizable(width=False, height=False)
        self.w.geometry('%dx%d+%d+%d' % (
            size[0], size[1], (self.w.winfo_screenwidth() - size[0]) / 2, (self.w.winfo_screenheight() - size[1]) / 2))
        self.w.focus_force()
        self.w.title(title)
        self.w.iconbitmap(icon)
        self.sent = False
        if typeObject == "about":
            Label(self.w, text="Creador: " + properties[5], font=DEFAULT_FONT_TITLE, border=5).pack()
            Label(self.w, text="Mail: " + properties[6], font=DEFAULT_FONT_TITLE, border=5).pack()
            Label(self.w, text="Version: " + str(properties[7]), font=DEFAULT_FONT_TITLE, border=5).pack()
            Button(self.w, text="Cerrar", command=self.w.destroy, relief=GROOVE).pack()
            self.w.bind("<Return>", self.destruir)
        elif typeObject in ["licence", "changelog", "ayuda", "longtext"]:
            archivo = open(properties[5], "r")
            Yscroll = Scrollbar(self.w)
            Yscroll.pack(side=RIGHT, fill=Y)
            texto = Text(self.w, wrap=NONE,
                         yscrollcommand=Yscroll.set, xscrollcommand=None)
            texto.focus_force()
            for i in archivo: texto.insert(INSERT, i)
            texto.pack()
            texto.configure(state="disabled")
            Yscroll.config(command=texto.yview)
            archivo.close()
            self.w.bind("<Return>", self.destruir)
            self.w.bind("<Escape>", self.destruir)
        elif typeObject == "ask":  # Realiza una pregunta que tiene resultado True/False
            try:
                winsound.MessageBeep(-1)
            except:
                pass
            Label(self.w, text=properties[5], font=DEFAULT_FONT_TITLE, border=10).pack()
            F = Frame(self.w)
            F.pack()
            Button(F, text="Si", command=lambda: self.response("si"), width=5, relief=GROOVE).pack(side=LEFT)
            Label(F, text=" ").pack(side=LEFT)
            Button(F, text="No", command=lambda: self.response("no"), width=5, relief=GROOVE).pack(side=LEFT)
            Label(F, text=" ").pack(side=LEFT)
            Button(F, text="Cancelar", command=lambda: self.response("cancel"), width=8, relief=GROOVE).pack()
        elif typeObject == "borrar":
            f = Frame(self.w, border=10)
            f.pack()
            Label(f, text="ID ", anchor=E, width=8).pack(side=LEFT)
            self.idsearch = Entry(f, relief=GROOVE, width=35)
            self.idsearch.pack()
            self.idsearch.focus_force()
            self.idsearch.bind("<Return>", self.borrar)
            Button(self.w, text="Borrar", relief=GROOVE, command=self.borrar).pack()
            self.w.bind("<Escape>", self.destruir)
        elif typeObject == "error":
            try:
                winsound.MessageBeep(0)
            except:
                pass
            Label(self.w, text=properties[5], wraplength=250, anchor=N, border=10).pack()
            Label(self.w, text="")
            Button(self.w, text="Cerrar", command=self.w.destroy, relief=GROOVE).pack()
            self.w.bind("<Return>", self.destruir)
            self.w.bind("<Escape>", self.destruir)
        elif typeObject == "insert":
            f = Frame(self.w, border=10)
            f.pack()
            Label(f, text="String ", anchor=E, width=8).pack(side=LEFT)
            self.insertentry = Entry(f, relief=GROOVE, width=35)
            self.insertentry.pack()
            self.insertentry.focus_force()
            self.insertentry.bind("<Return>", self.insert)
            Button(self.w, text="Insertar", relief=GROOVE, command=self.insert).pack()
            self.w.bind("<Escape>", self.destruir)
        elif typeObject == "modify":
            f = Frame(self.w, border=10)
            f.pack()
            Label(f, text="String ", anchor=E, width=7).pack(side=LEFT)
            self.insertentry = Entry(f, relief=GROOVE, width=35)
            self.insertentry.pack()
            self.insertentry.focus_force()
            self.insertentry.bind("<Return>", self.insert)
            self.insertentry.insert(0, properties[5])
            Button(self.w, text="Modificar", relief=GROOVE, command=self.insert).pack()
            self.w.bind("<Escape>", self.destruir)
        elif typeObject == "search":
            f = Frame(self.w, border=10)
            f.pack()
            Label(f, text="ID ", anchor=E, width=8).pack(side=LEFT)
            self.idsearch = Entry(f, relief=GROOVE, width=35)
            self.idsearch.pack()
            self.idsearch.focus_force()
            self.idsearch.bind("<Return>", self.search)
            Button(self.w, text="Buscar", relief=GROOVE, command=self.search).pack()
            self.w.bind("<Escape>", self.destruir)
        elif typeObject == "searchformodify":
            f = Frame(self.w, border=10)
            f.pack()
            Label(f, text="ID ", anchor=E, width=8).pack(side=LEFT)
            self.idsearch = Entry(f, relief=GROOVE, width=35)
            self.idsearch.pack()
            self.idsearch.focus_force()
            self.idsearch.bind("<Return>", self.search)
            Button(self.w, text="Continuar", relief=GROOVE, command=self.search).pack()
            self.w.bind("<Escape>", self.destruir)
        elif typeObject == "newlang":
            f = Frame(self.w, border=10)
            f.pack()
            Label(f, text="Idioma ", anchor=E, width=8).pack(side=LEFT)
            self.newlangentry = Entry(f, relief=GROOVE, width=35)
            self.newlangentry.pack()
            self.newlangentry.focus_force()
            self.newlangentry.bind("<Return>", self.newlang)
            Button(self.w, text="Crear idioma", relief=GROOVE, command=self.newlang).pack()
            self.w.bind("<Escape>", self.destruir)

    # Función que envia una lista de numeros (id's para borrar)
    def borrar(self, e=None):
        i = self.idsearch.get().decode('utf-8')
        if len(i) != 0 and i.strip().replace(",", "").isdigit():
            i = i.strip().split(",")
            self.values.append(i)
            self.sent = True
            self.destruir()

    # Función que destruye la ventana
    def kill(self):
        self.sent = False
        self.w.destroy()

    # Función para destruir la ventana via evento
    def destruir(self, e=None):
        self.w.destroy()

    # Función que inserta un string
    def insert(self, e=None):
        a = self.insertentry.get().decode('utf-8')
        if len(a) != 0:
            if AUTOTITLE:
                self.values.append(str(a).title())
            else:
                self.values.append(str(a))
        else:
            self.values.append(False)
        self.sent = True
        self.destruir()

    # Función que inserta un string
    def newlang(self, e=None):
        a = self.newlangentry.get().decode('utf-8')
        if len(a) != 0:
            self.values.append(str(a))
            self.sent = True
            self.destruir()

    # Función que envia una respuesta
    def response(self, res):
        if res == "si":
            self.values.append("si")
        elif res == "no":
            self.values.append("no")
        else:
            self.values.append("cancel")
        self.sent = True
        self.destruir()

    # Función que manda un id a buscar
    def search(self, e=None):
        i = self.idsearch.get()
        if isNumerable(i):
            self.values.append(i)
            self.sent = True
            self.destruir()


# Se cargan las configuraciones
try:
    conf_file = open(CONFIGURATIONFILE, "r")
    for i in conf_file:
        i = i.strip()
        c_command = i.split("=")
        if c_command[0].strip() == "XSIZE":
            c_after_command = str(c_command[1]).split(",")
            if isNumerable(c_after_command[0]) and int(c_after_command[0]) >= C_DATA[0]: C_DATA[0] = int(
                c_after_command[0])
        if c_command[0].strip() == "YSIZE":
            c_after_command = str(c_command[1]).split(",")
            if isNumerable(c_after_command[0]) and int(c_after_command[0]) >= C_DATA[1]: C_DATA[1] = int(
                c_after_command[0])
        if c_command[0].strip() == "DEFAULTLANG":
            c_after_command = str(c_command[1]).split(",")
            if (c_after_command[0].strip() != "%") and (c_after_command[0].strip().upper() + LANGEND in LANGLIST):
                C_DATA[2] = c_after_command[0].strip().upper()
        if c_command[0].strip() == "AUTOFOCUS":
            c_after_command = str(c_command[1]).split(",")
            if c_after_command[0].strip().upper() == "ON":
                C_DATA[3] = True
            else:
                C_DATA[3] = False
        if c_command[0].strip() == "REZISE":
            c_after_command = str(c_command[1]).split(",")
            if c_after_command[0].strip().upper() == "ON":
                C_DATA[4] = True
            else:
                C_DATA[4] = False
        if c_command[0].strip() == "DELIMITER":
            c_after_command = str(c_command[1]).split(",")
            if len(c_after_command[0].strip()) > 0: C_DATA[5] = c_after_command[0].strip()
        if c_command[0].strip() == "AUTOTITLE":
            c_after_command = str(c_command[1]).split(",")
            if c_after_command[0].strip().upper() == "ON":
                C_DATA[6] = True
            else:
                C_DATA[6] = False
    conf_file.close()
except:
    # Se genera un nuevo archivo de configuraciones
    archivo = open(CONFIGURATIONFILE, "w")
    archivo.write("#Archivo de Configuraciones\n")
    archivo.write("#No haga cambios indebidos, ellos pueden afectar al comportamiento del programa\n\n")
    archivo.write("#Largo minimo en pixeles del programa, min: 600px\n")
    archivo.write("XSIZE = " + str(C_DATA[0]) + "\n\n")
    archivo.write("#Alto minimo en pixeles del programa, min: 400px\n")
    archivo.write("YSIZE = " + str(C_DATA[1]) + "\n\n")
    archivo.write("#Idioma a cargar por defecto\n")
    archivo.write("DEFAULTLANG = %\n\n")
    archivo.write("#Autofocus de la lista\n")
    archivo.write("AUTOFOCUS = ON\n\n")
    archivo.write("#Reescalado de las columnas tras insertar un elemento\n")
    archivo.write("REZISE = OFF\n\n")
    archivo.write("#Delimitador de los archivos\n")
    archivo.write("DELIMITER = " + str(C_DATA[5]).replace(" ", "*") + "\n\n")
    archivo.write("#Automaticamente se formatea el string\n")
    archivo.write("AUTOTITLE = OFF")
    archivo.close()

# Constantes tras configuración
AUTOFOCUS = C_DATA[3]
AUTOTITLE = C_DATA[6]
DATADELIMITER = C_DATA[5]
PROGRAMSIZE = [C_DATA[0], C_DATA[1]]
RESIZE = C_DATA[4]

# Se guardan las constantes en un archivo de configuraciones
archive = open(CONSTANTFILE, "w")
archive.write(LANGEND + "\n")
archive.write(DATADELIMITER + "\n")
archive.close()
DATADELIMITER = DATADELIMITER.replace("*", " ")


class langs:
    # Función constructora
    def __init__(self, lang=False):
        self.root = Tk()
        self.root.title(TITLE)
        self.root.minsize(width=PROGRAMSIZE[0], height=PROGRAMSIZE[1])
        self.root.geometry(
            '%dx%d+%d+%d' % (PROGRAMSIZE[0], PROGRAMSIZE[1], (self.root.winfo_screenwidth() - PROGRAMSIZE[0]) / 2, \
                             (self.root.winfo_screenheight() - PROGRAMSIZE[1] - 50) / 2))
        self.root.iconbitmap(ICONPROGRAM)
        self.root.focus_force()
        # Menu
        menu = Menu(self.root)
        self.root.config(menu=menu)
        archivomenu = Menu(menu, tearoff=0)
        archivomenu.add_command(label="Nuevo", command=self.newLang, accelerator="Ctrl+N")
        archivomenu.add_command(label="Cargar", command=self.loadLang, accelerator="Ctrl+L")
        archivomenu.add_command(label="Guardar", command=self.saveLang, accelerator="Ctrl+G")
        archivomenu.add_separator()
        archivomenu.add_command(label="Salir", command=self.exitLang, accelerator="Ctrl+G")
        menu.add_cascade(label="Archivo", menu=archivomenu)
        edicionmenu = Menu(menu, tearoff=0)
        edicionmenu.add_command(label="Borrar", command=self.borrar, accelerator="Ctrl+B")
        edicionmenu.add_command(label="Buscar", command=self.buscar, accelerator="Ctrl+F")
        edicionmenu.add_command(label="Insertar", command=self.insertar, accelerator="Ctrl+I")
        edicionmenu.add_command(label="Modificar", command=self.modificar, accelerator="Ctrl+M")
        menu.add_cascade(label="Edición", menu=edicionmenu)
        ayudamenu = Menu(menu, tearoff=0)
        ayudamenu.add_command(label="Acerca de", command=self.about)
        ayudamenu.add_command(label="Ayuda", command=self.helpme, accelerator="Ctrl+A")
        # ayudamenu.add_command(label="Estados",command=self.helpsates)
        ayudamenu.add_command(label="Licencia", command=self.licencia)
        menu.add_cascade(label="Ayuda", menu=ayudamenu)
        # Eventos
        self.root.bind("<Control-B>", self.borrar)
        self.root.bind("<Control-b>", self.borrar)
        self.root.bind("<Control-F>", self.buscar)
        self.root.bind("<Control-f>", self.buscar)
        self.root.bind("<Control-G>", self.saveLang)
        self.root.bind("<Control-g>", self.saveLang)
        self.root.bind("<Control-I>", self.insertar)
        self.root.bind("<Control-i>", self.insertar)
        self.root.bind("<Control-M>", self.modificar)
        self.root.bind("<Control-m>", self.modificar)
        self.root.bind("<Control-N>", self.newLang)
        self.root.bind("<Control-n>", self.newLang)
        self.root.bind("<Control-L>", self.loadLang)
        self.root.bind("<Control-l>", self.loadLang)
        self.root.bind("<Control-S>", self.exitLang)
        self.root.bind("<Control-s>", self.exitLang)
        self.root.bind("<Control-A>", self.helpme)
        self.root.bind("<Control-a>", self.helpme)
        self.root.protocol("WM_DELETE_WINDOW", self.exitLang)
        # Variables del programa
        self.ml_data = [(0, "STRING", 0)]
        self.loaded = False
        self.namelang = "%"
        self.tree = None
        self.changes = False
        self._setup_widgets()
        self._build_tree()
        self._autofocus()
        self.ml_data.pop(0)  # Si no se autocarga un idioma
        if lang == "False":
            self._delete_all()
            self._hide_tree()
        else:
            self.loadLang(0, str(lang) + LANGEND)
        self.root.mainloop(0)

    # Establece el widget de la lista
    def _setup_widgets(self):
        self.treecontainer = Frame(border=0)
        self._show_tree()
        self.tree = ttk.Treeview(columns=ml_columns, show="headings", padding=-2)
        vsb = Scrollbar(orient="vertical", command=self.tree.yview)
        if RESIZE:
            hsb = Scrollbar(orient="horizontal", command=self.tree.xview)
            self.tree.configure(xscrollcommand=hsb.set)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self.treecontainer)
        self.tree.bind("<Double-1>", self._click_tree)
        self.tree.bind("<Return>", self._click_tree)
        self.tree.bind("<Delete>", self._delete_element)
        vsb.grid(column=1, row=0, sticky='ns', in_=self.treecontainer)
        if RESIZE: hsb.grid(column=0, row=1, sticky='ew', in_=self.treecontainer)
        self.treecontainer.grid_columnconfigure(0, weight=1)
        self.treecontainer.grid_rowconfigure(0, weight=1)

    # Realiza autofoco
    def _autofocus(self):
        if AUTOFOCUS:
            try:
                item = self.tree.get_children()[0]
                self.tree.selection_set(item)
                self.tree.focus_set()
                self.tree.focus(item)
            except:
                pass

    # Escribe la lista
    def _build_tree(self):
        for col in ml_columns:
            self.tree.heading(col, text=col,
                              command=lambda c=col: sortby(self.tree, c, 0))
            self.tree.column(col, width=tkFont.Font().measure(col.title()))
        for item in self.ml_data:
            self._insert_item(item)

    # Clickeo de una lista
    def _click_tree(self, event):
        try:
            item = self.tree.selection()[0]
            (a, b) = self.tree.item(item, "values")
            i = self.lookindexfromid(a)
            q = pop(['Modificar', ICONPROGRAM, 'modify', 77, 300, b])
            q.w.mainloop(1)
            if q.sent and q.values[0] != False:
                self.tree.item(item, values=(a, str(q.values[0])))
                self.ml_data[i] = (a, q.values[0])
                if q.values[0] != b: self.titlefy(True)
            del (q)
        except:
            pass

    # Borrado de un elemento
    def _delete_element(self, event=None):
        try:
            item = self.tree.selection()[0]
            pos = self.tree.get_children().index(item)
            self.deletefromid(int(self.tree.item(item, "values")[0]))
            self.tree.delete(item)
            self.titlefy(True)
            if (len(self.tree.get_children()) - pos) >= 1:
                self.tree.selection_set(self.tree.get_children()[pos])
                self.tree.focus_set()
                self.tree.focus(self.tree.get_children()[pos])
        except:
            pass

    # Borra un elemento de la lista
    def _delete_item(self, i):
        self.tree.delete(i)

    # Borra todos los elementos de la lista
    def _delete_all(self):
        child = self.tree.get_children()
        for i in child: self.tree.delete(i)

    # Inserta un elemento
    def _insert_item(self, item):
        self.tree.insert('', 'end', values=item)
        if RESIZE:  # Ajusta el largo de las columnas
            for indx, val in enumerate(item):
                ilen = tkFont.Font().measure(val)
                if self.tree.column(ml_columns[indx], width=None) < ilen: self.tree.column(ml_columns[indx], width=ilen)

    # Inserta todos los valores de la matriz de datos de nuevo
    def _insert_all(self):
        self._delete_all()
        for item in self.ml_data:
            (a, b) = item
            try:
                self.tree.insert('', 'end', values=(a, b.decode('utf-8')))
            except:
                e = pop(["Error al cargar el idioma", ALERTICON, "error", 75, 300, "Hay un error en la linea {0}," + \
                         " no se puede cargar. Posible error en el formato del archivo. Este debe ser UTF-8".format(
                             str(int(a)))])
                e.w.mainloop(0)
            if RESIZE:  # Ajusta el largo de las columnas
                for indx, val in enumerate(item):
                    ilen = tkFont.Font().measure(val)
                    if self.tree.column(ml_columns[indx], width=None) < ilen: self.tree.column(ml_columns[indx],
                                                                                               width=ilen)

    # Muestra la lista
    def _show_tree(self):
        self.treecontainer.pack(fill='both', expand=True)

    # Oculta la lista
    def _hide_tree(self):
        self.treecontainer.pack_forget()

    # Función que muestra el acerca de del programa
    def about(self, e=False):
        pop(["Acerca de", ICONPROGRAM, "about", 115, 220, AUTOR, EMAIL, VERSION]).w.mainloop(0)

    # Función que borra un string (elegido, o a buscar)
    def borrar(self, t="", m=False, e=False):
        if self.loaded:  # si el idioma esta cargado
            q = pop(['Borrar', ICONPROGRAM, 'borrar', 77, 280])
            q.w.mainloop(1)
            if q.sent and q.values[0] != False:
                notfound = ""
                for k in q.values[0]:
                    item = ""
                    k = int(k)
                    for i in self.tree.get_children():
                        if int(self.tree.item(i, "values")[0]) == k:
                            item = i
                            self.deletefromid(k)
                            self.tree.delete(item)
                            self.titlefy(True)
                            break
                    if item == "":
                        if notfound == "":
                            notfound += str(k) + " "
                        else:
                            notfound += "," + str(k) + " "
                if notfound != "":
                    if notfound.count(",") == 0:
                        msg = "La ID " + notfound + " no ha sido encontrada."
                    else:
                        msg = "Las IDs: " + notfound + "no han sido encontradas."
                    e = pop(["Error", ALERTICON, "error", 75, 250, msg])
                    e.w.mainloop(0)
                    del (e)
            del (q)

    # Función que busca un string (elegido, o a buscar)
    def buscar(self, t="", m=False, e=False):
        if self.loaded:  # Si hay un idioma ya cargado
            q = pop(['Buscar', ICONPROGRAM, 'search', 77, 280])
            q.w.mainloop(1)
            if q.sent and q.values[0] != False:
                item = ""
                for i in self.tree.get_children():
                    if int(self.tree.item(i, "values")[0]) == int(q.values[0]):
                        item = i
                        self.tree.selection_set(item)
                        self.tree.focus_set()
                        self.tree.focus(item)
                        break
                if item == "":
                    e = pop(["Error", ALERTICON, "error", 75, 250, "Elemento no encontrado."])
                    e.w.mainloop(0)
                    del (e)
            del (q)

    # Busca un id en la matriz y lo elimina
    def deletefromid(self, j):
        j = int(j)
        k = 0
        for i in self.ml_data:
            if int(i[0]) == j:
                self.ml_data.pop(k)
                self.titlefy(True)
                break
            k += 1

    # Busca un elemento en una matriz y retorna su index
    def lookindexfromid(self, j):
        j = int(j)
        k = 0
        for i in self.ml_data:
            if int(i[0]) == j: return k
            k += 1
        return False

    # Función que cierra el programa
    def exitLang(self, e=False):
        if self.loaded and self.changes:  # Comprueba si hay un idioma cargado
            e = pop(["Aviso", ALERTICON, "ask", 80, 250, "Desea guardar?"])
            e.w.mainloop(1)
            if e.sent:
                if e.values[0] == "si":
                    self.saveLang()
                elif e.values[0] == "cancel":
                    return
                else:
                    pass
            del (e)
        try:
            os.remove("main.pyc")
        except:
            pass
        os.system("taskkill /PID " + str(os.getpid()) + " /F")

    # Función que carga la ayuda al programa
    def helpme(self, e=False):
        pop(["Ayuda", ICONPROGRAM, "licence", 400, 600, DATADOCUMENTS + "AYUDA.txt"]).w.mainloop(0)

    # Función que carga la ayuda de los estados
    def helpsates(self, e=False):
        pop(["Estados", ICONPROGRAM, "licence", 400, 600, DATADOCUMENTS + "STATES.txt"]).w.mainloop(0)

    # Función que inserta un string
    def insertar(self, t="", m=False, e=False):
        if self.loaded:  # Si hay un idioma ya cargado
            q = pop(['Insertar', ICONPROGRAM, 'insert', 73, 280])
            q.w.mainloop(1)
            if q.sent and q.values[0] != False:
                try:
                    i = int(self.ml_data[len(self.ml_data) - 1][0]) + 1
                except:
                    i = 10
                item = (str(i).zfill(5), q.values[0])
                self.ml_data.append(item)
                self._insert_item(item)
                self.titlefy(True)
            del (q)

    # Función que crea un nuevo idioma
    def newLang(self, e=False):
        q = pop(['Crear nuevo idioma', ICONPROGRAM, 'newlang', 77, 280])
        q.w.mainloop(1)
        if q.sent:
            lang = q.values[0].upper().strip() + LANGEND
            if lang in LANGLIST:
                e = pop(["Aviso", ALERTICON, "ask", 80, 250, "Desea reeplazar el idioma?"])
                e.w.mainloop(1)
                if e.sent and e.values[0]:
                    self.namelang = lang
                    self.loaded = True
                    self._show_tree()
                del (e)
            else:
                self.namelang = lang
                self.loaded = True
                self._show_tree()
            self.titlefy()
            self._delete_all()
            delMatrix(self.ml_data)
        del (q)

    # Función que modifica un string (a buscar)
    def modificar(self, t="", m=False, e=False):
        if self.loaded:  # Si hay un idioma ya cargado
            q = pop(['ID a modificar', ICONPROGRAM, 'searchformodify', 77, 280])
            q.w.mainloop(1)
            if q.sent and q.values[0] != False:
                i = self.lookindexfromid(q.values[0])
                if i:
                    e = pop(['Modificar', ICONPROGRAM, 'modify', 77, 300, self.ml_data[i][1]])
                    e.w.mainloop(1)
                    if e.sent and e.values[0] != False:
                        self.ml_data[i] = (q.values[0], e.values[0], self.ml_data[i][2])
                        for k in self.tree.get_children():
                            if int(self.tree.item(k, "values")[0]) == q.values[0]:
                                self.tree.item(k, values=self.ml_data[i])
                                self.titlefy(True)
                                break
                    del (e)
                else:
                    e = pop(["Error", ALERTICON, "error", 75, 250, "Elemento no encontrado."])
                    e.w.mainloop(0)
                    del (e)
            del (q)

    # Función que carga la licencia del programa
    def licencia(self, e=False):
        pop(["Licencia GNU", ICONPROGRAM, "licence", 400, 600, DATADOCUMENTS + "GNU.txt"]).w.mainloop(0)

    def loadLang(self, e=False, t="Noset"):  # Función que carga un idioma
        try:
            if t == "Noset":
                archivo = str(askopenfilename(title="Cargar idioma", initialdir=DATALANGS, defaultextension=LANGEND,
                                              filetypes=[("LANG", LANGEND)]))
                namelang = archivo.split("/")
                self.namelang = namelang[len(namelang) - 1]
            else:
                archivo = t
                self.namelang = t
            if self.namelang != "":
                self._delete_all()
                delMatrix(self.ml_data)
                archivo = open(archivo, "r")
                for i in archivo:
                    item = i.strip().split(DATADELIMITER)
                    if "\xef\xbb\xbf" in item[0]: item[0] = item[0][3:]
                    self.ml_data.append((item[0].zfill(5), item[1].replace("|", " ")))
                archivo.close()
                self.loaded = True
                self._insert_all()
                self._show_tree()
                self._autofocus()
                self.titlefy()
                self.ml_data.sort()
        except:
            self.loaded = False
            self.namelang = ""
            self._hide_tree()
            self._delete_all()
            delMatrix(self.ml_data)
            e = pop(["Error al cargar", ALERTICON, "error", 75, 300, "Error al cargar el idioma"])
            e.w.mainloop(0)
            del (e)

    # Función que guarda un idioma
    def saveLang(self, e=False):
        if self.loaded:  # Si hay un idioma cargado
            try:
                if not self.namelang in LANGLIST:  # Si no esta el idioma en la lista se guarda
                    LANGLIST.append(self.namelang)
                    LANGLIST.sort()
                    save_from_list(LANGFILE, LANGLIST)
                self.ml_data.sort()
                archive = open(DATALANGS + self.namelang, "w")  # Se guarda el archivo de idioma
                for i in self.ml_data: archive.write(
                    str(int(i[0])) + DATADELIMITER + str(i[1]).replace(" ", "|") + "\n")
                archive.close()
                # Se guarda el archivo de idioma en la carpeta de recuperación
                #                 archive = open(DATARECOVER + self.namelang.replace(LANGEND, \
                #                                                                   " - ") + str(datetime.datetime.now())[0:19].replace(":", "-") + LANGEND, "w")
                #                 for i in self.ml_data: archive.write(str(int(i[0])) + DATADELIMITER + str(i[1]).replace(" ", "|") + "\n")
                #                 archive.close()
                self.titlefy()
            except:
                e = pop(["Error", ALERTICON, "error", 75, 275, "Error al guardar el idioma"])
                e.w.mainloop(0)
                del (e)

    # Modifica el titulo del programa
    def titlefy(self, asterisco=False):
        if asterisco:
            self.root.title(TITLE + " - " + self.namelang.replace(LANGEND, "") + "*")
            self.changes = True
        else:
            self.root.title(TITLE + " - " + self.namelang.replace(LANGEND, ""))
            self.changes = False


langs(str(C_DATA[2]))
