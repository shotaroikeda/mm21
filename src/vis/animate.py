import visualizer
import pygame
import vis_constants as const

def interpolate(screen, draw_json, json_data):
    for i in range(200):
        screen.fill(const.WHITE)
        for key, value in draw_json.iteritems():
            if value['type'] == 'isp':
                pygame.draw.circle(screen, const.RED, [value['x'], value['y']], const.isp_size)
            elif value['type'] == 'datacenter':
                pygame.draw.circle(screen, const.GREEN, [value['x'], value['y']], const.datacenter_size)
            elif value['type'] == 'city':
                pygame.draw.circle(screen, const.BLUE, [value['x'], value['y']], const.city_size)
        for edge in json_data['edges']:
            v1, v2 = edge
            pygame.draw.circle(screen, const.BLACK, [draw_json[v1]['x'] * i/199 + draw_json[v2]['x'] * (199 - i) /199, draw_json[v1]['y'] * i / 199 + draw_json[v2]['y'] * (199 - i) /199], 3)
        pygame.display.update()
        pygame.display.flip()
