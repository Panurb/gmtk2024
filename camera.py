import pygame


class Camera:
    def __init__(self, position, zoom, target):
        self.position = position
        self.zoom = zoom
        self.target = target
        self.surface_center = pygame.Vector2(0, 0)
        self.resolution = target.get_size()

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    @property
    def w(self):
        return self.resolution[0]

    @property
    def h(self):
        return self.resolution[1]

    @property
    def width(self):
        return self.w / self.zoom

    @property
    def height(self):
        return self.h / self.zoom

    def world_to_screen(self, position):
        x = position.x
        y = position.y
        return int((x - self.x) * self.zoom) + self.w / 2, int((self.y - y) * self.zoom) + self.h / 2

    def screen_to_world(self, x, y):
        return pygame.Vector2((x - self.w / 2) / self.zoom + self.x, self.y - (y - self.h / 2) / self.zoom)

    def draw_surface(self, surface, position, angle=0, pivot=None):
        if angle:
            surface = pygame.transform.rotate(surface, angle)
            if pivot is not None:
                r = pivot - position
                r_rotated = r.rotate(angle)
                offset = r - r_rotated
                position += offset

        x, y = self.world_to_screen(position)
        x -= surface.get_width() // 2
        y -= surface.get_height() // 2
        self.target.blit(surface, (x, y))

    def draw_rectangle(self, color, position, width, height):
        x, y = self.world_to_screen(position)
        x -= width * self.zoom // 2
        y -= height * self.zoom // 2
        width, height = int(width * self.zoom), int(height * self.zoom)
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.target, color, rect)

    def draw_rectangle_outline(self, color, position, width, height, line_width=1):
        x, y = self.world_to_screen(position)
        x -= width * self.zoom // 2
        y -= height * self.zoom // 2
        width, height = int(width * self.zoom), int(height * self.zoom)
        pygame.draw.rect(self.target, color, pygame.Rect(x, y, width, height), line_width)

    def draw_text(self, text, position, size):
        font = pygame.font.Font(None, int(size * self.zoom))
        text = font.render(text, True, (255, 255, 255))
        x, y = self.world_to_screen(position)
        x -= text.get_width() // 2
        y -= text.get_height() // 2
        self.target.blit(text, (x, y))

    def draw_line(self, color, start, end, width):
        start = self.world_to_screen(start)
        end = self.world_to_screen(end)
        pygame.draw.line(self.target, color, start, end, int(width * self.zoom))

    def draw_circle(self, color, position, radius):
        x, y = self.world_to_screen(position)
        radius = int(radius * self.zoom)
        pygame.draw.circle(self.target, color, (x, y), radius)

    def draw_image(self, image, position, size, angle):
        image = pygame.transform.smoothscale(image, (int(size.x * self.zoom), int(size.y * self.zoom)))
        image = pygame.transform.rotate(image, angle)
        x, y = self.world_to_screen(position)
        x -= image.get_width() // 2
        y -= image.get_height() // 2
        self.target.blit(image, (x, y))

    def draw_transparent_circle(self, color, position, radius):
        x, y = self.world_to_screen(position)
        radius = int(radius * self.zoom)
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, (radius, radius), radius)
        self.target.blit(surface, (x - radius, y - radius))
