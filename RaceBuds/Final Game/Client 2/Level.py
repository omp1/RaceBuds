import pickle
import pygame
from Tiles import Tile, WinningTile
from Settings import tile_size, screen_width, screen_height

from Player import Player2
import sys

class Level:
    def __init__(self, level_structure, surface):
        #level setup
        self.display_surf = surface
        self.setup_level(level_structure)

    
        

    def setup_level(self, map_num):
        self.tiles = pygame.sprite.Group()
        # self.player = pygame.sprite.GroupSingle()
        # self.player2 = pygame.sprite.GroupSingle()

        self.players = pygame.sprite.Group()    
        self.winbound = pygame.sprite.Group()
        
        #nested for loop using enumerate to get the col/row index
        for row_index,row in enumerate(map_num):
            for col_index, cell in enumerate(row):
                if cell== 'X':
                    #multiply index by tile size pixels to find location to place tile
                    x= col_index*tile_size
                    y= row_index*tile_size
                    tile = Tile(tile_size, (x,y))
                    self.tiles.add(tile)
                if cell=='U':
                    x= col_index*tile_size
                    y= row_index*tile_size
                    player_sprite2 = Player2((x,y))
                    self.players.add(player_sprite2)
                if cell == 'W':
                    x= col_index*tile_size
                    y= row_index*tile_size
                    boundary = WinningTile(tile_size, (x,y))
                    self.winbound.add(boundary)

        global client2_socket
        client2_socket = player_sprite2.client2


        
                
    def barrier(self):
        for player in self.players.sprites():
            if player == self.players.sprites()[0]:
                player_x = player.rect.centerx #track x coordinate of player
                direction_x = player.direction.x

                if player_x < 0 and direction_x < 0: #direction < 0 means left
                    player.speed = 0
                elif player_x > screen_width and direction_x >0:
                    player.speed = 0
                else:
                    player.speed = 4     



    def horizontal_collision(self):
        #player = self.player.sprite
        for player in self.players.sprites():

            player.rect.x += player.direction.x*player.speed
            
            

            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.x < 0:
                        player.rect.left = sprite.rect.right
                    elif player.direction.x > 0:
                        player.rect.right = sprite.rect.left
                    #if player.direction.y >0:

                    

    def vertical_collision(self):
        #player = self.player.sprite
        #player.rect.x += player.direction.x*player.speed
        for player in self.players.sprites():
            player.gravity()
            for sprite in self.tiles.sprites():
                if sprite.rect.colliderect(player.rect):
                    if player.direction.y < 0:
                        player.rect.top = sprite.rect.bottom
                        player.direction.y = 0
                    elif player.direction.y > 0:
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0


    
    def end_map_collision(self):
        for player in self.players.sprites():
            for sprite in self.winbound.sprites():
                if player == self.players.sprites()[0]:
                    if sprite.rect.colliderect(player.rect):
                        pygame.quit()
                        print("PLAYER 2 (BLUE) WINS")
                        sys.exit()
                        

                    
    def fall_off_map(self):
        for player in self.players.sprites():
            if player.rect.top > screen_height:
                if player == self.players.sprites()[0]:
                    pygame.quit()
                    print("PLAYER 2 (BLUE) FELL, SO PLAYER 1 (PINK) WINS")
                    sys.exit()
                elif player == self.players.sprites()[1]:
                    pygame.quit()
                    print("PLAYER 1 (PINK) FELL, SO PLAYER 2 (BLUE) WINS")
                    sys.exit()

    def recvFromNet(self):
        # Get player 2 from client 2
    
        try:
            data, addr = client2_socket.recvfrom(16384)
            global player1
            player1 = pickle.loads(data)
            
            
        except TimeoutError:
            print("connection ended")
        rect= player1
        player1image = pygame.image.load("Pink_Monster.png").convert_alpha()
        self.display_surf.blit(player1image, rect)
        

    def run(self):
        #level tiles
        self.tiles.draw(self.display_surf)
        self.winbound.draw(self.display_surf)
        
        self.barrier()
        self.end_map_collision()
        self.fall_off_map()
        # self.sprite_colllision()
        
        self.horizontal_collision()
        self.vertical_collision()

        self.players.draw(self.display_surf)
        self.players.update()
        self.recvFromNet()
        # rect= player1
        # pygame.draw.rect(self.display_surf, 'red', rect)
        
        # self.player.draw(self.display_surf)
        # self.player2.draw(self.display_surf)
        

        