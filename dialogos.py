from opciones import*

class Dialogo():
    def __init__(self,game,id):
        #dialogo entre el jugador y otra persona
        self.game = game
        
        #hacer esto una vez se tenga el id, no en el init
        self.id = id
        self.game.dialogando = True
        self.iniciativa = self.game.data.dialogos[id]['iniciativa']
        self.conversacion = self.game.data.dialogos[id]['frases']
        self.elecciones = self.game.data.dialogos[id]['opciones']
        
        #elementos para dibujar en pantalla
        self.x = 30
        self.y = 10
        #condiciones
        self.agregando = True
        self.eligiendo = False
        #elecciones
        self.lugar_eleciones = [(30,40),(400,40),(30,70),(400,70)]
        #marcador
        self.last_update_marcador = 0
        self.marcadores = [(700,110),(720,110),(740,110)]
        self.marcador = 0
        #texto
        self.last_update = 0
        self.acelerar = 1
        #contadores
        self.dialogo = 0            # cambia cada vez que habla el otro personaje
        self.contador_frases = 0    #cambia cada vez que un personaje habla mas de una vez seguida
        self.contador_letras = 0    # cambia cada vez que se agrega una letra


        self.frase_actual = self.conversacion[self.dialogo][self.contador_frases]
        self.letras_actuales = str()  #letras que se estan dibujando
        
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
        
        if self.game.dialogando:
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
            #no se esta dialogando
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
            #Terminar dialogo o colocar opciones
            self.eligiendo = True
            #self.game.dialogando = False

        self.agregando = True
        self.last_update_marcador = 0
        self.marcador = 0
        self.last_update = 0
        self.contador_letras = 0
        self.letras_actuales = str()
        self.frase_actual = self.conversacion[self.dialogo][self.contador_frases]
        
    def dibujar_elecciones(self):
        self.escribir(self.frase_actual, 'chica', (self.x,self.y))
        for cont, eleccion in enumerate(self.elecciones):
            pos = self.lugar_eleciones[cont]
            rect = self.escribir(eleccion[2], 'chica', pos)
            
            if rect.collidepoint(self.game.mouse.pos):    #falta hacer colisionar solo a un rect, no 2 al mismo tiempo
                inicio, final = ((rect.bottomleft[0],rect.bottomleft[1]-6), 
                                (rect.bottomright[0],rect.bottomright[1]-6))
                pg.draw.line(self.game.pantalla,NEGRO,inicio,final)
            
        


    
class Texto():
    def __init__(self,x,y,tipo):
        pass
    
    
    
    
    
"""class Dialogo():
    def __init__(self, id_dialogo,game):
        self.id = id_dialogo
        self.game = game
        self.game.dialogando = True

    def comenzar(self):
        if self.id == 1:
            pass
        elif self.id == n:
            #se colocan los nodos y respuestas y condiciones de cada uno
            #de un dialogo en especiico
            #no debe detener el juego
            pass
            

    def eperar(self):
        #cuando se suelte espacio al final, avanza de frase
        pass

    def aclerar(self):
        #al presionar espacio, avanza mas rapido lo que dic el otro

    def escribir_respuesta(self):
        pass

class Opcion():
    def __init__(self,frase,x,y,game):
        self.game = game
        self.rect = pg.Rect(self.frase.get_ancho(),20,x,y)
        self.game.opciones_actuales.append((frase,self.rect))
        
    def escrbir(self):
        escribir(self.game.patalla,texto)

    def resaltar(self):
        pass

    def elgir(self):
        "remover todos lo otros dialogos, menos el elegido, desvanciendolos"

    def remover(self):
        self.game.remove(opcion.index)
        """
        
        

