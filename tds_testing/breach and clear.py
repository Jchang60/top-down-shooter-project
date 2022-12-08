import pygame
import sys
import math
pygame.init()

display = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

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


player = Player(400, 400, 50, 50)

display_scroll = [0,0]

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