from mapa import*


def load_frames():
    pass

def load_capas():
    pass

def load_music():
    pass

def load_mapas():
    global maps
    maps = dict()
    for mapas in os.listdir(map_dir):
        name = mapas.replace('.txt', '')
        maps[name]= Mapa(mapas)
        
def load_data(): 
    load_capas()
    load_music()
    load_mapas()
    load_frames()
    

load_data()
