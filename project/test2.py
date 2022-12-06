import pygame, math, sys, random
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
import map

# at the beginning: set camera
camera = pygame.math.Vector2((0, 0))
walk_channel = pygame.mixer.Channel(2)

class SoundManagerWalk:
    sounds = [pygame.mixer.Sound('run_concrete1.wav'), 
              pygame.mixer.Sound('run_concrete2.wav'), 
              pygame.mixer.Sound('run_concrete3.wav'), 
              pygame.mixer.Sound('run_concrete4.wav'), 
              pygame.mixer.Sound('run_concrete5.wav'), 
              pygame.mixer.Sound('run_concrete6.wav')]

    @staticmethod
    def playRandom():
        random.choice(SoundManagerWalk.sounds).play()

class SoundManagerYell:
    sounds = [pygame.mixer.Sound('[CALL]YellAtSuspect_0.wav'), 
              pygame.mixer.Sound('[CALL]YellAtSuspect_1.wav'), 
              pygame.mixer.Sound('[CALL]YellAtSuspect_2.wav'), 
              pygame.mixer.Sound('[CALL]YellAtCivilian_9.wav')] # list of sound objects

    @staticmethod
    def playRandom():
        random.choice(SoundManagerYell.sounds).play()
    
def yell():
    SoundManagerYell.playRandom()

# def floor(floor_x, floor_y):
#     display.blit(floor_image, (floor_x, floor_y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(pygame.image.load('arrow_up.png'), (100, 120))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 6
        pos_on_the_screen = (self.x - camera.x, self.y - camera.y)

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, x, y):
        self.rect.move_ip(x * self.velocity, y * self.velocity)

# class Handgun():
#      def __init__(self, x, y):
#         self.x = player.image.get_rect()[0]
#         self.y = player.image.get_rect()[1]
#         self.mag_capacity = 17

#      def main(self, display):
#         self.x = player.rect[0]
#         self.y = player.rect[1]

class PlayerBullet():
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 99
        self.angle = math.atan2(y -mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    
    def main(self, display):
        self.x -= float(self.x_vel)
        self.y -= float(self.y_vel)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 1)



def walk():
    if not walk_channel.get_busy():
        SoundManagerWalk.playRandom()

def fire():
    pygame.mixer.Sound.play(gunshot_sound)
    pygame.time.Clock().tick(1000)
    random_multiple1 = random.randrange(0, 99)
    if random_multiple1 <= 33:
        pygame.mixer.Sound.play(shellcasing_sound1)
    elif 33 > random_multiple1 < 66:
        pygame.mixer.Sound.play(shellcasing_sound2)
    elif random_multiple1 > 66:
        pygame.mixer.Sound.play(shellcasing_sound3)

class Enemy():
    def __init__(self, x, y, mode, dist, walk=3):
        #mode 0 = vertical
        #mode 1 = horizontal
        self.x = x
        self.y = y
        self.walk = walk
        self.mode = mode
        self.dist = dist
        self.hp = 100
        self.counter = 0
    
    def main(self, display):
        if self.mode == 0:
            self.y += self.walk
            self.counter += 1
            if self.counter >= self.dist:
                self.counter = 0
                self.walk *= -1
        if self.mode == 1:
            self.x += self.walk
            self.counter += self.walk
            if self.counter >= self.dist:
                self.counter = 0
                self.walk *= -1
                
        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, 16, 16), 1)
'''  
    def advanced_movement(self, display, hlist, vlist):
        if self.mode == 0:
            self.y += self.walk
            self.counter += 1
            if self.counter >= self.dist:
                self.counter = 0
                self.walk *= -1
        if self.mode == 1:
            self.x += self.walk
            self.counter += self.walk
            if self.counter >= self.dist:
                self.counter = 0
                self.walk *= -1
                
        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, 16, 16), 1)
        
'''
        
pygame.init()
display_width = 1600
display_height = 900

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
#display_scroll = [0, 0]
player_bullets = [] 
player = Player(*display.get_rect().center)

enemy1 = Enemy(100, 100, 0, 200)

all_sprites = pygame.sprite.Group(player)

#background
floor_image = pygame.image.load('grid1.png')
#sound effects
gunshot_sound = pygame.mixer.Sound('glock17_indoor_close.wav')
shellcasing_sound1 = pygame.mixer.Sound('9mm_shell_concrete1.wav')
shellcasing_sound2 = pygame.mixer.Sound('9mm_shell_concrete2.wav')
shellcasing_sound3 = pygame.mixer.Sound('9mm_shell_concrete3.wav')
turn_sound1 = pygame.mixer.Sound('turn_tile_01.wav')
turn_sound2 = pygame.mixer.Sound('turn_tile_02.wav')
turn_sound3 = pygame.mixer.Sound('turn_tile_03.wav')
yell1 = pygame.mixer.Sound('[CALL]YellAtSuspect_0.wav')
yell2 = pygame.mixer.Sound('[CALL]YellAtSuspect_1.wav')
yell3 = pygame.mixer.Sound('[CALL]YellAtSuspect_2.wav')
yelllist = [pygame.mixer.Sound('[CALL]YellAtSuspect_0.wav'), pygame.mixer.Sound('[CALL]YellAtSuspect_1.wav'), pygame.mixer.Sound('[CALL]YellAtSuspect_2.wav')]
reload1 = pygame.mixer.Sound('weap_mag_shaftlock.wav')
reload2 = pygame.mixer.Sound('weap_magrelease_button.wav')
reload3 = pygame.mixer.Sound('weap_magout_plastic.wav')
reload4 = pygame.mixer.Sound('weap_magdrop_plastic.wav')
reload5 = pygame.mixer.Sound('weap_magin_rig.wav')
reload6 = pygame.mixer.Sound('weap_magin_plastic.wav')
reload7 = pygame.mixer.Sound('weap_round_in_chamber_mag.wav')


run = True
while run:
    # in the main loop: adjust the camera position to center the player
    camera.x = player.x - display_width / 2
    camera.y = player.y - display_height / 2
    
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                fire()
                player_bullets.append(PlayerBullet(player.rect.center[0], player.rect.center[1], mouse_x, mouse_y))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                yell()

    player.point_at(*pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()
    player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])
    
    #scroll mechanic?
    #floor(0 - display_scroll[0], 0 - display_scroll[1])
    
    #test enemy
    pygame.draw.rect(display, (255, 0, 0), (100 - camera[0], 100 - camera[1], 16, 16))


    if keys[pygame.K_a]:
        walk()
    if keys[pygame.K_d]:
        walk()
    if keys[pygame.K_w]:
        walk()
    if keys[pygame.K_s]:
        walk()
    
    # display.fill((255, 255, 255))
    display.fill((69, 69, 69))
    for bullet in player_bullets:
        bullet.main(display)
    all_sprites.draw(display)
    enemy1.main(display)
    pygame.display.flip()
    clock.tick(60)
    pygame.display.update()

pygame.quit()
exit()