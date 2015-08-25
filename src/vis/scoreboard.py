#!/usr/bin/env python2
import pygame
import sys
import vis_constants as const


class Scoreboard(object):

    def __init__(self, ):
        # Check and init vis
        self.screenHeight = 400
        self.screenWidth = 400
        self.title = "Scoreboard"
        self.fps = 60
        self.running = True
        self.scores = []

        pygame.init()
        self.setup_pygame()
        self.run()

    def setup_pygame(self):
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.myfont = pygame.font.SysFont("monospace", 12)
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
        pygame.display.update()
        pygame.display.flip()
