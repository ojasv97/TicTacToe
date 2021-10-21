import pygame
from grid import Grid

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'


surface = pygame.display.set_mode((600,600))
pygame.display.set_caption('TicTacToe Server')

import threading

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

import socket
HOST = '127.0.0.1'
PORT = 65530

connection_established = False
conn, addr = None, None

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind((HOST, PORT))
sock.listen(2)

clientCount = 0

def receive_data():
    global turn
    while True:
        data = conn.recv(1024).decode().split('-')
        x = int(data[0])
        y = int(data[1])
        if(data[2]=='yourturn'):
            turn = True
        if data[3]=='False':
            grid.game_over = True
        if grid.get_cell_value(x,y)==0:
            grid.set_cell_value(x,y,'O')

def waiting_for_connection():
    global connection_established, conn, addr, clientCount
    conn, addr = sock.accept() #wait for a connection, it is a blocking call
    print('Client {} is connected'.format(clientCount))
    connection_established = True
    clientCount+=1
    try:
        receive_data()
    except:
        global running
        conn.close()
        print('Client {} disconnected'.format(clientCount))
        clientCount-=1
        if clientCount==0:
            sock.close()
            running = False

create_thread(waiting_for_connection)
    

grid = Grid()
running = True
player = "X"
turn = True
playing = 'True'


while running:
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            print("Server closed itself")
            running = False
        if(event.type == pygame.MOUSEBUTTONDOWN and connection_established):
            if(pygame.mouse.get_pressed()[0]):
                if turn and not grid.game_over:
                    pos = pygame.mouse.get_pos()
                    pos_x = pos[0]//200
                    pos_y = pos[1]//200
                    grid.get_mouse(pos_x, pos_y, player)
                    if grid.game_over:
                        playing='False'
                    send_data = '{}-{}-{}-{}'.format(pos_x,pos_y,'yourturn',playing).encode()
                    try:
                        conn.send(send_data)
                    except:
                        conn.close()
                        print('Client {} disconnected\n'.format(clientCount))
                        clientCount-=1
                        if clientCount==0:
                            sock.close()
                            running = False
                    turn = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over=False
                turn = True
                playing = 'True'
            if event.key == pygame.K_ESCAPE:
                print("Server closed itself")
                running = False
                break

    surface.fill((0,0,0))
    grid.draw(surface)
    pygame.display.flip()
