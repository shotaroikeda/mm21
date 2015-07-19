

class Animation(object):

    def __init__(self):
        self.current_tick = 0
        self.num_ticks = 0
        self.current_image = 0
        self.images = []
        self.image_switch = []
        self.image_rects = []

    def setup_animation():
        # TODO create basic animation
        self.images[0] = 0 

    def update(self):
        if (self.image_switch[0] == self.current_tick):
            self.current_image += 1
            self.image_switch.pop()

    def draw(self, screen):
        screen.blit(self.images[self.current_image], self.image_rects[self.current_image])
        if (self.current_tick == self.numticks):
            return True
