import sys
from opciones import *
from sprites import*
from mapa import*
from data import *


class Game():
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        self.x = pg.Surface((ANCHO,ALTO))
        pg.display.set_caption('hola')
        self.clock = pg.time.Clock()
        self.grupos = Grupos(self)
        self.data = Data(self)
        self.new()
        self.run()
        
    def new(self):
        self.jugador = Jugador(self,PLAYER_LAYER)
        self.map = self.data.mapas['mapa1']
        self.map.render()
        self.camara = Camara(self.map.ancho,self.map.alto)
        
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
                    if self.cam:
                        self.cam = False
    
    def update(self):
        pg.display.set_caption(str(round(self.clock.get_fps())))
        self.grupos.update()
        self.camara.update(self.jugador)
    
    def draw(self):
        self.pantalla.fill(BLANCO)
        
        #for x1 in range(0,ANCHO,CUADRADO):
        #    pg.draw.line(self.pantalla,(20,20,20), (x1,0),(x1,ALTO))
        #for y1 in range(0,ALTO,CUADRADO):
        #    pg.draw.line(self.pantalla,(20,20,20), (0,y1), (ANCHO, y1))
            
        self.grupos.dibujar(camara = True)
        pg.display.update()
        
       
        
g = Game()
