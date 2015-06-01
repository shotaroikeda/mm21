#!/usr/bin/env python2
import pygame
import sys
import math
import vis_constants as const


class Visualizer(object):

    def __init__(self, json_data):
        self.screenHeight = const.screenHeight
        self.screenWidth = const.screenWidth
        self.isp_radius = const.isp_radius
        self.isp_size = const.isp_size
        self.datacenter_radius = const.datacenter_radius
        self.datacenter_size = const.datacenter_size
        self.city_radius = const.city_radius
        self.city_size = const.city_size
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

        j = 0
        cont_blocks = len(self.json_data['continents'])
        for cont in self.json_data['continents']:
            center_x = (self.screenWidth / cont_blocks) * (j + 1 - 0.5)
            center_y = 250

            i = 0
            isp_amount = len(cont['isps'])
            for isp in cont['isps']:
                self.draw_json[isp['id']] = {}
                self.draw_json[isp['id']]['type'] = 'isp'
                self.draw_json[isp['id']]['x'] = int(center_x + self.isp_radius * math.cos((2 * math.pi / isp_amount) * i))
                self.draw_json[isp['id']]['y'] = int(center_y + self.isp_radius * math.sin((2 * math.pi / isp_amount) * i))

                k = 0
                city_amount = len(isp['cities'])
                for city in isp['cities']:
                    self.draw_json[city.uid] = {}
                    self.draw_json[city.uid]['type'] = 'city'
                    self.draw_json[city.uid]['x'] = int(self.draw_json[isp['id']]['x'] + self.city_radius * math.cos((2 * math.pi / city_amount) * k))
                    self.draw_json[city.uid]['y'] = int(self.draw_json[isp['id']]['y'] + self.city_radius * math.sin((2 * math.pi / city_amount) * k))
                    k += 1
                i += 1

            i = 0
            datacenter_amount = len(cont['datacenters'])
            for datacenter in cont['datacenters']:
                self.draw_json[datacenter['id']] = {}
                self.draw_json[datacenter['id']]['type'] = 'datacenter'
                self.draw_json[datacenter['id']]['x'] = int(center_x + self.datacenter_radius * math.cos((2 * math.pi / datacenter_amount) * i))
                self.draw_json[datacenter['id']]['y'] = int(center_y + self.datacenter_radius * math.sin((2 * math.pi / datacenter_amount) * i))
                i += 1
            j += 1

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

    def update(self):
        self.fps = 60

    def draw(self):
        self.screen.fill(const.WHITE)
        for key, value in self.draw_json.iteritems():
            if value['type'] == 'isp':
                pygame.draw.circle(self.screen, const.RED, [value['x'], value['y']], self.isp_size)
            elif value['type'] == 'datacenter':
                pygame.draw.circle(self.screen, const.GREEN, [value['x'], value['y']], self.datacenter_size)
            elif value['type'] == 'city':
                pygame.draw.circle(self.screen, const.BLUE, [value['x'], value['y']], self.city_size)
        for edge in self.json_data['edges']:
            v1, v2 = edge
            pygame.draw.line(self.screen, const.BLACK, [self.draw_json[v1]['x'], self.draw_json[v1]['y']],
                                                     [self.draw_json[v2]['x'], self.draw_json[v2]['y']], 1)
        pygame.display.update()
        pygame.display.flip()
