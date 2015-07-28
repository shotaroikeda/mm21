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
        screen.blit(self.images[self.image_tick[self.current_tick]], self.image_rects[self.image_tick[self.current_tick]])
        if (self.current_tick >= len(self.image_tick)):
            return True
        return False


class Upgrade(Animation):

    def __init_(self):
        Animation.__init__()
        self.setup_animation()

    def setup_animation(self):
        self.images[0] = pygame.image.load("vis/sprites/upgrade_1.png")
        self.images[1] = pygame.image.load("vis/sprites/upgrade_2.png")
        self.images[2] = pygame.image.load("vis/sprites/upgrade_3.png")
        self.images[3] = pygame.image.load("vis/sprites/upgrade_4.png")
        self.images[4] = pygame.image.load("vis/sprites/upgrade_5.png")
        self.image_tick = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
        for i in range(len(self.images)):
            self.image_rects[i] = self.images[i].get_rect()
