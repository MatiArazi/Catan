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
        self.recurso = {
            "Ladrillo" :0,
            "Piedra": 0,
            "Trigo": 0,
            "Lana": 0,
            "Madera": 0
            }
    
    def cantidad_de(recursos): 
        print(recursos)
