import pygame, sys
from Settings import *
from Tiles import Tile,WinningTile
from Level import Level
# import socket

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Port = 1234
# Host = socket.gethostname()

# s.connect((Host, Port)) #tuple
# s.sendall(b"test")
# map_chosen = s.recv(2048).decode('utf-8')
# print(map_chosen)

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

level = Level(map2, screen)
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('black')
        level.run()
        
        

        pygame.display.flip()
        clock.tick(60)

main()