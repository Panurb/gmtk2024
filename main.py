import asyncio
import os
from collections import defaultdict
from enum import Enum
import random

import pygame

from ball import Ball
from button import Button
from camera import Camera
from player import Player
from powerup import Powerup

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
WEB = True


class State(Enum):
    QUIT = 0
    GAME = 1
    MENU = 2


class InputHandler:
    def __init__(self):
        self.key_down = defaultdict(bool)
        self.mouse = pygame.Vector2(0, 0)
        self.mouse_clicked = [False] * 6

    def update(self, camera):
        x, y = pygame.Vector2(pygame.mouse.get_pos())
        self.mouse = camera.screen_to_world(x, y)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.key_down[event.key] = True
            if event.type == pygame.KEYUP:
                self.key_down[event.key] = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_clicked[event.button] = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_clicked[event.button] = False


class ImageHandler:
    def __init__(self):
        self.images = {}

        for file in os.listdir("images"):
            image = file.split(".")[0]
            self.images[image] = self.load_image(f"images/{image}.png")

    def load_image(self, path):
        return pygame.image.load(path)

    def get_image(self, name):
        return self.images[name]


class Main:
    def __init__(self, width, height):
        # init mixer first to prevent audio delay
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()

        pygame.init()
        pygame.display.set_caption('Ant soccer')

        self.info = pygame.display.Info()
        self.screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
        self.camera = Camera(pygame.Vector2(0, 0), 50, self.screen)
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.input_handler = InputHandler()
        self.image_handler = ImageHandler()

        self.state = State.MENU

        self.players = []

        self.players.append(Player(pygame.Vector2(-8, 0), "player1"))
        self.players.append(Player(pygame.Vector2(8, 0), "player2", ai_enabled=False))

        self.ball = Ball(pygame.Vector2(0, 0), 0.5)

        self.powerups = []
        self.powerup_timer = 300

        self.max_score = 5

        self.win_timer = 0

        self.buttons = []
        self.buttons.append(Button(pygame.Vector2(0, 3), "1 vs 1", lambda: self.reset(ai_enabled=False)))
        self.buttons.append(Button(pygame.Vector2(0, 0), "1 vs AI", lambda: self.reset(ai_enabled=True)))

    def reset(self, ai_enabled=False):
        self.players = []

        self.players.append(Player(pygame.Vector2(-8, 0), "player1"))
        self.players.append(Player(pygame.Vector2(8, 0), "player2", ai_enabled=ai_enabled))

        self.ball = Ball(pygame.Vector2(0, 0), 0.5)

        self.powerups = []
        self.powerup_timer = 300

        self.state = State.GAME

    def input(self):
        self.input_handler.update(self.camera)

        for player in self.players:
            player.input(self.input_handler)

        for button in self.buttons:
            button.input(self.input_handler)

        if self.input_handler.key_down[pygame.K_ESCAPE]:
            self.state = State.MENU

    def update(self):
        match self.state:
            case State.GAME:
                if self.win_timer > 0:
                    self.win_timer -= 1
                    if self.win_timer == 0:
                        self.state = State.MENU
                    return

                for player in self.players:
                    player.update(self.players, self.ball, self.powerups)
                    if player.score >= self.max_score:
                        self.win_timer = 100
                self.ball.update(self.players)

                self.powerup_timer -= 1

                if len(self.powerups) < 5 and self.powerup_timer <= 0:
                    self.powerups.append(Powerup())
                    self.powerup_timer = 300

                for powerup in self.powerups:
                    powerup.update(self.players, self.ball, self.powerups)
            case State.MENU:
                pass

    def draw(self):
        self.camera.draw_image(self.image_handler.get_image("background"), pygame.Vector2(0, 0), angle=90)

        match self.state:
            case State.GAME:
                for player in self.players:
                    player.draw(self.camera, self.image_handler)
                self.ball.draw(self.camera, self.image_handler)
                for powerup in self.powerups:
                    powerup.draw(self.camera)

                if self.win_timer > 0:
                    self.camera.draw_text("Player 1 wins!" if self.players[0].score >= self.max_score else "Player 2 wins!", pygame.Vector2(0, 0), 2)
            case State.MENU:
                for button in self.buttons:
                    button.draw(self.camera)

    def main_loop(self):
        while self.state != State.QUIT:
            self.input()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

            pygame.display.update()

    async def main_loop_web(self):
        while self:
            self.input()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)
            await asyncio.sleep(0)


def main():
    main_window = Main(SCREEN_WIDTH, SCREEN_HEIGHT)
    if WEB:
        asyncio.run(main_window.main_loop_web())
    else:
        main_window.main_loop()


if __name__ == '__main__':
    main()
