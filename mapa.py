import pygame as pg
from opciones import*
from sprites import*
import random
from vector import *
        
class Mouse():
    def __init__(self,game):
        self.game = game
        pg.mouse.set_pos(ANCHO/2, ALTO/2)
        pg.mouse.set_visible(False)
        self.pos = Vec(ANCHO/2, ALTO/2)
        self.botones = [False,False,False]
        self.boton_up = False
        
        self.blanco = pg.image.load(arch_dir + '/blanco.png')
        self.negro = pg.image.load(arch_dir + '/negro.png')
        self.morado = pg. image.load(arch_dir +'/morado.png')
        self.image = self.blanco

        
    def update(self):
        #actualiza variables
        self.pos.x, self.pos.y = pg.mouse.get_pos()
        self.botones = pg.mouse.get_pressed()
        
        #actualiza el color del mouse
        if self.botones[2]:
            self.image = self.negro
        elif self.botones[0]:
            self.image = self.morado
        else:
            self.image = self.blanco

        
    def draw(self):
        self.game.pantalla.blit(self.image, (self.pos))
     
class Grupos():
    # grupos que definen las diferentes capas donde se ubican los sprites
    
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
        if  not self.game.funciones.pausa and not self.game.funciones.animando:
            self.game.pantalla.fill(BLANCO)
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
                      
class Mapa:
    def __init__(self, game, carpeta):
        self.game = game
        self.layers = dict()
        
        #coloca al jugador dependiendo del mapa, aun pendiente
        self.player_layer = 2
        if carpeta == "direccion/mapa1":
            self.player_layer = 2
            
        #Crea las instancias de las capas
        contador = 1
        for txt in os.listdir(carpeta):
            self.layers[contador] = Layer(self.game, archivo.format(carpeta,txt), contador)
            contador +=1
            
        #dimensiones de la capa donde esta el jugador, necesarias para la camara
        self.ancho = self.layers[self.player_layer].ancho + 500
        self.alto = self.layers[self.player_layer].alto  + 500
        
    def render(self):
        #cambia al jugador de layer, dependiendo del mapa que se cargue
        # dibuja los sprites en la pantalla, limpiando los grupos y agregando los nuevos sprites
        self.game.grupos.vaciar()
        self.game.jugador = Jugador(self.game, self.player_layer)
        for layer in self.layers.values():
            layer.render()
            
class Layer:
    def __init__(self,game,filename, layer):
        # carga el txt como una matriz
        self.layer = layer
        self.sprites = list()
        self.game = game
        self.data = list()
        txt = open(filename)
        for linea in txt:
            self.data.append(linea.strip())
        txt.close()
        self.ancho = len(self.data[0]) * CUADRADO
        self.alto = len(self.data) *CUADRADO
        
        #carga los sprites de la capa(lee la matriz)
        cont_y = 0
        for fila in self.data:
            cont_y+=1
            cont_x =0
            for lugar in fila:
                cont_x+=1
                #carga el sprite dependiendo de la id que se lee
                if lugar == '1':
                    self.sprites.append(Wall(self.game,cont_x,cont_y,layer))
                    
    def render(self):
        # agrega los sprites a los grupos
        for sprite in self.sprites:
            self.game.grupos.layers[self.layer].add(sprite)
            sprite.layer = self.layer
                      
class Camara():
    #sigue al jugador y dibuja el resto de los objetos en direccion contraria al movimiento del jugador
    def __init__(self,game,ancho,alto):
        self.rect = pg.Rect(0,0,ancho,alto)
        self.game = game
        self.ancho = ancho
        self.alto = alto
        self.update_camara = True
        self.layer = 3
        self.seguir_jugador = False
    
    def aplicar(self, objeto):
        #no mueve ningun objeto, lo que hace es dibujarlo con un offset
        x,y = self.rect.topleft
        
        # division necesaria para que el jugador quede estatico y el resto se mueva en "perspectiva"
        x = x * objeto.layer/self.layer
        y = y * objeto.layer/self.layer
        
        return objeto.rect.move(x,y)
    
    def update (self, objeto):
        
        self.layer = objeto.layer
        if self.seguir_jugador:
            #se deja al jugador al centro y se mueve el escenario en la direccion contraria al mismo
            
            x = -objeto.rect.centerx + int(ANCHO/2)
            y = -objeto.rect.centery + int(ALTO/2)
            
            # deja avanzar al objeto pero la camara se detiene en los bordes del mapa
            x = min(0, x)  #izquierda
            y = min (0,y)  # arriba
            x = max(-(self.ancho - ANCHO), x)  # derecha
            y = max(-(self.alto - ALTO), y)  # abajo
            
            self.rect = pg.Rect(x,y,self.ancho,self.alto)
        else:
            #se deja estatico el escenario y se mueve el jugador
            pass
            
        