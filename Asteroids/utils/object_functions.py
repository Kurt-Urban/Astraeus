def movement(self, **kwargs):

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
