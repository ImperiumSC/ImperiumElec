import math
import os
import time

import numpy as np
import pygame

# Constants
OS_CONSTANT_WINDOWS = "Windows"
OS_CONSTANT_WINDOWS_NT = "nt"
print(os.name)
DEBUGGING_ENABLED = True

if os.name == OS_CONSTANT_WINDOWS_NT or os.name == OS_CONSTANT_WINDOWS:
    import ctypes

    ctypes.windll.user32.SetProcessDPIAware()

RED = (255, 0, 0)
DARK_RED = (128, 0, 0)
GREEN = (0, 255, 0)
DARK_DARK_GREEN = (0, 64, 0)
DARK_GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRON_BLUE = (0, 255, 255)
HALF_BRIGHT_TRON_BLUE = (0, int(255 / 2), int(255 / 2))
TRON_EVIL_ORANGE = (255, 178, 0)
TRON_HALF_EVIL_ORANGE = (int(TRON_EVIL_ORANGE[1] / 2), int(TRON_EVIL_ORANGE[1] / 2), int(TRON_EVIL_ORANGE[2] / 2))

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


def fill_circle_segment_in_between(screen, midpoint, inner_radius, outer_radius, degrees, steps, color, start_angle=-1,
                                   end_angle=-1):
    lw = 25
    if start_angle == -1 and end_angle == -1:
        start_angle = math.floor(360 - 90 - degrees / 2 - 180)
        end_angle = math.ceil(360 - 90 + degrees / 2 - 180)
    else:
        # start_angle = start_angle - 180
        # end_angle = end_angle - 180
        pass
    mid_x = midpoint[0]
    mid_y = midpoint[1]
    start_angle = start_angle - 180
    end_angle = end_angle - 180
    for angle_degrees in np.linspace(start_angle, end_angle, steps, endpoint=False):
        angle_radians = angle_degrees * math.pi / 180
        start_xy = (int((inner_radius + 1) * math.cos(angle_radians) + mid_x),
                    int((inner_radius + 1) * math.sin(angle_radians)) + mid_y)
        end_xy = (int((outer_radius + 1) * math.cos(angle_radians)) + mid_x,
                  int((outer_radius + 1) * math.sin(angle_radians)) + mid_y)
        pygame.draw.line(screen, color, start_xy, end_xy, lw)


def draw_initial_gui(screen, speed=45, charge=50):
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
    center_circle_radius = math.floor(min(display_width, display_height) / 2)
    center_circle_width = math.floor(0.02315 * 2 * center_circle_radius)  # width of curve creating circle
    center_circle_radius_ratio = 0.8  # How big should the inner circle be, with respect to outer circle
    pygame.draw.circle(screen, MAIN_GAUGE_COLOR, display_midpoint_tuple, center_circle_radius, center_circle_width)
    draw_tron_center_circle(screen, center_circle_radius - center_circle_width, center_circle_radius,
                            display_midpoint_tuple)
    # Draw the outer circle.
    # 1) A plain circle, to ensure anti-aliasing and stuff doesn't ruin the effect
    # 2) Draw progressively smaller circles
    pygame.draw.circle(screen, MAIN_GAUGE_COLOR, display_midpoint_tuple,
                       int(center_circle_radius_ratio * center_circle_radius), center_circle_width)
    draw_tron_center_circle(screen,
                            int(center_circle_radius * center_circle_radius_ratio - center_circle_width),
                            int(center_circle_radius_ratio * center_circle_radius),
                            display_midpoint_tuple)
    bottom_center_segment_width = 75
    # fill_circle_segment_in_between(screen, display_midpoint_tuple,
    #                                int(center_circle_radius * center_circle_radius_ratio),
    #                                int(center_circle_radius - center_circle_width), 360,
    #                                400, TRON_EVIL_ORANGE)
    pygame.draw.circle(screen, TRON_EVIL_ORANGE, display_midpoint_tuple, center_circle_radius - center_circle_width,
                       center_circle_width)
    # fill_circle_segment_in_between(screen, display_midpoint_tuple,
    #                                int(center_circle_radius * center_circle_radius_ratio),
    #                                int(center_circle_radius - center_circle_width), bottom_center_segment_width,
    #                                200, HALF_BRIGHT_TRON_BLUE)
    draw_power_consumption(bottom_center_segment_width, center_circle_radius, center_circle_radius_ratio,
                           center_circle_width, charge, display_height, display_width, screen)

    # speed_tuple = speedometer(bottom_center_segment_width, speed)
    # charge_tuple = chargeometer(bottom_center_segment_width, charge)
    # # fill_circle_segment_in_between(screen, display_midpoint_tuple, int(center_circle_radius*center_circle_radius_ratio),
    # #                                int(center_circle_radius-center_circle_width),-1, 5000, GREEN,
    # #                                -90+bottom_center_segment_width/2, 90)
    # fill_circle_segment_in_between(screen, display_midpoint_tuple,
    #                                int(center_circle_radius * center_circle_radius_ratio),
    #                                int(center_circle_radius - center_circle_width), -1, 200, GREEN,
    #                                speed_tuple[0], speed_tuple[1])
    # fill_circle_segment_in_between(screen, display_midpoint_tuple,
    #                                int(center_circle_radius * center_circle_radius_ratio),
    #                                int(center_circle_radius - center_circle_width), -1, 200, RED,
    #                                charge_tuple[0], charge_tuple[1])

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


def draw_power_consumption(bottom_center_segment_width, center_circle_radius, center_circle_radius_ratio,
                           center_circle_width, charge, display_height, display_width, screen):
    start_x_shading = int((
                                  display_width - display_height + 2 * center_circle_width) / 2)  # (display_width - center_circle_radius) / 2 + center_circle_width/2
    start_y_shading = center_circle_width
    radius = center_circle_radius - center_circle_width
    width = int(center_circle_radius - center_circle_radius_ratio * center_circle_radius - center_circle_width)
    start_angle = math.radians(-90 + bottom_center_segment_width / 2)
    charge_range = 180 - bottom_center_segment_width / 2
    end_angle = math.radians(charge_range * charge / 100 - 90 + bottom_center_segment_width / 2)
    print(start_angle)
    print(end_angle)
    center_circle_segment_shade(screen, (start_x_shading, start_y_shading, radius * 2, radius * 2), BLUE, width,
                                start_angle, end_angle)


def speedometer(width, percentage):
    range = 90 - (-90 + width / 2)
    range = range * percentage / 100
    start = -90 + width / 2
    end = range + start
    return (start, end)


def chargeometer(width, percentage):
    range = int(percentage / 100 * (180 - width / 2))
    meme = (-90 - width / 2, -90 - width / 2 - range)
    return meme


def center_circle_segment_shade(screen, rect, color, width, start, end):
    pygame.draw.arc(screen, color, rect, start, end, width)


def draw_tron_center_circle(screen, radius_start, radius_end, midpoint_tuple):
    red_gradiant = 0.75
    bg_gradiant = 0.15
    radius_end = radius_end + 1
    circle_width = abs(radius_start - radius_end)
    half_circle_width = math.ceil(circle_width / 2)
    curr_color = TRON_BLUE
    counter = 0
    for i in range(radius_start, radius_end, 1):
        pygame.draw.circle(screen, curr_color, midpoint_tuple, i, 1)
        temp_color = [0, 0, 0]
        for j in range(3):
            if j == 0:
                temp_color[j] = int(math.pow(math.sqrt(curr_color[j]) + red_gradiant, 2))
            else:
                temp_color[j] = int(math.pow(math.sqrt(curr_color[j]) - bg_gradiant, 2))
        curr_color = (temp_color[0], temp_color[1], temp_color[2])


def conditional_print(s):
    if DEBUGGING_ENABLED:
        print(s)


def main():
    screen = initialize_pygame()
    init = time.process_time_ns()
    draw_initial_gui(screen)
    # Debugging statement -- to allow viewer to view initial screen before quitting
    print(time.process_time_ns() - init)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                exit(0)


main()
