import pickle
import pygame
from Tiles import Tile, WinningTile
from Settings import tile_size, screen_width, screen_height
from Player import Player
import sys
from os import listdir
from os.path import isfile,join

# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# pygame.display.update()


# def flip(sprites):
#         return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

# def load_sheets(dir1, dir2, width, height, direction=False):
#     path = join("animations", dir1, dir2)
#     images = [f for f in listdir(path) if isfile(join(path, f))]

#     all_sprites = {}

#     for image in images:
#         sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

#         sprites = []
#         for i in range(sprite_sheet.get_width() // width):
#             surface2 = pygame.Surface((width, height), pygame.SRCALPHA, 32)
#             rect = pygame.Rect(i * width, 0, width, height)
#             surface2.blit(sprite_sheet, (0,0), rect)
#             sprites.append(pygame.transform.scale2x(surface2))

#         if direction:
#             all_sprites[image.replace(".png", "") + "_right"] = sprites
#             all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
#         else:
#             all_sprites[image.replace(".png", "")] = sprites


class Level:
    
    # SPRITES = load_sheets("chars", "Dude", 32, 32, True)
    def __init__(self, level_structure, surface):
        #level setup
        self.display_surf = surface
        self.setup_level(level_structure)


    
    def setup_level(self, map_num):
        
        
        self.tiles = pygame.sprite.Group()

        self.players = pygame.sprite.Group()    #ADDED THE TWO SPRITES TO A GROUP TO MANAGE THEM TOGETHER
        self.winbound = pygame.sprite.Group()
        
        #nested for loop using enumerate to get the col/row index
        for row_index,row in enumerate(map_num):
            for col_index, cell in enumerate(row):
                if cell== 'X':
                    x= col_index*tile_size
                    y= row_index*tile_size
                    tile = Tile(tile_size, (x,y))
                    self.tiles.add(tile)
                if cell=='P':
                    x= col_index*tile_size
                    y= row_index*tile_size
                    player_sprite = Player((x,y))
                    self.players.add(player_sprite)
                if cell == 'W':
                    x= col_index*tile_size
                    y= row_index*tile_size
                    boundary = WinningTile(tile_size, (x,y))
                    self.winbound.add(boundary)


        global client1_socket
        client1_socket = player_sprite.client1       
                
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
                        print("PLAYER 1 (PINK) WINS")
                        sys.exit()
                        

    # def sprite_colllision(self):
    #     if self.players.sprites()[0].rect.colliderect(self.players.sprites()[1]):
    #         print("PLAYER 1 (M) GOT CAUGHT, PLAYER 2 (C) WINS")
    #         pygame.quit()
    #         sys.exit()
                    
    def fall_off_map(self):
        for player in self.players.sprites():
            if player.rect.top > screen_height:
                if player == self.players.sprites()[0]:
                    pygame.quit()
                    print("PLAYER 1 (PINK) FELL, SO PLAYER 2 (BLUE) WINS")
                    sys.exit()
                elif player == self.players.sprites()[1]:
                    pygame.quit()
                    print("PLAYER 2 (BLUE) FELL, SO PLAYER 1 (PINK) WINS")
                    sys.exit()



    def recvFromNet(self):
        # Get player 2 from client 2
        MAX_RETRIES = 50

        for i in range(MAX_RETRIES):
            try:
                data, addr = client1_socket.recvfrom(16384)
                global player2
                player2 = pickle.loads(data)
                break
            except TimeoutError:
                print("connection ended")
            except ConnectionResetError:
                if i < MAX_RETRIES-1:
                    continue
                else:
                    raise

        rect = player2
        # pygame.draw.rect(self.display_surf, 'green', rect)
        player2image = pygame.image.load("Dude_Monster.png").convert_alpha()
        self.display_surf.blit(player2image, rect)


    def run(self):




        #level tiles
        #self.tiles.update(self.thecam_shift)
        self.tiles.draw(self.display_surf)
        self.winbound.draw(self.display_surf)
        
        self.recvFromNet()
        #player
        # self.player.update()
        # self.player2.update()
        
        self.players.draw(self.display_surf)
        # self.display_surf.blit(sprites[0])
        #self.sprites.draw(self.display_surf)


        # self.begx+=player2.x*6
        # self.begy+=player2.y
        # player2x, player2y = player2
        # rect = pygame.Rect(player2x, player2y, 32, 64)
        # pygame.draw.rect(self.display_surf, (0,255,0), rect)
        # self.begy-=(player2.y)/6
        
        self.barrier()
        self.end_map_collision()
        self.fall_off_map()
        # self.sprite_colllision()
        
        self.horizontal_collision()
        self.vertical_collision()
        self.players.update()
        
        
        
        # self.player2.draw(self.display_surf)

        
        