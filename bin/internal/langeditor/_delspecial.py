#importacion de librerias
import sys


reload(sys)
sys.setdefaultencoding('UTF8') #@UndefinedVariable

if len(sys.argv)>1: #si el argumento existe
    archive = open(sys.argv[1],"r")
    text = []
    for i in archive:
        text.append(i)
        for j in i:
            print unicode(j)