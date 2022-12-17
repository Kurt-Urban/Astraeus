import pygame
import random
from enum import Enum
from Asteroids.utils.object_functions import movement, screen_wrap, off_screen


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen, size=Enum("size", ["lg", "md", "sm"]), **kwargs) -> None:
        pygame.sprite.Sprite.__init__(self)

        # Set size
        size_dict = {"lg": 120, "md": 80, "sm": 50}
        size_px = size_dict[size]

        speed_dict = {
            "lg": [0.4, 0.6, 0.8],
            "md": [0.9, 1.2, 1.5, 2],
            "sm": [2, 3, 3.5, 4, 5],
        }

        x, y = off_screen()

        self.size = size
        self.screen = screen
        self.image = pygame.image.load(f"assets/asteroid{random.randint(1,5)}.png")
        self.image = pygame.transform.scale(self.image, (size_px, size_px))
        self.rotated_img = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.choice(speed_dict[size])
        self.heading = random.randint(-360, 360)
        self.img_heading = random.randint(-360, 360)

        if "pos" in kwargs:
            x, y = kwargs["pos"]
            self.rect.center = (x, y)
            self.heading = kwargs["heading"]

        self.velocity = pygame.math.Vector2(self.speed, 0)
        self.position = pygame.math.Vector2(x, y)
        self.rotation_speed = random.randint(-3, 3)

    def update(self):
        movement(self)
        screen_wrap(self, asteroid=True)

        # Rotate asteroid
        if self.rotation_speed == 0:
            self.rotation_speed = 1
        self.img_heading += self.rotation_speed
        self.blitRotateCenter(self.rect.topleft, self.img_heading)

    def blitRotateCenter(self, topleft, angle):
        rotated_image = pygame.transform.rotate(self.image, angle)
        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=topleft).center
        )

        self.screen.blit(rotated_image, new_rect)

    def split(self, pos):
        heading = random.randint(-360, 360)
        if self.size == "lg":
            return [
                Asteroid(self.screen, "md", pos=pos, heading=heading),
                Asteroid(
                    self.screen,
                    "md",
                    pos=pos,
                    heading=heading + random.randint(90, 240),
                ),
            ]
        elif self.size == "md":
            return [
                Asteroid(self.screen, "sm", pos=pos, heading=heading),
                Asteroid(
                    self.screen,
                    "sm",
                    pos=pos,
                    heading=heading + random.randint(90, 240),
                ),
            ]
        else:
            return []
