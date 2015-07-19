#!/usr/bin/env python2
import pygame
import sys
import math
import random
from node import Node
import vis_constants as const
# import animate as ani


class Visualizer(object):

    def __init__(self, _map_json_data, _width=const.screenWidth, _height=const.screenHeight, _log_json_data=None):
        # Check and init vis
        self.screenHeight = _height
        self.screenWidth = _width
        self.title = const.title
        self.fps = const.FPStgt
        self.running = True
        self.json_data = _map_json_data
        self.ticks = 0
        self.ticks_per_turn = 60
        self.turn_json = []

        if(_log_json_data is not None):
            for item in _log_json_data:
                self.add_turn(item)

        pygame.init()
        self.setup_pygame()
        self.process_json()
        self.run()

    def setup_pygame(self):
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.gameClock = pygame.time.Clock()

    def process_json(self):
        self.draw_json = {}

        cont_blocks = len(self.json_data['continents'])
        blocks = math.ceil(math.sqrt(cont_blocks))                  # for calculating the blocks the screen going to be seperated
        cont_blocks_taken = [0] * (int(blocks) ** 2)
        j = random.randint(0, int(blocks) ** 2 - 1)

        for cont in self.json_data['continents']:
            while(cont_blocks_taken[j] == 1):
                j = random.randint(0, int(blocks) ** 2 - 1)
            cont_blocks_taken[j] = 1
            x_blockSize = math.floor(self.screenWidth / blocks)
            y_blockSize = math.floor(self.screenHeight / blocks)
            x_rand = random.randint(-math.floor(x_blockSize * const.center_offset), math.floor(x_blockSize * const.center_offset))
            y_rand = random.randint(-math.floor(y_blockSize * const.center_offset), math.floor(y_blockSize * const.center_offset))
            center_x = (x_blockSize) * ((j % blocks) + 1 - 0.5) + x_rand
            center_y = (y_blockSize) * (math.floor(j / blocks) + 1 - 0.5) + y_rand

            i = 0
            isp_amount = len(cont['isps'])
            for isp in cont['isps']:
                x_offset = random.randint(-math.floor(x_blockSize * const.isp_offset), math.floor(x_blockSize * const.isp_offset))
                y_offset = random.randint(-math.floor(y_blockSize * const.isp_offset), math.floor(y_blockSize * const.isp_offset))
                x = int(center_x + (const.isp_radius * x_blockSize / 2) * math.cos((2 * math.pi / isp_amount) * i)) + x_offset
                y = int(center_y + (const.isp_radius * y_blockSize / 2) * math.sin((2 * math.pi / isp_amount) * i)) + y_offset
                self.draw_json[isp['id']] = Node(x, y, 'isp')

                k = 0
                city_amount = len(isp['cities'])
                for city in isp['cities']:
                    x_offset = random.randint(-math.floor(x_blockSize * const.city_offset), math.floor(x_blockSize * const.city_offset))
                    y_offset = random.randint(-math.floor(y_blockSize * const.city_offset), math.floor(y_blockSize * const.city_offset))
                    x = int(self.draw_json[isp['id']].x + (const.city_radius * x_blockSize / 2) * math.cos((2 * math.pi / city_amount) * k)) + x_offset
                    y = int(self.draw_json[isp['id']].y + (const.city_radius * y_blockSize / 2) * math.sin((2 * math.pi / city_amount) * k)) + y_offset
                    self.draw_json[city.uid] = Node(x, y, 'small_city')
                    k += 1
                i += 1

            i = 0
            datacenter_amount = len(cont['datacenters'])
            for datacenter in cont['datacenters']:
                x_offset = random.randint(-math.floor(x_blockSize * const.datacenter_offset), math.floor(x_blockSize * const.datacenter_offset))
                y_offset = random.randint(-math.floor(y_blockSize * const.datacenter_offset), math.floor(y_blockSize * const.datacenter_offset))
                x = int(center_x + (const.datacenter_radius * x_blockSize / 2) * math.cos((2 * math.pi / datacenter_amount) * i)) + x_offset
                y = int(center_y + (const.datacenter_radius * y_blockSize / 2) * math.sin((2 * math.pi / datacenter_amount) * i)) + y_offset
                self.draw_json[datacenter['id']] = Node(x, y, 'datacenter')
                i += 1

    def run(self):
        while 1:
            # Make sure game is on 60 FPS
            self.gameClock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = False if self.running else True
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.quit()
                        pygame.quit()
                        sys.exit()
            if self.running:
                self.ticks += 1
                if(self.ticks % self.ticks_per_turn == 0):
                    self.change_turn(self.ticks / self.ticks_per_turn)
                self.update()
                self.draw()

    def update(self):
        return None

    def draw(self):
        # ani.interpolate(self.screen, self.draw_json, self.json_data, 200)
        self.screen.fill(const.WHITE)
        for key, value in self.draw_json.iteritems():
            value.draw(self.screen)
        for edge in self.json_data['edges']:
            v1, v2 = edge
            pygame.draw.line(self.screen, const.BLACK, [self.draw_json[v1].x, self.draw_json[v1].y], [self.draw_json[v2].x, self.draw_json[v2].y], 1)
        pygame.display.update()
        pygame.display.flip()

    def add_turn(self, json):
        self.turn_json.append(json)

    def change_turn(self, turn):
        if(len(self.turn_json) > turn):
            return None
        else:
            print("Next turn does not exist")
            self.ticks -= 1
            self.running = False
