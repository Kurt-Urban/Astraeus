import pygame


class UFO(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, direction):
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = direction

    def update(self):
        self.rect.x += self.speed * self.direction

    def reverse(self):
        self.direction *= -1

    def reset(self):
        self.rect.x = 0
        self.rect.y = 0

    def get_position(self):
        return self.rect.x, self.rect.y
