import pygame
import math


class Ship(pygame.sprite.Sprite):
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/ship.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rotated = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (xy, xy)
        self.rotate_speed = 4
        self.speed = 0
        self.heading = 0
        self.velocity = pygame.math.Vector2(self.speed, 0)
        self.position = pygame.math.Vector2(xy, xy)

    def update(self):
        # Decelerate
        if self.speed > 0.1:
            self.speed *= 0.98
        else:
            self.speed = 0

        self.get_key_press()
        self.screen_wrap()

        self.position += self.velocity

        self.rect.center = (round(self.position[0]), round(self.position[1]))

    def foward(self):
        self.speed += 0.5
        if self.speed >= 5:
            self.speed = 5
        self.velocity.from_polar((self.speed, self.heading + 270))

    def rotate(self, angle):
        if self.heading >= 360:
            self.heading = -360
        if self.heading <= -360:
            self.heading += 360

        self.heading += angle
        self.image = pygame.transform.rotate(self.rotated, -self.heading)
        self.rect = self.image.get_rect(center=self.rect.center)

    def screen_wrap(self):
        if self.position.x > 800:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = 800
        if self.position.y <= 0:
            self.position.y = 800
        if self.position.y > 800:
            self.position.y = 0

    def get_key_press(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] == True:
            self.foward()
        if keys[pygame.K_a] == True:
            self.rotate(-self.rotate_speed)
        if keys[pygame.K_d] == True:
            self.rotate(self.rotate_speed)
