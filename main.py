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
        self.mouse = Mouse(self)
        self.new()
        
        
    def new(self):
        self.jugador = Jugador(self,PLAYER_LAYER)
        self.map = self.data.mapas['mapa1']
        self.map.render()
        self.camara = Camara(self, self.map.ancho,self.map.alto)
        
        # despues de cargar todos los datos, se inicia el juego
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
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                    
                if event.key == pg.K_p:
                    self.funciones.pausa = not self.funciones.pausa
                        
                # estas son funciones que no influyen en el funcionamiento del programa
                if not self.funciones.pausa:
                    if event.key == pg.K_a:
                        self.camara.seguir_jugador = not self.camara.seguir_jugador
                        
                    if event.key == pg.K_SPACE:
                        self.funciones.transicion_pantalla()
                    
    def update(self):
        if  not self.funciones.pausa and not self.funciones.animando:
            self.mouse.update()
            self.grupos.update()
            self.camara.update(self.jugador)
        pg.display.set_caption(str(round(self.clock.get_fps())))
            
    def draw(self):  
        self.grupos.dibujar()
        self.mouse.draw()
        self.funciones.aplicar_filtros()
        pg.display.update()
        
g = Game()
