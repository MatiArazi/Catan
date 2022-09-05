import pygame
from math import pi,cos,sin
import numpy as np
import threading
import juego
import time
import queue
from clases import Asentamiento,Ciudad


from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

image_per_resource = {
    "Ladrillo": "img/brick.png",
    "Trigo"   : "img/wheat.png",
    "Madera"  : "img/wood.png",
    "Piedra"  : "img/ore.png",
    "Lana"    : "img/sheep.png",
    "Desierto" : "img/desert.png",
}

card_per_resource = {
    "Ladrillo": "img/brick_card.png",
    "Trigo"   : "img/wheat_card.png",
    "Madera"  : "img/wood_card.png",
    "Piedra"  : "img/ore_card.png",
    "Lana"    : "img/sheep_card.png",
}

colors_per_resource = {
    "Ladrillo": pygame.Color("#dc5539"),
    "Trigo"   : pygame.Color("#ebbd68"),
    "Madera"  : pygame.Color("#5d2906"),
    "Piedra"  : pygame.Color("#888c8d"),
    "Lana"    : pygame.Color("#00A619"),
}
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
desert_color = (234,215,149)
thief_color = black
current_thief_tile = -1
previous_thief_tile = -1

def draw_hexagon(surface, background_image, radius, position):
    n, r = 6, radius
    x, y = position
    hexagon = [
        (x + r * cos(2 * pi * (i +0.5) / n), y + r * sin(2 * pi * (i +0.5) / n))
        for i in range(n)
    ]
    #Fill
    left_x,left_y = x + radius * cos(2 * pi * (2.5) / n), y - radius * sin(2 * pi * 1.5 / n)
    left_corner = (left_x,left_y)
    #mask_surface = pygame.Surface((2*r,2*r))
    background_image = pygame.transform.scale(background_image, (2*radius*cos(2*pi*0.5/n) + 1, radius*2 + 1))
    #pygame.draw.aalines(mask_surface, white, True, hexagon)
    #background_image.blit(mask_surface, left_corner, None, pygame.BLEND_RGBA_MULT)
    surface.blit(background_image, left_corner)
    pygame.draw.polygon(surface, desert_color, hexagon,4)
    pygame.display.update()
    

def draw_thief(position,screen):
    x,y = position
    thief_width = 18
    thief_head_radius = 12/2
    pygame.draw.rect(screen,thief_color,pygame.Rect(x - thief_width/2,y - thief_width,thief_width,thief_width))
    pygame.draw.circle(screen,thief_color,(x,y - thief_width),thief_width/2)
    pygame.draw.circle(screen,thief_color,(x,y - thief_width*3/2 - thief_head_radius),thief_head_radius)

def draw_tile(surface,tile, position,radius = 50):
    #Imagen a cargar
    background_image = pygame.image.load(image_per_resource[tile.recurso]).convert_alpha()
    masked_result = background_image.copy()
    draw_hexagon(surface,masked_result,radius,position)
    if not tile.recurso == "Desierto":
        font = pygame.font.Font('freesansbold.ttf', 22)
        number_color = black if tile.numero not in [6,8] else red
        number = font.render(str(tile.numero),True,number_color,desert_color)
        numberRect = number.get_rect(center = position)
        pygame.draw.circle(surface,desert_color,position,17.5)
        surface.blit(number,numberRect)

def draw_tile_elements(surface,tile, position,radius = 50,width = 15):
    n, r = 6, radius
    x, y = position
    vertexes = [
        (x - r * cos(2 * pi * (i +1.5) / n), y - r * sin(2 * pi * (i +1.5) / n))
        for i in range(n)
    ] 
    #Dibujo los caminos
    roads = tile.obtener_caminos()
    for pos,road in roads:
        pygame.draw.line(surface,road.jugador.color,vertexes[pos],vertexes[(pos + 1)%n],width + 2)  
    #Dibujo las casas
    houses = tile.obtener_asentamientos()
    for pos,house in houses:
        if isinstance(house,Asentamiento):
            pygame.draw.circle(surface,house.jugador.color,vertexes[pos],15)
            pygame.draw.circle(surface,black,vertexes[pos],15,width=3)
        elif isinstance(house,Ciudad):
            pygame.draw.rect(surface,house.jugador.color,pygame.Rect(vertexes[pos][0] - 15,vertexes[pos][1] - 15,30,30))
            pygame.draw.rect(surface,black,pygame.Rect(vertexes[pos][0] - 15,vertexes[pos][1] - 15,30,30),3)
    #Dibujo al ladrón
    if tile.ladron:
       draw_thief((x,y - 18),surface)
       if not tile.recurso == "Desierto":
        pygame.draw.circle(surface,thief_color,position,17.5,3)
    
def draw_catan_board(tiles,screen,center,update=False):
    global previous_thief_tile
    global current_thief_tile
    radius = 75
    deltaX = cos(pi/6) *radius
    deltaY = sin(pi/6) *radius
    positions = []
    for row,row_span in enumerate([2,3,4,3,2]):
        x_center,y_center = center
        for x in np.arange(-deltaX*row_span,deltaX*row_span +1,deltaX*2):
            positions.append((x_center + x,y_center + (row-2)*(radius + deltaY) ))
    for number,tile in enumerate(tiles):
        if tile.ladron and number != current_thief_tile:
            previous_thief_tile = current_thief_tile
            current_thief_tile  = number
        if not update:
            draw_tile(screen,tile,positions[number],radius)
        elif previous_thief_tile == number:
            draw_tile(screen,tile,positions[number],radius)
            previous_thief_tile = -1
        draw_tile_elements(screen,tile,positions[number],radius,6)
    pygame.display.flip()


def draw_resources(player,screen,start):
    x,y = start
    for position,resource in enumerate(["Madera","Trigo","Ladrillo","Lana","Piedra"]):
        card_image = pygame.image.load(card_per_resource[resource]).convert_alpha()
        card_image = pygame.transform.scale(card_image,(40,65))
        screen.blit(card_image, (x + position*50,y))
        font = pygame.font.Font('freesansbold.ttf', 25)
        quantity = font.render(str(player.cantidad_de(resource)),True,black,white)
        quantity_rect = quantity.get_rect(center = (x + position*50 + 20,y + 81))
        pygame.draw.rect(screen,white,pygame.Rect(x + position*50,y + 66,40,30))
        pygame.draw.rect(screen,black,pygame.Rect(x + position*50,y + 66,40,30),1)
        screen.blit(quantity,quantity_rect)


def draw_player(player,screen,position):
    center_x,center_y = position
    width = 450
    height = 150
    pygame.draw.rect(screen,player.color,pygame.Rect(center_x - width/2,center_y - height/2,width,height))
    pygame.draw.rect(screen,black,pygame.Rect(center_x - width/2,center_y - height/2,width,height),3)
    font = pygame.font.Font('freesansbold.ttf', 30)
    name = font.render(player.nombre,True,black,white)
    name_rect = name.get_rect(center = (center_x,center_y - height/3))
    screen.blit(name,name_rect)
    pygame.draw.rect(screen,black,pygame.Rect(name_rect.left - 2,name_rect.top - 2,name_rect.width + 4,name_rect.height + 4),2)
    draw_resources(player,screen,(center_x - width/2 + 25,center_y - 25))

def draw_players(players,screen,start,step):
    for number,player in enumerate(players):
        x,y = start
        pos = (x,y + step*number)
        draw_player(player,screen,pos)

def draw_dice(dice,screen):
    pygame.draw.rect(screen,white,pygame.Rect(30,606,70,70))
    pygame.draw.rect(screen,black,pygame.Rect(30,606,70,70),3)
    font = pygame.font.Font('freesansbold.ttf', 50)
    number = font.render(str(dice),True,black,white)
    number_rect = number.get_rect(center = (65,641))
    screen.blit(number,number_rect)
    font = pygame.font.Font('freesansbold.ttf', 30)
    text = font.render("DADOS",True,black,white)
    text_rect = text.get_rect(center = (65,590))
    screen.blit(text,text_rect)

#tablero_lock = threading.Lock()
#jugadores_lock = threading.Lock()

#class LockWrapper():
#    def __init__(self, baseObject,lock):
#        self.internal : object = baseObject
#        self.lock : threading.Lock = lock
#    def __getattr__(self,attr):
#        def lock(*args, **kwargs):
#            self.lock.acquire()
#            returned_value = getattr(self.internal,attr)(*args, **kwargs)
#            self.lock.release()
#            return returned_value  
#        return lock
#    def __iter__(self):
#        return iter(self.internal)
#    def __getitem__(self, item):
#        self.lock.acquire()
#        result = self.internal[item]
#        self.lock.release()
#        return result
#    def __len__(self):
#        return len(self.internal)


def jugar_con_interfaz(jugadores,tablero):
    quit_game = False
    jugs = jugadores.copy()
    dice = queue.Queue()

    student_dice = juego.tirar_dados

    def tirar_dados_con_queue():
        amount = student_dice()
        dice.put(amount)
        return amount

    juego.tirar_dados = tirar_dados_con_queue

    class Input(threading.Thread):
        def run(self):
            juego.jugar_catan(jugadores,tablero)


    i : threading.Thread = Input()
    i.start()

    pygame.init()
    pygame.display.set_caption('Catán')
    Icon = pygame.image.load('img/game_logo.svg')
    pygame.display.set_icon(Icon)
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 704

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((255, 255, 255))

    draw_catan_board(tablero.fichas(),screen,(SCREEN_WIDTH/3,SCREEN_HEIGHT/2))

    while not quit_game and i.is_alive() :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
        draw_catan_board(tablero.fichas(),screen,(SCREEN_WIDTH/3,SCREEN_HEIGHT/2),True)
        draw_players(jugadores,screen,(SCREEN_WIDTH*4/5,88),176)
        try:
            dice_number = dice.get(False)
        except queue.Empty:
            dice_number = None
        if dice_number != None:
            draw_dice(dice_number,screen)
        #time.sleep(0.25)
    pygame.quit()