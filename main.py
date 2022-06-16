import pygame
import os
pygame.init()
clock = pygame.time.Clock()

e_img_hit = ["Enemy1_attack_L1.png","Enemy1_attack_L2.png","Enemy1_attack_L3.png"]
e_img_left = ["Enemy1_walk_L1.png", "Enemy1_walk_L2.png", "Enemy1_walk_L3.png" ]
e_img_right = ["Enemy1_walk_R1.png", "Enemy1_walk_R2.png", "Enemy1_walk_R3.png"]
e_img_up = ["Enemy1_walk_U1.png", "Enemy1_walk_U2.png", "Enemy1_walk_U3.png"]
e_img_down = ["Enemy1_walk_D1.png", "Enemy1_walk_D2.png", "Enemy1_walk_D3.png"]

img_hit = ["Hero_hit_R1","Hero_hit_R2","Hero_hit_R3","Hero_hit_R4"]
img_left = ["Hero_stay_L1.png", "Hero_walk_L1.png", "Hero_walk_L2.png", "Hero_walk_L3.png", "Hero_walk_L4.png" ]
img_right = ["Hero_stay_R2.png", "Hero_walk_R1.png", "Hero_walk_R2.png", "Hero_walk_R3.png", "Hero_walk_R4.png" ]
img_up = ["Hero_stay_u1.png", "Hero_walk_u1.png", "Hero_walk_u2.png", "Hero_walk_u3.png", "Hero_walk_u4.png" ]
img_down = ["Hero_walk0.png", "Hero_walk1.png", "Hero_walk2.png", "Hero_walk3.png", "Hero_walk4.png" ]

#stationary_d = pygame.image.load(os.path.join("Hero_walk0.png"))
#stationary_u = pygame.image.load(os.path.join("Hero_stay_u1.png"))
#stationary_r = pygame.image.load(os.path.join("Hero_stay_R2.png"))
#stationary_l = pygame.image.load(os.path.join("Hero_stay_L1.png"))

#e_stationary_d = pygame.image.load(os.path.join("Enemy1_walk_D1.png"))
#e_stationary_u = pygame.image.load(os.path.join("Enemy1_walk_U1.png"))
#e_stationary_r = pygame.image.load(os.path.join("Enemy1_walk_R1.png"))
#e_stationary_l = pygame.image.load(os.path.join("Enemy1_walk_L1.png"))

move = [True, True, True, True]

window = pygame.display.set_mode((960,540))
pygame.display.set_caption("Zelda_FM")

bg_img = pygame.image.load("Bg.png")
bg = pygame.transform.scale(bg_img,(1200,3000))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, hit):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65,65)) 
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.stepIndex = 0
        self.dirrection = pygame.math.Vector2()
        self.hit = hit
        self.HP = 100
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.time_out_anim = 5
    
    def setHP(self, target_e):
        target_e.HP -= self.hit
        if target_e.HP <= 0:
            target_e.kill()

    def getHP(self):
        return self.HP

    def attack(self, target_e):
        if abs(target_e.rect.left - self.rect.right) <= 20:
           self.setHP(target_e)
        elif abs(target_e.rect.right - self.rect.left) <= 20:
           self.setHP(target_e)
        elif abs(target_e.rect.top - self.rect.bottom) <= 20:
            self.setHP(target_e)
        elif abs(target_e.rect.bottom - self.rect.top) <= 20:
            self.setHP(target_e)  

    def move(self, speed):
        self.rect.center += self.dirrection * speed
        print(self.rect.center)

            
class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

class Player(GameSprite):
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.dirrection.y = -1
            self.move_up = True
            self.move_down = False
        elif keys[pygame.K_DOWN]:
            self.dirrection.y = 1
            self.move_up = False
            self.move_down = True
        else:
            self.dirrection.y = 0
            self.move_up = False
            self.move_down = False

        if keys[pygame.K_RIGHT]:
            self.dirrection.x = 1
            self.move_right = True
            self.move_left = False
        elif keys[pygame.K_LEFT]:
            self.dirrection.x = -1
            self.move_left = True
            self.move_right = False
        else:
            self.dirrection.x = 0
            self.move_left = False
            self.move_right = False

    def move(self, speed):
        self.rect.center += self.dirrection * speed
        print(self.rect.center)

    def update(self):
        self.input()
        self.move(self.speed)
        print(self.dirrection)

    def reset(self):
        global render_count, move
        if render_count == 5:
            render_count == 0
        if self.stepIndex >= 3:
            self.stepIndex = 0
        if self.move_left:
            window.blit(pygame.image.load(
                img_left[self.stepIndex]), (self.rect.x, self.rect.y))
            self.time_out_anim -= 1
            if self.time_out_anim <= 0:
                self.stepIndex += 1
                self.time_out_anim = 5
            move = [False, False, False, True]
        elif self.move_right:
            window.blit(pygame.image.load(
                img_right[self.stepIndex]), (self.rect.x, self.rect.y))
            self.time_out_anim -= 1
            if self.time_out_anim <= 0:
                self.stepIndex += 1
                self.time_out_anim = 5
            move = [False, False, True, False]
        elif self.move_down:
            window.blit(pygame.image.load(
                img_down[self.stepIndex]), (self.rect.x, self.rect.y))
            self.time_out_anim -= 1
            if self.time_out_anim <= 0:
                self.stepIndex += 1
                self.time_out_anim = 5
            move = [False, True, False,  False]
        elif self.move_up:
            window.blit(pygame.image.load(
                img_up[self.stepIndex]), (self.rect.x, self.rect.y))
            self.time_out_anim -= 1
            if self.time_out_anim <= 0:
                self.stepIndex += 1
                self.time_out_anim = 5
            move = [True, False,  False, False]
        else:
            if move[0]:
                window.blit(pygame.image.load(
                    img_up[0]), (self.rect.x, self.rect.y))
            elif move[1]:
                window.blit(pygame.image.load(
                    img_down[0]), (self.rect.x, self.rect.y))
            elif move[2]:
                window.blit(pygame.image.load(
                    img_right[0]), (self.rect.x, self.rect.y))
            elif move[3]:
                window.blit(pygame.image.load(
                    img_left[0]), (self.rect.x, self.rect.y))


class Enemy(GameSprite):
       def reset(self):
        global render_count
        if render_count == 5:
            render_count == 0
        if self.stepIndex >= 3:
            self.stepIndex = 0
        if move_left:
            if render_count % 5 == 0:
                window.blit(pygame.image.load(
                    img_left[self.stepIndex]), (self.rect.x, self.rect.y))
                self.stepIndex += 1
        elif move_right:
            window.blit(pygame.image.load(
                img_right[self.stepIndex]), (self.rect.x, self.rect.y))
            self.stepIndex += 1
        elif move_down:
            window.blit(pygame.image.load(
                img_down[self.stepIndex]), (self.rect.x, self.rect.y))
            self.stepIndex += 1
        elif move_up:
            window.blit(pygame.image.load(
                img_up[self.stepIndex]), (self.rect.x, self.rect.y))
            self.stepIndex += 1
        else:
            if move[0]:
                window.blit(pygame.image.load(
                    img_up[0]), (self.rect.x, self.rect.y))
            elif move[1]:
                window.blit(pygame.image.load(
                    img_down[0]), (self.rect.x, self.rect.y))
            elif move[2]:
                window.blit(pygame.image.load(
                    img_right[0]), (self.rect.x, self.rect.y))
            elif move[3]:
                window.blit(pygame.image.load(
                    img_left[0]), (self.rect.x, self.rect.y))


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


enemy = GameSprite("Enemy1_walk_D1.png", 3, 550, 300, 0)
player = Player("Hero_walk0.png", 3, 500, 300, 0)
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
    #enemy.update()
    #enemy.reset()
    camera.box_target_camera(player)
    camera.custom_draw(player)
    player.reset()
    player.update()
    pygame.display.update()
    clock.tick(15)



       
