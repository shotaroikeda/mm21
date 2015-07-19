

class Animation(object):

    def __init__(self):
        self.current_tick = 0
        self.num_ticks = 0
        self.current_image = 0
        self.images = []
        self.image_switch = []
        self.image_rects = []

    def update(self):
        if (self.image_switch[0] == self.current_tick):
            self.current_image += 1
            self.image_switch.pop()

    def draw(self, screen):
        screen.blit(self.images[self.current_image], self.image_rects[self.current_image])
        if (self.current_tick == self.numticks):
            return True


class Infiltration(Animation):

    def __init__(self):
        Animation.__init__()

    def setup_animation(self):
        # TODO write
        self.num_ticks = 12
        self.images = []
        self.image_switch = [2, 4, 6, 8, 10, 12]
        for i in range(len(self.images)):
            self.image_rects[i] = self.images[i].get_rect()
