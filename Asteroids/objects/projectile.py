import pygame
from Asteroids.utils.object_functions import movement, screen_wrap


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, heading, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/projectile.png")
        self.image = pygame.transform.scale(self.image, (5, 5))
        self.center = pos
        self.rect = self.image.get_rect(center=self.center)
        self.screen = screen
        self.heading = heading
        self.speed = 15
        self.life = 30
        self.velocity = pygame.math.Vector2(self.speed, 0)
        self.position = pygame.math.Vector2(pos[0], pos[1])

    def update(self):
        self.life -= 1
        if self.life <= 0:
            self.kill()

        self.screen.blit(self.image, self.position)

        movement(self)
        screen_wrap(self)
