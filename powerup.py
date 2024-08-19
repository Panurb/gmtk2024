import random
from enum import Enum

import pygame

from level import Level


class PowerupType(Enum):
    SPEED = "SPEED"
    RADIUS = "SIZE"
    BALL_RADIUS = "BALL SIZE"


class Powerup:
    def __init__(self):
        self.radius = 0.5
        self.position = Level.random_position(self.radius)
        self.powerup_type = random.choice(list(PowerupType))
        self.spawn_timer = 100
        self.remove_timer = -1

    def update(self, players, ball, powerups, sound_handler):
        if self.remove_timer > 0:
            self.remove_timer -= 1
            if self.remove_timer == 0:
                powerups.remove(self)
            return

        if self.spawn_timer > 0:
            self.spawn_timer -= 1
        else:
            for player in players:
                if self.position.distance_to(player.position) < self.radius + player.radius:
                    self.apply(player, ball)
                    sound_handler.play("nom")
                    break

    def draw(self, camera, image_handler):
        if self.remove_timer > 0:
            camera.draw_text("+" + self.powerup_type.value, self.position, 1)
            return

        shadow_radius = self.radius * (1 + self.spawn_timer / 100)
        camera.draw_transparent_circle(Level.shadow_color, self.position, shadow_radius * 1.1)

        if self.spawn_timer == 0:
            camera.draw_image(image_handler.get_image("candy"), self.position,
                              pygame.Vector2(self.radius * 2.5, self.radius * 2.5))

    def apply(self, player, ball):
        if self.powerup_type == PowerupType.SPEED:
            player.speed = 0.125
            player.speed_timer = 400
        if self.powerup_type == PowerupType.RADIUS:
            player.radius = 1.0
            player.radius_timer = 400
        if self.powerup_type == PowerupType.BALL_RADIUS:
            if ball.radius < 2:
                ball.radius *= 2
                ball.frame = 0
                ball.radius_timer = 600

        self.remove_timer = 50
