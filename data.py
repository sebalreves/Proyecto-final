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
    for map1 in os.listdir(map_dir):
        name = map1.replace('.txt', '')
        maps[name]= Mapa(map1)
        
def load_data(): 
    load_capas()
    load_music()
    load_mapas()
    load_frames()
    

load_data()
