import pygame, math, sys, random

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
        self.speed = 90
        self.angle = math.atan2(y -mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
    
    def main(self, display):
        self.x -= int(self.x_vel)
        self.y -= int(self.y_vel)

        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 2)

pygame.init()
display_width = 1440
display_height = 800

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
player_bullets = [] 
player = Player(*display.get_rect().center)
all_sprites = pygame.sprite.Group(player)

run = True
while run:
    clock.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                #fire()
                if mouse_y < 400:
                    #player_bullets.append(PlayerBullet(player.rect.centerx + 50, player.rect.centery + 18, mouse_x, mouse_y))
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
    
    display.fill((255, 255, 255))
    for bullet in player_bullets:
        bullet.main(display)
    all_sprites.draw(display)
    pygame.display.flip()
    pygame.display.update()

pygame.quit()
exit()