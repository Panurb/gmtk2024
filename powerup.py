import random
from enum import Enum

import pygame


class PowerupType(Enum):
    SPEED = 0
    RADIUS = 1
    BALL_RADIUS = 2


class Powerup:
    def __init__(self, position):
        self.position = position
        self.powerup_type = random.choice(list(PowerupType))
        self.powerup_type = PowerupType.BALL_RADIUS
        self.radius = 0.5

    def draw(self, camera):
        camera.draw_circle(pygame.Color('yellow'), self.position, self.radius)

    def apply(self, player, ball):
        if self.powerup_type == PowerupType.SPEED:
            player.speed *= 1.1
        if self.powerup_type == PowerupType.RADIUS:
            player.radius *= 1.1
        if self.powerup_type == PowerupType.BALL_RADIUS:
            ball.radius *= 1.5
