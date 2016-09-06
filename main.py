import sys

from opciones import *
from sprites import*
from mapa import*



class Game():
    def __init__(self):
        pg.init()
        self.pantalla = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption('hola')
        self.clock = pg.time.Clock()
        self.new()
        self.run()
        
    
        
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        import data
        self.jugador = Jugador(self)
        self.map = data.maps['map']
        self.map.render(self)
        self.camara = Camara(self.map.ancho,self.map.alto)
        
        
        
    def run(self):
        while True:
            self.dt = self.clock.tick(FPS) /1000.0
            self.events()
            self.update()
            self.draw()
            
                    
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
    
    def update(self):
        pg.display.set_caption(str(round(self.clock.get_fps())))
        self.all_sprites.update()
        self.camara.update(self.jugador)
        pg.display.update()
    
    def draw(self):
        self.pantalla.fill(BLANCO)
        for x1 in range(0,ANCHO,CUADRADO):
            pg.draw.line(self.pantalla,(20,20,20), (x1,0),(x1,ALTO))
        for y1 in range(0,ALTO,CUADRADO):
            pg.draw.line(self.pantalla,(20,20,20), (0,y1), (ANCHO, y1))


        for sprite in self.all_sprites:
            self.pantalla.blit(sprite.image, self.camara.aplicar(sprite))
            
        #self.all_sprites.draw(self.pantalla)
        pg.display.flip()

    def load_map(self):
        pass
        
        
g = Game()
