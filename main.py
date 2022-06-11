import pygame
import os
pygame.init()

stationary_d = pygame.image.load(os.path.join("Hero_walk0.png"))
stationary_u = pygame.image.load(os.path.join("Hero_stay_u1.png"))
stationary_r = pygame.image.load(os.path.join("Hero_stay_R2.png"))
stationary_l = pygame.image.load(os.path.join("Hero_stay_L1.png"))

move = [True, True, True, True]

window = pygame.display.set_mode((960,540))
pygame.display.set_caption("Zelda_FM")

bg_img = pygame.image.load("Bg.png")
bg = pygame.transform.scale(bg_img,(1200,3000))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, dirrection):
        super().__init__()
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.dirrection = dirrection

class Player():
    def __init__(self, x, y):
        self.images_down = []
        self.images_up = []
        self.images_left = []
        self.images_right = []
        self.index = 0
        self.counter = 0
        for num in range(1 , 5):
            img_down = pygame.image.load(f'Hero_walk{num}.png')
            img_down = pygame.transform.scale(img_down, (60,60))
            img_up = pygame.image.load(f'Hero_walk_u{num}.png')
            img_up = pygame.transform.scale(img_up, (60,60))
            img_left = pygame.image.load(f'Hero_walk_L{num}.png')
            img_left = pygame.transform.scale(img_left, (60,60))
            img_right = pygame.image.load(f'Hero_walk_R{num}.png')
            img_right = pygame.transform.scale(img_right, (60,60))
            self.images_down.append(img_down)
            self.images_up.append(img_up)
            self.images_left.append(img_left)
            self.images_right.append(img_right)
        self.image = self.images_down[self.index]
        self.rect = self.image.get_rect()
        self.rect_x = x
        self.rect_y = y

game = True
width = 1200
height = 600
x = 200
y = 230
step = 10
radius = 15
i = 0
move_left = False
move_right = False
move_down = False
move_up = False

while game:

    window.blit(bg, (i, -3000+600))
    window.blit(bg, (i+width,0))
    window.blit(bg, (i - width, 0))
    if i == -width:
        window.blit(bg, (i, 0))
        i = 0
    if i == width:
        window.blit(bg, (i, 0))
        i = 0

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False

    pygame.display.update()
    pygame.time.delay(50)


       
