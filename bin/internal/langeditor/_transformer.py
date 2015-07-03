#!/usr/bin/env python
# -*- coding: utf-8 -*-
#transformer - permite adaptar los archivos traducidos desde google a archivos válidos para hoa
#Pablo Pizarro, 2014

import os
import sys

reload(sys)
sys.setdefaultencoding('UTF8') #@UndefinedVariable

DL = "//"
DL2 = " // "

try:
    namearchive = raw_input("Ingrese el nombre del archivo que desea transformar: ").replace(".txt", "")
    archivo = open(namearchive+".txt","r")
except:
    print "El archivo no existe!"
    exit()

archivo2 = open(namearchive+"_transformed"+".txt","w")
for line in archivo:
    line = line.strip().replace(" ","").replace("\xef\xbb\xbf","").split(DL)
    digit = str(line[0])
    text = line[1]
    if digit.isdigit() or "!" in digit:
        newline = str(int(digit.replace("!", "")))+DL2+text
        archivo2.write(newline+"\n")
    else:
        archivo2.write("Error en la linea '"+digit+"'\n")
        print "Error en la linea '"+digit+"'"
        print "Se terminó la ejecución del script debido a un error en el formato del archivo a transformar."
        archivo2.close()
        archivo.close()
        exit()

print "El archivo se transformó correctamente a '"+namearchive+"_transformed.txt."
#cierro los archivos
archivo2.close()
archivo.close()
try: os.remove("_transformer.pyc")
except: pass