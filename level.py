import random

import pygame


class Level:
    left = -12
    right = 12
    top = 6
    bottom = -6

    goal_width = 6

    shadow_color = pygame.Color(0, 0, 0, 50)

    @staticmethod
    def random_position(margin=0):
        return pygame.Vector2(random.uniform(Level.left + margin, Level.right - margin),
                              random.uniform(Level.bottom + margin, Level.top - margin))
