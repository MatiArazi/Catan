import pytest
from tablero import TableroCatan
from juego import jugar_catan, rellenar_tablero,ORDEN_ESPECIAL
from clases import Asentamiento, Camino, Jugador, Ciudad

@pytest.fixture
def tablero_lleno() -> TableroCatan:
    tablero = TableroCatan()
    rellenar_tablero(tablero)
    return tablero

@pytest.fixture
def recursos(tablero_lleno : TableroCatan):
    rec = {}
    for ficha in range(1,20):
        recurso = tablero_lleno.obtener_ficha(ficha).recurso
        if recurso in rec.keys():
            rec[recurso] += 1
        else:
            rec[recurso] = 1
    return rec

@pytest.fixture
def numeros(tablero_lleno : TableroCatan):
    num = []
    for ficha in range(1,20):
        num.append(tablero_lleno.obtener_ficha(ficha).numero)
    return num

class TestLlenado:
    def test_recursos(self,recursos):
        for recurso,numero_esperado in [('Madera',4),('Lana',4),('Trigo',4),('Piedra',3),('Ladrillo',3)]:
            assert recurso in recursos.keys(), f"No hay {recurso} en el tablero"
            numero_encontrado = recursos[recurso]
            assert  numero_encontrado == numero_esperado, f"Se esperaban {numero_esperado} de {recurso}, pero se encontraron {numero_encontrado}"
    def test_numeros(self,numeros):
        ns = [0]*12
        for n in numeros:
            if isinstance(n,int) and 1 <= n <= 12:
                ns[n - 1] += 1
        for n in [2,12]:
            amount = ns[n - 1]
            assert amount == 1, f"Tiene que haber un solo {n}, pero hay {amount}"
        for n in [3,4,5,6,8,9,10,11]:
            amount = ns[n - 1]
            assert amount == 2, f"Tiene que haber dos {n}, pero hay {amount}"
        assert ns[6] == 0, f"No tiene que haber 7s, sin embargo hay{ns[6]}"
    def test_casilla_central(self,tablero_lleno : TableroCatan):
        casilla_central = tablero_lleno.obtener_ficha(10)
        recurso_central = casilla_central.recurso
        assert recurso_central == "Desierto", f"A la casilla central no se le debe modificar el recurso, sin embargo tiene {recurso_central}"
        numero_central  = casilla_central.numero
        assert not(isinstance(numero_central,int) and 2 <= numero_central <= 12), f"La casilla central no debe tener un número posible de dado, sin embargo tiene al {numero_central}"

def jugadores(n) -> list[Jugador]:
    js = []
    colores = [(255,0,0),(0,0,255),(250,253,15),(0,0,0)]
    for i in range(n):
        js.append(Jugador(str(i + 1),colores[i]))
    return js

def falso_input(inputs,jugadores = 2):
    comandos = []
    if ORDEN_ESPECIAL:
        primeros_comandos = []
        segundos_comandos = []
        for n_jug in range(jugadores):
            primeros_comandos.append(inputs[n_jug*4])
            primeros_comandos.append(inputs[n_jug*4 + 1])
            segundos_comandos.append(inputs[n_jug*4 + 3])
            segundos_comandos.append(inputs[n_jug*4 + 2])
        segundos_comandos.reverse()
        posteriores = inputs[jugadores*4:]
        comandos = primeros_comandos + segundos_comandos + posteriores
    else:
        comandos = inputs
    print(comandos)
    def f(texto):
        sig_input = comandos.pop(0)
        return sig_input
    return f

class TestInicio:
    def test_2_jugadores(self,tablero_lleno : TableroCatan,monkeypatch):
        f = falso_input(["1 3","1 2","14 4","14 3","15 2","15 1","8 3","8 3","fin"])
        jugs = jugadores(2)
        monkeypatch.setattr('builtins.input', f)
        jugar_catan(jugs,tablero_lleno)
        for ficha_as,pos_as in [(1,3),(14,4),(15,2),(8,3)]:
            assert isinstance(tablero_lleno.obtener_asentamiento(ficha_as,pos_as),Asentamiento),f"No hay un asentamiento en la ficha {ficha_as}, posición {pos_as}"
        for ficha_c,pos_c in [(1,2),(14,3),(15,1),(8,3)]:
            assert isinstance(tablero_lleno.obtener_camino(ficha_as,pos_as),Camino),f"No hay un camino en la ficha {ficha_c}, posición {pos_c}"
    def test_3_jugadores(self,tablero_lleno : TableroCatan,monkeypatch):
        f = falso_input(["1 3","1 2","14 4","14 3","15 2","15 1","8 3","8 3","1 1","1 6","3 2","3 2","fin"],3)
        jugs = jugadores(3)
        monkeypatch.setattr('builtins.input', f)
        jugar_catan(jugs,tablero_lleno)
        for ficha_as,pos_as in [(1,3),(14,4),(15,2),(8,3),(1,1),(3,2)]:
            assert isinstance(tablero_lleno.obtener_asentamiento(ficha_as,pos_as),Asentamiento),f"No hay un asentamiento en la ficha {ficha_as}, posición {pos_as}"
        for ficha_c,pos_c in [(1,2),(14,3),(15,1),(8,3),(1,6),(3,2)]:
            assert isinstance(tablero_lleno.obtener_camino(ficha_as,pos_as),Camino),f"No hay un camino en la ficha {ficha_c}, posición {pos_c}"
    def test_4_jugadores(self,tablero_lleno : TableroCatan,monkeypatch):
        f = falso_input(["1 3","1 2","14 4","14 3","15 2","15 1","8 3","8 3","1 1","1 6","3 2","3 2","4 5","4 5","19 4","19 4","fin"],4)
        jugs = jugadores(4)
        monkeypatch.setattr('builtins.input', f)
        jugar_catan(jugs,tablero_lleno)
        for ficha_as,pos_as in [(1,3),(14,4),(15,2),(8,3),(1,1),(3,2),(4,5),(19,4)]:
            assert isinstance(tablero_lleno.obtener_asentamiento(ficha_as,pos_as),Asentamiento),f"No hay un asentamiento en la ficha {ficha_as}, posición {pos_as}"
        for ficha_c,pos_c in [(1,2),(14,3),(15,1),(8,3),(1,6),(3,2),(4,5),(19,4)]:
            assert isinstance(tablero_lleno.obtener_camino(ficha_as,pos_as),Camino),f"No hay un camino en la ficha {ficha_c}, posición {pos_c}"

iniciales_2_jugadores = ["1 3","1 2","14 4","14 3","11 2","11 1","8 3","8 3"]
nombres_recursos = ["Madera","Trigo","Ladrillo","Lana","Piedra"]

@pytest.fixture
def tablero_ordenado():
    tablero = TableroCatan()
    resources = ["Ladrillo"]*3 + ["Trigo"]*4 + ["Lana"]*4 + ["Madera"]*4 + ["Piedra"]*3
    numbers = [2] + list(range(3,12)) + [12] + list(range(3,12))
    while 7 in numbers:
        numbers.remove(7)
    for n,recurso,numero in zip([n for n in range(1,20) if n != 10],resources,numbers):
        tablero.colocar_recurso_y_numero(n,recurso,numero)
    return tablero

@pytest.fixture
def tablero_especial():
    tablero = TableroCatan()
    resources = ["Ladrillo"] + ["Madera"] + ["Lana"] + ["Trigo"] + ["Ladrillo"]*2 + ["Trigo"]*3 + ["Lana"]*3 + ["Madera"]*3 + ["Piedra"]*3
    numbers = [11]*2 + [10]*2 + [2] + list(range(3,10)) + [12] + list(range(3,10))
    while 7 in numbers:
        numbers.remove(7)
    for n,recurso,numero in zip([n for n in range(1,20) if n != 10],resources,numbers):
        tablero.colocar_recurso_y_numero(n,recurso,numero)
    return tablero


class TestRecursos:
    def test_sin_asentamientos(self,tablero_ordenado:TableroCatan,monkeypatch):
        f = falso_input(iniciales_2_jugadores  + ["fin"])
        jugs = jugadores(2)
        monkeypatch.setattr('builtins.input', f)
        monkeypatch.setattr('juego.tirar_dados', lambda: 7)
        for ficha,numero in [(1,3),(14,4),(11,2),(8,3)]:
            tablero_ordenado.colocar_asentamiento(ficha,numero,None)
        jugar_catan(jugs,tablero_ordenado)
        for jugador in jugs:
            for rec in nombres_recursos:
                assert jugador.cantidad_de(rec) == 0,f"Los jugadores no tienen asentamientos, y por lo tanto deben tener 0 {rec}, no {jugador.cantidad_de(rec)}"
    def test_sin_numero(self,tablero_ordenado:TableroCatan,monkeypatch):
        f = falso_input(iniciales_2_jugadores  + ["fin"])
        jugs = jugadores(2)
        monkeypatch.setattr('builtins.input', f)
        monkeypatch.setattr('juego.tirar_dados', lambda: 7)
        jugar_catan(jugs,tablero_ordenado)
        for jugador in jugs:
            for rec in nombres_recursos:
                assert jugador.cantidad_de(rec) == 0,f"Salió 7 en el dado, y por lo tanto deben tener 0 {rec}, no {jugador.cantidad_de(rec)}"
    def test_recurso_correcto(self,tablero_ordenado:TableroCatan,monkeypatch):
        f = falso_input(iniciales_2_jugadores  + ["fin"])
        jugs = jugadores(2)
        monkeypatch.setattr('builtins.input', f)
        monkeypatch.setattr('juego.tirar_dados', lambda: 2)
        jugar_catan(jugs,tablero_ordenado)
        for jugador in jugs:
            for rec in nombres_recursos:
                if jugador == jugs[0] and rec == "Ladrillo":
                    assert jugador.cantidad_de(rec) == 1,f"Salió 2 en el dado, y por lo tanto el jugador {jugador.nombre} deben tener 1 {rec}, no {jugador.cantidad_de(rec)}, ya que tiene un asentamiento en la ficha que tiene a 2 como número"
                else:
                    assert jugador.cantidad_de(rec) == 0,f"Salió 2 en el dado, y por lo tanto el jugador {jugador.nombre} deben tener 0 {rec}, no {jugador.cantidad_de(rec)}, ya que no tiene asentamientos en la ficha que tiene a 2 como número"
    def test_distintos_jugadores_fichas_distintas(self,tablero_ordenado:TableroCatan,monkeypatch):
        f = falso_input(iniciales_2_jugadores + ["fin"])
        jugs = jugadores(2)
        monkeypatch.setattr('builtins.input', f)
        monkeypatch.setattr('juego.tirar_dados', lambda: 3)
        jugar_catan(jugs,tablero_ordenado)
        for jugador in jugs:
            for rec in nombres_recursos:
                if jugador == jugs[0] and rec == "Ladrillo":
                    assert jugador.cantidad_de(rec) == 1,f"Salió 3 en el dado, y por lo tanto el jugador {jugador.nombre} deben tener 1 {rec}, no {jugador.cantidad_de(rec)}, ya que tiene un asentamiento en la ficha que tiene a 3 como número"
                elif jugador == jugs[1] and rec == "Lana":
                    assert jugador.cantidad_de(rec) == 1,f"Salió 3 en el dado, y por lo tanto el jugador {jugador.nombre} deben tener 1 {rec}, no {jugador.cantidad_de(rec)}, ya que tiene un asentamiento en la ficha que tiene a 3 como número"
                else:
                    assert jugador.cantidad_de(rec) == 0,f"Salió 3 en el dado, y por lo tanto el jugador {jugador.nombre} deben tener 0 {rec}, no {jugador.cantidad_de(rec)}, ya que no tiene asentamientos en la ficha que tiene a 3 como número"
    def test_distintos_jugadores_misma_ficha(self,tablero_ordenado:TableroCatan,monkeypatch):
        f = falso_input(iniciales_2_jugadores[:-2] + ["1 6","1 5"] + ["fin"])
        jugs = jugadores(2)
        monkeypatch.setattr('builtins.input', f)
        monkeypatch.setattr('juego.tirar_dados', lambda: 2)
        jugar_catan(jugs,tablero_ordenado)
        for jugador in jugs:
            for rec in nombres_recursos:
                if rec == "Ladrillo":
                    assert jugador.cantidad_de(rec) == 1,f"Salió 2 en el dado, y por lo tanto el jugador {jugador.nombre} deben tener 1 {rec}, no {jugador.cantidad_de(rec)}, ya que tiene un asentamiento en la ficha que tiene a 2 como número"
                else:
                    assert jugador.cantidad_de(rec) == 0,f"Salió 2 en el dado, y por lo tanto el jugador {jugador.nombre} deben tener 0 {rec}, no {jugador.cantidad_de(rec)}, ya que no tiene asentamientos en la ficha que tiene a 2 como número"
        
class TestComandos:
    class TestFin:
        def test_fin_primer_comando(self,monkeypatch,tablero_lleno):
            f = falso_input(iniciales_2_jugadores  + ["fin"])
            jugs = jugadores(2)
            monkeypatch.setattr('builtins.input', f)
            jugar_catan(jugs,tablero_lleno)
            assert True
    class TestPasar:
        def test_pasar_sin_comandos(self,monkeypatch,tablero_ordenado):
            f = falso_input(iniciales_2_jugadores  + ["pas","fin"])
            jugs = jugadores(2)
            monkeypatch.setattr('builtins.input', f)
            monkeypatch.setattr('juego.tirar_dados', lambda: 2)
            jugar_catan(jugs,tablero_ordenado)
            for jugador in jugs:
                for rec in nombres_recursos:
                    if jugador == jugs[0] and rec == "Ladrillo":
                        assert jugador.cantidad_de(rec) == 2,f"Luego de 2 turnos, el jugador {jugador.nombre} deben tener 2 {rec}, no {jugador.cantidad_de(rec)}, ya que tiene un asentamiento en la ficha que tiene a 2 como número, y el 2 salió 2 veces"
                    else:
                        assert jugador.cantidad_de(rec) == 0,f"Salió 2 en el dado, y por lo tanto el jugador {jugador.nombre} deben tener 0 {rec}, no {jugador.cantidad_de(rec)}, ya que no tiene asentamientos en la ficha que tiene a 2 como número"
    class TestAsentamiento:
        def test_asentamiento_falta_recursos(self,tablero_ordenado : TableroCatan,monkeypatch):
            f = falso_input(iniciales_2_jugadores + ["ase 6 3","fin"])
            jugs = jugadores(2)
            monkeypatch.setattr('builtins.input', f)
            monkeypatch.setattr('juego.tirar_dados', lambda: 3)
            jugar_catan(jugs,tablero_ordenado)
            assert not isinstance(tablero_ordenado.obtener_asentamiento(6,3),Asentamiento), f"No tiene que haber un asentamiento en la ficha 6 posición 3 por falta de recursos"
            for jugador in jugs:
                for rec in nombres_recursos:
                    if jugador == jugs[0] and rec == "Ladrillo":
                        assert jugador.cantidad_de(rec) == 1,f"No se colocó el asentamiento, entonces la cantidad de {rec} del jugador {jugador.nombre} debe ser 1, no {jugador.cantidad_de(rec)}"
                    elif jugador == jugs[1] and rec == "Lana":
                        assert jugador.cantidad_de(rec) == 1,f"No se colocó el asentamiento, entonces la cantidad de {rec} del jugador {jugador.nombre} debe ser 1, no {jugador.cantidad_de(rec)}"
                    else:
                        assert jugador.cantidad_de(rec) == 0,f"No se colocó el asentamiento, entonces la cantidad de {rec} del jugador {jugador.nombre} debe ser 0, no {jugador.cantidad_de(rec)}"
        def test_asentamiento_jugador1(self,tablero_especial:TableroCatan,monkeypatch):
            f = falso_input(["1 4","1 3","2 3","3 4","11 2","11 2","18 6","17 1"] + ["pas","pas","ase 6 3","fin"])
            jugs = jugadores(2)
            monkeypatch.setattr('builtins.input', f)
            dados = [11,10,12]
            monkeypatch.setattr('juego.tirar_dados', lambda: dados.pop(0))
            jugar_catan(jugs,tablero_especial)
            assert isinstance(tablero_especial.obtener_asentamiento(6,3),Asentamiento), f"Tiene que haber un asentamiento en la ficha 6 posición 3, y no hay"
            assert tablero_especial.obtener_asentamiento(6,3).jugador == jugs[0], f"El asentamiento debe pertencer al jugador {jugs[0].nombre}, no al jugador {tablero_especial.obtener_asentamiento(6,3).jugador.nombre}"
            for jugador in jugs:
                for rec in nombres_recursos:
                    if jugador == jugs[0]:
                        assert jugador.cantidad_de(rec) == 0,f"El jugador {jugador.nombre} gastó los recursos recibidos durante la partida, así que debe tener 0, no {jugador.cantidad_de(rec)} de {rec}"
                    else:
                         assert jugador.cantidad_de(rec) == 0,f"El jugador {jugador.nombre} no recibió recursos durante la partida, así que debe tener 0, no {jugador.cantidad_de(rec)} de {rec}"
        def test_asentamiento_jugador2(self,tablero_especial:TableroCatan,monkeypatch):
            f = falso_input(["11 2","11 2","18 6","17 1","1 4","1 3","2 3","3 4"] + ["pas","ase 6 3","fin"])
            jugs = jugadores(2)
            monkeypatch.setattr('builtins.input', f)
            dados = [11,10,12]
            monkeypatch.setattr('juego.tirar_dados', lambda: dados.pop(0))
            jugar_catan(jugs,tablero_especial)
            assert isinstance(tablero_especial.obtener_asentamiento(6,3),Asentamiento), f"Tiene que haber un asentamiento en la ficha 6 posición 3, y no hay"
            assert tablero_especial.obtener_asentamiento(6,3).jugador == jugs[1], f"El asentamiento debe pertencer al jugador {jugs[0].nombre}, no al jugador {tablero_especial.obtener_asentamiento(6,3).jugador.nombre}"
            for jugador in jugs:
                for rec in nombres_recursos:
                    if jugador == jugs[1]:
                        assert jugador.cantidad_de(rec) == 0,f"El jugador {jugador.nombre} gastó los recursos recibidos durante la partida, así que debe tener 0, no {jugador.cantidad_de(rec)} de {rec}"
                    else:
                         assert jugador.cantidad_de(rec) == 0,f"El jugador {jugador.nombre} no recibió recursos durante la partida, así que debe tener 0, no {jugador.cantidad_de(rec)} de {rec}"
    class TestCamino:
        def test_camino_falta_recursos(self,tablero_especial:TableroCatan,monkeypatch):
            f = falso_input(["11 2","11 2","18 6","17 1","1 4","1 3","2 3","3 4"] + ["cam 2 2","fin"])
            jugs = jugadores(2)
            monkeypatch.setattr('builtins.input', f)
            dados = [11,10,12]
            monkeypatch.setattr('juego.tirar_dados', lambda: dados.pop(0))
            jugar_catan(jugs,tablero_especial)
            assert not isinstance(tablero_especial.obtener_camino(2,2),Camino), f"No tiene que haber un camino en la ficha 2 posición 2 por falta de recursos"
            for jugador in jugs:
                for rec in nombres_recursos:
                    if jugador == jugs[1] and (rec == "Ladrillo" or rec == "Madera"):
                        assert jugador.cantidad_de(rec) == 1,f"No se colocó el camino, entonces la cantidad de {rec} del jugador {jugador.nombre} debe ser 1, no {jugador.cantidad_de(rec)}"
                    else:
                        assert jugador.cantidad_de(rec) == 0,f"No se colocó el camino, entonces la cantidad de {rec} del jugador {jugador.nombre} debe ser 0, no {jugador.cantidad_de(rec)}"
        def test_camino_jugador1(self,tablero_especial : TableroCatan,monkeypatch):
            f = falso_input(["1 4","1 3","2 3","3 4","11 2","11 2","18 6","17 1"] + ["cam 2 2","fin"])
            jugs = jugadores(2)
            monkeypatch.setattr('builtins.input', f)
            dados = [11,10,12]
            monkeypatch.setattr('juego.tirar_dados', lambda: dados.pop(0))
            jugar_catan(jugs,tablero_especial)
            assert isinstance(tablero_especial.obtener_camino(2,2),Camino), f"Tiene que haber un camino en la ficha 2 posición 2"
            for jugador in jugs:
                for rec in nombres_recursos:
                    assert jugador.cantidad_de(rec) == 0,f"Se colocó el camino, entonces la cantidad de {rec} del jugador {jugador.nombre} debe ser 0, no {jugador.cantidad_de(rec)}"
        def test_camino_jugador2(self,tablero_especial : TableroCatan,monkeypatch):
            f = falso_input(["11 2","11 2","18 6","17 1","1 4","1 3","2 3","3 4"] + ["pas","cam 2 2","fin"])
            jugs = jugadores(2)
            monkeypatch.setattr('builtins.input', f)
            dados = [10,11,12]
            monkeypatch.setattr('juego.tirar_dados', lambda: dados.pop(0))
            jugar_catan(jugs,tablero_especial)
            assert isinstance(tablero_especial.obtener_camino(2,2),Camino), f"Tiene que haber un camino en la ficha 2 posición 2"            
            for jugador in jugs:
                for rec in nombres_recursos:
                    if jugador == jugs[1] and (rec == "Ladrillo" or rec == "Madera"):
                        assert jugador.cantidad_de(rec) == 0,f"Se colocó el camino, entonces la cantidad de {rec} del jugador {jugador.nombre} debe ser 0, no {jugador.cantidad_de(rec)}"
                    if jugador == jugs[1] and (rec == "Lana" or rec == "Trigo"):
                        assert jugador.cantidad_de(rec) == 1,f"Se colocó el camino, entonces la cantidad de {rec} del jugador {jugador.nombre} debe ser 1, no {jugador.cantidad_de(rec)}"
                    else:
                        assert jugador.cantidad_de(rec) == 0,f"Se colocó el camino, entonces la cantidad de {rec} del jugador {jugador.nombre} debe ser 0, no {jugador.cantidad_de(rec)}"
