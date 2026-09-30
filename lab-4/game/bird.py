import pygame

class Bird:
    def __init__(self, x, y, radius=15):
        self.x = float(x)
        self.y = float(y)
        self.radius = radius
        self.velocity = 0.0
        self.gravity = 0.5
        self.flap_strength = -8.0

    def flap(self):
        self.velocity = self.flap_strength

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def rect(self):
        return pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2)
