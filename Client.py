import pygame
from grid import Grid

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '700,100'


surface = pygame.display.set_mode((600,600))
pygame.display.set_caption('TicTacToe Client')
import threading

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

import socket
HOST = '127.0.0.1'
PORT = 65530

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

def receive_data():
    global turn
    while True:
        try:
            data = sock.recv(1024).decode().split('-')
            x = int(data[0])
            y = int(data[1])
            if(data[2]=='yourturn'):
                turn = True
            if data[3]=='False':
                grid.game_over = True
            if grid.get_cell_value(x,y)==0:
                grid.set_cell_value(x,y,'X')
        except:
            global running
            running = False
            print('Server disconnected')
            break

create_thread(receive_data)

grid = Grid()
running = True
turn = False
player = "O"
playing = 'True'


while running:
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            print("Client closed itself")
            running = False
        if(event.type == pygame.MOUSEBUTTONDOWN and grid.game_over==False):
            if(pygame.mouse.get_pressed()[0]):
                if turn and not grid.game_over:

                    pos = pygame.mouse.get_pos()

                    pos_x = pos[0]//200
                    pos_y = pos[1]//200
                    grid.get_mouse(pos_x, pos_y, player)
                    if grid.game_over:
                        playing='False'
                    send_data = '{}-{}-{}-{}'.format(pos_x,pos_y, 'yourturn',playing).encode()
                    try:
                        sock.send(send_data)
                    except:
                        running = False
                        print('Server disconnected')
                        sock.close()
                    turn = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over=False
                turn = False
                playing = 'True'
            if event.key == pygame.K_ESCAPE:
                print("Client closed itself")
                running = False
                break

    surface.fill((0,0,0))
    grid.draw(surface)
    pygame.display.flip()
