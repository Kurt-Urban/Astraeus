import pygame
import random
from .objects.ship import Ship
from .objects.ufo import UFO
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

        # Initialize UFO Group
        self.ufo_group = pygame.sprite.Group()
        ufo = UFO(self.screen)
        self.ufo_group.add(ufo)

        # Game Variables
        self.total_destroyed_asteroids = 0
        self.destroyed_asteroids = 0
        self.total_destroyed_ufos = 0
        self.destroyed_ufos = 0
        self.current_score = 0
        self.round_scores = []
        self.round = 1
        self.lives = 3
        self.resetting = False
        self.reset_timer_default = 150
        self.reset_timer = self.reset_timer_default
        self.game_over = False
        self.draw_ship = True
        self.round_timer_default = 5000
        self.round_timer = self.round_timer_default

        self.start_asteroids_round()

    def update(self) -> None:
        # Display logic
        self.draw()

        self.ship_group.update()
        self.ufo_group.update()

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

        self.get_current_score()

        # UFO logic
        # Shooting Percentage
        if len(self.ufo_group) > 0:
            if random.randint(0, 100) <= 1:
                self.projectile_group.add(self.ufo_group.sprites()[0].shoot("sm"))

        # Round logic
        if len(self.asteroids_group) == 0:
            self.round += 1
            self.start_asteroids_round()

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
                self.current_score = self.current_score * 0.75
            else:
                self.game_over = True
                print(
                    f"Final Score: {self.get_total_score()}\n"
                    f"Destroyed Asteroids: {self.total_destroyed_asteroids}\n"
                )

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
            asteroid, projectile = shot_asteroid.popitem()
            if not projectile[0].ufo_shot:
                pygame.sprite.groupcollide(
                    self.asteroids_group, self.projectile_group, True, True
                )
                self.destroyed_asteroids += 1
                self.total_destroyed_asteroids += 1
                if asteroid.size == "lg" or asteroid.size == "md":
                    self.asteroids_group.add(asteroid.split(asteroid.rect.center))

    def start_asteroids_round(self):
        asteroids = []
        for _ in range(self.round + 3):
            asteroids.append(Asteroid(self.screen, "lg"))

        self.round_timer = self.round_timer_default

        if self.round != 1:
            self.current_score = 0
            self.round_scores.append(self.get_current_score())
            self.destroyed_asteroids = 0

        self.asteroids_group.add(asteroids)

    # Ancillary functions
    def draw_text(self, text, text_color, x, y):
        img = self.font.render(text, True, text_color)
        self.screen.blit(img, (x, y))

    def draw(self) -> None:
        self.clock.tick(self.fps)
        self.screen.fill((0, 0, 0))

        self.ufo_group.draw(self.screen)

        # Draw Ship
        if self.draw_ship:
            self.ship_group.draw(self.screen)

        self.draw_text(str(f"Lives: {self.lives}"), "WHITE", 20, 20)

    def run(self) -> None:
        while self.game_over == False:
            self.update()

    def get_current_score(self):
        if self.round_timer > 1 and len(self.asteroids_group) != 0:
            self.round_timer -= 1

        self.current_score = self.destroyed_asteroids * self.round_timer
        return self.current_score

    def get_total_score(self):
        return str(int(sum(self.round_scores) + self.current_score / 100))
