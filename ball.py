import math

import pygame

from level import Level


class Ball:
    def __init__(self, position, radius):
        self.position = position
        self.angle = 0.0
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.score = 1
        self.respawn_timer = 0
        self.max_speed = 0.3
        self.frame = 0
        self.frame_timer = 0
        self.bounce = 0.5
        self.image = "blueberry"

    @property
    def speed(self):
        return self.velocity.length()

    def reset(self):
        self.position = pygame.Vector2(0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.score = 1
        self.respawn_timer = 0

    def score_goal(self, player):
        if self.score:
            player.add_score(self.score)
            self.score = 0
            self.respawn_timer = 100

    def animate(self):
        if self.speed == 0:
            return

        if self.image == "blueberry":
            frames = 8
        elif self.image == "apple":
            frames = 10
        else:
            frames = 6
        delay = int(2 * math.pi * self.radius / (self.speed * frames))

        # Ball animation is half rotation
        if self.image == "ball":
            delay = int(delay / 2)

        if self.frame_timer > delay:
            self.frame = (self.frame + 1) % frames
            self.frame_timer = 0
        else:
            self.frame_timer += 1

    def update(self, players):
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer == 0:
                self.reset()

        if self.speed > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.angle = self.velocity.as_polar()[1]

        self.animate()

        self.position += self.velocity
        self.velocity *= 0.99

        if self.score == 0:
            return

        if self.position.x < Level.left:
            self.score_goal(players[0])
        if self.position.x > Level.right:
            self.score_goal(players[1])

        if self.position.x - self.radius < Level.left:
            if abs(self.position.y) > Level.goal_width / 2:
                self.position.x = Level.left + self.radius
                self.velocity.x *= -self.bounce
        if self.position.x + self.radius > Level.right:
            if abs(self.position.y) > Level.goal_width / 2:
                self.position.x = Level.right - self.radius
                self.velocity.x *= -self.bounce
        if self.position.y - self.radius < Level.bottom:
            self.position.y = Level.bottom + self.radius
            self.velocity.y *= -self.bounce
        if self.position.y + self.radius > Level.top:
            self.position.y = Level.top - self.radius
            self.velocity.y *= -self.bounce

        for goal_post in Level.goal_posts():
            if self.position.distance_to(goal_post) < self.radius + Level.goal_post_radius:
                self.position = goal_post + (self.position - goal_post).normalize() * (self.radius + Level.goal_post_radius)
                # circle-circle collision response
                self.velocity = self.velocity - 2 * self.velocity.dot(self.position - goal_post) * (self.position - goal_post) / (self.position - goal_post).length_squared()

        for player in players:
            if player.respawn_timer > 0:
                continue

            if self.position.distance_to(player.position) < self.radius + player.radius:
                if self.radius > player.radius:
                    player.die()
                else:
                    if (self.position - player.position).length() == 0:
                        self.position = player.position + pygame.Vector2(0.001, 0)
                    self.position = player.position + (self.position - player.position).normalize() * (self.radius + player.radius)
                    self.velocity *= -self.bounce

    def draw(self, camera, image_handler):
        if self.radius < 1.0:
            self.image = "blueberry"
        elif self.radius < 2.0:
            self.image = "apple"
        else:
            self.image = "ball"

        camera.draw_transparent_circle(Level.shadow_color, self.position, self.radius * 1.25)
        camera.draw_image(image_handler.get_image(self.image, self.frame), self.position,
                          pygame.Vector2(self.radius * 2.5, self.radius * 2.5),
                          self.angle + image_handler.angle_offset[self.image])

    def kick(self, direction):
        if direction.length() > 0:
            self.velocity += direction.normalize() * 0.05 / self.radius
