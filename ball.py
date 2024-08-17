import pygame


class Ball:
    def __init__(self, position, radius):
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.score = 1
        self.respawn_timer = 0

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

        self.position += self.velocity
        self.velocity *= 0.98

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
                self.position.x = -10
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
                    self.position = player.position + (self.position - player.position).normalize() * (self.radius + player.radius)
                    self.velocity *= -1

    def draw(self, camera):
        camera.draw_circle(pygame.Color('white'), self.position, self.radius)

    def kick(self, direction):
        self.velocity += direction
