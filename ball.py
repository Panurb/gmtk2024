import pygame


class Ball:
    def __init__(self, position, radius):
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.score = 1
        self.respawn_timer = 0
        self.max_speed = 1.0

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

    def update(self, players):
        if self.respawn_timer > 0:
            self.respawn_timer -= 1
            if self.respawn_timer == 0:
                self.reset()

        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed

        self.position += self.velocity
        self.velocity *= 0.99

        if self.position.x < -10:
            if abs(self.position.y) < 3:
                self.score_goal(players[1])
            else:
                self.position.x = -10
                self.velocity.x *= -1
        if self.position.x > 10:
            if abs(self.position.y) < 3:
                self.score_goal(players[0])
            else:
                self.position.x = 10
                self.velocity.x *= -1
        if self.position.y < -5:
            self.position.y = -5
            self.velocity.y *= -1
        if self.position.y > 5:
            self.position.y = 5
            self.velocity.y *= -1

        for player in players:
            if self.position.distance_to(player.position) < self.radius + player.radius:
                if self.radius > player.radius:
                    player.die()
                else:
                    if (self.position - player.position).length() == 0:
                        self.position = player.position + pygame.Vector2(0.001, 0)
                    self.position = player.position + (self.position - player.position).normalize() * (self.radius + player.radius)
                    self.velocity *= -1

    def draw(self, camera, image_handler):
        camera.draw_transparent_circle(pygame.Color(0, 0, 0, 20), self.position, self.radius * 1.1)
        camera.draw_image(image_handler.get_image("blueberry"), self.position, pygame.Vector2(self.radius * 2.5, self.radius * 2.5), 0)

    def kick(self, direction):
        if direction.length() > 0:
            self.velocity += direction.normalize() * 0.1 / self.radius
