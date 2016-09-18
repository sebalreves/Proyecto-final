import pygame, random
pygame.init()

blanco = (255,255,255)
negro= (0,0,0)
gris = (200,200,200)

ancho_p = 1000
alto_p = 560
pantalla = pygame.display.set_mode([ancho_p, alto_p])
pantalla_otro = pygame.Rect(0,0,ancho_p,95)
pantalla_jugador = pygame.Rect(0,465, ancho_p, 95)
dialogo_otro = (200, 0)
dialogo_jugador = (200, 465) 


reloj = pygame.time.Clock()
fps = 24
fpst = 1

fuente_chica = pygame.font.Font('fuente.ttf', 22)
fuente_media = pygame.font.Font('fuente.ttf', 25)
fuente_grande = pygame.font.Font('fuente.ttf', 30)


arbol = pygame.image.load('imagenes/fondo/arbol.png')
gota = pygame.image.load('imagenes/lluvia/gota.png').convert()
gota2 = pygame.image.load('imagenes/lluvia/gota2.png').convert()

ray = pygame.image.load('ray.png')
ray = pygame.transform.scale(ray, (200,200))
pygame.display.update()
z = 0
continuar_dialogo_down0 = pygame.image.load('imagenes/dialogo/dialogo_siguiente0.png')
continuar_dialogo_down25 = pygame.image.load('imagenes/dialogo/dialogo_siguiente25.png')
continuar_dialogo_down50 = pygame.image.load('imagenes/dialogo/dialogo_siguiente50.png')
continuar_dialogo_down75 = pygame.image.load('imagenes/dialogo/dialogo_siguiente75.png')
continuar_dialogo_down100 = pygame.image.load('imagenes/dialogo/dialogo_siguiente100.png')

continuar_dialogo_down = [continuar_dialogo_down0,
                        continuar_dialogo_down25,
                        continuar_dialogo_down50, 
                        continuar_dialogo_down75, 
                        continuar_dialogo_down100]

continuar_dialogo_up0 = pygame.transform.flip(continuar_dialogo_down0,False,True)
continuar_dialogo_up25 = pygame.transform.flip(continuar_dialogo_down25,False,True)
continuar_dialogo_up50 = pygame.transform.flip(continuar_dialogo_down50,False,True)
continuar_dialogo_up75 = pygame.transform.flip(continuar_dialogo_down75,False,True)
continuar_dialogo_up100 = pygame.transform.flip(continuar_dialogo_down100,False,True)

continuar_dialogo_up = [continuar_dialogo_up0, 
                        continuar_dialogo_up25,
                        continuar_dialogo_up50,
                        continuar_dialogo_up75, 
                        continuar_dialogo_up100]

fin_dialogo_down0 = pygame.image.load('imagenes/dialogo/fin0.png')
fin_dialogo_down25 = pygame.image.load('imagenes/dialogo/fin25.png')
fin_dialogo_down50 = pygame.image.load('imagenes/dialogo/fin50.png')
fin_dialogo_down75 = pygame.image.load('imagenes/dialogo/fin75.png')
fin_dialogo_down100 = pygame.image.load('imagenes/dialogo/fin100.png')

fin_dialogo_down = [fin_dialogo_down0,
                    fin_dialogo_down25,
                    fin_dialogo_down50, 
                    fin_dialogo_down75, 
                    fin_dialogo_down100]

fin_dialogo_up0 = pygame.transform.flip(fin_dialogo_down0,False,True)
fin_dialogo_up25 = pygame.transform.flip(fin_dialogo_down25,False,True)
fin_dialogo_up50 = pygame.transform.flip(fin_dialogo_down50,False,True)
fin_dialogo_up75 = pygame.transform.flip(fin_dialogo_down75,False,True)
fin_dialogo_up100 = pygame.transform.flip(fin_dialogo_down100,False,True)

fin_dialogo_up = [fin_dialogo_up0,
                    fin_dialogo_up25,
                    fin_dialogo_up50, 
                    fin_dialogo_up75, 
                    fin_dialogo_up100]

def obtener_dialogos(archivo= None):
    archivo = open(archivo)
    lineas = list()
    for linea in archivo:
        lineas = linea.strip().split('||')
    return lineas

def objetos_mensaje (texto, color, tamano):
    if tamano == 'chica':
        textSurface = fuente_chica.render(texto, True, color)
    elif tamano == 'media':
        textSurface = fuente_media.render(texto, True, color)
    elif tamano == 'grande':
        textSurface = fuente_grande.render(texto, True, color)
        
    return textSurface, textSurface.get_rect()

def pausar(pausado):
    if pausado:
        pausado = False
    else:
        pausado = True
    return pausado

def  mensaje_pantalla(texto, color=blanco, x=0, y=0, tamano = 'chica'):
    
    frases = texto.split('-')
    ant_x = x
    for frase in frases:
        superficie, rectangulo = objetos_mensaje(frase, color, tamano)
        rectangulo[0], rectangulo[1] = x, y
        pantalla.blit(superficie, rectangulo)
        y+=27
        x= ant_x

def generar_rect():
        x = random.randrange(1000)- random.randrange(1000)+random.randrange(1000)
        y = random.randrange(-100,100) - random.randrange(-100,100) + random.randrange(-100,100)
        ancho = random.randrange(15,30)
        alto= random.randrange (14,30)

        return pygame.Rect(x, y, ancho, alto)

        

class lluvia(pygame.sprite.Sprite):
    def __init__(self, cantidad, cantidad1):
        self.contador = 0
        self.tope = 20
        self.cantidad = cantidad
        self.lista = []
        self.cantidad_inicial= 1
        self.lloviendo = False
        for aux in range(self.cantidad_inicial):
            self.lista.append(generar_rect())
        self.contador1 = 0
        self.tope1 = 15
        self.cantidad1 = cantidad1
        self.lista1 = []
        self.cantidad_inicial1= 1
        self.lloviendo1 = False
        for aux in range(self.cantidad_inicial1):
            self.lista1.append(generar_rect())
            
    def cambiar_condicion(self):
        if not self.lloviendo:
            self.lloviendo = True
        else :
            self.lloviendo = False

    def regenerar_gota(self):
        self.contador +=1
        for aux in range(len(self.lista)):
            if self.lista[aux].top > 500:
                self.lista[aux] = generar_rect()
                if self.cantidad_inicial < self.cantidad:
                    if self.contador >= self.tope:
                        self.lista.append(generar_rect())
                        self.cantidad_inicial += 1
                        self.contador = 0

        self.contador1 +=1
        for aux in range(len(self.lista1)):
            if self.lista1[aux].top > 500:
                self.lista1[aux] = generar_rect()
                if self.cantidad_inicial1 < self.cantidad1:
                    if self.contador1 >= self.tope1:
                        self.lista1.append(generar_rect())
                        self.cantidad_inicial1 += 1
                        self.contador1 = 0
                
    def mover(self):
        for rectangulo in self.lista:
            rectangulo.move_ip(0,45)
        for rectangulo in self.lista1:
            rectangulo.move_ip(0,30)

    def render(self):
        for rectangulo in self.lista:
            pantalla.blit(gota, (rectangulo[0], rectangulo[1]))
        for rectangulo in self.lista1:
            pantalla.blit(gota2, (rectangulo[0], rectangulo[1]))
            

        
class personaje(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.Surface((20,20))
        self.image.fill(negro)
        self.rect = self.image.get_rect()
        self.rect.x = pantalla.get_rect().center[0]
        self.rect.y = 200
        self.mov = 0
        self.izquierda, self.derecha= False, False

    def update(self):
        
##        for event in pygame.event.get():         #quitar el for usar pygame.key.get_pressed()[K_UP] != 0
##            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_RIGHT:
##                    self.mover('derecha')
##                if event.key == pygame.K_LEFT:
##                    self.mover('izquierda')
##            if event.type == pygame.KEYUP:
##                if event.key == pygame.K_RIGHT:
##                    self.detenerse('derecha')
##                if event.key == pygame.K_LEFT:
##                    self.detenerse('izquierda')
                    
        self.rect.x += self.mov
        
    def mover(self, direccion):
        if direccion =='derecha':
            if not self.izquierda:
                self.mov = 20
            self.derecha = True
        else:
            if not self.derecha:
                self.mov = -20
            self.izquierda = True
        
    def detenerse(self, direccion):
        if direccion == 'derecha':
            self.derecha = False
            if self.izquierda:
                self.mov = -20
            else:
                self.mov = 0
        else:
            self.izquierda = False
            if self.derecha:
                self.mov = 20
            else:
                self.mov = 0

             

    
class dialogo(pygame.sprite.Sprite):
    def __init__(self, archivo, iniciativa='jugador'):
        self.frases = obtener_dialogos(archivo)
        self.repetir_mismo_personaje=  False
        self.escribiendo = False
        self.en_espera= False
        self.termino= False
        self.contador_letra=0
        self.contador_frase = 0
        self.contador_fps_ima = 0
        self.contador_ima = 0
        self.tiempo_intervalo = 10
        self.tiempo_actual=0
        self.letras_totales= str()
        self.frase_actual = list()
        self.sumando = True
        if iniciativa == 'jugador':
            self.coordenadas = dialogo_jugador
            self.coordenada_animacion = (0,345)
            self.imagen_continuar = continuar_dialogo_down0
            
        else:
            self.coordenadas = dialogo_otro
            self.coordenada_animacion = (0,95)
            self.imagen_continuar = continuar_dialogo_up0
                  
    def disminuir_velocidad(self):
        self.tiempo_intervalo = fpst
        
    def cambiar_condicion_o_aumentar_velocidad(self):
        if self.en_espera:
            self.en_espera = False
            self.contador_letra = 0
            self.contador_frase +=1
            self.cambiar_lugar_dialogos()
            self.letras_totales = str()
        if self.escribiendo:
            self.tiempo_intervalo = fpst -1
            if self.termino:
                self.escribiendo = False
        elif not self.termino:
            self.escribiendo = True
            
    def cambiar_lugar_dialogos(self):
        if not self.repetir_mismo_personaje:
            if self.coordenadas == dialogo_jugador:
                self.coordenadas = dialogo_otro
            else:
                self.coordenadas = dialogo_jugador

    def animar_espera(self):
        if self.contador_fps_ima > 2:
            self.contador_fps_ima = 0
            if self.coordenadas == dialogo_jugador:
                self.coordenada_animacion = (0,345)
                if self.sumando:
                    if self.contador_ima < 4:
                        self.contador_ima +=1
                    else:
                        self.contador_ima -=1
                        self.sumando = False  
                else:
                    if self.contador_ima > 0:
                        self.contador_ima -=1
                    else:
                        self.contador_ima +=1
                        self.sumando = True
                self.imagen_continuar = continuar_dialogo_down[self.contador_ima]
            else:
                self.coordenada_animacion = (0,95)
                if self.sumando:
                    if self.contador_ima < 4:
                        self.contador_ima +=1
                    else:
                        self.contador_ima -=1
                        self.sumando = False         
                else:
                    if self.contador_ima > 0:
                        self.contador_ima -=1
                    else:
                        self.contador_ima +=1
                        self.sumando = True
                self.imagen_continuar = continuar_dialogo_up[self.contador_ima]
        else:
            self.contador_fps_ima +=1
        pantalla.blit(self.imagen_continuar, self.coordenada_animacion)


    def animar_final(self):
        if self.contador_fps_ima > 2:
            self.contador_fps_ima = 0
            if self.contador_ima < 4:
                self.contador_ima +=1                
            if self.coordenadas == dialogo_jugador:
                self.imagen_continuar = fin_dialogo_down[self.contador_ima]
                self.coordenada_animacion = (0,345)
            else:
                self.imagen_continuar = fin_dialogo_up[self.contador_ima]
                self.coordenada_animacion= (0,95)

        pantalla.blit(self.imagen_continuar, self.coordenada_animacion)
                         
    def update(self):
        if not self.termino:
            if not self.en_espera:
                if self.tiempo_actual >= self.tiempo_intervalo:
                    self.tiempo_actual =0
                    self.escribir()
                    if self.contador_letra < len(self.frase_actual)-1:
                        self.contador_letra +=1
                    elif self.contador_frase < len(self.frases)-1 :
                        self.en_espera= True
                        self.contador_ima = 0
                        self.contador_fps_ima= 2
                    else:
                        self.termino= True
                else:
                    self.tiempo_actual += 1
            else:
                self.animar_espera()
        else:
            self.animar_final()
            
        self.render()

        
    def render(self):
        mensaje_pantalla(self.letras_totales, blanco, self.coordenadas[0], self.coordenadas[1])

    def escribir(self):
        self.frase_actual = self.frases[self.contador_frase]
        self.letra_actual = self.frase_actual[self.contador_letra]
        if '&' in self.frase_actual:
            self.frase_actual = self.frase_actual.replace('&', '')
            self.repetir_mismo_personaje = True
        else:
            self.repetir_mismo_personaje = False
        self.letras_totales += self.letra_actual
        
        



#____________________________________________________________________________#
pygame.init()
pausado = False


sprites = pygame.sprite.Group()

llover = lluvia(15, 25)
texto1=dialogo('dialogos/prueba.txt')
Personaje = personaje()
sprites.add(Personaje)



pantalla.fill(blanco)
pygame.display.update()


while True :
    #pantalla.fill(blanco)
    x,y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if pygame.mouse.get_pressed()[0]:
        z= 1
    else:
        z = 0
    if z == 1:
        pantalla.blit(ray,(x-100,y-100))
        pygame.display.update()



            
        if event.type == pygame.KEYDOWN:
            
            if event.key== pygame.K_SPACE:
                texto1.cambiar_condicion_o_aumentar_velocidad()
                llover.cambiar_condicion()
                
            if event.key == pygame.K_p:
                pausado = pausar(pausado)

                
        if event.type == pygame.KEYUP:

            if event.key== pygame.K_SPACE:
                texto1.disminuir_velocidad()
                
    if pausado:
        mostrar_pausa= pygame.image.load('imagenes/pantalla_actual.jpeg')
        pantalla.blit(mostrar_pausa, (0,0))
        
    else:
        pygame.image.save(pantalla, 'imagenes/pantalla_actual.jpeg')


##        sprites.update()
##        pantalla.fill(blanco)
##        if llover.lloviendo:
##            llover.mover()
##            llover.render()
##            llover.regenerar_gota()
##        pantalla.blit(arbol, (50,273))
##        pantalla.fill(negro, pantalla_otro)
##        pantalla.fill(negro, pantalla_jugador)
##        sprites.draw(pantalla)
    

             
        if texto1.escribiendo:
            texto1.update()

        pygame.display.update()
    reloj.tick(fps)
    
pygame.quit()  

