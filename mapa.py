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
        self.borde = False
        self.opciones = False
        self.name = carpeta.strip().split('/')[-1]
        
        #carga las caracteristicas del mapa
        txt = open(carpeta + '/info.txt')
        lineas = txt.readlines()
        txt.close()
        for linea in lineas:
            llave, valor = linea.strip().split('::')
            self.info[llave.strip()] = valor.strip()
            
        self.player_layer = int(self.info['jugador'])
        self.izquierda = self.info['izquierda'].split(',')
        self.derecha = self.info['derecha'].split(',')
        self.velocidad = 1
        if 'vel' in self.info.keys():
            self.velocidad = int (self.info['vel'])
            print self.velocidad
        
        #Crea una capa de profundidad por cada txt que conforme el mapa
        contador = 1
        for txt in os.listdir(carpeta):
            self.layers[contador] = Layer(self.game, archivo.format(carpeta,txt), contador)
            contador +=1
            
        #dimensiones de la capa donde esta el jugador, necesarias para la camara
        
        self.ancho = self.layers[self.player_layer].ancho 
        self.alto = self.layers[self.player_layer].alto  

      
    def render(self):
        #cambia al jugador de layer, dependiendo del mapa que se cargue
        # dibuja los sprites en la pantalla, limpiando los grupos y agregando los nuevos sprites
        self.game.all_sprites.empty()
        for cont,layer in enumerate(self.layers.values()):
            self.game.all_sprites.add(self.game.jugador)
            self.game.all_sprites.add(layer.sprites)
            
        self.game.all_sprites.change_layer(self.game.jugador, self.player_layer)
                
            
    #falta crear funcion para cada mapa, la manera en que spawnea el jugador
        
            
    def update(self):
        self.borde = False
        self.opciones = False
        # saliendo del mapa
        if self.game.jugador.draw_pos.x > 600 and self.game.mouse.pos.x >600 :
            if len(self.derecha[0]) > 0 :
                
                if 'central' in self.derecha[0] and self.derecha[0] != 'central1':
                    if self.game.mouse.botones[2]:
                        self.cambiar_mapa = True
                        self.lugar = 1
                        self.eleccion = self.derecha[0]
                else:
                    self.opciones = True
                    
        if self.game.jugador.draw_pos.x < 150 and self.game.mouse.pos.x < 150:
            if len(self.izquierda[0])>0:
                if 'central' in self.izquierda[0]:
                    if self.game.mouse.botones[2]:
                        self.cambiar_mapa = True
                        self.lugar = -1
                        self.eleccion = self.izquierda[0]
                else:
                    self.opciones = True
                
        if self.game.jugador.draw_pos.x > 750 or self.game.jugador.draw_pos.x < 50: 
            self.game.jugador.vel *= 0.1
        if self.cambiar_mapa:
            self.game.funciones.transicion_pantalla(3)
            self.cambiar_mapa = False
            
        if self.game.funciones.alpha == 255: #cambia el mapa cuando todo este negro
            self.salir_del_mapa()
            self.game.funciones.transicion_pantalla(6)
            
            
    def mostrar_opciones(self):
        
        self.sobre_boton = False
        
        if self.game.mouse.pos.x > 600:
            for cont, eleccion in enumerate(self.derecha):
                rect = self.game.funciones.escribir_derecha(eleccion, (50*cont +15))
                if rect.collidepoint(self.game.mouse.pos):
                    if not self.sobre_boton: 
                        self.sobre_boton = True
                        inicio, final = ((rect.bottomleft[0],rect.bottomleft[1]-6), 
                                        (rect.bottomright[0],rect.bottomright[1]-6))
                        if self.game.mouse.boton_up[0]:
                            self.cambiar_mapa = True
                            self.lugar = 1
                            self.eleccion = eleccion
                            
                    pg.draw.line(self.game.pantalla,NEGRO,inicio,final)
                    
        else:
            for cont, eleccion in enumerate(self.izquierda):
                rect = self.game.funciones.escribir(eleccion, (20,50*cont +15))
                if rect.collidepoint(self.game.mouse.pos):
                    if not self.sobre_boton: 
                        self.sobre_boton = True
                        inicio, final = ((rect.bottomleft[0],rect.bottomleft[1]-6), 
                                        (rect.bottomright[0],rect.bottomright[1]-6))
                        if self.game.mouse.boton_up[0]:
                            self.cambiar_mapa = True
                            self.lugar = -1
                            self.eleccion = eleccion
                            
                    pg.draw.line(self.game.pantalla,NEGRO,inicio,final)
                    
            
    def spawn_jugador(self):
        if self.lugar == 1:
            self.game.jugador.pos.x = 0
        elif self.lugar == -1:
            self.game.jugador.pos.x = self.game.map.ancho
            
        self.game.jugador.name = 'caminar'
        self.game.jugador.vel.x = 1.88 * self.lugar
    
    def salir_del_mapa(self):
        #elimina sprites actuales y carga loos del nuevo mapa
        #self.game.jugador.aparecer(self.eleccion)
        
        self.game.dialogo = 0
        self.game.map = self.game.data.mapas[self.eleccion]
        self.game.map.render()
        self.game.camara.ancho = self.game.map.ancho
        self.spawn_jugador()
        self.game.init_map = True
            
class Layer:
    def __init__(self,game,filename, layer):
        # carga el txt como una matriz
        self.layer = layer
        self.sprites = list()
        self.game = game
        self.data = list()
        txt = open(filename)
        for linea in txt:
            self.data.append(linea.strip().split('|')[1:-1])
        txt.close()
        self.ancho = (len(self.data[0])) * CUADRADO
        self.alto = (len(self.data)) *CUADRADO
        
        
        #carga los sprites de la capa(lee la matriz)
        cont_y = 0
        for fila in self.data:
            cont_y+=1
            cont_x =0
            for lugar in fila:
                cont_x+=1
                #carga el sprite dependiendo de la id que se lee
                if lugar != '':
                    self.sprites.append(Wall(self.game,lugar,cont_x-1,cont_y-1,layer))
                    

    
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
        self.seguir_jugador = True
        self.moviendose = False #independiente del jugador
    
    def aplicar(self, objeto):
        #no mueve ningun objeto, lo que hace es dibujarlo con un offset
        x,y = self.rect.topleft
        
        # division necesaria para que el jugador quede estatico y el resto se mueva en "perspectiva"
        x = x * objeto._layer/self.layer 
        y = y * objeto._layer/self.layer
        
        return objeto.rect.move(x,y)

    
    def update (self, objeto):
        self.layer = objeto._layer
        if self.seguir_jugador:
            #se deja al jugador al centro y se mueve el escenario en la direccion contraria al mismo
            x = -objeto.rect.centerx + int(ANCHO/2)
            #y = -objeto.rect.centery + int(ALTO/2)
            y = 0
            
            # deja avanzar al objeto pero la camara se detiene en los bordes del mapa
            x = min(0, x)  #izquierda
            #y = min (0,y)  # arriba
            x = max(-(self.ancho - ANCHO), x)  # derecha
            #y = max(-(self.alto - ALTO), y)  # abajo
            self.rect = pg.Rect(x,y,self.ancho,self.alto)
        else:
            if self.moviendose:
                self.mover_camara()
            #------------------------------------------- x,y = self.rect.topleft
            #--------------- se deja estatico el escenario y se mueve el jugador
            #------------------------------------- if self.game.keys[pg.K_LEFT]:
                #-------------------------------------------------------- x -= 5
            #------------------------------------ if self.game.keys[pg.K_RIGHT]:
                #-------------------------------------------------------- x += 5
            #------------------------------------------- self.rect.topleft = x,y
            #--------------------------------------------------- print self.rect


            
        
