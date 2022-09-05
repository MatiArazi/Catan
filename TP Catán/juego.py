ORDEN_ESPECIAL = False

def tirar_dados():
    pass

def rellenar_tablero(tablero):
    recurso = ["Ladrillo"] * 3 + ["Piedra"] * 3 + ["Trigo"] * 4 + ["Lane"] * 4 + ["Madera"] * 4
    numeross.push(2)
    for i in range(3,12):
        if i == 7:
            pass
        numeross.push(i)
        numeross.push(i)
    numeross.push(12)

    for i in range(numeross.size()):
        rand = randint(0,numeross.size())
        colocar_recurso_y_numero(numeross[rand], recurso[rand])
        recurso.delete(rand)
        numero.delete(rand)


def jugar_catan(jugadores,tablero):
    pass