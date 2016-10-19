from opciones import*

class Dialogo():
    #dialogo entre el jugador y otra persona
    def __init__(self,game):
        self.game = game
        self.game.dialogo = 1
        #elementos para dibujar en pantalla
        self.x = 30
        self.y = 10

        self.iniciando_dialogo = False 
         
        #elecciones
        self.lugar_eleciones = [(30,40),(400,40),(30,70),(400,70)]
        
        #marcador
        self.marcadores = [(700,110),(720,110),(740,110)]

        #texto
        self.acelerar = 1
        
    def agregar_letras(self):
        now = pg.time.get_ticks()
        if now - self.last_update > RAPIDEZ_DIALOGO/self.acelerar:
            self.last_update = now
            self.contador_letras += 1
            if self.contador_letras == len(self.frase_actual):
                self.letras_actuales = self.frase_actual
                self.agregando = False
            else:
                if self.frase_actual[self.contador_letras-1] != '-':
                    self.letras_actuales = self.frase_actual[:-len(self.frase_actual) + self.contador_letras]
                    
                    
    def update(self):  #pasar el id en el update, id cero correspondera a no escribir nada
        
        if self.game.dialogo: 
            if not self.iniciando_dialogo:
                #init de cada dialogo, por asi decirlo
                self.iniciando_dialogo = True
                self.game.dialogando = True
                self.iniciativa = self.game.data.dialogos[self.game.dialogo]['iniciativa']
                self.conversacion = self.game.data.dialogos[self.game.dialogo]['frases']
                self.elecciones = self.game.data.dialogos[self.game.dialogo]['opciones']
                self.agregando = True
                self.eligiendo = False
                self.marcador = 0
                self.last_update_marcador = 0  #contador de tiempo
                self.last_update = 0           #contador de tiempo
                self.dialogo = 0            # cambia cada vez que habla el otro personaje
                self.contador_frases = 0    #cambia cada vez que un personaje habla mas de una vez seguida
                self.contador_letras = 0    # cambia cada vez que se agrega una letra
                self.frase_actual = self.conversacion[self.dialogo][self.contador_frases]
                self.letras_actuales = str()

                
            if not self.eligiendo:
                #acelerar tipeado en pantalla
                if self.game.mouse.botones[0]:
                    self.acelerar = 3
                else:
                    self.acelerar = 1
                #agregar letras a las frases
                if self.agregando:
                    self.agregar_letras()
                    
                #dibujar el texto
                numero_linea = 1
                for numero_linea,linea in enumerate(self.letras_actuales.split(' - ')):
                    pos = (self.x, self.y + ((numero_linea)*30))
                    self.escribir(linea, 'chica', pos)

                    
                #espera entre un dialogo y otro    
                if not self.agregando:
                    #pasar a la siguiente frase
                    if self.game.mouse.boton_up[0]:
                        self.avanzar_frase()
                    #dibujar marcador "esperando"
                    now = pg.time.get_ticks()
                    if now - self.last_update > RAPIDEZ_MARCADORES:
                        self.last_update = now
                        self.marcador = (self.marcador + 1)% 3
                    pg.draw.circle(self.game.pantalla, MORADO, self.marcadores[self.marcador],6,3)
                    
            else:
                # se esta eligiendo entre las opciones
                self.dibujar_elecciones()

                    
        else:
            #no se esta dialogando, pues el nodo es 0
            pass

    def escribir(self,texto,tamano, pos):
        if tamano == 'chica':
            superficie = fuente_chica.render(texto, True, NEGRO)
        elif tamano == 'media':
            superficie = fuente_media.render(texto, True, NEGRO)
        rect = superficie.get_rect()
        
        rect.topleft = pos
        self.game.pantalla.blit(superficie, rect)
        return rect
        
    def avanzar_frase(self):
        if self.contador_frases < len(self.conversacion[self.dialogo])-1:
            #pasar otra frase dle mismo personaje
            self.contador_frases +=1
        elif self.dialogo < len(self.conversacion)-1:
            #pasar a otro personaje
            self.dialogo += 1
            self.contador_frases = 0
        else:
            if len(self.elecciones) > 0:
                #elegir entre las opciones que tiene la conversacion
                self.eligiendo = True
            else:
                #terminar la conversacion
                self.game.dialogo = 0
            #self.game.dialogando = False

        self.agregando = True
        self.last_update_marcador = 0
        self.marcador = 0
        self.last_update = 0
        self.contador_letras = 0
        self.letras_actuales = str()
        self.frase_actual = self.conversacion[self.dialogo][self.contador_frases]
        
    def dibujar_elecciones(self):
        self.sobre_boton = False
        self.escribir(self.frase_actual, 'chica', (self.x,self.y))
        for cont, eleccion in enumerate(self.elecciones):
            pos = self.lugar_eleciones[cont]
            rect = self.escribir(eleccion[1], 'chica', pos)
            
            if rect.collidepoint(self.game.mouse.pos):
                if not self.sobre_boton: 
                    self.sobre_boton = True
                    inicio, final = ((rect.bottomleft[0],rect.bottomleft[1]-6), 
                                    (rect.bottomright[0],rect.bottomright[1]-6))
                    if self.game.mouse.boton_up[0]:
                        self.game.dialogo = int(eleccion[0])
                        self.iniciando_dialogo = False
                        
                      
                pg.draw.line(self.game.pantalla,NEGRO,inicio,final)
                