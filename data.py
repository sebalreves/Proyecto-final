from mapa import*

class Data:
    def __init__(self,game):
        #carga todo antes de correr el juego
        self.game = game
        self.mapas = dict()
        self.animaciones = dict()
        self.musica = dict()
        self.dialogos = dict()
        
        self.load_dialogos()
        self.load_mapas()
        self.load_animaciones()
        self.load_music()
        
    def load_mapas(self):
        for carpeta in os.listdir(map_dir):
            self.mapas[carpeta] = Mapa(self.game, archivo.format(map_dir,carpeta))

    def load_animaciones(self):
        for carpeta in os.listdir(frame_dir):
            self.animaciones[carpeta] = Animacion(archivo.format(frame_dir,carpeta))
            
    def load_dialogos(self):
        txt = open(dialogo_dir + '/dialogos.txt')
        lineas = txt.readlines()
        txt.close()
        nodo = 0
        for linea in lineas:
            if len(linea)>1:    #no cuenta los espacios
                if linea[0] == linea[1]:
                    if linea[0] == '#': #iniciativa
                        self.dialogos[nodo]['iniciativa'] = linea.strip().split('##')[1]
                        
                    if linea[0] == 'N': #nodo
                        nodo += 1
                        self.dialogos[nodo] = dict()
                        self.dialogos[nodo]['frases'] = list()
                        self.dialogos[nodo]['opciones'] = list()
                        self.dialogos[nodo]['iniciativa'] = list()
            
                    if linea[0] == '|': # frase
                        linea = linea.strip().split('||')[1]
                        self.dialogos[nodo]['frases'].append(linea.strip().split('&'))
                        
                    if linea[0] == '?':#opciones
                        self.dialogos[nodo]['opciones'].append(linea.strip().split('??')[1:]) # id otra conversacion, texto
                    
                    if linea[0] == '__': #final
                        pass
        

    def load_music(self):
        pass


