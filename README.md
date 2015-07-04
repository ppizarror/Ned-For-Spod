# Ned For Spod
![][image-1]
Juego en 2D de carreras de autos enteramente desarrollado en python-pygame.

## Introducción
Ned for Spod es un juego _top view_ de carreras de automóviles, el cual tiene por objetivo batir tiempos de vuelta de cada pista.

## Descripción
El juego posee tres tipos de vehículos distintos:
-Clásico
-Moderno
-Súper
Cada tipo de vehículo posee una dificultad distinta (y así distintos tiempos de vuelta), múltiples colores por cada auto, cuatro pistas (de manera inicial), múltiples ambientes, sonidos, fantasma de vuelta rápida y algunos efectos gráficos.
![][image-2]
![][image-3]
Adicionalmente tras cada vuelta el puntaje obtenido es subido a una plataforma online de puntajes, permitiendo así una mayor competitividad con el resto de los jugadores alrededor del mundo:
![][image-4]

## Requisitos
Ned for Spod funciona tanto en Windows como en Ubuntu, requiere la plataforma de Python 2.7 y la librería [http://www.pygame.org][1], adicionalmente se utilizan las siguientes librerías, las cuales se incluyen dentro del proyecto:
- mechanize
	- PIL (Python Imaging Library)
	- pyperclip
	- WConio
	Actualmente en OSX no se obtienen buenos resultados, sin embargo el programa puede ejecutarse sin mayores problemas.

## Licencia
Este proyecto está licenciado bajo GPLv2 (GNU General Public License, version 2) [https://www.gnu.org/licenses/gpl-2.0.html][2].

## Autor
Pablo Pizarro
2015

[1]:	http://www.pygame.org/ "http://www.pygame.org"
[2]:	https://www.gnu.org/licenses/gpl-2.0.html

[image-1]:	https://raw.githubusercontent.com/ppizarror/ppizarror.github.io/master/resources/images/nfs-python/splash.png "Menú principal"
[image-2]:	https://raw.githubusercontent.com/ppizarror/ppizarror.github.io/master/resources/images/nfs-python/gameplay3.png "Vuelta en el desierto"
[image-3]:	https://raw.githubusercontent.com/ppizarror/ppizarror.github.io/master/resources/images/nfs-python/gameplay1.png "Fantasma y algunos efectos gráficos"
[image-4]:	https://raw.githubusercontent.com/ppizarror/ppizarror.github.io/master/resources/images/nfs-python/results.png "Resultados"