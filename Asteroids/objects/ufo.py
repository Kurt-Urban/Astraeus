import pygame
import random
from .projectile import Projectile
from Asteroids.utils.object_functions import movement, screen_wrap, off_screen


class UFO(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        x, y = off_screen()

        self.image = pygame.image.load("assets/ufo.png")
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.center = (x, y)
        self.rect = self.image.get_rect(center=self.center)
        self.screen = screen
        self.heading = random.randint(0, 360)
        self.speed = 2
        self.life = 30
        self.turn_timer_default = 200
        self.turn_timer = self.turn_timer_default
        self.velocity = pygame.math.Vector2(self.speed, 0)
        self.position = pygame.math.Vector2(x, y)

    def update(self):

        self.turn_timer -= 1
        if self.turn_timer == 0:
            self.heading += random.randint(-160, 160)
            self.turn_timer_default = random.randint(50, 200)
            self.turn_timer = self.turn_timer_default

        movement(self)
        screen_wrap(self)

    def shoot(self, size) -> Projectile:
        if size == "sm":
            heading = random.randint(0, 360)

        return Projectile(self.position, heading, self.screen, True)
