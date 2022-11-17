import pygame

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


pygame.init()
display_width = 1440
display_height = 800

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()

player = Player(*display.get_rect().center)
all_sprites = pygame.sprite.Group(player)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    player.point_at(*pygame.mouse.get_pos())
    keys = pygame.key.get_pressed()
    player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])

    display.fill((255, 255, 255))
    all_sprites.draw(display)
    pygame.display.flip()

pygame.quit()
exit()