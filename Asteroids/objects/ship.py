import pygame
from .projectile import Projectile
from Asteroids.utils.object_functions import movement, screen_wrap


class Ship(pygame.sprite.Sprite):
    def __init__(self, xy, screen, ai_playing=False):
        pygame.sprite.Sprite.__init__(self)
        img1 = pygame.image.load("assets/ship1.png")
        img1 = pygame.transform.scale(img1, (30, 57))
        img2 = pygame.image.load("assets/ship2.png")
        img2 = pygame.transform.scale(img2, (30, 57))

        self.images = [img1, img2]
        self.image = self.images[0]
        self.screen = screen
        self.rotated = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (xy, xy)
        self.rotate_speed = 6
        self.top_speed = 4
        self.speed = 0
        self.heading = 0
        self.velocity = pygame.math.Vector2(self.speed, 0)
        self.position = pygame.math.Vector2(xy, xy)
        self.shot = False
        self.shooting_delay_default = 200
        self.shooting_delay = self.shooting_delay_default
        self.moving = False
        self.ai_playing = ai_playing

    def update(self):
        # Movement Logic
        # Decelerate
        if self.speed > 0.1:
            self.speed *= 0.98
        else:
            self.speed = 0
        movement(self, acceleration=0.985, ship=True)
        screen_wrap(self)
        self.display_thruster()

        if not self.ai_playing:
            self.get_key_press()

        # Shooting Logic
        if self.shot and self.shooting_delay != 0:
            self.shooting_delay -= 1

    def forward(self):
        self.moving = True
        self.speed += 0.3
        if self.speed >= self.top_speed:
            self.speed = self.top_speed
        self.velocity.from_polar((self.speed, self.heading + 270))

    def display_thruster(self):
        self.image = pygame.transform.rotate(
            self.images[1 if self.moving else 0], -self.heading
        )
        self.rect = self.image.get_rect(center=self.rect.center)

    def rotate(self, angle):
        if self.heading >= 360:
            self.heading = 0
        if self.heading <= -360:
            self.heading = 0

        self.heading += angle
        self.display_thruster()

    def get_key_press(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.forward()
        else:
            self.moving = False
        if keys[pygame.K_a]:
            self.rotate(-self.rotate_speed)
        if keys[pygame.K_d]:
            self.rotate(self.rotate_speed)
        # Shooting Keys Logic
        if keys[pygame.K_SPACE]:
            if self.shooting_delay == self.shooting_delay_default and not self.shot:
                self.shot = True
        if not keys[pygame.K_SPACE]:
            self.shot = False
            self.shooting_delay = self.shooting_delay_default

    def shoot(self) -> Projectile:
        return Projectile(self.position, self.heading, self.screen, False)

    def reset(self):
        self.speed = 0
        self.heading = 0
        self.position = pygame.math.Vector2(400, 400)
        self.rect.center = (400, 400)
        self.image = pygame.transform.rotate(self.rotated, -self.heading)
        self.rect = self.image.get_rect(center=self.rect.center)
