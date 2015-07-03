#!/usr/bin/env python
# -*- coding: utf-8 -*-
#TRANSLATE
#Pablo Pizarro, 2014
#Traduce gracias a google traductor los idiomas de Hero of Antair
#Método lento pero automático

#Importación de librerías
import json
import os
import re
import sys
import time
from urllib import urlencode
from urllib2 import urlopen, Request


#Elimino el archivo pyc generado
try: os.remove("translate.pyc")
except: pass

#Manejo y configuración de librerías
reload(sys)
sys.setdefaultencoding('UTF8')

#Definición de constantes
ARCHIVE_LANGS = "config/translates.ini" #archivo de idiomas disponibles para la traducción
DL = " // " #separador
LANGS = [] #idiomas disponibles
MAX_QUERY = 40 #consultas máximas entre delay
TIME_DELAY = 5 #tiempo de espera para max_query
TIME_QUERY = 0.5 #tiempo de espera entre consultas

try: #Se cargan los idiomas disponibles
    langs = open(ARCHIVE_LANGS,"r")
    for i in langs:
        LANGS.append(i[0:5].replace(" ",""))
    langs.close()
except: #Error al cargar
    print "Error :: No se pueden cargar los idiomas disponibles"
    exit()

#Función adquirida desde
#http://www.3engine.net/wp/2013/12/python-como-traducir-textos-usando-google-translate/
def get_google_translate(text, translate_lang, source_lang=None): #Traduce una linea
    if source_lang == None:    source_lang= 'auto'
    params = urlencode({'client':'t', 'tl':translate_lang, 'q':text.encode('utf-8'), 'sl':source_lang})
    http_headers = {"User-Agent":"Mozilla/4.0 (compatible; MSIE 5.5;Windows NT)"}
    request_object = Request('http://translate.google.com/translate_a/t?'+params, None, http_headers)
    try:
        response = urlopen(request_object)
        string = re.sub(',,,|,,',',"0",', response.read())
        n = json.loads(string)
        translate_text = n[0][0][0]
        res_source_lang = n[2]
        return translate_text
    except Exception, e: print e

try: #Comienza la ejecución
    #Obtengo el nombre del archivo a traducir
    namearchive = raw_input("Ingrese el nombre del archivo que desea traducir: ").replace(".txt", "")
    archivo = open(namearchive+".txt","r")
    cant = 0
    for i in archivo: cant+=1
    archivo.close()
    archivo = open(namearchive+".txt","r")
except: #Si el archivo a traducir no existe
    print "Error :: El archivo no existe!"
    exit()

#Obtengo el idioma a traducir
tolang = raw_input("Ingrese el idioma de destino: ").lower()
if tolang == "": print "El idioma no puede ser nulo"; exit()

if tolang in LANGS: #Si el idioma existe
    toarchive = raw_input("Ingrese el archivo de destino: ").upper() #Consulto el idioma de destino
    if toarchive!="": #Si el nombre es válido
        toarchive+=".txt"
        newarchive = open(toarchive,"w") #Se crea el nuevo archivo
        count = 0
        for i in archivo: #Se recorren las lineas
            os.system('cls') #borro la pantalla
            print "Traduciendo ...",str(count+1).zfill(4), "de", str(cant+1).zfill(4), str(int((count+1)*100//cant+1))+"%"
            linea = i.strip().split(DL)
            nwlinea = linea[1].replace("|"," ")+"\n"
            newarchive.write(linea[0]+DL+get_google_translate(nwlinea, tolang).replace(" ","|")+"\n")
            time.sleep(TIME_QUERY)
            count+=1
            if count==MAX_QUERY: time.sleep(TIME_DELAY)
        print "El archivo se ha traducido correctamente"
        newarchive.close()
    else: print "Error :: El nombre del archivo de destino no puede estar vacio!"
    archivo.close()
else: #Si el idioma no está en la lista de idiomas disponibles
    print "Error :: El idioma '{0}' no existe, consulte la documentacion!".format(tolang)

print "Cerrando programa ...",; os.system("taskkill /PID "+str(os.getpid())+" /F")