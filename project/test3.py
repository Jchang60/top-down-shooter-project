import pygame, math, sys, random
from pygame.math import Vector2
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
import map

# at the beginning: set camera
camera = pygame.math.Vector2((0, 0))
walk_channel = pygame.mixer.Channel(2)
turn_channel = pygame.mixer.Channel(3)

# SFX
class SoundManagerWalk:
    sounds = [pygame.mixer.Sound('run_concrete1.wav'), pygame.mixer.Sound('run_concrete2.wav'), pygame.mixer.Sound('run_concrete3.wav'), pygame.mixer.Sound('run_concrete4.wav'), pygame.mixer.Sound('run_concrete5.wav'), pygame.mixer.Sound('run_concrete6.wav')]

    @staticmethod
    def playRandom():
        random.choice(SoundManagerWalk.sounds).play()

class SoundManagerYell:
    sounds = [pygame.mixer.Sound('[CALL]YellAtSuspect_0.wav'), pygame.mixer.Sound('[CALL]YellAtSuspect_1.wav'), pygame.mixer.Sound('[CALL]YellAtSuspect_2.wav')] # list of sound objects

    @staticmethod
    def playRandom():
        random.choice(SoundManagerYell.sounds).play()
        random.choice(SoundManagerYell.sounds).set_volume(0.72)
    
class SoundManagerReloadYell:
    sounds = [pygame.mixer.Sound('usec3_weap_reload_01.wav'), pygame.mixer.Sound('usec3_weap_reload_02.wav'), pygame.mixer.Sound('usec3_weap_reload_09_bl.wav')] # list of sound objects

    @staticmethod
    def playRandom():
        random.choice(SoundManagerReloadYell.sounds).play()
    
def reloadyell():
    SoundManagerReloadYell.playRandom()

def yell():
    SoundManagerYell.playRandom()


def turn():
    if not turn_channel.get_busy():
        random_multiple = random.randrange(0, 100)
        if random_multiple <= 33:
            pygame.mixer.Sound.play(turn_sound1)
            turn_sound1.set_volume(0.25)
            pygame.mixer.Sound.stop
        
        elif 33 > random_multiple <= 66:
            pygame.mixer.Sound.play(turn_sound2)
            turn_sound2.set_volume(0.25)
            pygame.mixer.Sound.stop
        
        else:
            pygame.mixer.Sound.play(turn_sound3)
            turn_sound3.set_volume(0.25)
            pygame.mixer.Sound.stop
    
# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, pos, walls, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(pygame.image.load('arrow_up.png'), (100, 120))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = pos)
        self.velocity = Vector2(0,0)
        self.pos = Vector2(pos)
        self.walls = walls
        self.camera = Vector2
        
        def update(self):
        self.camera -= self.vel  # Change the camera pos if we're moving.
        # Horizontal movement.
        self.pos.x += self.vel.x
        self.rect.centerx = self.pos.x
        # Change the rect and self.pos coords if we touched a wall.
        for wall in pygame.sprite.spritecollide(self, self.walls, False):
            if self.vel.x > 0:
                self.rect.right = wall.rect.left
            elif self.vel.x < 0:
                self.rect.left = wall.rect.right
            self.pos.x = self.rect.centerx
            self.camera.x += self.vel.x  # Also move the camera back.

        # Vertical movement.
        self.pos.y += self.vel.y
        self.rect.centery = self.pos.y
        for wall in pygame.sprite.spritecollide(self, self.walls, False):
            if self.vel.y > 0:
                self.rect.bottom = wall.rect.top
            elif self.vel.y < 0:
                self.rect.top = wall.rect.bottom
            self.pos.y = self.rect.centery
            self.camera.y += self.vel.y

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, x, y):
        self.rect.move_ip(x * self.velocity, y * self.velocity)

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
    gunshot_sound.set_volume(6.9)
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
    pygame.time.delay(850)
    pygame.mixer.Sound.fadeout(reload3, 900)
    pygame.mixer.Sound.play(reload4)
    pygame.time.Clock().tick(1200)
    pygame.mixer.Sound.play(reload5)
    pygame.time.Clock().tick(900)
    pygame.mixer.Sound.play(reload6)
    pygame.time.delay(400)
    pygame.mixer.Sound.fadeout(reload6, 400)
    pygame.mixer.Sound.play(reload7)


pygame.init()
# Display Settings
display_width = 1300
display_height = 750

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

for rect in ((100, 170, 90, 20), (200, 100, 20, 140),
                (400, 60, 150, 100), (300, 470, 150, 100)):
    walls.add(Wall(*rect))
all_sprites.add(walls)
player = Player((320, 240), walls, all_sprites)

# Background Music
pygame.mixer.music.load('BG_music.wav')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.59)

player_bullets = [] 
#player = Player(*display.get_rect().center)
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

# Main Game Setup
run = True
while run:
# in the main loop: adjust the camera position to center the player
camera.x = player.x - display_width / 2
camera.y = player.y - display_height / 2

mouse_x, mouse_y = pygame.mouse.get_pos()
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        run = False

    # Shooting Mechanic    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            fire()
            player_bullets.append(PlayerBullet(player.rect.center[0], player.rect.center[1], mouse_x, mouse_y))
    
    # Turning Sound Effect
    if event.type == pygame.MOUSEMOTION:
        turn()

    # Yell for Compliance
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_e:
            yell()

    # Reload Yell
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            reloadyell()
            reload()
    
    elif event.type == pg.KEYDOWN:
        if event.key == pg.K_d:
                player.vel.x = 5
        elif event.key == pg.K_a:
                player.vel.x = -5
        elif event.key == pg.K_w:
                player.vel.y = -5
        elif event.key == pg.K_s:
                player.vel.y = 5
    elif event.type == pg.KEYUP:
        if event.key == pg.K_d and player.vel.x > 0:
            player.vel.x = 0
        elif event.key == pg.K_a and player.vel.x < 0:
            player.vel.x = 0
        elif event.key == pg.K_w and player.vel.y < 0:
            player.vel.y = 0
        elif event.key == pg.K_s and player.vel.y > 0:
            player.vel.y = 0

    all_sprites.update()

    screen.fill((30, 30, 30))
    for sprite in all_sprites:
        # Add the player's camera offset to the coords of all sprites.
        screen.blit(sprite.image, sprite.rect.topleft+player.camera)

    pg.display.flip()
    clock.tick(30)

player.point_at(*pygame.mouse.get_pos())
keys = pygame.key.get_pressed()
player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])

#test enemy(not working)
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
display.fill((71, 71, 71))
for bullet in player_bullets:
    bullet.main(display)
all_sprites.draw(display)
pygame.display.flip()
clock.tick(60)
pygame.display.update()

pygame.quit()
exit()