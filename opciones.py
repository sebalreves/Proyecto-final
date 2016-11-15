import os
import pygame as pg
import random

dir = os.getcwd()
arch_dir = dir + '/' + 'archivos'
frame_dir = arch_dir + '/' + 'fotogramas'
map_dir = arch_dir + '/' + 'mapas'
music_dir = arch_dir + '/' + 'musica'
sprites_dir = arch_dir + '/' + 'sprites'
dialogo_dir = arch_dir +'/' + 'dialogos'
archivo = '{}/{}'   #carpeta/archivo


ANCHO = 800   #32 * 25
ALTO = 480   #32 * 15


FPS = 60
ANI_FPS = 45 # corresponde a 24fps

CUADRADO = 32
ANCHO_T = ANCHO/CUADRADO
ALTO_T = ALTO/CUADRADO

BLANCO =(255,255,255)
NEGRO = (0,0,0)
MORADO = (215,203,253)
GRIS_1 =(30,30,30)
GRIS_2 =(60,60,60)
GRIS_3 =(90,90,90)
GRIS_4 =(120,120,120)
GRIS_5 =(150,150,150)
GRIS_6 =(180,180,180)
GRIS_7 =(210,210,210)
GRIS_8 =(240,240,240)
GRISES_CLAROS = [GRIS_5,GRIS_6,GRIS_7,GRIS_8]
GRISES_OSCUROS= [GRIS_1,GRIS_2,GRIS_3,GRIS_4]

#player
PLAYER_ACC = 0.16
PLAYER_FRICTION = -0.085
PLAYER_RADIO = 60
PLAYER_SPEED = 300

#LAYER
PLAYER_LAYER = 2
WALL_LAYER = 7


#PARLANCHINES
PARLANCHIN_HITBOX = pg.Rect(0,0, 250,200)

#camara
MAX_SPEED = 5

#dialogos
fuente_dir = arch_dir +'/fuente.ttf'
pg.font.init()
fuente_chica = pg.font.Font(fuente_dir, 22)
fuente_media = pg.font.Font(fuente_dir, 25)
fuente_grande = pg.font.Font(fuente_dir, 30)
RAPIDEZ_DIALOGO = 70
RAPIDEZ_MARCADORES = 500

'''|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||
|||||||||||||||||||||'''





