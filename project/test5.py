import pygame, math, sys, random
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
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100
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
    
    def move(camera, x, y):
        
        if camera.rect.x < 0:
            camera.rect.x = 0
        if camera.rect.y < 0:
            camera.rect.y = 0
        if camera.rect.x > 1175:
            camera.rect.x = 1175
        if camera.rect.y > 620:
            camera.rect.y = 620

        camera.rect.move_ip(x * camera.velocity, y * camera.velocity)


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
            self.counter += 1
            if self.counter >= self.dist:
                self.counter = 0
                self.walk *= -1
        
        if not self.hp <= 0:        
            pygame.draw.rect(display, (255, 0, 0), (self.x - 12.5, self.y - 12.5, 25, 25), True)
            
            if self.counter % 25 == 0 and not player.hp <= 0:
                rando = random.randint(0, 3)
                if rando == 0:
                    enemy_bullets.append(EnemyBullet(enemy.x, enemy.y, player.rect.center[0], player.rect.center[1]))
        

class EnemyBullet():
    def __init__(self, x, y, player_x, player_y):
        self.x = x
        self.y = y
        self.player_x = player_x
        self.player_y = player_y
        self.speed = 7.5
        self.angle = math.atan2(y - player_y, x - player_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    
    def main(self, display):
        self.x -= float(self.x_vel)
        self.y -= float(self.y_vel)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 3)

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

# camera_group = pygame.sprite.Group()

# Background Music

player_bullets = [] 
player = Player(*display.get_rect().center)
enemy_bullets = []
all_sprites = pygame.sprite.Group(player)

enemy1 = Enemy(100, 100, 0, 200)
enemy2 = Enemy(550, 250, 1, 150)
enemy3 = Enemy(350, 550, 1, 100)
enemy4 = Enemy(200, 200, 0, 50)
enemies_list = [enemy1, enemy2, enemy3, enemy4]

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
color = (71, 71, 71)
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

    player.point_at(*pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()
    player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])
    
    if keys[pygame.K_a]:
        walk()
    if keys[pygame.K_d]:
        walk()
    if keys[pygame.K_w]:
        walk()
    if keys[pygame.K_s]:
        walk()
    
    # display.fill((255, 255, 255))
    display.fill(color)
    for bullet in player_bullets:
        bullet.main(display)
    for bullet in enemy_bullets:
        bullet.main(display)
    if not player.hp <= 0:
        all_sprites.draw(display)
    for enemy in enemies_list:
        enemy.main(display)
    
    for bullet in player_bullets:
        for enemy in enemies_list:
            if abs(bullet.x - enemy.x) <= 50 and abs(bullet.y - enemy.y) <= 50:
                enemy.hp -= 25
                break
    
    for bullet in enemy_bullets:
        if abs(bullet.x - (player.rect.center[0] + 100)) <= 200 and abs(bullet.y - (player.rect.center[1] + 50)) <= 200:
            color = (255, 0, 0)
            enemy_bullets.remove(bullet)
            player.hp -= 10
            
        else:
            if not player.hp <= 0:
                color = (71, 71, 71)
    pygame.display.flip()
    clock.tick(60)
    pygame.display.update()

pygame.quit()
exit()