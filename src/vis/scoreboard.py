#!/usr/bin/env python2
import pygame
import sys
import vis_constants as const


class Scoreboard(object):

    def __init__(self, ):
        # Check and init vis
        self.screenHeight = 360
        self.screenWidth = 720
        self.title = "Scoreboard"
        self.fps = 60
        self.running = True
        self.scores = []
        self.CATEGORY = ['Team', 'Processing', 'Networking', 'Total', 'S. City', 'M. City', 'L. City', 'ISP', 'DC']
        self.SPACING = [100, 100, 100, 60, 75, 75, 75, 50, 0]

        pygame.init()
        self.setup_pygame()
        self.run()

    def setup_pygame(self):
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.myfont = pygame.font.SysFont("monospace", 14)
        self.gameClock = pygame.time.Clock()

    def run(self):
        while 1:  # Run game forever till exit
            self.gameClock.tick(self.fps)  # Make sure game is on 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()
            if self.running:
                self.draw()

    def draw(self):
        self.screen.fill(const.WHITE)
        x, y = 10, 10
        for c in range(len(self.CATEGORY)):
            label = self.myfont.render(self.CATEGORY[c], 1, const.BLACK)
            self.screen.blit(label, (x, y))
            x += self.SPACING[c]
        x = 10
        y += 20
        pygame.draw.line(self.screen, const.BLACK, (x, y), (self.screenWidth - x, y))
        y += 5


        # assuming there are 10 entries
        for j in range(10):
            for i in range(len(self.CATEGORY)):
                num = self.myfont.render(str(i) + ", "+ str(j), 1, const.BLACK)
                self.screen.blit(num, (x,y))
                x += self.SPACING[i]
            x = 10
            y += 20
        x = 100
        y = 10
        pygame.draw.line(self.screen, const.BLACK, (x, y), (x, self.screenHeight - y))

        pygame.display.update()
        pygame.display.flip()


if __name__ == '__main__':
    score = Scoreboard()
