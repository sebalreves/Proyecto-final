import pygame as pg
from opciones import*
from vector import *
import os

class Animacion():
    #carga las animaciones en la data
    def __init__(self, directorio):
        self.directorio = directorio
        self.frames = list()
        
        # se cargan los fotogramas de una animacion
        i = 0
        frames_name = os.listdir(self.directorio)   #ordena los archivos contenidos en la carpeta
        for aux in frames_name:
            frames_name[i] = aux.replace('.jpeg', '')
            i+=1
        frames_name = map(int, frames_name)
        frames_name.sort() 
        
        for frame in frames_name:   #probar aux en for
            img = pg.image.load(archivo.format(self.directorio,frame)+'.jpeg')
            img = pg.transform.scale(img,(300, 300))  #hacer el escalado fuera del programa para ahorrar
            self.frames.append(img)
        
        
            
class Animado():
    # atributos de un objeto animado, no carga ningun dato
    def __init__(self,game,inicial):
        self.game = game
        self.last_update = 0
        self.current_frame = 0
        self.image = self.game.data.animaciones[inicial].frames[0]
        self.rect = self.image.get_rect()
        
    def animar(self, name):
        #dependiendo de la situacion, se animaran distintas cosas en un mismo objeto animado
        now = pg.time.get_ticks()
        if now - self.last_update > ANI_FPS:
            self.last_update = now
            self.current_frame = (self.current_frame + 1)% len(self.game.data.animaciones[name].frames)
            self.image = self.game.data.animaciones[name].frames[self.current_frame]
            self.rect = self.image.get_rect()

class Jugador(pg.sprite.Sprite,Animado):
    def __init__(self,game,layer):
        Animado.__init__(self, game,'caminar')
        pg.sprite.Sprite.__init__(self)
        game.grupos.agregar(self,layer)
        
        self.layer = layer
        self.game = game
        self.image = pg.Surface((30,30))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()
        self.draw_rect = self.image.get_rect()
        self.rect.center = (ANCHO/2, ALTO/2)
        self.pos = Vec(ANCHO/2, ALTO/2)
        self.acc = Vec(0,0)
        self.vel = Vec(0,0)
        
        
    def update(self):
        self.animar('caminar')
        
        self.acc.x, self.acc.y = 0,0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_DOWN]:
            self.acc.y = PLAYER_ACC
        
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel) < 0.1 :
            self.vel = 0
            
        self.pos += self.vel + (self.acc**2)/2

        if self.pos.x > ANCHO + self.rect.width/2:
            self.pos.x = ANCHO + self.rect.width/2
        if self.pos.x< 0- self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        
        self.rect.center = self.pos
        
        
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y,layer):
        #self.groups = game.grupos.layers[layer]
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,30))
        self.layer = layer
        
        #define color
        if self.layer == 1:
            self.image.fill((100,30,30))
        elif self.layer == 2:
            self.image.fill((150,0,0))
        else:
            self.image.fill((200,0,0))
        self.rect = self.image.get_rect()
        self.draw_rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = x*CUADRADO, y*CUADRADO
 

