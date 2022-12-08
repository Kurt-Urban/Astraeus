import pygame
import random
from Asteroids.utils.object_functions import movement, screen_wrap


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, screen, size) -> None:
        pygame.sprite.Sprite.__init__(self)

        # Generate starting location
        x = random.randint(-100, 900)
        y = 0
        if x < -20 or x > 820:
            y = random.randint(0, 800)
        else:
            y_choice = random.randint(-100, -20), random.randint(820, 900)
            y = random.choice(y_choice)

        self.screen = screen
        self.image = pygame.image.load("assets/asteroid1.png")
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rotated_img = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = random.randint(1, 4)
        self.heading = random.randint(-360, 360)
        self.img_heading = random.randint(-360, 360)
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
