import random
import tablero
import clases

ORDEN_ESPECIAL = True

def tirar_dados():
    dado1 = random.randint(1,6)
    dado2 = random.randint(1,6)
    print(dado1+dado2)
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
        # if ficha in lugares_invalidos:
        #     while numeross[rand] == 6 or numeross[rand] == 8:
        #         rand = random.randint(0,len(numeross)-1)
        # else:
        #     if numeross[rand] == 6 or numeross[rand] == 8:
        #         lugares_invalidos.add(ficha)
        #         lugares_invalidos.add(ficha+1)
        #         lugares_invalidos.add(ficha-1)
        #         lugares_invalidos.add(ficha-4)
        #         lugares_invalidos.add(ficha+4)
        tablero.colocar_recurso_y_numero(ficha,recurso[rand], numeross[rand])
        ficha+=1
        if ficha == 10:
            ficha+=1
        recurso.pop(rand)
        numeross.pop(rand)


def jugar_catan(jugadores,tablero):

    termino = False

    for i in jugadores:  
            PrimerAsentamiento = input("Coloque primer ASENTAMIENTO: ").split(" ")
            tablero.colocar_asentamiento(int(PrimerAsentamiento[0]), int(PrimerAsentamiento[1]), clases.Asentamiento(i))
            PrimerCamino = input("Coloque primer CAMINO"). split(" ")
            tablero.colocar_camino(int(PrimerCamino[0]),int(PrimerCamino[1]),clases.Camino(i))
        # Recorre todos los jugadores pide primer Asentamiento y primer Camino 

    for i in reversed(jugadores):
        SegundoAsentamineto = input ("Coloque segundo ASENTAMIENTO: ").split(" ")
        tablero.colocar_asentamiento(int(SegundoAsentamineto[0]), int(SegundoAsentamineto[1]), clases.Asentamiento(i))
        SegundoCamino = input ("Coloque segundo CAMINO: ").split(" ")
        tablero.colocar_camino(int(SegundoCamino[0]),int(SegundoCamino[1]),clases.Camino(i))

    n_turno = 0

    while not termino:
        jugador = jugadores[n_turno % len(jugadores)]
         # Durante Juego 
        dados = []
        turno = True
        
        dados= tirar_dados()    
        for ficha in range (1,20):
                if(dados == tablero.obtener_numero_de_ficha(ficha)):
                    recurso_tipo = tablero.obtener_recurso_de_ficha(ficha)
                    for asentamiento in tablero.asentamientos_por_ficha(ficha):
                        asentamiento.jugador.guardar_recursos(recurso_tipo)

        # Aca empiezan los "turnos"
        while turno and not termino:
            inputUsuario = input("Ingrese un comando: ")
            inputUsuario = inputUsuario.split(" ")

            if(inputUsuario[0] == "fin"):
                termino = True
                break

            if(inputUsuario[0] == "pas"):
                turno = False
                break

            if(inputUsuario[0] == "ase"):
                if(jugador.cantidad_de("Ladrillo") >= 1 and jugador.cantidad_de("Madera") >= 1 and jugador.cantidad_de("Lana") >= 1 and jugador.cantidad_de("Trigo") >= 1):
                    tablero.colocar_asentamiento(int(inputUsuario[1]), int(inputUsuario[2]), clases.Asentamiento(i))
                    jugador.gastar_recursos(recurso="Ladrillo")
                    jugador.gastar_recursos(recurso="Madera")
                    jugador.gastar_recursos(recurso="Lana")
                    jugador.gastar_recursos(recurso="Trigo")

            if(inputUsuario[0] == "cam"):
                if(jugador.cantidad_de("Ladrillo") >= 1 and jugador.cantidad_de("Madera") >= 1):
                    tablero.colocar_camino(int(inputUsuario[1]), int(inputUsuario[2]), clases.Asentamiento(i))
                    jugador.gastar_recursos(recurso="Ladrillo")
                    jugador.gastar_recursos(recurso="Madera")


        n_turno +=1
