import pygame, sys, math, random
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

display = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

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

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def main(self, display):
        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, self.width, self.height))


class PlayerBullet:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x= mouse_x
        self.mouse_y = mouse_y
        self.speed = 10
        self.angle = math.atan2(y-mouse_y, x-mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0,0,255), (self.x, self.y), 5)

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

player = Player(400, 400, 50, 50)

display_scroll = [0,0]

# Background Music
pygame.mixer.music.load('BG_music.wav')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.59)

player_bullets = []
b = pygame.image.load("C:\\Users\jjdd9\Downloads\\box.png")
def box(x,y):
    display.blit(b, (x,y))
while True:
    display.fill((0,0,0))
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.QUIT

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))

    keys = pygame.key.get_pressed()
    
    pygame.draw.rect(display, (255,255,255), (100-display_scroll[0], 100-display_scroll[1], 16, 16))
   
    pygame.draw.rect(display, (0,255,0), (0-display_scroll[0], 0-display_scroll[1], 1800, 5))
    pygame.draw.rect(display, (0,255,0), (0-display_scroll[0], 0-display_scroll[1], 5, 1600))
    pygame.draw.rect(display, (0,255,0), (0-display_scroll[0], 1600-display_scroll[1], 1800, 5))
    pygame.draw.rect(display, (0,255,0), (1800-display_scroll[0], 0-display_scroll[1], 5, 1600))

    box(500, 800)

    if keys[pygame.K_a]:
        display_scroll[0] -= 5
        if display_scroll[0] <= -395:
            display_scroll[0] = -395
    if keys[pygame.K_d]:
        display_scroll[0] += 5
        if display_scroll[0] >= 1350:
            display_scroll[0] = 1350
    if keys[pygame.K_w]:
        display_scroll[1] -= 5
        if display_scroll[1] <= -395:
            display_scroll[1] = -395
    if keys[pygame.K_s]:
        display_scroll[1] += 5
        if display_scroll[1] >= 1150:
            display_scroll[1] = 1150

    player.main(display)


    for bullet in player_bullets:
        bullet.main(display)

    clock.tick(60)
    pygame.display.update()

    print(display_scroll[0])
    print(display_scroll[1])