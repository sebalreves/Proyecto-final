import sys
from opciones import *
from sprites import*
from mapa import*
from data import *
from funciones import*


class Game():
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.pantalla_rect = pg.Rect(0,0,ANCHO,ALTO)
        self.clock = pg.time.Clock()
        self.grupos = Grupos(self)
        self.data = Data(self)
        self.funciones = Funciones(self)
        self.new()
        self.run()
        
    def new(self):
        self.seguir_jugador = True
        self.jugador = Jugador(self,PLAYER_LAYER)
        self.map = self.data.mapas['mapa1']
        self.map.render()
        self.camara = Camara(self, self.map.ancho,self.map.alto)
        
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
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                    
                if event.key == pg.K_SPACE:
                    if self.seguir_jugador:
                        self.seguir_jugador = False
                    else:
                        self.seguir_jugador = True
                        
    
    def update(self):
        pg.display.set_caption(str(round(self.clock.get_fps())))
        self.grupos.update()
        self.camara.update(self.jugador)
        
    def draw(self):
        self.pantalla.fill(BLANCO)
        self.grupos.dibujar()
        self.funciones.aplicar_filtros()
        pg.display.update()
        
            
        
g = Game()
