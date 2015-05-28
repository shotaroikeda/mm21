#!/usr/bin/env python2
import pygame
import sys
import math
import vis_constants as const


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
        self.isp_radius = 100
        self.isp_size = 10
        self.datacenter_radius = 30
        self.datacenter_size = 10
        self.city_radius = 20
        self.city_size = 5
        self.draw_json = {}

        j = 0
        cont_blocks = len(self.json_data['continents'])
        for cont in self.json_data['continents']:
            center_x = (self.screenWidth / cont_blocks) * (j + 1) - (self.screenWidth / cont_blocks)/2
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
            self.update()
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

    def update(self):
        self.fps = 60

    def draw(self):
        self.screen.fill((255, 255, 255))
        for key, value in self.draw_json.iteritems():
            if value['type'] == 'isp':
                pygame.draw.circle(self.screen, (255, 0, 0), [value['x'], value['y']], self.isp_size)
            if value['type'] == 'datacenter':
                pygame.draw.circle(self.screen, (0, 255, 0), [value['x'], value['y']], self.datacenter_size)
            if value['type'] == 'city':
                pygame.draw.circle(self.screen, (0, 0, 255), [value['x'], value['y']], self.city_size)
        for edge in self.json_data['edges']:
            v1, v2 = edge
            pygame.draw.line(self.screen, (0, 0, 0), [self.draw_json[v1]['x'], self.draw_json[v1]['y']],
                                                     [self.draw_json[v2]['x'], self.draw_json[v2]['y']], 1)
        pygame.display.flip()
