import math
import random
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

# def ellipse_interp(screen, draw_json, json_data, frames):
#     interp_num = frames - 1
#     b = random.randint(1, 5)
#     for i in range(frames):
#         screen.fill(const.WHITE)
#         for key, value in draw_json.iteritems():
#             if value['type'] == 'isp':
#                 pygame.draw.circle(screen, const.RED, [value['x'], value['y']], const.isp_size)
#             elif value['type'] == 'datacenter':
#                 pygame.draw.circle(screen, const.GREEN, [value['x'], value['y']], const.datacenter_size)
#             elif value['type'] == 'city':
#                 pygame.draw.circle(screen, const.BLUE, [value['x'], value['y']], const.city_size)
#         for edge in json_data['edges']:
#             v1, v2 = edge
#             # ellipse formula
#             # (x - h)^2 / a^2 + (y - k)^2 / b^2 = 1
#             # solving for y
#             # y = k + sqrt((1 - (x-h)^2/a^2) * b^2) 
#             x1 = draw_json[v1]['x']
#             x2 = draw_json[v2]['x']
#             y1 = draw_json[v1]['y']
#             y2 = draw_json[v2]['y']
#             h = (x1 + x2) / 2
#             k = (y1 + y2) / 2
#             a = x1 - h
#             if a == 0:
#                 a = math.hypot(x1 - h, y1 - k)
#             drawX = x1 * i / interp_num + x2 * (interp_num - i) / interp_num
#             drawY = k + math.sqrt(abs((1 - (drawX - h)**2 / a**2) * b**2))
#             pygame.draw.circle(screen, const.BLACK, [int(drawX), int(drawY)], 3)
#         pygame.display.update()
#         pygame.display.flip()
