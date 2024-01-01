import pygame
import socket
import pickle

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32,32))
        
        self.image = pygame.image.load("Pink_Monster.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)


        self.client1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client1.settimeout(100.50)
        self.client1.bind(('0.0.0.0', 2346))
        self.client2_ip = '127.0.0.1'
        self.client2_port = 2345
        


        self.direction = pygame.math.Vector2(0,0)
        self.speed = 4
        self.grav = 1.0
        self.jump_speed = -13
        self.isJump = False

    def get_input(self):
        keys = pygame.key.get_pressed()

        
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.jump()

        datasent = pickle.dumps(self.rect)
        self.client1.sendto(datasent, (self.client2_ip, self.client2_port))

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
        