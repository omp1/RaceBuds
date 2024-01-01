import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        self.image = pygame.Surface((size,size))

        #CAN add a sprite sheet here for the tile
        self.image.fill('white')
        self.image = pygame.image.load("x2.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift

class WinningTile(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        self.image = pygame.Surface((size,size), pygame.SRCALPHA)

        #CAN add a sprite sheet here for the tile
        #self.image.fill((255,255,255,0))
        self.image = pygame.image.load("checker.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        self.rect.x += x_shift