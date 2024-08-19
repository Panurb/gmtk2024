import pygame


class Button:
    def __init__(self, position, image, on_click):
        self.position = position
        self.on_click = on_click
        self.selected = False
        self.width = 5
        self.height = 2
        self.image = image

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

    def draw(self, camera, image_handler):
        if self.selected:
            camera.draw_image(image_handler.get_image(self.image + "_hover"), self.position)
        else:
            camera.draw_image(image_handler.get_image(self.image), self.position)
