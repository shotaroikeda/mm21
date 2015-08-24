#!/usr/bin/env python2
import pygame
import sys
import math
import random
from node import Node
from animation import Upgrade, ChangeOwner, AddRootkit, CleanRootkit, ISP, Infiltration, Heal, DDOS
import vis_constants as const
# import animate as ani


class Visualizer(object):

    def __init__(self, _map_json_data, _width=const.screenWidth, _height=const.screenHeight, _debug=False, _log_json_data=None):
        # Check and init vis
        self.screenHeight = _height
        self.screenWidth = _width
        self.title = const.title
        self.fps = const.FPStgt
        self.running = True
        self.debug = _debug
        self.json_data = _map_json_data
        self.ticks = 0
        self.ticks_per_turn = 60
        self.turn_json = []
        self.game_animations = []

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
        self.myfont = pygame.font.SysFont("monospace", 12)
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
                    self.draw_json[city] = Node(x, y, 'small_city')
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
        while 1:  # Run game forever till exit
            self.gameClock.tick(self.fps)  # Make sure game is on 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.running = False if self.running else True
                    if (self.debug):
                        if event.key == pygame.K_LEFT:
                            self.ticks -= self.ticks_per_turn + self.ticks % self.ticks_per_turn
                            if (self.ticks < 0):
                                self.ticks = 0
                            print("Changed to turn " + str(self.ticks / self.ticks_per_turn))
                        if event.key == pygame.K_ESCAPE:
                            pygame.display.quit()
                            pygame.quit()
                            sys.exit()
            if self.running:
                if(self.ticks % self.ticks_per_turn == 0 and self.ticks > 0):
                    self.change_turn(self.ticks / self.ticks_per_turn)
                self.update()
                self.draw()
                self.ticks += 1

    def update(self):
        for key, value in self.draw_json.iteritems():
            value.update()
        for anim in self.game_animations:
            anim.update()

    def draw(self):
        # ani.interpolate(self.screen, self.draw_json, self.json_data, 200)
        self.screen.fill(const.WHITE)
        if self.debug:
            for edge in self.json_data['edges']:
                v1, v2 = edge
                pygame.draw.line(self.screen, const.BLACK, [self.draw_json[v1].x, self.draw_json[v1].y], [self.draw_json[v2].x, self.draw_json[v2].y], 1)
        for key, value in self.draw_json.iteritems():
            value.draw(self.screen)
            if self.debug:
                node_id = self.myfont.render(str(key), 1, (0, 0, 0))
                self.screen.blit(node_id, (value.x - 7, value.y - 7))
        for anim in self.game_animations:
            anim.draw()  # draw global animations
        pygame.display.update()
        pygame.display.flip()

    def add_turn(self, json):
        self.turn_json.append(json)

    def change_turn(self, turn):
        if(len(self.turn_json) > turn):
            if (self.debug):
                print("Processing turn " + str(self.ticks / self.ticks_per_turn))
            for node in self.turn_json[self.ticks / self.ticks_per_turn]['map']:
                # How it should work
                # self.add_animations(node, self.turn_json[(self.ticks / self.tickss_per_turn) - 1][node['id']])
                for prev_node in self.turn_json[(self.ticks / self.ticks_per_turn) - 1]['map']:
                    self.add_animations(node, prev_node)
        else:
            print("Next turn does not exist")
            self.running = False

    def add_animations(self, node, prev_node):
        # Upgrade has occured
        if (node['softwareLevel'] != prev_node['softwareLevel']):
            if (not self.found_anim(node, Upgrade)):
                self.draw_json[node['id']].animations.append(Upgrade())

        # Owner has changed, do CONTROL animation
        if node['owner'] != prev_node['owner']:
            if (not self.found_anim(node, ChangeOwner)):
                self.draw_json[node['id']].animations.append(ChangeOwner())

        # Rootkit has been cleaned or rooted
        if node['rootkits'] != prev_node['rootkits']:
            if prev_node is None:
                if (not self.found_anim(node, AddRootkit)):
                    self.draw_json[node['id']].animations.append(AddRootkit())
            else:
                # TODO Remove rootkit?
                if (not self.found_anim(node, CleanRootkit)):
                    self.draw_json[node['id']].animations.append(CleanRootkit())

        # infiltration protection activated
        if node['isIPSed'] is True:
            if (not self.found_anim(node, ISP)):
                self.draw_json[node['id']].animations.append(ISP())

        # infiltration
        for i in range(5):
            curr_infrat_num = node['infiltration'][str(i)]
            prev_infrat_num = prev_node['infiltration'][str(i)]
            if curr_infrat_num != prev_infrat_num:
                if curr_infrat_num > prev_infrat_num:
                    if (not self.found_anim(node, Infiltration)):
                        # Being infiltrated, An attack has occured
                        self.draw_json[node['id']].animations.append(Infiltration())
                    break
                else:
                    if (not self.found_anim(node, Heal)):
                        # Is currently healing
                        self.draw_json[node['id']].animations.append(Heal())
                    break

        if node['isDDoSed']:
            if (not self.found_anim(node, DDOS)):
                self.draw_json[node['id']].animations.append(DDOS())
        # To ERIC
        # These two action has not been done and needs to be added ~~~~~~~~~~ 'Scan' and 'Port Scan'
        # Ace said that on the newest node.py, it would have a dictionary entry 'isDDoSed', currently it would not work since it doesn't have that entry and
        # it would raise a keyerror. But this part should be okay to merge once we get the latest version of node.py
        # if node['isDDoSed']:
        #     # DDOS
        #     pass

    def found_anim(self, node, animation_type):
        for animation in self.draw_json[node['id']].animations:
            if(type(animation) is animation_type):
                return True
        return False
