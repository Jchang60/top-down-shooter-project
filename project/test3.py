import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load('arrow_up.png')
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))
        self.angle = 0
        self.direction = pygame.Vector2(1,0)
        self.velocity = 8

    def point_at(self, x, y):
        direction = pygame.math.Vector2(x, y) - self.rect.center
        angle = direction.angle_to((0, -1))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, x, y):
        self.rect.move_ip(x * self.velocity, y * self.velocity)

    def update(self, events, dt):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.groups()[0].add(Bullet(self.rect.center, self.direction.normalize()))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.angle += 3
        if pressed[pygame.K_d]:
            self.angle -= 3

        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def fire_weapon(self):
        return Bullet(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
#  class Handgun:
#      def __init__(self, x, y)
#          self.x = player.rect[0]
#          self.y = player.rect[1]
#          self.mag_capacity = 17

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, pygame.Color('orange'), (4, 4), 4)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, events, dt):
        self.pos += self.direction * dt
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()

def main():
    pygame.init()
    display_width = 1440
    display_height = 800
    display = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()
    dt = 0
    player = Player(*display.get_rect().center)
    all_sprites = pygame.sprite.Group(player)
    player_group = pygame.sprite.Group()
    player_group.add(player)

    bullet_group = pygame.sprite.Group()


#display_scroll = [0, 0]

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
                    bullet_group.add(player.fire_weapon())
        
        player.point_at(*pygame.mouse.get_pos())
        keys = pygame.key.get_pressed()
        player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])    

        display.fill((80, 80, 80))
        player_group.draw(display)
        bullet_group.draw(display)
        player_group.update()
        bullet_group.update()
        all_sprites.draw(display)
        pygame.display.flip()    
    

        #display(0 - display_scroll[0], 0 - display_scroll[1])
        player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])
        #enemy/static object
        #pygame.draw.rect(display, (255, 0, 0), (100 - display_scroll[0], 100 - display_scroll[1], 16, 16))    

        # #player movement
        # if keys[pygame.K_a]:
        #     display_scroll[0] -= 5
        #     #walk()
        # if keys[pygame.K_d]:
        #     display_scroll[0] += 5
        #     #walk()
        # if keys[pygame.K_w]:
        #     display_scroll[1] -= 5
        #     #walk()
        # if keys[pygame.K_s]:
        #     display_scroll[1] += 5
        #     #walk()    

        dt = clock.tick(60)
        pygame.display.update()  

    if __name__ == '__main__':
        main()
    pygame.quit()
    exit()    
    

    # while True:
    #     display.fill((80, 80, 80))    

    #     mouse_x, mouse_y = pygame.mouse.get_pos()
    #     # player.angle = math.atan2(player.y -mouse_y, player.x - mouse_x)
    #     # pygame.transform.rotate(player_handgun_walk_images[player.animation_count], player.angle)
       
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             sys.exit()
    #             pygame.QUIT    

    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             if event.button == 1:
    #                 fire()
    #                 player_bullets.append(PlayerBullet(player.x, player.y, mouse_x, mouse_y))
    #         #yell
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_e:
    #                 yell()    

    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_r:
    #                 reloadyell()
    #                 reload()    

            
    #         # if event.type == pygame.MOUSEMOTION:
    #         #     player
    #     player.point_at(*pygame.mouse.get_pos())
    #     keys = pygame.key.get_pressed()
    #     #floor scroll
    #     floor(0 - display_scroll[0], 0 - display_scroll[1])
    #     player.move(keys[pygame.K_d]-keys[pygame.K_a], keys[pygame.K_s]-keys[pygame.K_w])    

    #     #enemy/static object
    #     pygame.draw.rect(display, (255, 0, 0), (100 - display_scroll[0], 100 - display_scroll[1], 16, 16))    

    #     #player movement
    #     if keys[pygame.K_a]:
    #         player.move(-1, 0)
    #         display_scroll[0] -= 5
    #         walk()
    #     if keys[pygame.K_d]:
    #         player.move(1, 0)
    #         display_scroll[0] += 5
    #         walk()
    #     if keys[pygame.K_w]:
    #         player.move(0, -1)
    #         display_scroll[1] -= 5
    #         walk()
    #     if keys[pygame.K_s]:
    #         player.move(0, 1)
    #         display_scroll[1] += 5
    #         walk()    

    #     player.main(display)    

    #     for bullet in player_bullets:
    #         bullet.main(display)    

    #     clock.tick(60)
    #     pygame.display.update()