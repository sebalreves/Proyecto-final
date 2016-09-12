from mapa import*

class Data:
    def __init__(self,game):
        #carga todo antes de correr el juego
        self.game = game
        self.mapas = dict()
        self.animaciones = dict()
        self.musica = dict()
        self.load_mapas()
        self.load_frames()
        self.load_music()
        
    def load_mapas(self):
        for carpeta in os.listdir(map_dir):
            self.mapas[carpeta] = Mapa(self.game, archivo.format(map_dir,carpeta))

    def load_frames(self):
        for carpeta in os.listdir(frame_dir):
            self.animaciones[carpeta] = Animacion(archivo.format(frame_dir,carpeta))

    def load_music(self):
        pass


