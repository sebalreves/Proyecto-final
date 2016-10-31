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
        self.data = Data(self)
        self.funciones = Funciones(self)
        self.mouse = Mouse(self)
        self.dialogos = Dialogo(self)
        
        self.nuevo_mundo()
        self.run()

    def run(self):
        while True:
            self.dt = self.clock.tick(FPS) /1000.0
            self.events()
            if  not self.funciones.pausa and not self.funciones.animando:
                self.update()
                self.draw()
                 
    def events(self):
        pg.display.set_caption(str(round(self.clock.get_fps())))
        self.mouse.boton_up = [False,False,False]
        self.keys = pg.key.get_pressed()
        
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
                        #print 'jugador ' + str(self.jugador.pos)
                        #print'camara' + str(self.camara.rect[0:2])
                        pass
                        
                    
    def update(self):
        if  not self.funciones.pausa and not self.funciones.animando:
            self.update_game()
            self.mouse.update()
            self.all_sprites.update()
            
            self.camara.update(self.jugador)
            self.map.update()
        
            
            
    def draw(self):  
        
        self.pantalla.fill((255,255,254))
        #self.funciones.escribir(self.map.name, (500,50))
        for sprite in self.all_sprites:
            # mover rectangulo auxiliar para hacer colisiones
            sprite.draw_rect.topleft = self.camara.aplicar(sprite)[0:2]
            #el objeto se dibujara solo si esta dentro de la pantalla
            #if sprite.draw_rect.colliderect(self.pantalla_rect):
            self.pantalla.blit(sprite.image, self.camara.aplicar(sprite))
            
            
            if type(sprite) == Parlanchin:
                if sprite.nodo:   # si es que el sprite va a hablar}
                    
                    if sprite.hit_box.collidepoint(self.jugador.rect.center):  #usar centro del jugador
                        self.pantalla.blit(self.data.sprites['dialogo'], sprite.rect.midtop)
                    
            
            

                
        if not self.map.borde:
            self.dialogos.update()
        else:
            
            self.map.mostrar_opciones()
        self.funciones.filtros()
        self.mouse.draw()
        self.funciones.filtros_sobre_mouse()
        pg.display.update()
        
g = Programa()



