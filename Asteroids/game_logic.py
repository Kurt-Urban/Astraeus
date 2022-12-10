import pygame
from .objects.ship import Ship
from .objects.asteroid import Asteroid


class AsteroidsGame:
    def __init__(self) -> None:
        # Initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.screen_size = 800
        self.screen = pygame.display.set_mode([self.screen_size, self.screen_size])
        pygame.display.set_caption("Asteroids")
        self.font = pygame.font.SysFont("Bauhaus 93", 40)
        self.font_color = (255, 255, 255)  # White

        # Initialize Ship
        self.ship = Ship(400, self.screen)
        self.ship_group = pygame.sprite.Group()
        self.ship_group.add(self.ship)

        # Initialize Projectile Group
        self.projectile_group = pygame.sprite.Group()

        # Initialize Asteroids Group
        self.asteroids_group = pygame.sprite.Group()

        # Game Variables
        self.destroyed_asteroids = 0
        self.current_score = 0
        self.round_scores = []
        self.round = 1
        self.lives = 3
        self.resetting = False
        self.reset_timer_default = 150
        self.reset_timer = self.reset_timer_default
        self.game_over = False
        self.draw_ship = True
        self.round_timer_default = 7500
        self.round_timer = self.round_timer_default

        self.start_round()

    def update(self) -> None:
        # Display logic
        self.draw()

        # Ship logic
        self.ship_group.update()

        # Projectile logic
        if (
            self.ship.shot
            and self.ship.shooting_delay == self.ship.shooting_delay_default - 1
        ):
            self.projectile_group.add(self.ship.shoot())

        self.projectile_group.update()

        # Asteroid logic
        self.asteroids_group.update()
        self.split_asteroid()

        # Collision logic
        self.life_lost()

        self.get_score()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    # Main game logic functions
    def life_lost(self) -> None:
        if (
            pygame.sprite.groupcollide(
                self.asteroids_group, self.ship_group, False, False
            )
            and self.resetting == False
        ):
            if self.lives > 0:
                self.resetting = True
                self.lives -= 1
                self.ship.reset()
            else:
                self.game_over = True
                print("Game Over")

        # Gives invincibility frames
        if self.resetting:
            self.reset_timer -= 1
            if self.reset_timer <= 0:
                self.resetting = False
                self.reset_timer = self.reset_timer_default
            # Indicate invincibility
            if self.reset_timer in [10, 30, 50, 70, 90, 110, 130, 150]:
                self.draw_ship = not self.draw_ship

    def split_asteroid(self):
        shot_asteroid = pygame.sprite.groupcollide(
            self.asteroids_group, self.projectile_group, False, False
        )
        if shot_asteroid:
            pygame.sprite.groupcollide(
                self.asteroids_group, self.projectile_group, True, True
            )
            self.destroyed_asteroids += 1
            asteroid, _ = shot_asteroid.popitem()
            if asteroid.size == "lg" or asteroid.size == "md":
                self.asteroids_group.add(asteroid.split(asteroid.rect.center))

    def start_round(self):
        asteroids = []
        if self.round == 1:
            for _ in range(4):
                asteroids.append(Asteroid(self.screen, "lg"))
        else:
            self.round_timer = self.round_timer_default
            self.round_scores.append(self.get_score())

        self.asteroids_group.add(asteroids)

    # Ancillary functions
    def draw_text(self, text, text_color, x, y):
        img = self.font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def draw(self) -> None:
        self.clock.tick(self.fps)
        self.screen.fill((0, 0, 0))

        # Draw Ship
        if self.draw_ship:
            self.ship_group.draw(self.screen)

        self.draw_text(str(f"Lives: {self.lives}"), "WHITE", 20, 20)
        self.draw_text(str(f"Score: {self.get_score()}"), "WHITE", 600, 20)

    def run(self) -> None:
        while self.game_over == False:
            self.update()

    def get_score(self):
        if self.round_timer > 1 and len(self.asteroids_group) != 0:
            self.round_timer -= 1

        self.current_score = self.destroyed_asteroids * self.round_timer
        return self.current_score
