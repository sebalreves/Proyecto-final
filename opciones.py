import os

dir = os.getcwd()
arch_dir = dir + '/' + 'archivos'
frame_dir = arch_dir + '/' + 'fotogramas'
map_dir = arch_dir + '/' + 'mapas'
music_dir = arch_dir + '/' + 'musica'
capa_dir = arch_dir + '/' + 'capas'
dialogo_dir = arch_dir +'/' + 'dialogos'
archivo = '{}/{}'   #carpeta/archivo


ANCHO = 800   #16 x 12
ALTO = 600


FPS = 60
ANI_FPS = 75 # [ms]

CUADRADO = 50
ANCHO_T = ANCHO/CUADRADO
ALTO_T = ALTO/CUADRADO

BLANCO =(255,255,255)
NEGRO = (0,0,0)

PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.06

#LAYER
PLAYER_LAYER = 1
WALL_LAYER = 2

