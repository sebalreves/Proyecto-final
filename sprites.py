from opciones import*
from vector import *
import os

class Animacion():
    #carga las animaciones en la data
    def __init__(self, directorio):
        self.directorio = directorio
        self.frames = list()
        
        # se cargan los fotogramas de una animacion
        names = range(len(os.listdir(self.directorio))+1)[1:]
        tipo_archivo = os.listdir(self.directorio)[0].split('.')[1]

        for frame in names:
            img = pg.image.load(archivo.format(self.directorio,frame) + '.' + tipo_archivo)
            #img = pg.transform.scale(img,(300, 300))  #hacer el escalado fuera del programa para ahorrar
            self.frames.append(img)
        
        
            
class Animado():
    # atributos de un objeto animado, no carga ningun dato
    def __init__(self,game):
        self.game = game
        self.last_update = 0
        self.current_frame = 0

        
    def animar(self, name):
        #un objeto puede tener distintas animaciones
        now = pg.time.get_ticks()
        if now - self.last_update > ANI_FPS:
            self.last_update = now
            self.current_frame = (self.current_frame + 1)% len(self.game.data.animaciones[name].frames)
            self.image = self.game.data.animaciones[name].frames[self.current_frame]
            self.rect = self.image.get_rect()
            
            

class Jugador(pg.sprite.Sprite, Animado):
    def __init__(self,game):
        Animado.__init__(self, game)
        self._layer = 1
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.image = pg.Surface((30,30))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()   # rect real de la imagen
        self.draw_rect = self.image.get_rect()   # rect que se dibuja con un offset de la camara
        #la idea es que el draw_rect depende de el rect real, pero no viceversa
        self.rect.center = (ANCHO/2, ALTO/2)
        self.pos = Vec(ANCHO/2, ALTO/2)
        self.draw_pos = Vec(ANCHO/2, ALTO/2)
        self.acc = Vec(0,0)
        self.vel = Vec(0,0)
        
        
    def update(self):
        #self.animar('girar')
        self.acc.x, self.acc.y = self.seguir()
        
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel) < 0.1 :
            self.vel = 0
            
        self.pos += self.vel + (self.acc**2)/2
        self.rect.center = self.pos
        
        # update draw_rect,
        self.draw_pos.x = self.draw_rect.center[0]
        self.draw_pos.y = self.draw_rect.center[1]

    def seguir(self):
        #sigue al mouse cuando se oprime boton izquierdo
        if self.game.mouse.botones[2]:
            self.desired = (self.game.mouse.pos - self.draw_pos)
            dist = self.desired.get_length()
            self.desired.normalized()
            if dist < PLAYER_RADIO:
                self.desired *= dist/PLAYER_RADIO * PLAYER_MAX_SPEED
            else:
                self.desired *= PLAYER_MAX_SPEED
                
            steer = self.desired - self.acc
            if steer.get_length() > 0.1:
                steer = (self.desired - self.acc).normalized() * 0.1
            steer.y = 0
            return steer
        else:
            return 0,0
        
    def aparecer(self, lugar):
        pass
            


#------------------------------------------------------- class Parlanchin(Wall):
    #------------------------- def __init__(self,game,x,y,layer,personaje,nodo):
        #-------------------------------- Wall.__init__(self, game, x, y, layer)
        #------------------------------------- self.image = imagen del personaje
#------------------------------------------------------------------------------ 
    #--------------------------------------------------------- def update(self):
        
        
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y,layer):
        self._layer = layer
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
 

