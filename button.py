import pygame


class Button:
    def __init__(self, position, text, on_click=None):
        self.position = position
        self.text = text
        self.on_click = on_click
        self.selected = False
        self.width = 5
        self.height = 2

    def click(self):
        if self.on_click:
            self.on_click()

    def input(self, input_handler):
        if self.position.x - self.width / 2 < input_handler.mouse.x < self.position.x + self.width / 2 and \
                self.position.y - self.height / 2 < input_handler.mouse.y < self.position.y + self.height / 2:
            self.selected = True
            if input_handler.mouse_clicked[1]:
                self.click()
        else:
            self.selected = False

    def draw(self, camera):
        if self.selected:
            camera.draw_rectangle(pygame.Color('blue'), self.position, self.width, self.height)
        else:
            camera.draw_rectangle(pygame.Color('black'), self.position, self.width, self.height)
        camera.draw_text(self.text, self.position, 2)
