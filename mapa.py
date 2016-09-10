import pygame as pg
from opciones import*
from sprites import*


            
class Mapa():
    def __init__(self, game, carpeta):
        #coloca al jugador dependiendo del mapa
        self.player_layer = 2
        if carpeta == "direccion/mapa1":
            self.player_layer = 2
            
        #Crea las instancias de las capas
        self.game = game
        self.layers = dict()
        contador = 1
        for txt in os.listdir(carpeta):
            self.layers[contador] = Layer(self.game, archivo.format(carpeta,txt), contador)
            contador +=1
            
        #dimensiones de la capa donde esta el jugador, necesarias para la camara
        self.ancho = self.layers[self.player_layer].ancho
        self.alto = self.layers[self.player_layer].alto
        
    def render(self):
        #cambia al jugador de layer
        self.game.jugador.layer = self.player_layer
        
        #coloca todo en la pantalla
        for layer in self.layers.values():
            layer.render()
            
class Layer:
    def __init__(self,game,filename, layer):
        # lee el txt corresponiente
        self.layer = layer
        self.game = game
        self.data = list()
        txt = open(filename)
        for linea in txt:
            self.data.append(linea.strip())
        txt.close()
        self.ancho = len(self.data[0]) * CUADRADO
        self.alto = len(self.data) *CUADRADO
    def render(self):
        #coloca todo en su lugar dependiendo del id 
        cont_y = 0
        for fila in self.data:
            cont_y+=1
            cont_x =0
            for lugar in fila:
                cont_x+=1
                if lugar == '1':
                    Wall(self.game,cont_x,cont_y,self.layer)
                                
                    
class Camara():
    def __init__(self,ancho,alto):
        self.rect = pg.Rect(0,0,ancho,alto)
        self.ancho = ancho
        self.alto = alto
        self.layer = None
    
    def aplicar(self, objeto):
        #mueve un objeto ubicado en el mapa
        x,y = self.rect.topleft
        # division necesaria para que el jugador quede estatico y el resto se mueva en "perspectiva"
        x = x * objeto.layer/self.layer
        y = objeto.layer/self.layer
        return objeto.rect.move(x,y)
    
    def update (self, objeto):
        self.layer = objeto.layer
        #sigue al objeto, dejandolo en el centro
        x = -objeto.rect.centerx + int(ANCHO/2)
        y = -objeto.rect.centery + int(ALTO/2)
        
        self.rect = pg.Rect(x,y,self.ancho,self.alto)  
