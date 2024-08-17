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

        if self.frame_timer == 0:
            self.frame = (self.frame + 1) % 8
            self.frame_timer = int(0.2 / self.speed)
        else:
            self.frame_timer -= 1

    def update(self, players):
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer == 0:
                self.reset()

        if self.speed > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.angle = self.velocity.as_polar()[1] - 30

        self.animate()

        self.position += self.velocity
        self.velocity *= 0.99

        if self.score == 0:
            return

        if self.position.x - self.radius < Level.left:
            if abs(self.position.y) < Level.goal_width / 2:
                self.score_goal(players[1])
            else:
                self.position.x = Level.left + self.radius
                self.velocity.x *= -self.bounce
        if self.position.x + self.radius > Level.right:
            if abs(self.position.y) < Level.goal_width / 2:
                self.score_goal(players[0])
            else:
                self.position.x = Level.right - self.radius
                self.velocity.x *= -self.bounce
        if self.position.y - self.radius < Level.bottom:
            self.position.y = Level.bottom + self.radius
            self.velocity.y *= -self.bounce
        if self.position.y + self.radius > Level.top:
            self.position.y = Level.top - self.radius
            self.velocity.y *= -self.bounce

        for player in players:
            if player.respawn_timer > 0:
                continue

            if self.position.distance_to(player.position) < self.radius + player.radius:
                if self.radius > player.radius and self.velocity.length() > 0.2:
                    player.die()
                else:
                    if (self.position - player.position).length() == 0:
                        self.position = player.position + pygame.Vector2(0.001, 0)
                    self.position = player.position + (self.position - player.position).normalize() * (self.radius + player.radius)
                    self.velocity *= -self.bounce

    def draw(self, camera, image_handler):
        camera.draw_transparent_circle(pygame.Color(0, 0, 0, 20), self.position, self.radius * 1.1)
        camera.draw_image(image_handler.get_image(f"blueberry{self.frame+1}"), self.position,
                          pygame.Vector2(self.radius * 2.5, self.radius * 2.5), self.angle)

    def kick(self, direction):
        if direction.length() > 0:
            self.velocity += direction.normalize() * 0.05 / self.radius
            self.frame_timer = 0
