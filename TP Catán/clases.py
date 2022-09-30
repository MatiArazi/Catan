import tablero
import juego

class Asentamiento:
    def __init__(self, jugador):
        self.jugador = jugador

class Ciudad:
    pass

class Camino:
    def __init__(self, jugador):
        self.jugador = jugador

class Jugador:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.recurso = 0
    
    def cantidad_de(): 
        dados = juego.tirar_dados()
        print(dados)
