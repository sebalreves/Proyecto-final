import sys
from dialogos import *
from sprites import*
from funciones import*
from mapa import*
from data import*
from juego import *


class Programa(Juego):
    def __init__(self):
        pg.init()
        Juego.__init__(self)
        self.grupos = Grupos(self)
        self.data = Data(self)
        self.funciones = Funciones(self)
        self.mouse = Mouse(self)
        self.dialogos = Dialogo(self)
        
        self.nuevo_mundo()
        self.x = pg.image.load('2.png')
        self.run()

    def run(self):
        while True:
            self.dt = self.clock.tick(FPS) /1000.0
            self.events()
            self.update()
            self.draw()
                 
    def events(self):
        self.mouse.boton_up = [False,False,False]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse.boton_up[0] = True
                if event.button == 3:
                    self.mouse.boton_up[2] = True


            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                    
                if event.key == pg.K_p:
                    self.funciones.pausa = not self.funciones.pausa
                    
                if not self.funciones.pausa:
                    if event.key == pg.K_a:
                        self.camara.seguir_jugador = not self.camara.seguir_jugador
                    
                    if event.key == pg.K_SPACE:
                        self.data.save_game()
                    
    def update(self):
        if  not self.funciones.pausa and not self.funciones.animando:
            self.mouse.update()
            self.grupos.update()
            self.camara.update(self.jugador)
            self.map.update()
        pg.display.set_caption(str(round(self.clock.get_fps())))
            
            
    def draw(self):  
        self.grupos.dibujar()
        self.dialogos.update()
        self.funciones.filtros()
        self.mouse.draw()
        self.funciones.filtros_sobre_mouse()
        pg.display.update()
        
g = Programa()
