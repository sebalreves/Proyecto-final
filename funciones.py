from opciones import *
import pygame as pg
import random
class Funciones:
    def __init__(self,game):
        self.game = game
        self.transicion = False
        self.oscurecer = False
        self.tiritar = False
        self.cuadriculado = False
        self.animando = False
        self.pausa = False 
        
        #transicion
        self.alpha = 0
        self.superficie = pg.Surface((ANCHO,ALTO))
        
    def aplicar_filtros(self):
        if not self.pausa: #se aplicaran los filtros solo si el juego no esta pausado
            #transicion
            if self.transicion :
                self.transicion_pantalla()
            if self.alpha != 0:
                self.game.pantalla.blit(self.superficie,(0,0))
                
            #tiritar
            if self.tiritar:
                if random.random() > 0.98:
                    x = 0 + int(random.uniform(-3,3))
                    y = 0 + int(random.uniform(-3,3))
                    self.tiritar_pantalla(x,y)
                
            #dibujar cuadriculado
            if self.cuadriculado:
                self.dibujar_cuadriculado()
                
            #animacion
            if self.animando:
                self.animar_pantalla(self.animacion)
        
    def cambiar_mapa(self,nuevo_mapa):
        #elimina sprites actuales y carga loos del nuevo mapa
        self.game.mapa = self.game.data.mapas[nuevo_mapa]
        self.game.mapa.render() 
        
    def transicion_pantalla(self):
        if not self.transicion :
            self.transicion = True
            if self.alpha == 0:
                self.aumentar = True
            else:
                self.aumentar = False
        #crea un efecto mistico para pasar de un mapa a otro
        
        if self.aumentar:
            self.alpha += 7
            if self.alpha >= 255:
                self.alpha = 255
                self.transicion = False
            self.superficie.set_alpha(self.alpha)
            
        else:
            self.alpha -=7
            if self.alpha <= 0:
                self.alpha = 0
                self.transicion = False
            self.superficie.set_alpha(self.alpha)
            
        
    def tiritar_pantalla(self,x,y):
        self.copia = self.game.pantalla.copy()
        self.game.pantalla.blit(self.copia,(x,y))
        
    def dibujar_cuadriculado(self):
        for x1 in range(0,ANCHO,CUADRADO):
            pg.draw.line(self.game.pantalla,(0,0,0), (x1,0),(x1,ALTO))
        for y1 in range(0,ALTO,CUADRADO):
            pg.draw.line(self.game.pantalla,(0,0,0), (0,y1), (ANCHO, y1))
        
        
    def animar_pantalla(self, animacion):
        #animacion que detiene la interacciones con el usuario mientras dure
        # es la misma idea que las animaciones de los sprites, pero esta se repite una sola vez
        if not self.animando:
            self.animando = True
            self.last_update = 0
            self.cont = 0
            self.animacion = animacion
        
        now = pg.time.get_ticks()
        if now - self.last_update > ANI_FPS:
            self.last_update = now
            if self.cont < len(self.game.data.animaciones[self.animacion].frames):
                self.game.pantalla.blit(self.game.data.animaciones[self.animacion].frames[self.cont],(0,0))
                self.cont += 1
            else:
                self.animando = False

        
        
        
        
        
        