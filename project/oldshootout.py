import pygame, math, sys, random
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

# Map
def floor(floor_x, floor_y):
    display.blit(floor_image, (floor_x, floor_y))

def walk():
    random_multiple = random.randrange(0, 200)
    if random_multiple <= 33:
        pygame.mixer.Sound.play(run_sound1)
    elif 33 > random_multiple < 66:
        pygame.mixer.Sound.play(run_sound2)
    elif 66 > random_multiple < 99:
        pygame.mixer.Sound.play(run_sound3)
    elif 99 > random_multiple < 133:
        pygame.mixer.Sound.play(run_sound4)
    elif 133 > random_multiple < 166:
        pygame.mixer.Sound.play(run_sound5)
    elif random_multiple > 166:
        pygame.mixer.Sound.play(run_sound6)
    pygame.mixer.fadeout(4500)

# def turn():
#     random_multiple = random.randrange(0, 99)
#     if random_multiple <= 33:
#         pygame.mixer.Sound.play(turn_sound1)
#     elif 33 > random_multiple < 66:
#         pygame.mixer.Sound.play(turn_sound2)
#     else:
#         pygame.mixer.Sound.play(turn_sound3)


def yell():
    random_multiple3 = random.randrange(0, 99)
    if random_multiple3 <= 33:
        pygame.mixer.Sound.play(yell1)
    elif 33 > random_multiple3 < 66:
        pygame.mixer.Sound.play(yell2)
    elif random_multiple3 > 66:
        pygame.mixer.Sound.play(yell3)

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

def reload():
    pygame.mixer.Sound.play(reload1)
    pygame.mixer.Sound.play(reload2)
    pygame.mixer.Sound.play(reload3)
    pygame.time.delay(900)
    pygame.mixer.Sound.play(reload4)
    pygame.time.Clock().tick(1200)
    pygame.mixer.Sound.play(reload5)
    pygame.time.Clock().tick(900)
    pygame.mixer.Sound.play(reload6)
    pygame.time.delay(400)
    pygame.mixer.Sound.play(reload7)
    
player_handgun_walk_images = [pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_0.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_1.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_2.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_3.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_4.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_5.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_6.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_7.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_8.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_9.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_10.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_11.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_12.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_13.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_14.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_15.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_16.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_17.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_18.png"), pygame.image.load("Top_Down_Survivor/handgun/move/survivor-move_handgun_19.png")]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.animation_count = 0
        pygame.sprite.Sprite.__init__(self)
        self.original_image = player_handgun_walk_images[self.animation_count]
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 5
        
    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def move(self, x, y):
        self.rect.move_ip(x * self.velocity, y * self.velocity)
        # self.x = x
        # self.y = y
        # self.width = width
        # self.height = height
    

    def main(self, display):
        if self.animation_count + 1 >= 20:
            self.animation_count = 0
        self.animation_count += 1

        # display.blit(pygame.transform.rotate(player_handgun_walk_images[self.animation_count]), self.angle)

        # pygame.draw.rect(display, (0, 0, 255), (self.x, self.y, self.width, self.height))

class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 90
        self.angle = math.atan2(y -mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 2)

class SoundManagerYell:
    sounds = [pygame.mixer.Sound('[CALL]YellAtSuspect_0.wav'), pygame.mixer.Sound('[CALL]YellAtSuspect_1.wav'), pygame.mixer.Sound('[CALL]YellAtSuspect_2.wav'), pygame.mixer.Sound('[CALL]YellAtCivilian_9.wav')] # list of sound objects

    @staticmethod
    def playRandom():
        random.choice(SoundManagerYell.sounds).play()
    
def yell():
    SoundManagerYell.playRandom()

class SoundManagerReloadYell:
    sounds = [pygame.mixer.Sound('usec3_weap_reload_01.wav'), pygame.mixer.Sound('usec3_weap_reload_02.wav'), pygame.mixer.Sound('usec3_weap_reload_09_bl.wav')] # list of sound objects

    @staticmethod
    def playRandom():
        random.choice(SoundManagerReloadYell.sounds).play()
    
def reloadyell():
    SoundManagerReloadYell.playRandom()
    

#Game Setup

floor_image = pygame.image.load('grid1.png')

# player = Player(400, 300, 32, 32)
player = Player(*display.get_rect().center)
all_sprites = pygame.sprite.Group(player)
all_sprites.draw(display)

display_scroll = [0, 0]

player_bullets = [] 
gunshot_sound = pygame.mixer.Sound('glock17_indoor_close.wav')
shellcasing_sound1 = pygame.mixer.Sound('9mm_shell_concrete1.wav')
shellcasing_sound2 = pygame.mixer.Sound('9mm_shell_concrete2.wav')
shellcasing_sound3 = pygame.mixer.Sound('9mm_shell_concrete3.wav')
run_sound1 = pygame.mixer.Sound('run_concrete1.wav')
run_sound2 = pygame.mixer.Sound('run_concrete2.wav')
run_sound3 = pygame.mixer.Sound('run_concrete3.wav')
run_sound4 = pygame.mixer.Sound('run_concrete4.wav')
run_sound5 = pygame.mixer.Sound('run_concrete5.wav')
run_sound6 = pygame.mixer.Sound('run_concrete6.wav')
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

while True:
    display.fill((80, 80, 80))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    # player.angle = math.atan2(player.y -mouse_y, player.x - mouse_x)
    # pygame.transform.rotate(player_handgun_walk_images[player.animation_count], player.angle)
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                fire()
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))
        #yell
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                yell()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reloadyell()
                reload()

        
        # if event.type == pygame.MOUSEMOTION:
        #     player
    player.point_at(*pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()
    #floor scroll
    floor(0 - display_scroll[0], 0 - display_scroll[1])
    player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])

    #enemy/static object
    pygame.draw.rect(display, (255, 0, 0), (100 - display_scroll[0], 100 - display_scroll[1], 16, 16))

    #player movement
    if keys[pygame.K_a]:
        player.move(-1, 0)
        display_scroll[0] -= 5
        walk()
    if keys[pygame.K_d]:
        player.move(1, 0)
        display_scroll[0] += 5
        walk()
    if keys[pygame.K_w]:
        player.move(0, -1)
        display_scroll[1] -= 5
        walk()
    if keys[pygame.K_s]:
        player.move(0, 1)
        display_scroll[1] += 5
        walk()

    player.main(display)

    for bullet in player_bullets:
        bullet.main(display)

    clock.tick(60)
    pygame.display.update()