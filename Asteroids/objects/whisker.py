import pygame


class Whisker(pygame.sprite.Sprite):
    def __init__(self, ship, length, index, total_whiskers):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/whisker.png")
        self.length = length
        self.index = index
        self.image = pygame.transform.scale(self.image, (self.length, 2))
        self.rotated = self.image
        self.rect = self.image.get_rect()
        self.angle = (360 / total_whiskers) * index
        self.image = pygame.transform.rotate(self.rotated, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.ship = ship
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if 0 <= self.angle < 90:
            self.rect.topleft = (self.ship.position.x, self.ship.position.y)
        if 90 <= self.angle < 180:
            self.rect.topright = (self.ship.position.x, self.ship.position.y)
        if 180 <= self.angle < 270:
            self.rect.bottomright = (self.ship.position.x, self.ship.position.y)
        if 270 <= self.angle < 360:
            self.rect.bottomleft = (self.ship.position.x, self.ship.position.y)
