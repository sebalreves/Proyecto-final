import pygame as pg
from opciones import *
from mapa import *


class Juego:
    def __init__(self):
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.pantalla_rect = pg.Rect(0,0,ANCHO,ALTO)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.data.load_mapas()
        self.clock = pg.time.Clock()
        self.mundo = 1
        
    def nuevo_mundo(self):
        if self.mundo == 1:
            self.init_map = True
            self.jugador = Jugador(self)
            self.map = self.data.mapas['mapa1']
            #self.map.render()
            
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
            if self.map.name == 'mapa1':
                if self.init_map:
                    #self.transito.agregar_to_allsprites(1)
                    #self.amigo1 = Parlanchin(self, 3, 10, 1, 'personaje', 1)
                    #self.all_sprites.add(self.amigo1)
                    self.init_map = False
                    
            elif self.map.name == 'mapa2':
                if self.init_map:
                    self.transito.agregar_to_allsprites(1)
                    self.init_map = False
                    
                
        elif self.mundo == 2:
            #4000, 1100
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

