#!/usr/bin/env python
# -*- coding: utf-8 -*-
#transformer - permite adaptar un exportado traducido a uno válido para hoa
#Pablo Pizarro, 2014

import os
import sys


reload(sys)
sys.setdefaultencoding('UTF8') #@UndefinedVariable

try:
    namearchive = raw_input("Ingrese el nombre del archivo que desea transformar: ").replace(".txt", "")
    archivo = open(namearchive+".txt","r")
except: 
    print "El archivo no existe!"
    exit()
    
l = []
nw = []
for i in archivo: l.append(i)
for j in range(0,len(l),2):
    num = l[j].replace("{","").replace("}","").replace("\n","")
    txt = l[j+1].replace(" ","|")
    linea = num+" // "+txt
    nw.append(linea)
print "Archivo importado correctamente"
archivo.close()

archivo2 = open(namearchive+".txt","w")
for i in nw:
    archivo2.write(i)
archivo2.close()

try: os.remove("_import.pyc")
except: pass