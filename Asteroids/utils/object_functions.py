def movement(self, speed, **kwargs):

    self.velocity.from_polar((speed, self.heading + 270))

    self.position += self.velocity

    if kwargs.get("acceleration") is not None:
        self.velocity += kwargs.get("acceleration")

    self.rect.center = (round(self.position[0]), round(self.position[1]))
