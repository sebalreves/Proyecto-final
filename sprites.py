import pygame as pg
from opciones import*
from vector import *
import os

class Grupos():
    def __init__(self, game):
        self.game = game
        
        self.layer_0= pg.sprite.Group()      #Grupo a uxuliar que no se ocupa
        self.layer_1= pg.sprite.Group()
        self.layer_2= pg.sprite.Group()
        self.layer_3= pg.sprite.Group()
        self.layer_4= pg.sprite.Group()
        self.layer_5= pg.sprite.Group()
        self.layer_6= pg.sprite.Group()
        self.layer_7= pg.sprite.Group()
        
        self.layers = [self.layer_0,
                       self.layer_1, 
                       self.layer_2, 
                       self.layer_3, 
                       self.layer_4,
                       self.layer_5,
                       self.layer_6,
                       self.layer_7]

    def dibujar(self):
        #se dibuja en la pantalla
        for layer in self.layers:
            for sprite in layer:
                # mover rectangulo auxiliar para hacer colisiones
                sprite.draw_rect.topleft = self.game.camara.aplicar(sprite)[0:2]
                
                #el objeto se dibujara solo si esta dentro de la pantalla
                if sprite.draw_rect.colliderect(self.game.pantalla_rect):
                    self.game.pantalla.blit(sprite.image, self.game.camara.aplicar(sprite))
                
    def agregar(self,sprite,layer):
        self.layers[layer].add(sprite)

    def vaciar(self, layer=0):
        if layer == 0:
            for layer in self.layers:
                layer.empty()
        else:
            self.layers[layer].empty()
            
    def update(self):
        # llama a actualizarse a todos los sprites
        for layer in self.layers:
            layer.update()
            
    
class Animacion():
    #carga las animaciones en la data
    def __init__(self, directorio):
        self.directorio = directorio
        self.cargar_frames()
        
    def cargar_frames(self):
        # se cargan los fotogramas de una animacion
        self.frames = list()
        for frame in os.listdir(self.directorio):   #probar aux en for
            img = pg.image.load(archivo.format(self.directorio,frame))
            img = pg.transform.scale(img,(300, 300))
            self.frames.append(img)
            
class Animado():
    # atributos de un objeto animado, no carga ningun dato
    def __init__(self,game):
        self.game = game
        self.last_update = 0
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        
    def animar(self, name, tipo):
        now = pg.time.get_ticks()
        if now - self.last_update > ANI_FPS:
            self.last_update = now
            self.current_frame = (self.current_frame + 1)% len(self.frames)
            self.image = self.game.animaciones[name].frames[self.current_frame]
            self.rect = self.image.get_rect()

class Jugador(pg.sprite.Sprite):
    def __init__(self,game,layer):
        #Animado.__init__(self, game)
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
        #self.image, self.rect = self.game.data.animaciones['caminar'].animar(1)
        
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

        if self.acc.x != 0 and self.acc.y !=0:
                self.acc.x /= 1.414
                self.acc.y /= 1.414
        
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel) < 0.1 :
            self.vel = 0
            
        self.pos += self.vel + (self.acc**2)/2

        if self.pos.x > ANCHO + self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x< 0- self.rect.width/2:
            self.pos.x = ANCHO + self.rect.width/2 
        
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
 

