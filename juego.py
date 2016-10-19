import pygame as pg
from opciones import *
from mapa import *


class Juego:
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.pantalla_rect = pg.Rect(0,0,ANCHO,ALTO)
        self.all_sprites = pg.sprite.LayeredUpdates()
        
        self.clock = pg.time.Clock()
        self.mundo = 1
        
    def nuevo_mundo(self):
        if self.mundo == 1:
            self.jugador = Jugador(self)
            self.map = self.data.mapas['mapa1']
            self.map.render()
            self.camara = Camara(self, self.map.ancho,self.map.alto)
            

        elif self.mundo == 2:
            pass
            
        elif self.mundo == 3:
            pass
            
        elif self.mundo == 4:
            pass
            
        elif self.mundo == 5:
            pass
            
        elif self.mundo == 6:
            pass
            
        elif self.mundo == 7:
            pass
            
            
    def update_game(self):
        if self.mundo == 1:
            pass
                
        elif self.mundo == 2:
            pass
            
        elif self.mundo == 3:
            pass
            
        elif self.mundo == 4:
            pass
            
        elif self.mundo == 5:
            pass
            
        elif self.mundo == 6:
            pass
            
        elif self.mundo == 7:
            pass
    def leer_data(self):
        print'f'
    def guardar_data(self):
        pass
