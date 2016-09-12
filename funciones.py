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
        self.invertir = False
        self.pintar = False
        
        #transicion
        self.alpha = 0
        self.superficie = pg.Surface((ANCHO,ALTO))
        
    def aplicar_filtros(self):
        #transicion
        if self.transicion:
            if self.alpha == 0:
                self.oscurecer = True
            elif self.alpha == 255:
                self.oscurecer = False
            self.transicion = False
        if self.oscurecer:
            self.transicion_a_negro('+')
        else:
            self.transicion_a_negro('-')
            
        #tiritar
        if self.tiritar:
            if random.random() > 0.98:
                x = 0 + int(random.uniform(-3,3))
                y = 0 + int(random.uniform(-3,3))
                self.tiritar_pantalla(x,y)
            
        #dibujar cuadriculado
        if self.cuadriculado:
            self.dibujar_cuadriculado()

        #invertir
        if self.invertir:
            self.invertir_pantalla()

        #pintar
        if self.pintar:
            self.pintar_pantalla()
            
        #animacion
        
    def cambiar_mapa(self,nuevo_mapa):
        #elimina sprites actuales y carga loos del nuevo mapa
        self.game.mapa = self.game.data.mapas[nuevo_mapa]
        self.game.mapa.render() 
        
    def transicion_a_negro(self, tipo):
        #crea un efecto para pasar de un mapa a otro
        if tipo == '+':
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
        if self.alpha != 0:
            self.game.pantalla.blit(self.superficie,(0,0))
            
    def tiritar_pantalla(self,x,y):
        self.copia = self.game.pantalla.copy()
        self.game.pantalla.blit(self.copia,(x,y))

    def invertir_pantalla(self):
        self.copia = self.game.pantalla.copy()
        self.copia = pg.transform.flip(self.copia,True,True)
        self.game.pantalla.blit(self.copia,(0,0))

    def pintar_pantalla(self):
        self.superficie.fill((255,255,0))
        self.superficie.set_alpha(200)
        self.game.pantalla.blit(self.superficie,(0,0))
        
    def dibujar_cuadriculado(self):
        for x1 in range(0,ANCHO,CUADRADO):
            pg.draw.line(self.game.pantalla,(0,0,0), (x1,0),(x1,ALTO))
        for y1 in range(0,ALTO,CUADRADO):
            pg.draw.line(self.game.pantalla,(0,0,0), (0,y1), (ANCHO, y1))
        
        
    def short_animation(self):
        #animacion  a pantalla completa
        pass
        
        
        
        
        
        
