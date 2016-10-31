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
        self.timer = 0
        self.current_frame = 0
        self.direccion = '1'
        self.name = 'pie'
        self.next = None

    def animar(self):
        #un objeto puede tener distintas animaciones
        self.elegir_animaciones()
        now = pg.time.get_ticks()
        if now - self.last_update > ANI_FPS  :
            
            self.last_update = now
            self.current_frame = (self.current_frame + 1)% len(self.game.data.animaciones[self.name]['1'].frames)
            self.image = self.game.data.animaciones[self.name][self.direccion].frames[self.current_frame]
            self.rect = self.image.get_rect()
            
        self.mask = pg.mask.from_surface(self.image, 127)
        self.outline =  self.mask.outline(1)
        
    def elegir_animaciones(self):
        #la compreobacion se hace antes y se deja encargado a hacer para cuando el contador sea 0

        if not self.next or self.next == 'caminar':
            if self.vel.x > 0:
                self.direccion = '1'
            elif self.vel.x < 0 :
                self.direccion = '-1' 
            else:
                self.next = 'pie'
                
            if self.direccion == '1':
                if  self.acc.x > 0:
                    self.next = 'caminar'
                elif self.acc.x < 0:
                    self.next = 'cam-girar'
                    if self.vel.x == 0:
                        self.next = 'girar'

            elif self.direccion == '-1':
                if  self.acc.x < 0:
                    self.next = 'caminar'
                elif self.acc.x > 0:
                    self.next = 'cam-girar'
                    if self.vel.x == 0:
                        self.next = 'girar'
            
            
            if abs(self.vel.x) > 0 and self.acc.x == 0:
                self.next = 'cam-detenerse'
                
            if abs(round(self.vel.x,4))==0.1732:
                print 123
                
            if abs(self.vel.x) <= 0.32:
                if abs(self.acc.x) > 0 and (self.next == 'caminar' or self.next == 'pie'):
                    self.next = 'comenzar-avanzar' 
                
            if self.name== 'girar':
                self.next = 'pie'


        print self.next, self.name, self.vel.x, self.acc.x, self.current_frame
        
        if self.next and self.current_frame == len(self.game.data.animaciones[self.name]['1'].frames)-1: # solo se cambiara de animacion cuando haya terminado la anterior
            self.name = self.next
            self.current_frame = 0

            if self.next == 'cam-detenerse' or self.next == 'comenzar-avanzar':
                self.next = 'pie'
                
            else:
                self.next = None
                
            if self.name== 'girar':
                self.vel.x = 0
                
                
        # situaciones especiales
        if self.name == 'cam-detenerse' and abs(self.acc.x)>0:
            if self.acc.x * int(self.direccion) < 0:
                self.current_frame = 0
                self.name = 'cam-girar'
            self.acc.x = 0
            
        
        if self.name == 'girar':
            self.vel.x = self.vel.x / 12.0
            
        if self.name == 'caminar':
            self.acc.x = PLAYER_ACC* int(self.direccion)
        
        if self.name == 'cam-girar':
            self.next = 'pie'
            self.acc.x = PLAYER_ACC* int(self.direccion)*-0.65
            
            


                    

class Jugador(pg.sprite.Sprite, Animado):
    def __init__(self,game):
        Animado.__init__(self, game)
        self._layer = 3
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game
        self.image = pg.Surface((30,30))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()   # rect real de la imagen
        self.draw_rect = self.image.get_rect()   # rect que se dibuja con un offset de la camara
        #la idea es que el draw_rect depende de el rect real, pero no viceversa
        
        self.rect.center = (ANCHO/2, 470)
        self.pos = Vec(ANCHO/2, 470)
        self.draw_pos = Vec(ANCHO/2, 470)
        self.acc = Vec(0,0)
        self.vel = Vec(0,0)
        
        
    def update(self):
        #self.animar()

        #self.draw_mask()
        self.acc.x , self.acc.y = 0,0
        
        self.acc.x = self.seguir()
        
        self.animar()
        self.draw_mask()
        
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1 :
            self.vel.x = 0

            
        self.pos += self.vel + (self.acc**2)/2
        self.rect.center = self.pos
        
        # update draw_rect,
        self.draw_pos.x = self.draw_rect.center[0]
        self.draw_pos.y = self.draw_rect.center[1]
        
        

    def seguir(self):
        #sigue al mouse cuando se oprime boton izquierdo
        if self.game.mouse.botones[2]:
            distancia = (self.game.mouse.pos.x - self.draw_pos.x)

            if abs(distancia) > PLAYER_RADIO:
                if distancia > 0:
                    return PLAYER_ACC
                else:
                    return -1 * PLAYER_ACC
        return 0
    
    def draw_mask(self):
        self.mask = pg.mask.from_surface(self.image, 127)
        self.outline =  self.mask.outline(1)
        try:
            pg.draw.polygon(self.image,(102,178,255),self.outline)
            self.last_image = self.image
        except  ValueError:
            pass
            
        #suavizar superficie
    
    
    def aparecer(self,mapa_nuevo):
        mapa_anterior = self.game.map.name
        
        if mapa_nuevo == 'mapa1':
            if mapa_anterior == 'mapa2':
                self.pos.x = 63
                self.game.camara.rect.topleft = 0,0
                
        elif mapa_nuevo == 'mapa2':
            if mapa_anterior == 'mapa1':
                self.pos.x = 1230
                self.game.camara.rect.topleft = -100,0



class Parlanchin(pg.sprite.Sprite):
    def __init__(self,game, x, y, layer, personaje, nodo):
        self._layer = layer
        pg.sprite.Sprite.__init__(self)
        self.game = game
        #elementos sprite
        self.image = self.game.data.sprites[personaje]
        self.rect = self.image.get_rect()
        self.draw_rect = self.image.get_rect()
        self.rect.topleft = x*CUADRADO, y*CUADRADO
        self.hit_box = PARLANCHIN_HITBOX
        self.hit_box.center = self.rect.center
        
        #elementos dialogo
        self.nodo= nodo
        self.en_espera = False
        self.hablando = False

    def update(self):
        #se acabo la conversacion
        if not self.game.dialogo:
            if self.hablando:
                self.nodo = 0
                self.hablando = False
                
                
                
        if self.hit_box.collidepoint(self.game.jugador.rect.center):  #si el jugaodor esta cerca del parlanchin
            self.en_espera = True
        else:           #si el jugador esta lejos
            if self.hablando:   # si se estaba hablando pero se aleja el jugador
                self.game.dialogos.iniciar_parametros()
            self.en_espera = False
            self.hablando = False
            if self.game.dialogo:
                self.game.dialogo = 0
            
            
        if self.en_espera:
            #iniciar la conversacion
            if self.rect.collidepoint(self.game.mouse.pos):
                if self.game.mouse.boton_up[0]:
                    self.game.dialogo = self.nodo
                    self.hablando = True
                    

                
                    
        


        
        
        
        
        
        
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
 

