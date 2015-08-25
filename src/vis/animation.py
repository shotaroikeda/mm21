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
        return True


class Upgrade(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        # Add the images to the images
        for i in range(1, 6):
            self.images.append(pygame.image.load("vis/sprites/upgrade_" + str(i) + ".png"))
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


class ChangeOwner(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        # Add the images to the images
        for i in range(1):
            self.images.append(pygame.image.load("vis/sprites/change_owner_" + str(i) + ".png"))
        for i in range(60):
            self.image_tick.append(0)
        for i in range(len(self.images)):
            self.image_rects.append(self.images[i].get_rect())


class AddRootkit(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        # Add the images to the images
        for i in range(1):
            self.images.append(pygame.image.load("vis/sprites/add_rootkit_" + str(i) + ".png"))
        for i in range(60):
            self.image_tick.append(0)
        for i in range(len(self.images)):
            self.image_rects.append(self.images[i].get_rect())


class CleanRootkit(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        # Add the images to the images
        for i in range(1):
            self.images.append(pygame.image.load("vis/sprites/clean_rootkit_" + str(i) + ".png"))
        for i in range(60):
            self.image_tick.append(0)
        for i in range(len(self.images)):
            self.image_rects.append(self.images[i].get_rect())


class ISP(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        # Add the images to the images
        for i in range(1):
            self.images.append(pygame.image.load("vis/sprites/isp_" + str(i) + ".png"))
        for i in range(60):
            self.image_tick.append(0)
        for i in range(len(self.images)):
            self.image_rects.append(self.images[i].get_rect())


class Infiltration(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        # Add the images to the images
        for i in range(1):
            self.images.append(pygame.image.load("vis/sprites/infiltration_" + str(i) + ".png"))
        for i in range(60):
            self.image_tick.append(0)
        for i in range(len(self.images)):
            self.image_rects.append(self.images[i].get_rect())


class Heal(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        # Add the images to the images
        for i in range(1):
            self.images.append(pygame.image.load("vis/sprites/heal_" + str(i) + ".png"))
        for i in range(60):
            self.image_tick.append(0)
        for i in range(len(self.images)):
            self.image_rects.append(self.images[i].get_rect())


class DDOS(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        # Add the images to the images
        for i in range(1):
            self.images.append(pygame.image.load("vis/sprites/ddos_" + str(i) + ".png"))
        for i in range(60):
            self.image_tick.append(0)
        for i in range(len(self.images)):
            self.image_rects.append(self.images[i].get_rect())


class Scan(Animation):

    def __init__(self):
        Animation.__init__(self)
        self.setup_animation()

    def setup_animation(self):
        # Add the images to the images
        for i in range(1):
            self.images.append(pygame.image.load("vis/sprites/scan_" + str(i) + ".png"))
        for i in range(60):
            self.image_tick.append(0)
        for i in range(len(self.images)):
            self.image_rects.append(self.images[i].get_rect())

# Below are global animations


class PortScan(object):

    def __init__(self):
        self.x = 0
        self.speed += 1

    def update(self):
        self.x += self.speed

    def draw(self, screen):
        return None
