import pygame


class Node(object):

    def __init__(self, _x, _y, _node_type):
        self.x = _x
        self.y = _y
        self.node_type = _node_type
        self.animations = []
        self.update_city_sprite()

    def update_city_sprite(self):
        try:
            self.sprite = pygame.image.load("vis/sprites/" + self.node_type + ".png")
            self.sprite_rect = self.sprite.get_rect()
            self.sprite_rect[0] = self.x - self.sprite_rect[2] / 2
            self.sprite_rect[1] = self.y - self.sprite_rect[3] / 2
            if(self.node_type == "small_city"):
                self.sprite_rect[2] = 5
                self.sprite_rect[3] = 5
        except:  # TODO what is the exact exception?
            print("Failed to load sprite image")

    def update(self):
        for animation in self.animations:
            animation.update()

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite_rect)
        for animation in self.animations:
            animation.draw(screen)
