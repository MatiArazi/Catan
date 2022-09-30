from asyncio import constants
from gettext import install
from importlib import import_module
import random
from subprocess import CREATE_NEW_CONSOLE
from urllib.error import ContentTooShortError
import tablero 
import clases

ORDEN_ESPECIAL = False

def tirar_dados():
    dado1 = random.randint(1,6)
    dado2 = random.randint(1,6)
    print("Tirando dados")
    return dado1 + dado2

def rellenar_tablero(tablero):
    recurso = ["Ladrillo"] * 3 + ["Piedra"] * 3 + ["Trigo"] * 4 + ["Lana"] * 4 + ["Madera"] * 4
    numeross = []
    numeross.append(2)
    lugares_invalidos = set()
    for i in range(3,12):
        if i == 7:
            continue
        numeross.append(i)
        numeross.append(i)
    numeross.append(12)
    ficha = 1
    for i in range(len(numeross)):
        rand = random.randint(0,len(numeross)-1)
        print(rand)
        print(numeross)
        print(recurso)
        if ficha in lugares_invalidos:
            while numeross[rand] == 6 or numeross[rand] == 8:
                rand = random.randint(0,len(numeross)-1)
        else:
            if numeross[rand] == 6 or numeross[rand] == 8:
                lugares_invalidos.add(ficha)
                lugares_invalidos.add(ficha+1)
                lugares_invalidos.add(ficha-1)
                lugares_invalidos.add(ficha-4)
                lugares_invalidos.add(ficha+4)
        tablero.colocar_recurso_y_numero(ficha,recurso[rand], numeross[rand])
        ficha+=1
        if ficha == 10:
            ficha+=1
        recurso.pop(rand)
        numeross.pop(rand)


def jugar_catan(jugadores,tablero):
    for i in jugadores:  
        PrimerAsentamiento = input("Coloque primer ASENTAMIENTO: ").split(" ")
        tablero.colocar_asentamiento(int(PrimerAsentamiento[0]), int(PrimerAsentamiento[1]), clases.Asentamiento(i))
        PrimerCamino = input("Coloque primer CAMINO"). split(" ")
        tablero.colocar_camino(int(PrimerCamino[0]),int(PrimerCamino[1]),clases.Camino(i))

        SegundoAsentamineto = input ("Coloque segundo ASENTAMIENTO: ").split(" ")
        tablero.colocar_asentamiento(int(SegundoAsentamineto[0]), int(SegundoAsentamineto[1]), clases.Asentamiento(i))
        SegundoCamino = input ("Coloque segundo CAMINO: ").split(" ")
        tablero.colocar_camino(int(SegundoCamino[0]),int(SegundoCamino[1]),clases.Camino(i))

