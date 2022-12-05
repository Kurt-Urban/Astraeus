import pygame
from ship import Ship


class AsteroidsGame:
    def __init__(self) -> None:
        # Initialize pygame
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.screen_size = 800
        self.screen = pygame.display.set_mode([self.screen_size, self.screen_size])
        pygame.display.set_caption("Astroids")

        # Initialize Ship
        self.ship = Ship(400)
        self.ship_group = pygame.sprite.Group()
        self.ship_group.add(self.ship)

    def update(self) -> None:
        # Display logic
        self.draw()

        # Ship logic
        self.ship_group.update()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    def run(self, running) -> None:
        while running:
            self.update()

    def draw(self) -> None:
        self.clock.tick(self.fps)
        self.screen.fill((0, 0, 0))

        # Draw Ship
        self.ship_group.draw(self.screen)

    def astroids(self) -> None:
        pass

    def ship(self) -> None:
        pass


game = AsteroidsGame()
game.run(True)
