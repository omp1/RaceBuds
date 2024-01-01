import pygame, sys
from Settings import *
from Tiles import Tile,WinningTile
from Level import Level
import socket
import random


# mapnums = ("map1", "map2", "map3")
# map_chosen = random.choice(mapnums)
# print(type(map_chosen))
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# port = 1234

# s.bind(('localhost', port))

# s.listen(30)

# cs, addr = s.accept()
# print(cs.recv(2048))

# print(map_chosen)
# cs.send(bytes("map1", 'utf-8'))



pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
#level_input = input("Pick your level map: map1, map2 or map3 ")
#mapnums = {'map1', 'map2', 'map3'}
# while (level_input not in mapnums):
#     level_input = input("Invalid response. Pick from map1, map2, or map3")

# if level_input == "map1":
#     s.sendall(b"map1")
# elif level_input == "map2":
#     s.sendall(b"map2")
# elif level_input == "map3":
#     s.sendall(b"map3")
# cs.close()

# s.close()
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