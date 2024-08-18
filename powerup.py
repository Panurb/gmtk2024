import random
from enum import Enum

import pygame

from level import Level


class PowerupType(Enum):
    SPEED = 0
    RADIUS = 1
    BALL_RADIUS = 2


class Powerup:
    def __init__(self):
        self.radius = 0.5
        self.position = Level.random_position(self.radius)
        self.powerup_type = random.choice(list(PowerupType))
        self.spawn_timer = 100

    def update(self, players, ball, powerups):
        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        else:
            for player in players:
                if self.position.distance_to(player.position) < self.radius + player.radius:
                    self.apply(player, ball)
                    powerups.remove(self)
                    break

    def draw(self, camera):
        shadow_radius = self.radius * (1 + self.spawn_timer / 100)
        camera.draw_transparent_circle(pygame.Color(0, 0, 0, 20), self.position, shadow_radius * 1.1)

        if self.spawn_timer == 0:
            camera.draw_circle(pygame.Color('yellow'), self.position, self.radius)

    def apply(self, player, ball):
        if self.powerup_type == PowerupType.SPEED:
            player.speed *= 1.25
        if self.powerup_type == PowerupType.RADIUS:
            player.radius *= 1.25
        if self.powerup_type == PowerupType.BALL_RADIUS:
            ball.radius *= 2

        print(f"Player {player.name} picked up {self.powerup_type.name}")
