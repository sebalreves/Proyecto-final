from mapa import*

class Data:
    def __init__(self,game):
        self.game = game
        self.mapas = dict()
        self.frames = dict()
        self.musica = dict()
        self.load_mapas()
        self.load_frames()
        self.load_music()
        
    def load_mapas(self):
        for carpeta in os.listdir(map_dir):
            self.mapas[carpeta] = Mapa(self.game, archivo.format(map_dir,carpeta))

    def load_frames(self):
        pass

    def load_music(self):
        pass


