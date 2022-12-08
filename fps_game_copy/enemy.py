import pygame

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
                
        pygame.draw.rect(display, (255, 0, 0), (self.x, self.y, 16, 16), True)