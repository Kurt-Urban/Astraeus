import pygame
import random
import numpy as np
import math
from .projectile import Projectile
from Asteroids.utils.object_functions import movement, screen_wrap, off_screen


class UFO(pygame.sprite.Sprite):
    def __init__(self, size, screen):
        pygame.sprite.Sprite.__init__(self)
        x, y = off_screen()

        sm, lg = (65, 65), (85, 85)

        self.image = pygame.image.load("assets/ufo.png")
        self.image = pygame.transform.scale(self.image, sm if size == "sm" else lg)
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
        self.size = size

    def update(self):

        self.turn_timer -= 1
        if self.turn_timer == 0:
            self.heading += random.randint(-160, 160)
            self.turn_timer_default = random.randint(50, 200)
            self.turn_timer = self.turn_timer_default

        movement(self)
        screen_wrap(self)

    def shoot(self, **kwargs) -> Projectile:
        heading = random.randint(0, 360)

        if self.size == "sm":
            player_pos = kwargs.get("player_pos")
            angle = math.atan2(
                player_pos[1] - self.position[1], player_pos[0] - self.position[0]
            )
            heading = math.degrees(angle) + 90

        return Projectile(self.position, heading, self.screen, True)
