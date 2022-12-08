import pygame
from .projectile import Projectile


class Ship(pygame.sprite.Sprite):
    def __init__(self, xy, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/ship.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.screen = screen
        self.rotated = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (xy, xy)
        self.rotate_speed = 4
        self.top_speed = 4
        self.speed = 0
        self.heading = 0
        self.velocity = pygame.math.Vector2(self.speed, 0)
        self.position = pygame.math.Vector2(xy, xy)
        self.shot = False
        self.shooting_delay_default = 15
        self.shooting_delay = self.shooting_delay_default

    def update(self):
        # Movement Logic
        # Decelerate
        if self.speed > 0.1:
            self.speed *= 0.98
        else:
            self.speed = 0

        self.position += self.velocity
        self.velocity *= 0.985
        self.rect.center = (round(self.position[0]), round(self.position[1]))

        # Shooting Logic
        if self.shot == True and self.shooting_delay != 0:
            self.shooting_delay -= 1
        else:
            self.shooting_delay = self.shooting_delay_default
            self.shot = False

        self.get_key_press()
        self.screen_wrap()

    def foward(self):
        self.speed += 0.3
        if self.speed >= self.top_speed:
            self.speed = self.top_speed
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
        if keys[pygame.K_SPACE] == True:
            self.shot = True

    def shoot(self) -> Projectile:
        return Projectile(self.position, self.heading, self.screen)
