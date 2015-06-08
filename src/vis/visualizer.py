#!/usr/bin/env python2
import pygame
import sys
import math
import random
import vis_constants as const
import animate as ani


class Visualizer(object):

    def __init__(self, json_data):
        self.screenHeight = const.screenHeight
        self.screenWidth = const.screenWidth
        self.title = const.title
        self.fps = const.FPStgt
        self.running = True

        self.json_data = json_data

        pygame.init()
        self.setup()
        self.process_json()
        self.run()

    def setup(self):
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
                self.draw_json[isp['id']] = {}
                self.draw_json[isp['id']]['type'] = 'isp'
                x_offset = random.randint(-math.floor(x_blockSize * const.isp_offset), math.floor(x_blockSize * const.isp_offset))
                y_offset = random.randint(-math.floor(y_blockSize * const.isp_offset), math.floor(y_blockSize * const.isp_offset))
                self.draw_json[isp['id']]['x'] = int(center_x + (const.isp_radius * x_blockSize / 2) * math.cos((2 * math.pi / isp_amount) * i)) + x_offset
                self.draw_json[isp['id']]['y'] = int(center_y + (const.isp_radius * y_blockSize / 2) * math.sin((2 * math.pi / isp_amount) * i)) + y_offset

                k = 0
                city_amount = len(isp['cities'])
                for city in isp['cities']:
                    self.draw_json[city.uid] = {}
                    self.draw_json[city.uid]['type'] = 'city'
                    x_offset = random.randint(-math.floor(x_blockSize * const.city_offset), math.floor(x_blockSize * const.city_offset))
                    y_offset = random.randint(-math.floor(y_blockSize * const.city_offset), math.floor(y_blockSize * const.city_offset))
                    self.draw_json[city.uid]['x'] = int(self.draw_json[isp['id']]['x'] + (const.city_radius * x_blockSize / 2) * math.cos((2 * math.pi / city_amount) * k)) + x_offset
                    self.draw_json[city.uid]['y'] = int(self.draw_json[isp['id']]['y'] + (const.city_radius * y_blockSize / 2) * math.sin((2 * math.pi / city_amount) * k)) + y_offset
                    k += 1
                i += 1

            i = 0
            datacenter_amount = len(cont['datacenters'])
            for datacenter in cont['datacenters']:
                self.draw_json[datacenter['id']] = {}
                self.draw_json[datacenter['id']]['type'] = 'datacenter'
                x_offset = random.randint(-math.floor(x_blockSize * const.datacenter_offset), math.floor(x_blockSize * const.datacenter_offset))
                y_offset = random.randint(-math.floor(y_blockSize * const.datacenter_offset), math.floor(y_blockSize * const.datacenter_offset))
                self.draw_json[datacenter['id']]['x'] = int(center_x + (const.datacenter_radius * x_blockSize / 2) * math.cos((2 * math.pi / datacenter_amount) * i)) + x_offset
                self.draw_json[datacenter['id']]['y'] = int(center_y + (const.datacenter_radius * y_blockSize / 2) * math.sin((2 * math.pi / datacenter_amount) * i)) + y_offset
                i += 1

    def run(self):
        while 1:
            # Make sure game is on 60 FPS
            self.gameClock.tick(self.fps)

            self.update()
            self.draw()
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

    def update(self):
        self.fps = 60

    def draw(self):
        ani.interpolate(self.screen, self.draw_json, self.json_data)
        # for key, value in self.draw_json.iteritems():
        #     if value['type'] == 'isp':
        #         pygame.draw.circle(self.screen, const.RED, [value['x'], value['y']], const.isp_size)
        #     elif value['type'] == 'datacenter':
        #         pygame.draw.circle(self.screen, const.GREEN, [value['x'], value['y']], const.datacenter_size)
        #     elif value['type'] == 'city':
        #         pygame.draw.circle(self.screen, const.BLUE, [value['x'], value['y']], const.city_size)
        # for edge in self.json_data['edges']:
        #     v1, v2 = edge
        #     # pygame.draw.line(self.screen, const.BLACK, [self.draw_json[v1]['x'], self.draw_json[v1]['y']], [self.draw_json[v2]['x'], self.draw_json[v2]['y']], 1)
        # pygame.display.update()
        # pygame.display.flip()
