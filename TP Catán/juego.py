import random
ORDEN_ESPECIAL = False

def tirar_dados():
    pass

def rellenar_tablero(tablero):
    recurso = ["Ladrillo"] * 3 + ["Piedra"] * 3 + ["Trigo"] * 4 + ["Lana"] * 4 + ["Madera"] * 4
    numeross = []
    numeross.append(2)
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
        tablero.colocar_recurso_y_numero(ficha,recurso[rand], numeross[rand])
        ficha+=1
        if ficha == 10:
            ficha+=1
        recurso.pop(rand)
        numeross.pop(rand)


def jugar_catan(jugadores,tablero):
    pass