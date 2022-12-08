import pygame
from .objects.ship import Ship
from .objects.asteroid import Asteroid


class AsteroidsGame:
    def __init__(self) -> None:
        # Initialize pygame
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.screen_size = 800
        self.screen = pygame.display.set_mode([self.screen_size, self.screen_size])
        pygame.display.set_caption("Asteroids")

        # Initialize Ship
        self.ship = Ship(400, self.screen)
        self.ship_group = pygame.sprite.Group()
        self.ship_group.add(self.ship)

        # Initialize Projectile Group
        self.projectile_group = pygame.sprite.Group()

        # Initialize Asteroids Group
        self.asteroids_group = pygame.sprite.Group()
        self.asteroid = Asteroid(self.screen, 75)
        self.asteroids_group.add(self.asteroid)

    def update(self) -> None:
        # Display logic
        self.draw()

        # Ship logic
        self.ship_group.update()

        # Projectile logic
        if self.ship.shot == True and self.ship.shooting_delay == 10:
            self.projectile_group.add(self.ship.shoot())

        self.projectile_group.update()

        # Asteroid logic
        self.asteroids_group.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    def draw(self) -> None:
        self.clock.tick(self.fps)
        self.screen.fill((0, 0, 0))

        # Draw Ship
        self.ship_group.draw(self.screen)

    def run(self, running) -> None:
        while running:
            self.update()
