import pygame
import os
pygame.init()
clock = pygame.time.Clock()

img_hit = ["Hero_hit_R1","Hero_hit_R2","Hero_hit_R3","Hero_hit_R4"]
img_left = ["Hero_stay_L1.png", "Hero_walk_L1.png", "Hero_walk_L2.png", "Hero_walk_L3.png", "Hero_walk_L4.png" ]
img_right = ["Hero_stay_R2.png", "Hero_walk_R1.png", "Hero_walk_R2.png", "Hero_walk_R3.png", "Hero_walk_R4.png" ]
img_up = ["Hero_stay_u1.png", "Hero_walk_u1.png", "Hero_walk_u2.png", "Hero_walk_u3.png", "Hero_walk_u4.png" ]
img_down = ["Hero_walk0.png", "Hero_walk1.png", "Hero_walk2.png", "Hero_walk3.png", "Hero_walk4.png" ]

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
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65,65)) 
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.stepIndex = 0
        self.dirrection = pygame.math.Vector2()

    def input(self):
        keys = pygame.key.get_pressed()
        global move_up
        global move_down
        global move_left
        global move_right
        if keys[pygame.K_UP]:
            self.dirrection.y = -1
            move_up = True
            move_down = False
        elif keys[pygame.K_DOWN]:
            self.dirrection.y = 1
            move_up = False
            move_down = True
        else:
            self.dirrection.y = 0
            move_up = False
            move_down = False


        if keys[pygame.K_RIGHT]:
            self.dirrection.x = 1
            move_right = True
            move_left = False
        elif keys[pygame.K_LEFT]:
            self.dirrection.x = -1
            move_left = True
            move_right = False
        else:
            self.dirrection.x = 0
            move_left = False
            move_right = False
    
    def move(self, speed):
        self.rect.center += self.dirrection * speed
        print(self.rect.center)

    def update(self):
        self.input()
        self.move(self.speed)
        print(self.dirrection)

    def reset(self):
        global render_count
        if render_count == 5: render_count == 0
        if self.stepIndex >= 3:
            self.stepIndex = 0
        if move_left:
            if render_count % 5 == 0:
                window.blit(pygame.image.load(img_left[self.stepIndex]), (self.rect.x, self.rect.y))
                self.stepIndex +=1
        elif move_right:
            window.blit(pygame.image.load(img_right[self.stepIndex]), (self.rect.x, self.rect.y))
            self.stepIndex +=1
        elif move_down:
            window.blit(pygame.image.load(img_down[self.stepIndex]), (self.rect.x, self.rect.y))
            self.stepIndex +=1
        elif move_up:
            window.blit(pygame.image.load(img_up[self.stepIndex]), (self.rect.x, self.rect.y))
            self.stepIndex +=1
        else:
            if move[0]:
                 window.blit(stationary_u, (self.rect.x, self.rect.y))
            if move[1]:
                window.blit(stationary_d, (self.rect.x, self.rect.y))
            if move[2]:
                window.blit(stationary_d, (self.rect.x, self.rect.y))
            if move[3]:
                window.blit(stationary_d, (self.rect.x, self.rect.y))
            
class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

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

    def reset(self):
        if self.stepIndex >= 3:
            self.stepIndex = 0
        if move_left:
            window.blit(img_left[self.stepIndex], (self.rect_x, self.rect_y))
            self.stepIndex +=1
        elif move_right:
            window.blit(img_right[self.stepIndex], (self.rect_x, self.rect_y))
            self.stepIndex +=1
        elif move_right:
            window.blit(img_down[self.stepIndex], (self.rect_x, self.rect_y))
            self.stepIndex +=1
        elif move_right:
            window.blit(img_up[self.stepIndex], (self.rect_x, self.rect_y))
            self.stepIndex +=1
        else:
            if move[0]:
                 window.blit(stationary_u, (self.rect_x, self.rect_y))
            if move[1]:
                window.blit(stationary_d, (self.rect_x, self.rect_y))
            if move[2]:
                window.blit(stationary_d, (self.rect_x, self.rect_y))
            if move[3]:
                window.blit(stationary_d, (self.rect_x, self.rect_y))

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders["left"] + self.camera_borders["right"])
        h = self.display_surface.get_size()[0] - (self.camera_borders["top"] + self.camera_borders["bottom"])
        self.camera_rect = pygame.Rect(l,t,w,h)

        self.ground_surf = pygame.image.load("Bg.png").convert_alpha()
        self.ground_surf = pygame.transform.scale(self.ground_surf, (1200,2400)) #self.half_width,-3000 + self.display_surface.get_size()[0], 1200, 3000))
        self.ground_rect = self.ground_surf.get_rect(bottomleft = (0,600))
    
    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx- self.half_width
        self.offset.y = target.rect.centery- self.half_height
    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, target):

        self.center_target_camera(target)

        ground_offset = self.ground_rect.topleft - self.offset*2
        self.display_surface.blit(self.ground_surf, ground_offset)


player = GameSprite("Hero_walk0.png", 3, 500, 300, 0)
camera = CameraGroup()

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

render_count = 0

while game:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
    
    camera.box_target_camera(player)
    camera.custom_draw(player)
    player.reset()
    player.update()
    pygame.display.update()
    clock.tick(15)



       
