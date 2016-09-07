import pygame as pg
from opciones import*
from sprites import*


class Mapa():
    def __init__(self, filename):
        self.data = list()
        txt = open(archivo.format(map_dir,filename))
        for linea in txt:
            self.data.append(linea.strip())
            
        txt.close()
        self.ancho = len(self.data[0]) * CUADRADO
        self.alto = len(self.data) * CUADRADO

    def render(self,game):
        #agregar layer desde aca para no hacerlo en los sprite
        cont_y = 0
        for fila in self.data:
            cont_y+=1
            cont_x =0
            for lugar in fila:
                cont_x+=1
                if lugar == '1':
                    Wall(game,cont_x,cont_y)
                    
                    
class Camara():
    def __init__(self,ancho,alto):
        self.rect = pg.Rect(0,0,ancho,alto)
        self.ancho = ancho
        self.alto = alto
    
    def aplicar(self, objeto):
        #mueve al objeto
        return objeto.rect.move(self.rect.topleft)
    
    def update (self, objeto):
        #sigue al objeto, dejandolo en el centro
        x = -objeto.rect.centerx + int(ANCHO/2)
        y = -objeto.rect.centery + int(ALTO/2)
        
        self.rect = pg.Rect(x,y,self.ancho,self.alto)  
