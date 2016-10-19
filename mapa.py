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
        self.botones = [False,False,False]                #oprimidos
        self.boton_up = [False,False,False]               #soltados
        
        self.blanco = self.game.data.sprites['blanco']
        self.negro = self.game.data.sprites['negro']
        self.morado = self.game.data.sprites['morado']
        self.image = self.blanco

        
    def update(self):
        #actualiza variables
        self.pos.x, self.pos.y = pg.mouse.get_pos()
        self.botones = pg.mouse.get_pressed()
        
        #actualiza el color del mouse
        if self.botones[2]:
            self.image = self.negro
        elif self.botones[0] and self.game.dialogo:
            self.image = self.morado
        else:
            self.image = self.blanco

        
    def draw(self):
        self.game.pantalla.blit(self.image, (self.pos))
     
                      
class Mapa:
    def __init__(self, game, carpeta):
        self.game = game
        self.layers = dict()
        self.info = dict()
        
        #elementos para salir del mapa
        self.alpha = 40
        self.cambiar_mapa = False
        self.oscurito = False

        
        #carga las caracteristicas del mapa
        txt = open(carpeta + '/info.txt')
        lineas = txt.readlines()
        txt.close()
        for linea in lineas:
            llave, valor = linea.strip().split('::')
            self.info[llave.strip()] = valor.strip()
        
        self.player_layer = int(self.info['jugador'])
        self.izquierda = self.info['izquierda']
        self.derecha = self.info['derecha']
            
        #Crea una capa de profundidad por cada txt que conforme el mapa
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
        self.game.all_sprites.empty()
        for cont,layer in enumerate(self.layers.values()):
            self.game.all_sprites.add(layer.sprites)
            if cont == int(self.info['jugador']):
                self.game.all_sprites.add(self.game.jugador)
                
            
        #falta crear funcion para cada mapa, la manera en que spawnea el jugador
        
            
    def update(self):
        self.oscurecer = False
        # saliendo del mapa
        if self.game.jugador.rect.centerx > self.ancho - 150 :
            if self.game.mouse.pos.x > self.ancho-200 :
                self.oscurecer = True
                if self.game.mouse.boton_up[2]:
                    self.cambiar_mapa = True
                    
        if self.game.jugador.rect.centerx < 150:
            if self.game.mouse.pos.x < 100:
                self.oscurecer = True
                if self.game.mouse.boton_up[2]:
                    self.cambiar_mapa = True
                
        
        if self.cambiar_mapa:
            self.game.funciones.transicion_pantalla(3)
            self.cambiar_mapa = False
            
        if self.game.funciones.alpha == 255: #cambia el mapa cuando todo este negro
            self.salir_del_mapa()
            self.game.funciones.transicion_pantalla(6)
            

    def mostrar_opciones(self):
        if self.game.mouse.pos.x > 600:
            for cont, eleccion in enumerate(self.derecha):
                print eleccion
        else:
            for cont, eleccion in enumerate(self.izquierda):
                print eleccion
            
    def salir_del_mapa(self):
        #elimina sprites actuales y carga loos del nuevo mapa
        self.game.dialogo = 0
        self.game.mapa = self.game.data.mapas['mapa2']
        self.game.mapa.render()
            
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
                    

    
class Camara():
    #sigue al jugador y dibuja el resto de los objetos en direccion contraria al movimiento del jugador
    def __init__(self,game,ancho,alto):
        self.rect = pg.Rect(0,0,ancho,alto)
        self.pos = Vec(0,0)
        self.game = game
        self.ancho = ancho
        self.alto = alto
        self.update_camara = True
        self.layer = 3
        self.seguir_jugador = False
        self.moviendose = False #independiente del jugador
    
    def aplicar(self, objeto):
        #no mueve ningun objeto, lo que hace es dibujarlo con un offset
        x,y = self.rect.topleft
        
        # division necesaria para que el jugador quede estatico y el resto se mueva en "perspectiva"
        x = x * objeto._layer/self.layer
        y = y * objeto._layer/self.layer
        
        return objeto.rect.move(x,y)

    
    def update (self, objeto):
        if self.moviendose:
            self.mover_camara()
        self.layer = objeto._layer
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
            pass
            #------------------------------------------- x,y = self.rect.topleft
            #--------------- se deja estatico el escenario y se mueve el jugador
            #------------------------------------- if self.game.keys[pg.K_LEFT]:
                #-------------------------------------------------------- x -= 5
            #------------------------------------ if self.game.keys[pg.K_RIGHT]:
                #-------------------------------------------------------- x += 5
            #------------------------------------------- self.rect.topleft = x,y
            #--------------------------------------------------- print self.rect


            
        
