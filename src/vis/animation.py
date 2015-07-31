import pygame


class Animation(object):

    def __init__(self):
        self.current_tick = 0
        self.images = []
        self.image_tick = []
        self.image_rects = []

    def update(self):
        self.current_tick += 1

    def draw(self, screen, x, y):
        if (self.current_tick >= len(self.image_tick) - 1):
            self.current_tick = 0
        screen.blit(self.images[self.image_tick[self.current_tick]], (x, y))
        return False


class Upgrade(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        self.images.append(pygame.image.load("vis/sprites/upgrade_1.png"))
        self.images.append(pygame.image.load("vis/sprites/upgrade_2.png"))
        self.images.append(pygame.image.load("vis/sprites/upgrade_3.png"))
        self.images.append(pygame.image.load("vis/sprites/upgrade_4.png"))
        self.images.append(pygame.image.load("vis/sprites/upgrade_5.png"))
        for i in range(12):
            self.image_tick.append(0)
        for i in range(12):
            self.image_tick.append(1)
        for i in range(12):
            self.image_tick.append(2)
        for i in range(12):
            self.image_tick.append(3)
        for i in range(12):
            self.image_tick.append(4)
        for i in range(len(self.images)):
            self.image_rects.append(self.images[i].get_rect())
