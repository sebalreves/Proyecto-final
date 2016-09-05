class Dialogo():
    def __init__(self, id_dialogo,game):
        self.id = id_dialogo
        self.game = game
        self.game.dialogando = True

    def comenzar(self):
        if self.id == 1:
            .
            .
            .
        elif self.id == n:
            #se colocan los nodos y respuestas y condiciones de cada uno
            #de un dialogo en especiico
            #no debe detener el juego
            

    def eperar(self):
        #cuando se suelte espacio al final, avanza de frase

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
        
        
        

