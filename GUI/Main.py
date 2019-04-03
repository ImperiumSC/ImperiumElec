import math
import os
import time

import numpy as np
import pygame

# Programming Constants
OS_CONSTANT_WINDOWS = "Windows"
OS_CONSTANT_WINDOWS_NT = "nt"
DEBUGGING_ENABLED = False
WAIT_AT_END = True
TIMING_ENABLED = False
TIMES = 500
if os.name == OS_CONSTANT_WINDOWS_NT or os.name == OS_CONSTANT_WINDOWS:
    import ctypes

    ctypes.windll.user32.SetProcessDPIAware()
    # We do this for testing software in Windows 10, which uses scaling. Unsure if this applies to macs, as the current
    # main developers only use Win10.

# Aesthetic Constants (Ratios, etc), Constants
DEGREES_TO_RADIANS_CONSTANT = 0.017453292519943295  # pi/180
CIRCLE_OVERLAP_WIDTH = 1  # pixels
SHADING_LINE_WIDTH_FILL_CIRCLE_SEGMENT_IN_BETWEEN = 25  # More = better quality when shading using the sketchy method
GRAPHICS_TO_MATH_DEGREES_SUBTRACTANT = 180  # For converting graphics angles to regular math angles (0 = +x axis)
CENTER_CIRCLE_WIDTH_RATIO = 0.0463
INNER_CIRCLE_RADIUS_RATIO = 0.8
BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES = 75
SPEED_END_ANGLE = math.radians(270 - BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES / 2)
BOTTOM_CENTER_SEGMENT_START_ANGLE_RADIANS = math.radians(
    -92 - BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES / 2)  # -90 -2 because of graphics lining up

MAX_SPEED = 60  # Solar Car Max speed mph
MAX_CHARGE = 100  # Maximum charge unit undetermined
MAX_INSTANTANEOUS_CHARGE = 100  # Max/min instantaneous power consumption, Wh
INSTANTANEOUS_CHARGE = MAX_INSTANTANEOUS_CHARGE  # initialization
SPEED = MAX_SPEED  # initialization
PERCENTAGE_SPEED = 100
PERCENTAGE_INSTANTANEOUS_CHARGE = 101
CHARGE = MAX_CHARGE

PYGAME_DISPLAY_INFO = CURRENT_DISPLAY_INFO = DISPLAY_WIDTH = DISPLAY_HEIGHT = DISPLAY_MIDPOINT_TUPLE = OUTER_CENTER_CIRCLE_WIDTH = OUTER_CENTER_CIRCLE_RADIUS = SPACE_OUTER_INNER_CIRCLE = SCREEN = INNER_CENTER_CIRCLE_RADIUS = INNER_OUTER_CENTER_CIRCLE_RADIUS = INNER_INNER_CENTER_CIRCLE_RADIUS = OUTER_INNER_CENTER_CIRCLE_RADIUS = None

# Color Constants
#   Reds
RED = (255, 0, 0)
DARK_RED = (128, 0, 0)
DARK_DARK_RED = (64, 0, 0)
#   Greens
GREEN = (0, 255, 0)
DARK_GREEN = (0, 128, 0)
DARK_DARK_GREEN = (0, 64, 0)
#   Blues
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 128)
DARK_DARK_BLUE = (0, 0, 64)
#   Other
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
#   Tron-Specific
TRON_BLUE = (0, 255, 255)
HALF_BRIGHT_TRON_BLUE = (0, 128, 128)
TRON_EVIL_ORANGE = (255, 178, 0)
TRON_HALF_EVIL_ORANGE = (127, 89, 0)

# Object Color Constants
MAIN_GAUGE_COLOR = TRON_BLUE
SPEEDOMETER_COLOR = RED
CHARGEOMETER_COLOR = GREEN
INDICATOR_TURN_SIGNAL_OFF_COLOR = None
INDICATOR_TURN_SIGNAL_ON_COLOR = None
INDICATOR_BATTERY_TEMPERATURE_COOL_COLOR = DARK_BLUE
INDICATOR_BATTERY_TEMPERATURE_WARM_COLOR = DARK_DARK_GREEN
INDICATOR_BATTERY_TEMPERATURE_WARN_COLOR = DARK_RED
INDICATOR_BATTERY_TEMPERATURE_DANGER_COLOR = RED


# Initialize pygame with necessary parameters, returning the surface (screen) object
def initialize_GUI():
    global PYGAME_DISPLAY_INFO, CURRENT_DISPLAY_INFO, DISPLAY_WIDTH, DISPLAY_HEIGHT, DISPLAY_MIDPOINT_TUPLE, OUTER_CENTER_CIRCLE_RADIUS, OUTER_CENTER_CIRCLE_WIDTH, SPACE_OUTER_INNER_CIRCLE, SCREEN, INNER_CENTER_CIRCLE_RADIUS, INNER_OUTER_CENTER_CIRCLE_RADIUS, INNER_INNER_CENTER_CIRCLE_RADIUS, OUTER_INNER_CENTER_CIRCLE_RADIUS
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    PYGAME_DISPLAY_INFO = pygame.display.Info()
    CURRENT_DISPLAY_INFO = PYGAME_DISPLAY_INFO
    DISPLAY_WIDTH, DISPLAY_HEIGHT = CURRENT_DISPLAY_INFO.current_w, CURRENT_DISPLAY_INFO.current_h
    DISPLAY_MIDPOINT_TUPLE = (math.floor(DISPLAY_WIDTH / 2), math.floor(DISPLAY_HEIGHT / 2))
    OUTER_CENTER_CIRCLE_RADIUS = math.floor(min(DISPLAY_WIDTH, DISPLAY_HEIGHT) / 2)
    INNER_CENTER_CIRCLE_RADIUS = OUTER_CENTER_CIRCLE_RADIUS * INNER_CIRCLE_RADIUS_RATIO
    OUTER_CENTER_CIRCLE_WIDTH = math.floor(
        CENTER_CIRCLE_WIDTH_RATIO * OUTER_CENTER_CIRCLE_RADIUS)  # width of curve creating circle
    SPACE_OUTER_INNER_CIRCLE = INNER_CIRCLE_RADIUS_RATIO  # How big should the inner circle be, with respect to outer circle
    SCREEN = screen
    INNER_OUTER_CENTER_CIRCLE_RADIUS = OUTER_CENTER_CIRCLE_RADIUS - OUTER_CENTER_CIRCLE_WIDTH
    INNER_INNER_CENTER_CIRCLE_RADIUS = int(
        OUTER_CENTER_CIRCLE_RADIUS * SPACE_OUTER_INNER_CIRCLE - OUTER_CENTER_CIRCLE_WIDTH)
    OUTER_INNER_CENTER_CIRCLE_RADIUS = int(SPACE_OUTER_INNER_CIRCLE * OUTER_CENTER_CIRCLE_RADIUS)
    return screen


# Used for filling in the speed and instantaneous power consumption meters in the center circle
def fill_circle_segment_in_between(screen, midpoint, inner_radius, outer_radius, degrees, steps, color, start_angle=-1,
                                   end_angle=-1):
    if start_angle == -1 and end_angle == -1:
        half_degrees = degrees / 2.0
        start_angle = math.floor(90 - half_degrees)
        end_angle = math.ceil(90 + half_degrees)
    else:
        pass
    mid_x = midpoint[0]
    mid_y = midpoint[1]
    # -180 to convert graphics angle system to standard math...
    start_angle = start_angle - GRAPHICS_TO_MATH_DEGREES_SUBTRACTANT
    end_angle = end_angle - GRAPHICS_TO_MATH_DEGREES_SUBTRACTANT
    for angle_degrees in np.linspace(start_angle, end_angle, steps, endpoint=False):
        angle_radians = angle_degrees * DEGREES_TO_RADIANS_CONSTANT
        start_xy = (int((inner_radius + CIRCLE_OVERLAP_WIDTH) * math.cos(angle_radians) + mid_x),
                    int((inner_radius + CIRCLE_OVERLAP_WIDTH) * math.sin(angle_radians)) + mid_y)
        end_xy = (int((outer_radius + CIRCLE_OVERLAP_WIDTH) * math.cos(angle_radians)) + mid_x,
                  int((outer_radius + CIRCLE_OVERLAP_WIDTH) * math.sin(angle_radians)) + mid_y)
        pygame.draw.line(screen, color, start_xy, end_xy, SHADING_LINE_WIDTH_FILL_CIRCLE_SEGMENT_IN_BETWEEN)


# Draw the central circle with the speed and instantaneous charge filled
def draw_central_circle():
    # Get current display information, to allow for adaptive GUI.
    # *100 for decimal to percentage conversion
    # +1 for overlap, looks bad otherwise
    conditional_print("Entering draw_central_circle()")
    conditional_print("Display Width: " + str(DISPLAY_WIDTH))
    conditional_print("Display Height: " + str(DISPLAY_HEIGHT))

    # Find the midpoint of the display in (width, height) format
    conditional_print("display midpoint = " + str(DISPLAY_MIDPOINT_TUPLE))
    # Main Gauge (center-of-screen)
    draw_tron_center_circle(INNER_OUTER_CENTER_CIRCLE_RADIUS,
                            OUTER_CENTER_CIRCLE_RADIUS)  # INNER_OUTER_CENTER_CIRCLE_RADIUS = inner radius of the outermost circle
    draw_tron_center_circle(INNER_INNER_CENTER_CIRCLE_RADIUS, OUTER_INNER_CENTER_CIRCLE_RADIUS)
    draw_bottom_center_segment()
    draw_power_consumption()
    draw_speed()

    # Debugging Statement
    conditional_print("Radius of Center Circle: " + str(OUTER_CENTER_CIRCLE_RADIUS))
    pygame.display.update()
    return


def update_speed(new_speed):
    global SPEED, PERCENTAGE_SPEED
    SPEED = new_speed
    PERCENTAGE_SPEED = SPEED / MAX_SPEED * 100;


def update_instantaneous_charge(new_ic):
    global INSTANTANEOUS_CHARGE, PERCENTAGE_INSTANTANEOUS_CHARGE
    INSTANTANEOUS_CHARGE = new_ic
    PERCENTAGE_INSTANTANEOUS_CHARGE = (INSTANTANEOUS_CHARGE / MAX_INSTANTANEOUS_CHARGE) * 100 + 1


def draw_bottom_center_segment():
    """Draws the central-lower segment of the main circle"""
    start_x_shading = int((
                                  DISPLAY_WIDTH - DISPLAY_HEIGHT + 2 * OUTER_CENTER_CIRCLE_WIDTH) / 2)
    # (display_width - center_circle_radius) / 2 + center_circle_width/2
    start_y_shading = OUTER_CENTER_CIRCLE_WIDTH
    radius = OUTER_CENTER_CIRCLE_RADIUS - OUTER_CENTER_CIRCLE_WIDTH
    width = int(
        OUTER_CENTER_CIRCLE_RADIUS - SPACE_OUTER_INNER_CIRCLE * OUTER_CENTER_CIRCLE_RADIUS - OUTER_CENTER_CIRCLE_WIDTH)
    end_angle = math.radians(BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES - 90.0 + BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES / 2)
    conditional_print(BOTTOM_CENTER_SEGMENT_START_ANGLE_RADIANS)
    conditional_print(end_angle)
    center_circle_segment_shade(SCREEN, (start_x_shading, start_y_shading, radius * 2, radius * 2), DARK_DARK_RED,
                                width,
                                BOTTOM_CENTER_SEGMENT_START_ANGLE_RADIANS, end_angle)
    '''DRAW SEGMENTS'''  # Not Applicable


def draw_power_consumption():
    '''SHADING'''
    start_x_shading = int((DISPLAY_WIDTH - DISPLAY_HEIGHT + 2 * OUTER_CENTER_CIRCLE_WIDTH) / 2)
    # (display_width - center_circle_radius) / 2 + center_circle_width/2
    start_y_shading = OUTER_CENTER_CIRCLE_WIDTH
    radius = OUTER_CENTER_CIRCLE_RADIUS - OUTER_CENTER_CIRCLE_WIDTH
    width = int(
        OUTER_CENTER_CIRCLE_RADIUS - SPACE_OUTER_INNER_CIRCLE * OUTER_CENTER_CIRCLE_RADIUS - OUTER_CENTER_CIRCLE_WIDTH)
    start_angle = math.radians(-90 + BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES / 2)
    charge_range = 180 - BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES / 2.0
    end_angle = math.radians(
        charge_range * PERCENTAGE_INSTANTANEOUS_CHARGE / 100.0 - 90.0 + BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES / 2)
    conditional_print(start_angle)
    conditional_print(end_angle)
    center_circle_segment_shade(SCREEN, (start_x_shading, start_y_shading, radius * 2, radius * 2), BLUE, width,
                                start_angle, end_angle)
    '''DRAW SEGMENTS'''
    # Plan: Draw segments as line segments that extend from inner to outer circle...


def draw_speed():
    start_x_shading = int((DISPLAY_WIDTH - DISPLAY_HEIGHT + 2 * OUTER_CENTER_CIRCLE_WIDTH) / 2)
    start_y_shading = OUTER_CENTER_CIRCLE_WIDTH
    radius = OUTER_CENTER_CIRCLE_RADIUS - OUTER_CENTER_CIRCLE_WIDTH
    width = int(
        OUTER_CENTER_CIRCLE_RADIUS - SPACE_OUTER_INNER_CIRCLE * OUTER_CENTER_CIRCLE_RADIUS - OUTER_CENTER_CIRCLE_WIDTH)
    speed_range = 180 - BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES / 2
    start_angle = math.radians(270 - BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES / 2 - PERCENTAGE_SPEED / 100.0 * speed_range)
    center_circle_segment_shade(SCREEN, (start_x_shading, start_y_shading, radius * 2, radius * 2), GREEN, width,
                                start_angle, SPEED_END_ANGLE)
    conditional_print("Entered draw_speed()")
    conditional_print("\t + Bottom Center Width: " + str(BOTTOM_CENTER_SEGMENT_WIDTH_DEGREES))
    conditional_print("\t + Start Angle: " + str(start_angle))
    conditional_print("\t + End Angle:   " + str(SPEED_END_ANGLE))


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


def draw_tron_center_circle(radius_start, radius_end):
    red_gradiant = 0.75
    bg_gradiant = 0.15
    radius_end = radius_end + 1
    circle_width = abs(radius_start - radius_end)
    half_circle_width = math.ceil(circle_width / 2)
    curr_color = TRON_BLUE
    counter = 0
    for i in range(radius_start, radius_end, 1):
        pygame.draw.circle(SCREEN, curr_color, DISPLAY_MIDPOINT_TUPLE, i, 1)
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
    draw_central_circle()
    return


def timing_main(screen, times):
    for i in range(int(times)):
        main()
    return


def main_switcher():
    screen = initialize_GUI()
    if TIMING_ENABLED:
        init = time.process_time_ns()
        timing_main(screen, TIMES)
        ns = time.process_time_ns() - init
        ns = ns / 1000000000.0
        ns = ns / float(TIMES)
        print(str(1.0 / ns) + " fps averaged over " + str(TIMES) + " trials.")
    else:
        main()
    # Debugging statement -- to allow viewer to view initial screen before quitting
    if WAIT_AT_END:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    return  # exit(0)
    else:
        pygame.quit()
        return  # exit(0)


main_switcher()
