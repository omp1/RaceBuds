import pygame
import socket
import pickle
from os import listdir
from os.path import isfile,join




class Player2(pygame.sprite.Sprite):
    
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((32,32))
        
        self.image = pygame.image.load("Dude_Monster.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.side = "left"
        

        self.direction = pygame.math.Vector2(0,0)
        
        self.speed = 4
        self.grav = 1.0
        self.jump_speed = -13
        self.isJump = False
        self.client2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client2.settimeout(50.5)
        self.client2.bind(('0.0.0.0', 2345))
        self.client1_ip = '127.0.0.1'
        self.client1_port = 2346
        
    

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            
        else:
            self.direction.x = 0

        if keys[pygame.K_UP]:
            self.jump()

        
        datasent = pickle.dumps(self.rect)
        self.client2.sendto(datasent, (self.client1_ip, self.client1_port))
        

            

    def gravity(self):
        self.direction.y += self.grav
        self.rect.y += self.direction.y

    def jump(self):
        if (self.direction.y==0 and self.rect.top != 0): #only allow jumps if y position is stable
            if (not(self.isJump)):
                self.direction.y = self.jump_speed
                self.isJump = True
            else:
                self.isJump = False
        
        


    def update(self):
        self.get_input()
        