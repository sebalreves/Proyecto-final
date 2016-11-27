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
        self.escalado = 1
        
    def nuevo_mundo(self):
        if self.mundo == 1:
            self.init_map = True
            self.jugador = Jugador(self)
            self.map = self.data.mapas['primer mapa']
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
            if self.map.name == 'mapa1':
                if self.init_map:
                    self.jugador.pos.y = 370
                    self.transito.agregar_to_allsprites(1)
                    self.amigo1 = Parlanchin(self, 3, 10, 1, 'personaje', 1)
                    self.all_sprites.add(self.amigo1)
                    self.init_map = False
                    
            elif self.map.name == 'mapa2':
                if self.init_map:
                    self.transito.agregar_to_allsprites(1)
                    self.init_map = False
                    
            elif self.map.name == 'primer mapa':
                if self.init_map:
                    self.init_map = False
                    self.escalado = 1.3
                    self.jugador.pos.y = 370
                    
            elif 'central' in self.map.name:
                if self.init_map:
                    self.init_map = False
                    if self.map.name == 'central1':
                        self.escalado = 1
                        self.jugador.pos.y = 310
                    elif self.map.name == 'central2':
                        self.escalado = 1
                        self.jugador.pos.y = 306
                    elif self.map.name == 'central3':
                        self.escalado = 1
                        self.jugador.pos.y = 360
                    elif self.map.name == 'central4':
                        self.escalado = 1
                        self.jugador.pos.y = 310
                    elif self.map.name == 'central5':
                        self.escalado = 0.95
                        self.jugador.pos.y = 320
                    elif self.map.name == 'central6':
                        self.escalado = 0.93
                        self.jugador.pos.y = 334
                    elif self.map.name == 'central7':
                        self.escalado = 0.93
                        self.jugador.pos.y = 334
                    elif self.map.name == 'central8':
                        self.escalado = 0.93
                        self.jugador.pos.y = 327
                    elif self.map.name == 'central9':
                        self.escalado = 0.89
                        self.jugador.pos.y = 350
                    elif self.map.name == 'central10':
                        self.escalado = 0.93
                        self.jugador.pos.y = 350
                    elif self.map.name == 'central11':
                        self.escalado = 0.89
                        self.jugador.pos.y = 367
                    elif self.map.name == 'central12':
                        self.escalado = 0.90
                        self.jugador.pos.y = 295

                    
                
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

