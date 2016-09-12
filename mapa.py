import pygame as pg
from opciones import*
from sprites import*
import random
    
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
        self.ancho = self.layers[self.player_layer].ancho
        self.alto = self.layers[self.player_layer].alto
        
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
    def __init__(self,game,ancho,alto):
        self.rect = pg.Rect(0,0,ancho,alto)
        self.game = game
        self.ancho = ancho
        self.alto = alto
        self.update_camara = True
        self.layer = None
    
    def aplicar(self, objeto):
        #no mueve ningun objeto, lo que hace es dibujarlo con un offset
        x,y = self.rect.topleft
        
        # division necesaria para que el jugador quede estatico y el resto se mueva en "perspectiva"
        x = x * objeto.layer/self.layer
        y = y * objeto.layer/self.layer
        
        return objeto.rect.move(x,y)
    
    def update (self, objeto):
        self.layer = objeto.layer
        if self.game.seguir_jugador:
            #se deja al jugador al centro y se mueve el escenario en la direccion contraria al mismo
            
            x = -objeto.rect.centerx + int(ANCHO/2)
            y = -objeto.rect.centery + int(ALTO/2)
            
            self.rect = pg.Rect(x,y,self.ancho,self.alto)
        else:
            #se deja estatico el escenario y se mueve el jugador
            pass
            
        