import sys
import pygame
from pygame.locals import *
import os
import random
import tkinter
from tkinter import filedialog

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 设置屏幕大小
screen_width = 600
screen_height = 400

# 设置界面
screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

# 图标和背景
ico_img = pygame.image.load("resources/image/ico.jpg").convert_alpha()
ori_bg_img = pygame.image.load("resources/image/back_ground.jpg")  # .convert_alpha()
bg_img = pygame.transform.scale(ori_bg_img, (screen_width, screen_height))

# 设置标题及图标
pygame.display.set_caption("音乐播放器")
pygame.display.set_icon(ico_img)


color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_white = (255, 255, 255)

# 按钮种类标识
choose = 0
play_mode_1 = 1
play_mode_2 = 2
play_mode_3 = 3
last_song = 4
play = 5
pause = 6
next_song = 7
info = 8


music_mod = play_mode_1
play_index = 0
music_load = False
music_pause = False

class Button:
    def __init__(self, content, location, button_type):

        self.content = content
        self.font_size = int(screen_width * 0.02 + screen_height * 0.02)
        self.type = button_type
        self.font_color = color_green

        if self.type == play_mode_1:
            self.line_color = color_red
        else:
            self.line_color = color_white

        self.font = pygame.font.SysFont('SimHei', self.font_size)
        self.text = self.font.render(self.content, True, self.font_color)

        self.rect = self.text.get_rect()
        if self.type in [choose, play_mode_1, play_mode_2, play_mode_3, pause, next_song]:
            self.rect.topleft = location
        if self.type in [play, last_song]:
            self.rect.topright = location
        if self.type == info:
            self.rect.center = location

        self.line_gap = int(0.1 * self.rect.height)
        self.line_width = int(0.1 * self.rect.height)

    def draw(self):

        screen.blit(self.text, self.rect)
        pygame.draw.line(screen, self.line_color, (self.rect.left - self.line_gap, self.rect.top - self.line_gap), (self.rect.right + self.line_gap, self.rect.top - self.line_gap), self.line_width)
        pygame.draw.line(screen, self.line_color, (self.rect.right + self.line_gap, self.rect.top - self.line_gap), (self.rect.right + self.line_gap, self.rect.bottom + self.line_gap), self.line_width)
        pygame.draw.line(screen, self.line_color, (self.rect.right + self.line_gap, self.rect.bottom + self.line_gap),(self.rect.left - self.line_gap, self.rect.bottom + self.line_gap), self.line_width)
        pygame.draw.line(screen, self.line_color, (self.rect.left - self.line_gap, self.rect.bottom + self.line_gap), (self.rect.left - self.line_gap, self.rect.top - self.line_gap), self.line_width)

    def get_range(self):
        x_range = [self.rect.left - self.line_gap, self.rect.right + self.line_gap]
        y_range = [self.rect.top - self.line_gap, self.rect.bottom + self.line_gap]
        return x_range, y_range

    def update(self, location):
        self.font_size = int(screen_width * 0.02 + screen_height * 0.02)

        self.font = pygame.font.SysFont('SimHei', self.font_size)
        self.text = self.font.render(self.content, True, self.font_color)
        self.rect = self.text.get_rect()

        if self.type in [choose, play_mode_1, play_mode_2, play_mode_3, pause, next_song]:
            self.rect.topleft = location
        if self.type in [play, last_song]:
            self.rect.topright = location
        if self.type == info:
            self.rect.center = location

        self.line_gap = int(0.1 * self.rect.height)
        self.line_width = int(0.1 * self.rect.height)

    def change_color(self):
            if self.line_color == color_white:
                self.line_color = color_red
            else:
                self.line_color = color_white
    def get_red(self):
            self.line_color = color_red
    def get_white(self):
            self.line_color = color_white



# 收集某个目录及子目录下的MP3格式的文件
def collect_songs(fidir):
    musics = []
    for root, dirs, files in os.walk(fidir):
        for file in files:
            if file.endswith('mp3'):
                file = os.path.join(root, file)
                musics.append(file)
    return musics


def get_music(play_index):
    pygame.mixer.music.stop()
    pygame.mixer.music.load(musics[play_index])
    pygame.mixer.music.play()


def play_music(play_index):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.unpause()
    else:
        get_music(play_index)

def pause_music():
    pygame.mixer.music.pause()


def color_flash():
    if music_info.line_color == color_white:
        music_info.line_color = color_green
        return
    if music_info.line_color == color_green:
        music_info.line_color = color_red
        return
    if music_info.line_color == color_red:
        music_info.line_color = color_white
        return



# 建立按钮对象
choose_button = Button("加载音乐", [int(screen_width * 0.1), int(screen_height * 0.1)], choose)
play_mode_1_button = Button("顺序播放", [int(choose_button.rect.right + 0.5 * choose_button.rect.width), choose_button.rect.top], play_mode_1)
play_mode_2_button = Button("随机播放", [int(play_mode_1_button.rect.right + 0.5 * play_mode_1_button.rect.width), play_mode_1_button.rect.top], play_mode_2)
play_mode_3_button = Button("单曲循环", [int(play_mode_2_button.rect.right + 0.5 * play_mode_2_button.rect.width), play_mode_2_button.rect.top], play_mode_3)
play_button = Button("播放", screen.get_rect().center, play)
play_button.rect.midright = [int(screen.get_rect().centerx - 0.5 * play_button.rect.width), screen.get_rect().centery]
pause_button = Button("暂停", screen.get_rect().center, pause)
pause_button.rect.midleft = [int(screen.get_rect().centerx + 0.5 * pause_button.rect.width), screen.get_rect().centery]
last_song_button = Button("上一首", [play_button.rect.right, play_button.rect.bottom + int(1.5 * play_button.rect.height)], last_song)
next_song_button = Button("下一首", [pause_button.rect.left, pause_button.rect.bottom + int(1.5 * pause_button.rect.height)], next_song)
music_info = Button("音乐播放器", [screen.get_rect().centerx, screen.get_rect().centery - 50], info)
music_info.font_color = color_blue

i = 0

# 主循环
while True:
    screen.blit(bg_img, (0, 0))

    choose_button.draw()
    play_mode_1_button.draw()
    play_mode_2_button.draw()
    play_mode_3_button.draw()
    play_button.draw()
    pause_button.draw()
    last_song_button.draw()
    next_song_button.draw()
    music_info.draw()
    if music_load:
        i += 1
        if i == 25:
            i = 0
            if pygame.mixer.music.get_busy() and music_pause == False: 
                color_flash()
            else:
                music_info.line_color = color_white
        music_info.content = musics[play_index].split("\\")[-1]
        music_info.update([screen.get_rect().centerx, screen.get_rect().centery - 50])

    pygame.display.update()

    for event in pygame.event.get():
        # 退出
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # 鼠标单击
        if event.type == MOUSEBUTTONDOWN:
            choose_button_range_x, choose_button_range_y = choose_button.get_range()
            play_mode_1_button_range_x, play_mode_1_button_range_y = play_mode_1_button.get_range()
            play_mode_2_button_range_x, play_mode_2_button_range_y = play_mode_2_button.get_range()
            play_mode_3_button_range_x, play_mode_3_button_range_y = play_mode_3_button.get_range()
            play_button_range_x, play_button_range_y = play_button.get_range()
            pause_button_range_x, pause_button_range_y = pause_button.get_range()
            last_song_button_range_x, last_song_button_range_y = last_song_button.get_range()
            next_song_button_range_x, next_song_button_range_y = next_song_button.get_range()

            # 点击选择按钮
            if choose_button_range_x[0] <= event.pos[0] <= choose_button_range_x[1] and choose_button_range_y[0] <= event.pos[1] <= choose_button_range_y[1]:
                root = tkinter.Tk()
                root.withdraw()
                file_path = filedialog.askdirectory() # 选择目录，返回目录名
                if "fire_path" in vars():
                    musics = collect_songs(file_path)
                    music_load = True

            if play_mode_1_button_range_x[0] <= event.pos[0] <= play_mode_1_button_range_x[1] and play_mode_1_button_range_y[0] <= event.pos[1] <= play_mode_1_button_range_y[1]:
                if music_load:
                    play_mode_1_button.get_red()
                    play_mode_2_button.get_white()
                    play_mode_3_button.get_white()

            if play_mode_2_button_range_x[0] <= event.pos[0] <= play_mode_2_button_range_x[1] and play_mode_2_button_range_y[0] <= event.pos[1] <= play_mode_2_button_range_y[1]:
                if music_load:
                    play_mode_2_button.get_red()
                    play_mode_1_button.get_white()
                    play_mode_3_button.get_white()

            if play_mode_3_button_range_x[0] <= event.pos[0] <= play_mode_3_button_range_x[1] and play_mode_3_button_range_y[0] <= event.pos[1] <= play_mode_3_button_range_y[1]:
                if music_load:
                    play_mode_3_button.get_red()
                    play_mode_1_button.get_white()
                    play_mode_2_button.get_white()

            if play_button_range_x[0] <= event.pos[0] <= play_button_range_x[1] and play_button_range_y[0] <= event.pos[1] <= play_button_range_y[1]:
                if music_load:
                    play_music(play_index)
                    play_button.get_red()
                    pause_button.get_white()
                    music_pause = False

            if pause_button_range_x[0] <= event.pos[0] <= pause_button_range_x[1] and pause_button_range_y[0] <= event.pos[1] <= pause_button_range_y[1]:
                if music_load:
                    pause_music()
                    pause_button.get_red()
                    play_button.get_white()
                    music_pause = True

            if last_song_button_range_x[0] <= event.pos[0] <= last_song_button_range_x[1] and last_song_button_range_y[0] <= event.pos[1] <= last_song_button_range_y[1]:
                if music_load:
                    play_index -= 1
                    if play_index < 0:
                        play_index = len(musics) - 1
                    get_music(play_index)
                    last_song_button.change_color()
                    play_button.get_red()
                    pause_button.get_white()
                    music_pause = False


            if next_song_button_range_x[0] <= event.pos[0] <= next_song_button_range_x[1] and next_song_button_range_y[0] <= event.pos[1] <= next_song_button_range_y[1]:
                if music_load:
                    play_index += 1
                    if play_index >= len(musics):
                        play_index = 0
                    get_music(play_index)
                    next_song_button.change_color() 
                    play_button.get_red()
                    pause_button.get_white()
                    music_pause = False


        if event.type == MOUSEBUTTONUP:
            last_song_button_range_x, last_song_button_range_y = last_song_button.get_range()
            next_song_button_range_x, next_song_button_range_y = next_song_button.get_range()

            if last_song_button_range_x[0] <= event.pos[0] <= last_song_button_range_x[1] and last_song_button_range_y[0] <= event.pos[1] <= last_song_button_range_y[1]:
                if music_load:
                    last_song_button.change_color() 

            if next_song_button_range_x[0] <= event.pos[0] <= next_song_button_range_x[1] and next_song_button_range_y[0] <= event.pos[1] <= next_song_button_range_y[1]:
                if music_load:
                    next_song_button.change_color() 

        # 改变窗口大小
        if event.type == VIDEORESIZE:
            screen_width = event.size[0]
            screen_height = event.size[1]
            screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
            bg_img = pygame.transform.scale(ori_bg_img, (screen_width, screen_height))
            choose_button.update([int(screen_width * 0.1), int(screen_height * 0.1)])
            play_mode_1_button.update([int(choose_button.rect.right + 0.5 * choose_button.rect.width), choose_button.rect.top])
            play_mode_2_button.update([int(play_mode_1_button.rect.right + 0.5 * play_mode_1_button.rect.width), play_mode_1_button.rect.top])
            play_mode_3_button.update([int(play_mode_2_button.rect.right + 0.5 * play_mode_2_button.rect.width), play_mode_2_button.rect.top])
            play_button.update([int(screen.get_rect().centerx - 0.5 * play_button.rect.width), screen.get_rect().centery])
            pause_button.update([int(screen.get_rect().centerx + 0.5 * pause_button.rect.width), screen.get_rect().centery])
            last_song_button.update([play_button.rect.right, play_button.rect.bottom + int(1.5 * play_button.rect.height)])
            next_song_button.update([pause_button.rect.left, pause_button.rect.bottom + int(1.5 * pause_button.rect.height)])
            music_info.update([screen.get_rect().centerx, screen.get_rect().centery - 50])