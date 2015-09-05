#!/usr/bin/env python2
import pygame
import sys
import vis_constants as vis_const
import scoreboard_constants as const


class Scoreboard(object):

    def __init__(self, _debug):
        # Check and init vis
        self.screenHeight = const.screenHeight
        self.screenWidth = const.screenWidth
        self.title = const.title
        self.fps = const.FPStgt
        self.debug = _debug
        self.running = True
        self.scores = {}
        self.turns = []
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
        self.screen.fill(const.backgroundColor)
        x, y = 10, 10
        for c in range(len(self.CATEGORY)):
            label = self.myfont.render(self.CATEGORY[c], 1, const.textColor)
            self.screen.blit(label, (x, y))
            x += self.SPACING[c]
        x = 10
        y += 20
        pygame.draw.line(self.screen, const.lineColor, (x, y), (self.screenWidth - x, y))
        y += 5

        for j in range(len(self.scores)):
            for i in range(len(self.CATEGORY)):
                num = self.myfont.render(str(i) + ", " + str(j), 1, vis_const.TEAM_COLORS[j])
                self.screen.blit(num, (x, y))
                x += self.SPACING[i]
            x = 10
            y += 20
        x = 100
        y = 10
        pygame.draw.line(self.screen, const.lineColor, (x, y), (x, self.screenHeight - y))

        pygame.display.update()
        pygame.display.flip()

    def add_turn(self, json):
        if len(self.scores) == 0:
            for player_id in json:
                self.add_new_player(player_id, None)
        else:
            self.turns.append(json)

    def change_turn(self, turnNum):
        print turnNum

    def add_new_player(self, player_id, player_name):
        self.scores[player_id] = {'Team': player_id, 'P': 0, 'N': 0, 'T': 0, 'S': 0, 'M': 0, 'L': 0, 'ISP': 0, 'DC': 0}


if __name__ == '__main__':
    score = Scoreboard(True)
