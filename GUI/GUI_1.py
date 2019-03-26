# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 20:28:12 2019

@author: miked
"""

import pygame
import math
import time


pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

display = pygame.display.Info()
displayWidth, displayHeight = display.current_w, display.current_h
print("display width, height = " + str(displayWidth) + " , " + str(displayHeight))
displayCenter= (math.floor(displayWidth / 2), math.floor(displayHeight / 2))
print("display center = " + str(displayCenter))
pygame.draw.circle(screen, (255,0,255), displayCenter, int(min((displayWidth/2), (displayHeight/2))), 20)
pygame.display.update()
time.sleep(5)
pygame.quit()