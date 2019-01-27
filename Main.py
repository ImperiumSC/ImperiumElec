import pygame
import math
import time
import numpy as np
import os
from decimal import Decimal

# Constants
OS_CONSTANT_WINDOWS = "Windows"
OS_CONSTANT_WINDOWS_NT = "nt"
print(os.name)
DEBUGGING_ENABLED = True

if os.name == OS_CONSTANT_WINDOWS_NT or os.name == OS_CONSTANT_WINDOWS:
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRON_BLUE = (0, 255, 255)
HALF_BRIGHT_TRON_BLUE = (0, int(255/2),int(255/2))
TRON_EVIL_ORANGE = (255, 178, 0)
TRON_HALF_EVIL_ORANGE = (int(TRON_EVIL_ORANGE[1]/2), int(TRON_EVIL_ORANGE[1]/2), int(TRON_EVIL_ORANGE[2]/2))

MAIN_GAUGE_COLOR = TRON_BLUE
SPEEDOMETER_COLOR = RED
CHARGEOMETER_COLOR = GREEN
INDICATOR_TURN_SIGNAL_OFF_COLOR = None
INDICATOR_TURN_SIGNAL_ON_COLOR = None
INDICATOR_BATTERY_TEMPERATURE_COOL_COLOR = None
INDICATOR_BATTERY_TEMPERATURE_WARM_COLOR = None
INDICATOR_BATTERY_TEMPERATURE_WARN_COLOR = None
INDICATOR_BATTERY_TEMPERATURE_DANGER_COLOR = None


def initialize_pygame():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    return screen


def fill_circle_segment_in_between(screen, midpoint, inner_radius, outer_radius, degrees, steps, color, start_angle=-1, end_angle=-1):
    if start_angle==-1 and end_angle == -1:
        start_angle = math.floor(360-90-degrees/2-180)
        end_angle = math.ceil(360-90+degrees/2-180)
        mid_x = midpoint[0]
        mid_y = midpoint[1]
        for angle_degrees in np.linspace(start_angle, end_angle, steps, endpoint=False):
            angle_radians = angle_degrees * math.pi / 180
            start_xy = (int((inner_radius+1)*math.cos(angle_radians)+mid_x), int((inner_radius+1)*math.sin(angle_radians))+mid_y)
            end_xy = (int((outer_radius+1)*math.cos(angle_radians))+mid_x, int((outer_radius+1)*math.sin(angle_radians))+mid_y)
            pygame.draw.line(screen, color, start_xy, end_xy, 2)
    else:
        mid_x = midpoint[0]
        mid_y = midpoint[1]
        start_angle = start_angle-180
        end_angle = end_angle-180
        for angle_degrees in np.linspace(start_angle, end_angle, steps, endpoint=False):
            angle_radians = angle_degrees * math.pi / 180
            start_xy = (int((inner_radius + 1) * math.cos(angle_radians) + mid_x),
                        int((inner_radius + 1) * math.sin(angle_radians)) + mid_y)
            end_xy = (int((outer_radius + 1) * math.cos(angle_radians)) + mid_x,
                      int((outer_radius + 1) * math.sin(angle_radians)) + mid_y)
            pygame.draw.line(screen, color, start_xy, end_xy, 2)


def draw_initial_gui(screen):
    # Get current display information, to allow for adaptive GUI.
    current_display_info = pygame.display.Info()
    display_width, display_height = current_display_info.current_w, current_display_info.current_h
    conditional_print("Display Width: " + str(display_width))
    conditional_print("Display Height: " + str(display_height))

    # Find the midpoint of the display in (width, height) format
    display_midpoint_tuple = (math.floor(display_width / 2), math.floor(display_height / 2))
    conditional_print("display midpoint = " + str(display_midpoint_tuple))
    # Test statement, prints display size.
    # Main Gauge (center-of-screen)
    # pygame.draw.circle(display_surface, (color tuple), (center-position tuple), radius/diameter???, line width)
    center_circle_radius = math.floor(min(display_width, display_height) / 2)
    center_circle_width = math.floor(0.02315*2 * center_circle_radius)
    center_circle_radius_ratio = 0.8
    pygame.draw.circle(screen, MAIN_GAUGE_COLOR, display_midpoint_tuple, center_circle_radius,
                       center_circle_width)  # math.floor(min(display_width, display_height)/2)
    draw_tron_center_circle(screen, center_circle_radius-center_circle_width, center_circle_radius,
                            display_midpoint_tuple)
    pygame.draw.circle(screen, MAIN_GAUGE_COLOR, display_midpoint_tuple, int(center_circle_radius_ratio *
                                                                             center_circle_radius),
                       center_circle_width)
    draw_tron_center_circle(screen,
                            int(center_circle_radius*center_circle_radius_ratio - center_circle_width),
                            int(center_circle_radius_ratio * center_circle_radius),
                            display_midpoint_tuple)
    bottom_center_segment_width = 75
    fill_circle_segment_in_between(screen, display_midpoint_tuple,
                                   int(center_circle_radius * center_circle_radius_ratio),
                                   int(center_circle_radius - center_circle_width), 360,
                                   int(5000 / 75 * 360), TRON_EVIL_ORANGE)
    fill_circle_segment_in_between(screen, display_midpoint_tuple, int(center_circle_radius*center_circle_radius_ratio),
                                   int(center_circle_radius-center_circle_width), bottom_center_segment_width,
                                   5000, HALF_BRIGHT_TRON_BLUE)
    speed_tuple = speedometer_percentage(bottom_center_segment_width, 85)
    charge_tuple = chargeometer(bottom_center_segment_width, 45)
    # fill_circle_segment_in_between(screen, display_midpoint_tuple, int(center_circle_radius*center_circle_radius_ratio),
    #                                int(center_circle_radius-center_circle_width),-1, 5000, GREEN,
    #                                -90+bottom_center_segment_width/2, 90)
    fill_circle_segment_in_between(screen, display_midpoint_tuple,
                                   int(center_circle_radius * center_circle_radius_ratio),
                                   int(center_circle_radius - center_circle_width), -1, 5000, GREEN,
                                   speed_tuple[0], speed_tuple[1])
    fill_circle_segment_in_between(screen, display_midpoint_tuple,
                                   int(center_circle_radius * center_circle_radius_ratio),
                                   int(center_circle_radius - center_circle_width), -1, 5000, RED,
                                   charge_tuple[0], charge_tuple[1])


    # Debugging Statement
    conditional_print("Radius of Center Circle: " + str(center_circle_radius))

    # # DEBUGGING BOX
    # # break the midpoint tuple into x and debugging_rectangle_y variables
    # display_midpoint_x, display_midpoint_y = display_midpoint_tuple
    # # Draw the debugging box
    # # pygame.draw.rect(display_surface, (color tuple), (x, y, w, h), line width)
    # # debugging_rectangle_x, debugging_rectangle_y = position; debugging_rectangle_width, debugging_rectangle_height =
    # # dimensions of rect
    # debugging_rectangle_width = display_width / 2 - 500
    # debugging_rectangle_height = display_height / 2 - 500
    # debugging_rectangle_x = display_midpoint_x - debugging_rectangle_width / 2
    # debugging_rectangle_y = display_midpoint_y - debugging_rectangle_height / 2
    # pygame.draw.rect(screen, BLUE, (
    #     debugging_rectangle_x, debugging_rectangle_y, debugging_rectangle_width, debugging_rectangle_height), 3)
    # conditional_print("debugging_rectangle_width: " + str(debugging_rectangle_width))
    # conditional_print("debugging_rectangle_height: " + str(debugging_rectangle_height))
    # conditional_print("debugging_rectangle_x: " + str(debugging_rectangle_x))
    # conditional_print("debugging_rectangle_y: " + str(debugging_rectangle_y))
    # # Keep this block of code at the end -- used for updating the display and returning the final display, as necessary
    pygame.display.update()
    return screen

def speedometer_percentage(width, percentage):
    range = 90-(-90+width/2)
    range = range*percentage/100
    start = -90+width/2
    end = range+start
    return (start, end)


def chargeometer(width, percentage):
    range = int(percentage/100*(180-width/2))
    meme = (-90-width/2, -90-width/2-range)
    return meme



def draw_tron_center_circle(screen, radius_start, radius_end, midpoint_tuple):
    RED_GRADIANT = 0.75
    BG_GRADIANT = 0.15
    radius_end= radius_end+1
    circle_width = abs(radius_start-radius_end)
    half_circle_width = math.ceil(circle_width/2)
    # start_color = (TRON_BLUE[0]+half_circle_width*RED_GRADIANT, TRON_BLUE[1]-half_circle_width*BG_GRADIANT, TRON_BLUE[2]
    #                - half_circle_width*BG_GRADIANT)
    curr_color = TRON_BLUE
    counter = 0
    for i in range(radius_start,radius_end,1):
        pygame.draw.circle(screen, curr_color, midpoint_tuple, i, 1)

        curr_color = (int(math.pow(math.sqrt(curr_color[0]) + RED_GRADIANT,2)), int(math.pow(math.sqrt(curr_color[1]) - BG_GRADIANT,2)), int(math.pow(math.sqrt(curr_color[2]) - BG_GRADIANT,2)))
        # if counter < half_circle_width:
        #     curr_color = (curr_color[0] + GRADIANT, curr_color[1] - GRADIANT, curr_color[2] - GRADIANT)
        # else:
        #     curr_color = (curr_color[0] - GRADIANT, curr_color[1] + GRADIANT, curr_color[2] + GRADIANT)


def conditional_print(s):
    if DEBUGGING_ENABLED:
        print(s)


def main():
    screen = initialize_pygame()
    draw_initial_gui(screen)
    # Debugging statement -- to allow viewer to view initial screen before quitting
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                exit(0)


main()
