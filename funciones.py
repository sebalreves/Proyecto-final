from opciones import *
import pygame as pg
import random
import pytweening as tween
class Funciones:
    def __init__(self,game):
        self.game = game
        self.transicion = False
        self.oscurecer = False
        self.tiritar = False
        self.cuadriculado = False
        self.animando = False
        self.camara_en_movimiento = False  #movimiento independiente del jugador
        self.pausa = False 
        #Blur
        self.hacer_blur = False
        self.blur_range = 5
        self.blur_speed = 0.78
        self.loops = 2
           
        
        #transicion
        self.velocidad = 0
        self.alpha = 0
        self.alpha_2 = 0
        self.superficie = pg.Surface((ANCHO,ALTO))
        self.superficie_2 = pg.Surface((ANCHO,ALTO))
        
        
        
    def filtros_sobre_mouse(self):   #estan por sobre el mouse
        if not self.pausa:
            #transicion
            if self.transicion:
                self.transicion_pantalla(self.velocidad)
                
            if self.game.map.oscurecer:
                self.alpha_2+= 4
                if self.alpha_2 >= 50:
                    self.alpha_2 = 50
                    
            else:
                self.alpha_2 -=4
                if self.alpha_2 <=0:
                    self.alpha_2 = 0

            if self.alpha != 0:
                self.superficie.set_alpha(self.alpha)
                self.game.pantalla.blit(self.superficie,(0,0))

            if self.alpha_2!= 0:
                self.superficie_2.set_alpha(self.alpha_2)
                self.game.pantalla.blit(self.superficie_2,(0,0))
                

            
            
    def filtros(self):
        if not self.pausa: #se aplicaran los filtros solo si el juego no esta pausado
            
            #tiritar
            if self.tiritar:
                if random.random() > 0.9:
                    x = 0 + int(random.uniform(-2,2))
                    y = 0 + int(random.uniform(-2,2))
                    self.tiritar_pantalla(x,y)
                
            #dibujar cuadriculado
            if self.cuadriculado:
                self.dibujar_cuadriculado()
                
            if self.camara_en_movimiento:
                self.mover_camara()
            #animacion
            if self.animando:
                self.animar_pantalla(self.animacion)
                
            #blur
            if self.hacer_blur:
                self.blur()
        
    def cambiar_mapa(self,nuevo_mapa):   # colocar esto en clase mapa
        #elimina sprites actuales y carga loos del nuevo mapa
        self.game.mapa = self.game.data.mapas[nuevo_mapa]
        self.game.mapa.render()
        
    def transicion_pantalla(self,vel):
        if not self.transicion :
            self.velocidad = vel
            self.transicion = True
            if self.alpha < 255:
                self.aumentar = True
            else:
                self.aumentar = False
                
        #crea un efecto mistico para pasar de un mapa a otro
        if self.aumentar:
            self.alpha += self.velocidad
            if self.alpha >= 255:
                self.alpha = 255
                self.transicion = False
            
        else:
            self.alpha -= self.velocidad
            if self.alpha <= 0:
                self.alpha = 0
                self.transicion = False
            
    def oscurecer_pantalla(self,alpha):
        #oscurece levemente la pantalla
        self.superficie_2.set_alpha(40)
        self.game.pantalla.blit(self.superficie_2,(0,0))
            
        
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
        if now - self.last_update > ANI_FPS+400:
            self.last_update = now
            if self.cont < len(self.game.data.animaciones[self.animacion].frames):
                self.game.pantalla.blit(self.game.data.animaciones[self.animacion].frames[self.cont],(0,0))
                self.cont += 1
            else:
                self.animando = False
                
    def mover_camara(self,destino = 0):
        if not self.camara_en_movimiento:
            self.camara_en_movimiento = True
            self.destino = destino
            
        x_inicial,y = self.game.camara.rect.topleft
        x_final= self.destino
        
        distancia = x_final - x_inicial
        if distancia != 0:
            impulso = float(distancia/60)
            if impulso > 5:
                impulso = 5
            x_inicial += impulso
            
        if   self.destino -2   <  x_inicial  < self.destino + 2:
            self.moviendose = False
            x_inicial = self.destino
            
        self.game.camara.rect.topleft = x_inicial,y
        
    def escribir(self,texto, pos, duracion=0):
        superficie = fuente_chica.render(texto, True, NEGRO)
        rect = superficie.get_rect()
        rect.topleft = pos
        self.game.pantalla.blit(superficie, rect)
        return rect
    
    def blur(self):
        #difumina la pantalla
        if not  self.hacer_blur:
            self.hacer_blur = True
            self.signo = 1
            self.blur_value = 1
            self.step = 1.0
            self.last_update_blur = 0
            self.loop = 1
            print 'hola'
            
        #modificar blur
        now = pg.time.get_ticks()
        if now - self.last_update_blur > 50:
            self.last_update_blur = now
            offset = 5 * (tween.easeInOutSine(self.step/10))
            self.blur_value = round(self.blur_value + offset*self.signo, 3)
            
            self.step += 0.78
            if self.step > 5:
                if self.loop > 3:
                    self.hacer_blur = False
                self.step = 0
                self.signo *= -1
                self.loop +=1

                
        #aplicar blur
        surface = self.game.pantalla.copy()
        surf_size = surface.get_size()
        self.scale = 1.0 / self.blur_value
        scale_size = (int(surf_size[0]*self.scale), int(surf_size[1]*self.scale))
    
        surf = pg.transform.smoothscale(surface, scale_size)
    
        surf = pg.transform.smoothscale(surf, surf_size)
        self.game.pantalla.blit(surf,(0,0))

    
    def escribir_derecha(self, texto, pos_y):
        superficie = fuente_chica.render(texto, True, NEGRO)
        rect = superficie.get_rect()
        rect.topleft = ANCHO-rect.width-30, pos_y
        self.game.pantalla.blit(superficie, rect)
        return rect
    
    def escribir_nombre_mapa(self):
        pass

