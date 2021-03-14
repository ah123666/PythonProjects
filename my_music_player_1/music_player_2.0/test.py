import sys
import pygame
from pygame.locals import *
import os
import random
import tkinter
from tkinter import filedialog

# root = tkinter.Tk()
# root.withdraw()
# for i in range(3):
#     file_path = filedialog.askdirectory(title="选择音乐文件夹")  # 选择目录，返回目录名
#     root.destroy()

# 颜色定义
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_white = (255, 255, 255)


# 初始化pygame
pygame.init()
pygame.mixer.init()

# 设置界面
screen = pygame.display.set_mode((600, 480))

# sound = pygame.mixer.Sound("resources/music/森林狂想曲（陶笛） - 陶笛-犹豫的泥巴.flac")
# sound.play()
pygame.mixer.music.load("resources/music/森林狂想曲（陶笛） - 陶笛-犹豫的泥巴.flac")
pygame.mixer.music.play()
while True:
    screen.fill(color_blue)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
