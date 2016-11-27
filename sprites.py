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
        #Hace el cambio de fotograma cada cierto tiempo
            
        now = pg.time.get_ticks()
        if now - self.last_update > ANI_FPS  :
            self.last_update = now
            self.current_frame = (self.current_frame + 1)% len(self.game.data.animaciones[self.name]['1'].frames)
            self.image = self.game.data.animaciones[self.name][self.direccion].frames[self.current_frame]
            self.redimensionar(self.game.escalado)
            self.rect = self.image.get_rect()
            
            self.mask = pg.mask.from_surface(self.image, 127)
            self.outline =  self.mask.outline(1)
        

            

class Persona():
    def __init__(self,game):
        #necesario para el jugador, gente del escenario y otros personajes
        self._layer = 3
        self.groups = game.all_sprites
        
        self.game = game
        self.image = pg.Surface((30,30))
        self.image.fill(NEGRO)
        self.rect = self.image.get_rect()   # rect real de la imagen
        self.draw_rect = self.image.get_rect()   # rect que se dibuja con un offset de la camara
        #la idea es que el draw_rect depende de el rect real, pero no viceversa
        
        self.rect.center = (ANCHO/2, 310)
        self.pos = Vec(ANCHO/2, 310)
        self.draw_pos = Vec(ANCHO/2, 310)
        self.acc = Vec(0,0)
        self.vel = Vec(0,0)
        
    def movimiento_acelerado(self):
        self.acc += self.vel * (PLAYER_FRICTION/self.game.map.velocidad)
        self.vel += self.acc
        
        self.pos += self.vel + (self.acc/2)
        self.rect.center = self.pos
        
        if abs(self.vel.x)< 0.1:
            self.vel.x = 0
        if abs(self.acc.x) < 0.1:
            self.acc.x = 0
        
        # update draw_rect,
        self.draw_pos.x = self.draw_rect.center[0]
        self.draw_pos.y = self.draw_rect.center[1]
    def movimiento_lineal(self):
        self.vel.x = 0
        if self.acc.x > 0:
            self.vel.x = PLAYER_SPEED
        elif self.acc.x < 0:
            self.vel.x = PLAYER_SPEED*-1
        
        self.pos.x += self.vel.x* self.game.dt
        self.rect.center = self.pos
        
        self.draw_pos.x = self.draw_rect.center[0]
        self.draw_pos.y = self.draw_rect.center[1]
        
    
    def draw_mask(self,color=(102,178,255)):
        if self.game.data.save['animaciones']:
            self.mask = pg.mask.from_surface(self.image, 127)
            self.outline =  self.mask.outline(1)
            try:
                pg.draw.polygon(self.image,color,self.outline)
                self.last_image = self.image
            except  ValueError:
                pass
    
    def elegir_animaciones(self):
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
            
            
            if abs(self.vel.x) > 0.3 and self.acc.x == 0:
                self.next = 'cam-detenerse'
                
                
            if abs(self.vel.x) <= 0.32:
                if abs(self.acc.x) > 0 and (self.next == 'caminar' or self.next == 'pie'):
                    self.next = 'comenzar-avanzar' 
                
            if self.name== 'girar':
                self.next = 'pie'


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
    
    def elegir_penca(self):
        if abs(self.vel.x) >0:
            self.name = 'caminar penca'
        else:
            self.name = 'pie penca'
            
    def redimensionar(self,valor):
        ancho,alto = self.image.get_size()
        self.image = pg.transform.scale(self.image, (int(ancho*valor),int(alto*valor)))
        self.rect = self.image.get_rect()
        
    def reloco(self,valor):
        ancho = int(self.rect.width * valor)
        alto = int(self.rect.height * valor)
        self.image = pg.transform.scale(self.image, (ancho,alto))
        self.rect = self.image.get_rect()
        
        
class Jugador(pg.sprite.Sprite, Animado, Persona):
    def __init__(self,game):
        self._layer = PLAYER_LAYER
        Animado.__init__(self, game)
        Persona.__init__(self,game)
        pg.sprite.Sprite.__init__(self)
        self.loco = False
           
    def update(self):
        self.acc.x , self.acc.y = 0,0
        self.acc.x = self.seguir()
        
        if self.game.data.save['animaciones']:
            self.elegir_animaciones()
            self.animar()
            if self.loco:
                self.reloco(1.07)
            self.draw_mask()
            self.movimiento_acelerado()
            
        else:
            self.elegir_penca()
            self.animar()
            self.movimiento_lineal()
        #print self.acc.x, self.vel.x
            
        
    def seguir(self):
        #sigue al mouse cuando se oprime boton izquierdo
        if self.game.mouse.botones[2]:
            distancia = (self.game.mouse.pos.x - self.draw_pos.x)
            if abs(distancia) > PLAYER_RADIO:
                if abs(distancia) < 100:
                    self.vel.x = int (self.direccion)* 0.3
                    return 0
                
                if distancia > 0:
                    return PLAYER_ACC
                else:
                    return -1 * PLAYER_ACC
        return 0
        
    def aparecer(self,mapa_nuevo):
        #arreglar esto
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
                    

        
class Transito():
    def __init__(self,game):
        self.game = game
        self.grupo = list()
        self.cantidad_personas = 5
        for persona in range(self.cantidad_personas):
            t = Transeunte(self.game)
            self.grupo.append(t)

            
    def update(self):
        pass
                    
                
    def agregar_to_allsprites(self,layer):
        self.game.all_sprites.add(self.grupo)
        for sprite in self.grupo:
            self.game.all_sprites.change_layer(sprite, layer)
        
    def eliminar_from_allprites(self):
        for sprite in self.grupo:
            sprite.kill()
               
                    
                
        
class Transeunte(pg.sprite.Sprite,Animado,Persona):
    def __init__(self,game):
        self._layer = 1
        Animado.__init__(self, game)
        Persona.__init__(self,game)
        pg.sprite.Sprite.__init__(self)
        
        self.sentido = random.choice([-1,1])
        self.vel.x = 1.88*self.sentido
        
        spawn = random.randint(0,1200)
        self.rect.center = (spawn, 600)
        self.pos = Vec(spawn, 600)
        self.draw_pos = Vec(spawn, 600)
        self.spawntimer = 0
        
    def update(self):
        self.acc.x = PLAYER_ACC*self.sentido
        self.elegir_animaciones()
        self.animar()
        self.draw_mask(GRIS_7)
        self.movimiento_acelerado()
        
        if self.draw_pos.x > 1300 or self.draw_pos.x < -100:
            now =pg.time.get_ticks()
            if now- self.spawntimer > 1500:
                self.spawntimer = now
                self.reespawn()
        
    def reespawn(self):
        self.sentido = random.choice([-1,1])
        delta = 1200- self.game.jugador.draw_pos.x
        if self.sentido == 1:
            spawn = self.game.jugador.pos.x - (1200-delta+100)
        else:
            spawn = self.game.jugador.pos.x + delta + 100
            
        self.pos.x = spawn
            
        
        
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game,name, x, y,layer):
        self._layer = layer
        pg.sprite.Sprite.__init__(self)
        
        self.game = game
        self.image = pg.Surface((30,30))
        
        self.layer = layer
        
        #define color
        if False:
            if self.layer == 1:
                self.image.fill((100,30,30))
            elif self.layer == 2:
                self.image.fill((150,0,0))
            else:
                self.image.fill((200,0,0))

        self.image = self.game.data.sprites[name]
        
        self.rect = self.image.get_rect()
        self.draw_rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.topleft = x*CUADRADO, y*CUADRADO
        
        
        

 

