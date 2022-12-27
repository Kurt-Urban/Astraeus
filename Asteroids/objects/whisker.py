import pygame
import math


class Whisker(pygame.sprite.Sprite):
    def __init__(self, ship, index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/whisker.png")
        self.length = 255
        self.index = index
        self.image = pygame.transform.scale(self.image, (self.length, 2))
        self.rotated = self.image
        self.rect = self.image.get_rect()
        self.angle = 45 * index
        self.image = pygame.transform.rotate(self.rotated, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.ship = ship
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if self.angle in (0, 45):
            self.rect.topleft = (self.ship.position.x, self.ship.position.y)
        if self.angle in (90, 135):
            self.rect.topright = (self.ship.position.x, self.ship.position.y)
        if self.angle in (180, 225):
            self.rect.bottomright = (self.ship.position.x, self.ship.position.y)
        if self.angle in (270, 315):
            self.rect.bottomleft = (self.ship.position.x, self.ship.position.y)
