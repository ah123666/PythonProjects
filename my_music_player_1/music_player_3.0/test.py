import sys
import pygame
from pygame.locals import *
import os
import random
import tkinter
from tkinter import filedialog
import time

# 颜色定义
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_white = (255, 255, 255)


# 初始化pygame
pygame.init()
# pygame.mixer.init()

# 设置界面
screen = pygame.display.set_mode([600, 480])
# file_path1 = "resources\\music\\森林狂想曲（陶笛） - 陶笛-犹豫的泥巴.flac"
# file_path2 = "resources\\music\\沙漠绿洲 - 打飞机游戏-界面.mp3"
# file_path3 = "resources\\music\\下雨天.wav"
# sound = pygame.mixer.Sound(file_path1)
# print("总时长：", sound.get_length())
# sound.play()
# start_time = time.time()

# pygame.mixer.music.load("resources/music/森林狂想曲（陶笛） - 陶笛-犹豫的泥巴.flac")
# pygame.mixer.music.play()
while True:
    # for i in range(0, 200):
    #     for j in range(0, 200):
    #         screen.set_at([i, j], color_red)
    screen.fill(0)
    pygame.draw.line(screen, color_red, [0, 0], [200, 200], 5)

    pygame.display.update()
    # if not pygame.mixer.get_busy():
    #     print("当前时长：", time.time() - start_time)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
