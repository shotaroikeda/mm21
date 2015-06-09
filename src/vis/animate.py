import visualizer
import pygame
import vis_constants as const


def interpolate(screen, draw_json, json_data, frames):
    interp_num = frames - 1
    for i in range(frames):
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
            pygame.draw.circle(screen, const.BLACK, [draw_json[v1]['x'] * i / interp_num + draw_json[v2]['x'] * (interp_num - i) / interp_num, draw_json[v1]['y'] * i / interp_num + draw_json[v2]['y'] * (interp_num - i) / interp_num], 3)
        pygame.display.update()
        pygame.display.flip()
