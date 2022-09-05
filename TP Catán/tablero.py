class NodoCatan:
    def __init__(self,aristas = [None,None,None],contenido_default = None):
        self.contenido = contenido_default
        # 0 y 2 son las chanfleadas, 1 es la vertical
        self.aristas  = aristas.copy()
    def agregar_aristas(self,aristas):
        self.aristas = aristas
    def agregar_arista(self,arista,pos):
        assert pos in range(3), f"La posición es un número 0, 1 o 2, no puede ser {pos}" 
        self.aristas[pos] = arista
    def __str__(self):
        return f"({self.contenido})"

class AristaCatan:
    def __init__(self,nodoA = None,nodoB = None,contenido_default = None):
        self.contenido = contenido_default
        #Vistas de izquierda a derecha y de abajo a arriba
        self.nodos = [nodoA,nodoB]
    def agregar_nodo(self,nodo,pos):
        assert pos in range(2), f"La posición es 0 o 1, no puede ser {pos}"
        self.contenido[pos] = nodo
    def __str__(self):
        return f"--{self.contenido}--"

class GrafoHexagonal:
    def __init__(self,nodos = [None for _ in range(6)], aristas = [None for _ in range(6)],ficha_default = None,arista_default = None):
        self.nodos   = nodos.copy()
        self.aristas = aristas.copy()
        for i in range(6):
            posA = i
            posB = (i + 1)%6
            nodoA = self.nodos[posA] if self.nodos[posA] != None else NodoCatan(contenido_default=ficha_default)
            self.nodos[posA] = nodoA
            nodoB = self.nodos[posB] if self.nodos[posB] != None else NodoCatan(contenido_default=ficha_default)
            self.nodos[posB] = nodoB
            # Estas posiciones tienen los nodos al revés en el orden propuesto
            if i in [1,2,3]:
                nodoA,nodoB = nodoB,nodoA
            if  self.aristas[i] == None:
                aristaNueva = AristaCatan(nodoA,nodoB,contenido_default=arista_default)
                self.aristas[i] = aristaNueva
                # Que posición ocupan las aristas respecto al nodo es relativa a que segmento estoy construyendo 
                if i in [0,2,3,5]:
                    nodoA.agregar_arista(aristaNueva,2)
                    nodoB.agregar_arista(aristaNueva,0)
                elif i in [1,4]:
                    nodoA.agregar_arista(aristaNueva,1)
                    nodoB.agregar_arista(aristaNueva,1)
                #for nodo in [nodoA,nodoB]:
                #    print(str(nodo) + ":" + str(nodo.aristas[0]) + str(nodo.aristas[1]) + str(nodo.aristas[2]))

    def __str__(self):
        txt = f"Hex:"
        for i in range(6):
            txt += str(self.nodos[i])
            txt += str(self.aristas[i])
        return txt

class HexagonoCatan:
    def __init__(self,grafo_subyacente):
        self.recurso = ""
        self.numero  = 0
        self.ladron  = False
        self._grafo  = grafo_subyacente
    def obtener_asentamiento(self,vertice):
        assert vertice in range(1,7), f"El vértice es un número del 1 al 6, no {vertice}"
        return self._grafo.nodos[vertice - 1].contenido
    def colocar_asentamiento(self,vertice,asentamiento):
        assert vertice in range(1,7), f"El vértice es un número del 1 al 6, no {vertice}"
        nodo = self._grafo.nodos[vertice - 1]
        nodo.contenido = asentamiento
    def obtener_camino(self,arista):
        assert arista in range(1,7), f"La arista es un número del 1 al 6, no {arista}"
        return self._grafo.aristas[arista - 1].contenido
    def colocar_camino(self,arista,camino):
        assert arista in range(1,7), f"La arista es un número del 1 al 6, no {arista}"
        self._grafo.aristas[arista - 1].contenido = camino
    def obtener_asentamientos(self):
        #Modificar el None
        return [(pos,nodo.contenido) for pos,nodo in enumerate(self._grafo.nodos) if nodo.contenido != None]
    def obtener_caminos(self):
        #Modificar el None
        return [(pos,arista.contenido) for pos,arista in enumerate(self._grafo.aristas) if arista.contenido != None]
    def nodos_adyacentes(self,numero_de_nodo):
        nodo = self._grafo.nodos[numero_de_nodo - 1]
        caminos = nodo.aristas
        nodos_adyacentes = []
        for arista in caminos:
            nodos_adyacentes.append(next(n for n in arista.nodos if not n is nodo))
        return nodos_adyacentes

    def aristas_adyacentes(self,numero_de_arista):
        arista : AristaCatan = self._grafo.aristas[numero_de_arista - 1]
        nodos_adyacentes : list[NodoCatan] = arista.nodos
        aristas_adyacentes = []
        for nodo in nodos_adyacentes:
            aristas : AristaCatan = nodo.aristas
            for a in aristas:
                if a != arista:
                    aristas_adyacentes.append(a)
        return aristas_adyacentes

    def obtener_nodo(self,numero_de_nodo):
        return self._grafo.nodos[numero_de_nodo - 1]

    def obtener_arista(self,numero_de_arista):
        return self._grafo.aristas[numero_de_arista - 1]

    def __str__(self):
        return str(self._grafo)

class CasillaCentral(HexagonoCatan):
    def __init__(self, grafo_subyacente):
        super().__init__(grafo_subyacente)
        self.recurso = "Desierto"
        self.numero  = ""
        self.ladron  = True

class TableroCatan:
    def __init__(self,ficha_default = None,arista_default = None):
        self._tablero_hexagonal = [None]*19
        self.ficha_vacia = ficha_default
        self.arista_vacia = arista_default
        vecindarios = [
            [None,2   ,5   ,4   ,None,None],
            [None,3   ,6   ,5   ,1   ,None],
            [None,None,7   ,6   ,2   ,None],
            [1   ,5   ,9   ,8   ,None,None],
            [2   ,6   ,10  ,9   ,4   ,1   ],
            [3   ,7   ,11  ,10  ,5   ,2   ],
            [None,None,12  ,11  ,6   ,3   ],
            [4   ,9   ,13  ,None,None,None],
            [5   ,10  ,14  ,13  ,8   ,4   ],
            [6   ,11  ,15  ,14  ,9   ,5   ],
            [7   ,12  ,16  ,15  ,10  ,6   ],
            [None,None,None,16  ,11  ,7   ],
            [9   ,14  ,17  ,None,None,8   ],
            [10  ,15  ,18  ,17  ,13  ,9   ],
            [11  ,16  ,19  ,18  ,14  ,10  ],
            [12  ,None,None,19  ,15  ,11  ],
            [14  ,18  ,None,None,None,13  ],
            [15  ,19  ,None,None,17  ,14  ],
            [16  ,None,None,None,18  ,15  ]
        ]
        for i in range(19):
            nodos_preexistentes   = []
            aristas_preexistentes = []
            for pos in range(6):
                opt_a = vecindarios[i][pos]
                opt_b = vecindarios[i][(pos-1)%6]
                vec_a = self._tablero_hexagonal[opt_a-1] if opt_a != None else None
                vec_b = self._tablero_hexagonal[opt_b-1] if opt_b != None else None
                nodo   = None
                arista = None
                if vec_a != None:
                    nodo   = vec_a.nodos[(pos + 4)%6]
                    arista = vec_a.aristas[(pos + 3)%6]
                elif vec_b != None:
                    nodo   = vec_b.nodos[(pos + 2)%6]
                nodos_preexistentes.append(nodo)
                aristas_preexistentes.append(arista)
            #print(f"Nodo {i} se constuyo con {sum(1 for x in nodos_preexistentes if x != None)} nodos y {sum(1 for x in aristas_preexistentes if x != None)} aristas")
            self._tablero_hexagonal[i] = GrafoHexagonal(nodos_preexistentes,aristas_preexistentes,ficha_default,arista_default) 
        
        
        #Creando las fichas
        self._fichas = [HexagonoCatan(grafo) if n != 9 else CasillaCentral(grafo) for n,grafo in enumerate(self._tablero_hexagonal)]

    def obtener_asentamiento(self,ficha,vertice):
        return self._fichas[ficha - 1].obtener_asentamiento(vertice)

    def colocar_asentamiento(self,ficha,vertice,asentamiento):
        self._fichas[ficha - 1].colocar_asentamiento(vertice,asentamiento)

    def obtener_camino(self,ficha,arista):
        return self._fichas[ficha - 1].obtener_camino(arista)

    def colocar_camino(self,ficha,arista,camino):
        self._fichas[ficha - 1].colocar_camino(arista,camino)

    def asentamientos_por_ficha(self,numero_de_ficha):
        ficha = self._fichas[numero_de_ficha - 1]
        return [casa for pos,casa in ficha.obtener_asentamientos()]

    def colocar_recurso(self,numero_de_ficha,recurso):
        ficha = self._fichas[numero_de_ficha - 1]
        ficha.recurso = recurso

    def colocar_numero(self,numero_de_ficha,numero):
        ficha = self._fichas[numero_de_ficha - 1]
        ficha.numero  = numero

    def colocar_recurso_y_numero(self,numero_de_ficha,recurso,numero):
        self.colocar_recurso(numero_de_ficha,recurso)
        self.colocar_numero(numero_de_ficha,numero)

    def obtener_ficha(self,numero_de_ficha):
        return self._fichas[numero_de_ficha - 1]

    def obtener_recurso_de_ficha(self,numero_de_ficha):
        return self.obtener_ficha(numero_de_ficha).recurso
    
    def obtener_numero_de_ficha(self,numero_de_ficha):
        return self.obtener_ficha(numero_de_ficha).numero
    
    def asentamientos_adyacentes_a_nodo(self,numero_de_ficha,numero_nodo):
        ficha = self._fichas[numero_de_ficha - 1]
        return [nodo.contenido for nodo in ficha.nodos_adyacentes(numero_nodo) if nodo.contenido != None]

    def caminos_adyacentes_a_arista(self,numero_de_ficha,numero_arista):
        ficha = self._fichas[numero_de_ficha - 1]
        return [arista.contenido for arista in ficha.aristas_adyacentes(numero_arista) if arista.contenido != None]
    
    def obtener_nodo(self,numero_de_ficha,numero_nodo):
        return self._fichas[numero_de_ficha - 1].obtener_nodo(numero_nodo)

    def obtener_arista(self,numero_de_ficha,numero_arista):
        return self._fichas[numero_de_ficha - 1].obtener_arista(numero_arista)

    def colocar_ladron(self,numero_de_ficha):
        self._fichas[numero_de_ficha - 1].ladron = True

    def sacar_ladron(self,numero_de_ficha):
        self._fichas[numero_de_ficha - 1].ladron = False

    def tiene_ladron(self,numero_de_ficha):
        return self._fichas[numero_de_ficha - 1].ladron

    def fichas(self):
        return self._fichas

    def __str__(self):
        txt = ""
        for hex in self._fichas:
            txt += f"Ficha: {str(hex)}\n"
        return txt
