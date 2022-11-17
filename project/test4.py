import pygame, math, sys, random
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

def floor(floor_x, floor_y):
    display.blit(floor_image, (floor_x, floor_y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('arrow_up.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 8

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
        self.speed = 100
        self.angle = math.atan2(y -mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 1)

class SoundManagerWalk:
    sounds = [pygame.mixer.Sound('run_concrete1.wav'), pygame.mixer.Sound('run_concrete2.wav'), pygame.mixer.Sound('run_concrete3.wav'), pygame.mixer.Sound('run_concrete4.wav'), pygame.mixer.Sound('run_concrete5.wav'), pygame.mixer.Sound('run_concrete6.wav')]

    @staticmethod
    def playRandom():
        random.choice(SoundManagerWalk.sounds).play()

def walk():
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



pygame.init()
display_width = 1440
display_height = 800

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
display_scroll = [0, 0]
player_bullets = [] 
player = Player(*display.get_rect().center)
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
    
    display.fill((255, 80, 80))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                fire()
                if mouse_y < 400:
                    player_bullets.append(PlayerBullet(player.rect.centerx + 71, player.rect.centery, mouse_x, mouse_y))
                elif mouse_x > 720:
                    player_bullets.append(PlayerBullet(player.rect.centerx, player.rect.centery + 78, mouse_x, mouse_y))
                elif mouse_x < 720:
                    player_bullets.append(PlayerBullet(player.rect.centerx, player.rect.centery - 78, mouse_x, mouse_y))    
                else:
                    player_bullets.append(PlayerBullet(player.rect.centerx - 71, player.rect.centery, mouse_x, mouse_y))

    player.point_at(*pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()
    player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])
    
    #scroll mechanic?
    floor(0 - display_scroll[0], 0 - display_scroll[1])
    
    #test enemy
    pygame.draw.rect(display, (255, 0, 0), (100 - display_scroll[0], 100 - display_scroll[1], 16, 16))


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
    
    display.fill((255, 255, 255))
    for bullet in player_bullets:
        bullet.main(display)
    all_sprites.draw(display)
    #pygame.display.flip()
    clock.tick(60)
    pygame.display.update()

pygame.quit()
exit()