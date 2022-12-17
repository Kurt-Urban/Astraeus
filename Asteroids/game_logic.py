import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import random
from enum import Enum
from .utils.object_functions import get_dict_value
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

        # Game Variables
        self.total_destroyed_asteroids = 0
        self.destroyed_asteroids = 0
        self.total_destroyed_ufos = 0
        self.spawned_ufos = 0
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
        self.ufo_shoot_dict = {(1, 2, 3, 4): (150, 200), (5, 6, 7, 8): (100, 150)}
        self.ufo_shoot_timer = 200
        self.ufo_round_active = False
        self.set_ufo_shoot_timer()

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

        if not self.game_over:
            # Collision logic
            self.life_handler()
            self.ship_shot(self.ufo_group, "ufo")

            # Score
            self.get_current_score()

            # UFO logic
            self.ufo_handler()

            # Round logic
            self.round_handler()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()

    # Main game logic functions
    def life_handler(self) -> None:
        if (
            self.ship_hit_object(self.asteroids_group)
            or self.ship_hit_object(self.ufo_group)
            or self.ship_shot(self.ship_group, "ship")
            and not self.resetting
        ):
            if self.lives > 0:
                self.resetting = True
                self.lives -= 1
                self.ship.reset()
                self.current_score = self.current_score * 0.75
            else:
                self.game_over = True
                self.ship_group.sprites()[0].kill()
                print(
                    f"Final Score: {self.get_total_score()}\n"
                    f"Destroyed UFOs: {self.total_destroyed_ufos}\n"
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
            self.spawned_ufos = 0

        self.asteroids_group.add(asteroids)

    def ship_shot(self, group, type=Enum("type", ["ship", "ufo"])):
        projectile = pygame.sprite.groupcollide(
            group, self.projectile_group, False, False
        )
        if projectile:
            _, projectile = projectile.popitem()
            if projectile[0].ufo_shot and type == "ship":
                pygame.sprite.groupcollide(group, self.projectile_group, False, True)
                return True
            if type == "ufo" and not projectile[0].ufo_shot:
                self.total_destroyed_ufos += 1
                self.current_score += 1000
                pygame.sprite.groupcollide(group, self.projectile_group, True, True)

    def ship_hit_object(self, group) -> bool:
        return (
            pygame.sprite.groupcollide(group, self.ship_group, False, False)
            and self.resetting == False
        )

    def ufo_handler(self):
        if (
            self.round > 1
            and self.spawned_ufos < self.round
            and len(self.ufo_group) < self.round
            and self.ufo_round_active == False
        ):
            random.randint(1, 2000) <= 1 and self.spawn_ufo()

        # UFO Shooting Percentage
        if len(self.ufo_group) > 0:
            self.ufo_shoot_timer -= 1
            if self.ufo_shoot_timer == 0:
                player_pos = self.ship_group.sprites()[0].position
                ufo = self.ufo_group.sprites()[0]

                self.set_ufo_shoot_timer()
                self.projectile_group.add(ufo.shoot(player_pos=player_pos))

    def round_handler(self):
        if len(self.asteroids_group) == 0:
            if (
                len(self.ufo_group) == 0
                and self.ufo_round_active == False
                and self.spawned_ufos < self.round
            ):
                self.ufo_round_active = True
                self.spawn_ufo()
            elif len(self.ufo_group) == 0 and (
                self.ufo_round_active == True or self.spawned_ufos >= self.round
            ):
                self.round += 1
                self.ufo_round_active = False
                self.start_asteroids_round()

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
        self.draw_text(str(self.round), "WHITE", 760, 20)

        if self.game_over:
            self.draw_game_over_screen()

    def run(self) -> None:
        while True:
            self.update()

    def get_current_score(self) -> int:
        if (
            self.round_timer > 1
            and len(self.asteroids_group) != 0
            and not self.game_over
        ):
            self.round_timer -= 1

        self.current_score = (
            self.destroyed_asteroids * float(f"1.{self.round_timer}") * 10
        )
        return self.current_score

    def get_total_score(self) -> str:
        return str(int(sum(self.round_scores) + self.current_score))

    def set_ufo_shoot_timer(self):
        if self.round < 9:
            timer_options = get_dict_value(self.ufo_shoot_dict, self.round)
            self.ufo_shoot_timer = random.randint(timer_options[0], timer_options[1])
        else:
            self.ufo_shoot_timer = random.randint(20, 80)

    def spawn_ufo(self):
        self.spawned_ufos += 1
        self.ufo_group.add(UFO(random.choice(["lg", "sm"]), self.screen))

    def reset(self):
        self.__init__()

    def draw_game_over_screen(self):
        self.draw_text("Game Over", "RED", 200, 200)
        self.draw_text(f"Score: {self.get_total_score()}", "WHITE", 200, 250)
        self.draw_text("Press Space to Play Again", "WHITE", 200, 300)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.reset()
