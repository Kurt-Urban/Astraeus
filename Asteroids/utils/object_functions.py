import random
import math


def movement(self, **kwargs):
    if kwargs.get("ship") is None:
        self.velocity.from_polar((self.speed, self.heading + 270))

    self.position += self.velocity

    if kwargs.get("acceleration") is not None:
        self.velocity *= kwargs.get("acceleration")

    self.rect.center = (round(self.position[0]), round(self.position[1]))


def screen_wrap(self, **kwargs):
    top = 800
    btm = 0

    if kwargs.get("asteroid"):
        top = 830
        btm = -30

    if self.position.x > top:
        self.position.x = btm
    if self.position.x < btm:
        self.position.x = top
    if self.position.y <= btm:
        self.position.y = top
    if self.position.y > top:
        self.position.y = btm


def off_screen() -> tuple:
    # Generate starting location
    x = random.randint(-100, 900)
    y = 0
    if x < -20 or x > 820:
        y = random.randint(0, 800)
    else:
        y_choice = random.randint(-100, -20), random.randint(820, 900)
        y = random.choice(y_choice)

    return x, y


def get_dict_value(dict, key):
    return next(v for k, v in dict.items() if key in k)


def get_target_direction(ship_pos, obj_pos):
    angle = math.atan2(ship_pos[1] - obj_pos[1], ship_pos[0] - obj_pos[0])
    return int(math.degrees(angle) + 90)
