import random
ORDEN_ESPECIAL = False

def tirar_dados():
    dado1 = random.randint(1,6)
    dado2 = random.randint(1,6)
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
    LugarAsentamioento = input ("Coloque primer asentamiento: ")
    PrimerCamino = input ("Coloque el camino: ")

    print(LugarAsentamioento, PrimerCamino)

jugar_catan("A", "A")