import pygame as pg
import sys
from os import path
from opciones import *
from sprites import *


class Game():
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption('hola')
        self.clock = pg.time.Clock()
        self.new()
        
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.jugador = Jugador(self)
        self.all_sprites.add(self.jugador)
        self.run()
        
    def run(self):
        while True:
            self.dt = self.clock.tick(FPS) /1000.0
            self.events()
            self.update()
            self.draw()
            
                    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
    
    def update(self):
        self.all_sprites.update()
        pg.display.flip()
    
    def draw(self):
        pg.display.set_caption(str(round(self.clock.get_fps())))
        self.pantalla.fill(BLANCO)
        self.all_sprites.draw(self.pantalla)
        pg.display.flip()

    def load_date(self):
        pass
        
        
g = Game()
