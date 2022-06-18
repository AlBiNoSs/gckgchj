from tokenize import group
from turtle import speed
import pygame
import os
from pygame import mixer
pygame.init()
clock = pygame.time.Clock()
mixer.init()
e_img_hit = ["Enemy1_attack_L1.png",
             "Enemy1_attack_L2.png", "Enemy1_attack_L3.png"]
e_img_left = ["Enemy1_walk_L1.png", "Enemy1_walk_L2.png", "Enemy1_walk_L3.png"]
e_img_right = ["Enemy1_walk_R1.png",
               "Enemy1_walk_R2.png", "Enemy1_walk_R3.png"]
e_img_up = ["Enemy1_walk_U1.png", "Enemy1_walk_U2.png", "Enemy1_walk_U3.png"]
e_img_down = ["Enemy1_walk_D1.png", "Enemy1_walk_D2.png", "Enemy1_walk_D3.png"]

img_hit = ["Hero_hit_R1.png", "Hero_hit_R2.png", "Hero_hit_R3.png", "Hero_hit_R4.png"]
img_left = ["Hero_stay_L1.png", "Hero_walk_L1.png",
            "Hero_walk_L1.png", "Hero_walk_L3.png", "Hero_walk_L4.png"]
img_right = ["Hero_stay_R2.png", "Hero_walk_R1.png",
             "Hero_walk_R2.png", "Hero_walk_R3.png", "Hero_walk_R4.png"]
img_up = ["Hero_stay_u1.png", "Hero_walk_u1.png",
          "Hero_walk_u2.png", "Hero_walk_u3.png", "Hero_walk_u4.png"]
img_down = ["Hero_walk0.png", "Hero_walk1.png",
            "Hero_walk2.png", "Hero_walk3.png", "Hero_walk4.png"]
mixer.music.load('City_music.mp3')
mixer.music.set_volume(0.2)
# stationary_d = pygame.image.load(os.path.join("Hero_walk0.png"))
# stationary_u = pygame.image.load(os.path.join("Hero_stay_u1.png"))
# stationary_r = pygame.image.load(os.path.join("Hero_stay_R2.png"))
# stationary_l = pygame.image.load(os.path.join("Hero_stay_L1.png"))

# e_stationary_d = pygame.image.load(os.path.join("Enemy1_walk_D1.png"))
# e_stationary_u = pygame.image.load(os.path.join("Enemy1_walk_U1.png"))
# e_stationary_r = pygame.image.load(os.path.join("Enemy1_walk_R1.png"))
# e_stationary_l = pygame.image.load(os.path.join("Enemy1_walk_L1.png"))
pygame.font.init()
font2 = pygame.font.SysFont("Terminal", 50)
lose = font2.render('GAME OVER!',True, (255,1,0))

move = [True, True, True, True]

window = pygame.display.set_mode((960, 540))
pygame.display.set_caption("Zelda_FM")

bg_img = pygame.image.load("Bg.png")
bg = pygame.transform.scale(bg_img, (1200, 3000))

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y, hit, group, width, height, HP):
        super().__init__(group)
        self.image = player_image
        self.image = pygame.transform.scale(
            pygame.image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.stepIndex = 0
        self.dirrection = pygame.math.Vector2()
        self.hit = hit
        self.HP = HP
        self.move_up = False
        self.move_down = False
        self.move_left = False
        self.move_right = False
        self.time_out_anim = 5
        self.under_attack = False
        self.width = width
        self.height= height
        self.patrol_point1 = True
        self.point_x = True
        self.point_y = True
        self.path = []

    def collide(self, targets):
        global move
        for target in targets:
            if pygame.sprite.spritecollide(self, targets, False):
                if abs(self.rect.top - target.rect.bottom) < 15:
                    move = [True, False,  False, False]
                    self.rect.y += 10
                if abs(self.rect.bottom - target.rect.top) < 25:
                    move = [False, True, False,  False] 
                    self.rect.y -= 10
                if abs(self.rect.left - target.rect.right) < 25:
                    move = [False, False, False, True]
                    self.rect.x += 10
                if abs(self.rect.right - target.rect.left) < 25:
                    move = [False, False, True, False]
                    self.rect.x -= 10
            else:
                move =[ True,True, True, True]

    def setHP(self, target_e):
        #print(target_e.HP)
        target_e.HP = int(target_e.HP)
        target_e.HP -= self.hit
        target_e.under_attack = True
        if target_e.HP <= 0:
            pygame.sprite.Sprite.remove(target_e, camera)

    def getHP(self):
        return self.HP
    def attack(self, target_e):
        if abs(target_e.rect.left - self.rect.right) <= 25 and target_e in camera:
            self.setHP(target_e)
        elif abs(target_e.rect.right - self.rect.left) <= 25 and target_e in camera:
            self.setHP(target_e)
        elif abs(target_e.rect.top - self.rect.bottom) <= 25 and target_e in camera:
            self.setHP(target_e)
        elif abs(target_e.rect.bottom - self.rect.top) <= 25 and target_e in camera:
            self.setHP(target_e)
        else:
            target_e.under_attack = False

    def move(self, speed):
        self.rect.center += self.dirrection * speed
        #print(self.rect.center)

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

class Player(GameSprite):
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.dirrection.y = -2
            self.move_up = True
            self.move_down = False
        elif keys[pygame.K_DOWN]:
            self.dirrection.y = 2
            self.move_up = False
            self.move_down = True
        else:
            self.dirrection.y = 0
            self.move_up = False
            self.move_down = False

        if keys[pygame.K_RIGHT]:
            self.dirrection.x = 2
            self.move_right = True
            self.move_left = False
        elif keys[pygame.K_LEFT]:
            self.dirrection.x = -2
            self.move_left = True
            self.move_right = False
        else:
            self.dirrection.x = 0
            self.move_left = False
            self.move_right = False
        
        if keys[pygame.K_r]:
            self.hit = True
        else:
            self.hit = False

    def move(self, speed):
        self.rect.center += self.dirrection * self.speed
        #print(self.rect.center)

    def update(self):
        self.collide(walls)
        self.input()
        self.move(self.speed)
       #print(self.dirrection)

    def reset(self):
        global render_count, move
        if render_count == 5:
            render_count == 0
        if self.stepIndex >= 4:
            self.stepIndex = 0
        if self.move_left:
            self.image = (pygame.image.load(img_left[self.stepIndex]))
            self.time_out_anim -= 1
            if self.time_out_anim <= 0:
                self.stepIndex += 1
                self.time_out_anim = 5
            move = [False, False, False, True]
        elif self.move_right:
            self.image = (pygame.image.load(img_right[self.stepIndex]))
            self.time_out_anim -= 1
            if self.time_out_anim <= 0:
                self.stepIndex += 1
                self.time_out_anim = 5
            move = [False, False, True, False]
        elif self.move_down:
            self.image = (pygame.image.load(img_down[self.stepIndex]))
            self.time_out_anim -= 1
            if self.time_out_anim <= 0:
                self.stepIndex += 1
                self.time_out_anim = 5
            move = [False, True, False,  False]
        elif self.move_up:
            self.image = (pygame.image.load(img_up[self.stepIndex]))
            self.time_out_anim = 5
            move = [True, False,  False, False]
        elif self.hit:
            self.image = (pygame.image.load(img_hit[self.stepIndex]))
            self.time_out_anim -= 1
            if self.time_out_anim <= 0:
                self.stepIndex += 1
                self.time_out_anim = 5
            move = [False, False,  False, False]
        else:
            if move[0]:
                self.image = (pygame.image.load(img_up[0]))
            elif move[1]:
                self.image = (pygame.image.load(img_down[0]))
            elif move[2]:
                self.image = (pygame.image.load(
                    img_right[0]))
            elif move[3]:
                self.image = (pygame.image.load(
                    img_left[0]))

class Enemy(GameSprite):
    def chase(self, target_e):
        if abs(target_e.rect.left - self.rect.right) <= 205 and self in camera:
            dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,player.rect.y - self.rect.y)
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)
        elif abs(target_e.rect.right - self.rect.left) <= 205 and self in camera:
            dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,player.rect.y - self.rect.y)
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)
        elif abs(target_e.rect.top - self.rect.bottom) <= 205 and self in camera:
            dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,player.rect.y - self.rect.y)
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)
        elif abs(target_e.rect.bottom - self.rect.top) <= 205 and self in camera:
            dirvect = pygame.math.Vector2(player.rect.x - self.rect.x,player.rect.y - self.rect.y)
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)

    def update(self):
        self.collide(walls)
        self.follow(player)
    def follow(self, target_e ):
        if abs(target_e.rect.left - self.rect.right) <= 55 and target_e in camera:
            self.chase(target_e)
        elif abs(target_e.rect.right - self.rect.left) <= 55 and target_e in camera:
            self.chase(target_e)
        elif abs(target_e.rect.top - self.rect.bottom) <= 55 and target_e in camera:
            self.chase(target_e)
        elif abs(target_e.rect.bottom - self.rect.top) <= 55 and target_e in camera:
            self.chase(target_e)
        if abs(target_e.rect.left - self.rect.right) <= 20:
            self.attack(target_e)  

    def patrol(self):
        if self.speed > 0:  # If we are moving right
            if self.rect.x < self.path[1]: # If we have not reached the furthest right point on our path.
                self.rect.x += self.speed
            else: # Change direction and move back the other way
                self.speed = self.speed * -1
                self.rect.x += self.speed
                self.walkCount = 0
        else: # If we are moving left
            if self.rect.x > self.path[0]: # If we have not reached the furthest left point on our path
                self.rect.x += self.speed
            else:  # Change direction
                self.speed = self.speed * -1
                self.rect.x += self.speed
                self.walkCount = 0


    def reset(self):
        global render_count
        if render_count == 5:
            render_count == 0
        if self.stepIndex >= 3:
            self.stepIndex = 0
        if self.move_left:
            if render_count % 5 == 0:
                self.image = e_img_left[self.stepIndex]
                self.stepIndex += 1
        elif self.move_right:
            self.image = e_img_right[self.stepIndex]
            self.stepIndex += 1
        elif self.move_down:
            self.image = e_img_down[self.stepIndex]
            self.stepIndex += 1
        elif self.move_up:
            self.image = e_img_up[self.stepIndex]
            self.stepIndex += 1
        else:
            self.image = e_img_down[0]
        
class Wall(GameSprite):
    def update(self):
        pass
    
class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        self.ground_surf = pygame.image.load("Bg.png").convert_alpha()

        self.ground_surf = pygame.transform.scale(
            self.ground_surf, (2500, 5000))

        self.ground_rect = self.ground_surf.get_rect(bottomleft=(0, 600))
 
    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

    def custom_draw(self, player):

        self.center_target_camera(player)

        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.center):
            #img_rect = sprite.image.get_rect()
            #pygame.draw.rect(window, (255, 0 ,0), img_rect, 4)
            player.reset()
            sprite.image = pygame.transform.scale(sprite.image, (sprite.width, sprite.height))
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

walls = pygame.sprite.Group()
camera = CameraGroup()
enemy = Enemy("Enemy1_walk_D1.png", 4, 1400, 250, 1, camera, 65, 65, 25)
enemy_1 = Enemy("Enemy1_walk_D1.png", 4, 840, -2000, 1, camera, 65, 65, 25)
enemy_2 = Enemy("Enemy1_walk_D1.png", 4, 1020, -2000, 1, camera, 65, 65, 25)
player = Player("Hero_walk0.png", 3, 500, 250, 1, camera, 65, 65, 500)
wall_1 = Wall("no.png", 0, 450, 308, 0, camera, 1100, 10, 1000)
wall_2 = Wall("no.png", 0, 450, 74, 0, camera, 400, 10,1000)
wall_3 = Wall("no.png", 0, 450, 74, 0, camera, 11, 234,1000)
wall_4 = Wall("no.png", 0, 1290, 74, 0, camera, 260, 10,1000)
wall_5 = Wall("no.png", 0, 1290, 74, 0, camera, 260, 10,1000)
wall_6 = Wall("no.png", 0, 850, -2600, 0, camera, 10, 2680,1000)
wall_7 = Wall("no.png", 0, 1290, -2600, 0, camera, 10, 2680,1000)
wall_8 = Wall("no.png", 0, 1550, 74, 0, camera, 11, 234,1000)
wall_9 = Wall("no.png", 0, 1200, -2600, 0, camera, 90, 10,1000)
wall_10 = Wall("no.png", 0, 850, -2600, 0, camera, 200, 10,1000)
wall_11 = Wall("no.png", 0, 1050, -2900, 0, camera, 10, 300,1000)
wall_12 = Wall("no.png", 0, 1200, -2900, 0, camera, 10, 300,1000)
wall_13 = Wall("no.png", 0, 1050, -2900, 0, camera, 150, 10,1000)
walls.add(wall_1 )
walls.add(wall_2 )
walls.add(wall_3 )
walls.add(wall_4 )
walls.add(wall_5 )
walls.add(wall_6 )
walls.add(wall_7 )
walls.add(wall_8 )
walls.add(wall_9 )
walls.add(wall_10)
walls.add(wall_11)
walls.add(wall_12)
walls.add(wall_13)

enemy.path = [1400, 600]
enemy_1.path = [840, 1020]
enemy_2.path = [1020, 1220]


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
print(player.hit)
print(enemy.hit)
print(enemy_1.hit)
print(enemy_2.hit)
for wall in walls:
    print(wall.hit)
render_count = 0
print(walls)
while game:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
    # enemy.update()
    player.collide(walls)
    enemy.collide(walls)
    enemy_1.collide(walls)
    enemy_2.collide(walls)
    
    player.attack(enemy)
    player.attack(enemy_1)
    player.attack(enemy_2)
    enemy.attack(player)
    enemy_1.attack(player)
    enemy_2.attack(player)
    #print(enemy.getHP())
    # camera.center_target_camera(player)
    camera.update()
    camera.custom_draw(player)
    # player.reset()
    # player.update()
    # enemy.reset()
    #for wall in walls:
        #pygame.draw.rect(window, (0,0,150), wall.rect, 5)
    #pygame.draw.rect(window, (0,0,150), player.rect, 5)

    pygame.display.update()
    clock.tick(15)
