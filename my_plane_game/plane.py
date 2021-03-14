import pygame
from pygame.locals import *
from sys import exit
import random
import codecs
import math

# 设置屏幕大小
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 设置游戏界面大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置游戏标题图标
ic_launcher = pygame.image.load("resources/image/ic_launcher.jpeg").convert_alpha()

# 背景图
back_ground = pygame.image.load("resources/image/background.jpg").convert_alpha()

# 结束背景图
game_over = pygame.image.load("resources/image/gameover.png").convert_alpha()

blood_img = pygame.image.load("resources/image/blood.png").convert_alpha()

# 子弹图片
player_bullet_img = pygame.image.load("resources/image/bullet.png").convert_alpha()
enemy_bullet_img = pygame.image.load("resources/image/enemy_bullet.png").convert_alpha()

# 飞机图片
player_img1 = pygame.image.load("resources/image/player1.png").convert_alpha()
player_img2 = pygame.image.load("resources/image/player2.png").convert_alpha()
player_img3 = pygame.image.load("resources/image/player_off1.png").convert_alpha()
player_img4 = pygame.image.load("resources/image/player_off2.png").convert_alpha()
player_img5 = pygame.image.load("resources/image/player_off3.png").convert_alpha()

# 敌机图片
enemy_img1 = pygame.image.load("resources/image/enemy1.png").convert_alpha()
enemy_img2 = pygame.image.load("resources/image/enemy2.png").convert_alpha()
enemy_img3 = pygame.image.load("resources/image/enemy3.png").convert_alpha()
enemy_img4 = pygame.image.load("resources/image/enemy4.png").convert_alpha()

pause_image = pygame.image.load("resources\\image\\pause.png").convert_alpha()
unpause_image = pygame.image.load("resources\\image\\play.png").convert_alpha()

pause_rect = pause_image.get_rect()
pause_rect.topright = [SCREEN_WIDTH-10, 10]

# 背景音乐
bg_music = "resources\\music\\森林狂想曲（陶笛）.flac"
pygame.mixer.music.load(bg_music)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# 射击及爆炸音效
shoot_sound = "resources\\music\\shoot.wav"
boom_sound = "resources\\music\\enemy_boom.wav"
shoot_sound = pygame.mixer.Sound(shoot_sound)
shoot_sound.set_volume(0.1)
boom_sound = pygame.mixer.Sound(boom_sound)
boom_sound.set_volume(0.3)

# 设置游戏标题及图标
pygame.display.set_caption("彩图飞机大战")
pygame.display.set_icon(ic_launcher)

# 玩家飞机不同状态的图片列表，多张图片展示为动画效果
player_imgs = []
# 玩家飞机飞行图片
player_imgs.append(player_img1)
player_imgs.append(player_img2)
# 玩家飞机爆炸图片
player_imgs.append(player_img3)
player_imgs.append(player_img4)
player_imgs.append(player_img4)
player_imgs.append(player_img5)
player_imgs.append(player_img5)
player_imgs.append(player_img5)
player_pos = [0.5 * SCREEN_WIDTH, SCREEN_HEIGHT]  # 玩家飞机初始位置

# 敌机不同状态的图片列表，多张图片展示为动画效果
# 正常飞行图片
enemy_img = enemy_img1
enemy_rect = enemy_img.get_rect()
# 爆炸图片
enemy_down_imgs = [enemy_img1, enemy_img2, enemy_img3, enemy_img4]

# 子弹种类
player_main_bullet = 0
player_side_bullet = 1
enemy_main_bullet = 2
enemy_random_bullet = 3
blood_bottle = 4

score_path = "resources/score.txt"

class Item(pygame.sprite.Sprite):
    """
    道具类
    """
    def __init__(self, item_img, init_pos, speed, item_type):
        super(Item, self).__init__()
        self.image = item_img
        self.rect = self.image.get_rect()
        [self.rect.centerx, self.rect.centery] = init_pos
        self.speed = speed
        self.type = item_type
        if self.type == blood_bottle:
            self.recover = 50

    def move(self):
        if self.type == blood_bottle:
            self.rect.top += self.speed


class Bullet(pygame.sprite.Sprite):
    """
    子弹类
    """

    def __init__(self, bullet_img, init_pos, speed, bullet_type):
        super(Bullet, self).__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.type = bullet_type
        self.speed = speed

        if self.type == player_main_bullet:
            self.rect.midbottom = init_pos
            self.hurt = 20

        if self.type == player_side_bullet:
            self.rect.midbottom = init_pos
            self.hurt = 10

        if self.type == enemy_main_bullet:
            self.rect.midtop = init_pos
            self.hurt = 10

        if self.type == enemy_random_bullet:
            self.rect.midtop = init_pos
            self.angle = random.randint(-90, 90)
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.hurt = 5

    def move(self):
        # 子弹移动
        if self.type == player_main_bullet:
            self.rect.bottom -= self.speed
        if self.type == player_side_bullet:
            self.rect.bottom -= self.speed
        if self.type == enemy_main_bullet:
            self.rect.top += self.speed
        if self.type == enemy_random_bullet:
            self.rect.centerx += self.speed * math.sin(math.radians(self.angle))
            self.rect.centery += self.speed * math.cos(math.radians(self.angle))


class Player(pygame.sprite.Sprite):
    """
    玩家类
    """

    def __init__(self, player_imgs, init_pos, speed, shoot_frequency):
        super(Player, self).__init__()
        # 存储玩家飞机图片的列表
        self.image = player_imgs
        self.rect = self.image[0].get_rect()
        self.rect.midbottom = init_pos
        self.speed = speed
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False
        self.down_index = 32
        self.shoot_index = 0
        self.shoot_frequency = shoot_frequency
        self.score = 0
        self.max_blood = 200
        self.blood = 200

    # 发射子弹
    def shoot(self, bullet_img, init_pos, bullet_speed, bullet_type):
        bullet = Bullet(bullet_img, init_pos, bullet_speed, bullet_type)
        self.bullets.add(bullet)

    def draw_blood(self):
        for i in range(int(screen.get_rect().midtop[0] - 50), int(screen.get_rect().midtop[0] - 50 + 100 * (self.blood / self.max_blood))):
            for j in range(10, 20):
                screen.set_at([i, j], (255, 0, 0))
        for i in range(int(screen.get_rect().midtop[0] - 50 + 100 * (self.blood / self.max_blood)), int(screen.get_rect().midtop[0] + 50)):
            for j in range(10, 20):
                screen.set_at([i, j], (255, 255, 255))


    # 向上移动，需判断边界
    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed


class Enemy(pygame.sprite.Sprite):
    """
    敌机类
    """

    def __init__(self, enemy_img, enemy_down_imgs, init_pos, speed, shoot_frequency):
        super(Enemy, self).__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.midtop = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = speed
        self.bullets = pygame.sprite.Group()
        self.down_index = 0
        self.shoot_index = 0
        self.shoot_frequency = shoot_frequency
        self.max_blood = 50
        self.blood = 50

    # 发射子弹
    def shoot(self, bullet_img, init_pos, bullet_speed, bullet_type):
        bullet = Bullet(bullet_img, init_pos, bullet_speed, bullet_type)
        self.bullets.add(bullet)

    def move(self):
        self.rect.top += self.speed

    def draw_blood(self):
        for i in range(self.rect.topleft[0], int(self.rect.topleft[0] + self.rect.width * (self.blood / self.max_blood))):
            for j in range(self.rect.topleft[1] - 7, self.rect.topleft[1] - 4):
                screen.set_at([i, j], (0, 0, 255))
        for i in range(int(self.rect.topleft[0] + self.rect.width * (self.blood / self.max_blood)), self.rect.topright[0]):
            for j in range(self.rect.topleft[1] - 7, self.rect.topleft[1] - 4):
                screen.set_at([i, j], (255, 255, 255))


def start_game():
    """
    开始游戏
    """
    # 参数设置
    player_speed = 8
    player_shoot_frequency = 10
    player_bullet_speed = 8

    enemy_generate_index = 0
    enemy_generate_frequency = 50

    enemy_speed = 1
    enemy_shoot_frequency = 80
    enemy_bullet_speed = 3

    blood_bottle_speed = 5

    # 游戏循环帧率设置
    clock = pygame.time.Clock()

    # 判断游戏循环退出参数
    running = True

    # 背景音乐暂停标志
    music_pause = False

    # 初始化玩家飞机
    player = Player(player_imgs, player_pos, player_speed, player_shoot_frequency)  # 建立玩家对象

    # 存储敌机
    enemies = pygame.sprite.Group()

    # 存储被击毁的飞机，用来渲染击毁动画
    enemies_down = pygame.sprite.Group()

    # 用来存储道具
    items = pygame.sprite.Group()

    # 游戏暂停标志
    game_pause = False

    """
    游戏主循环
    """
    while running:
        if game_pause:
            font = pygame.font.SysFont('SimHei', 30)
            text = font.render("Press P Continue!", True, (0, 255, 0))
            text_rect = text.get_rect()
            text_rect.centerx = screen.get_rect().centerx
            text_rect.centery = screen.get_rect().centery + 24
            screen.blit(text, text_rect)

            pygame.display.update()
            # pygame.mixer.pause()
            pygame.mixer.music.pause()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        game_pause = not game_pause
                        # pygame.mixer.unpause()
                        pygame.mixer.music.unpause()
            continue

        # 控制游戏最大帧率为60
        clock.tick(60)

        # 绘制背景
        screen.fill(0)
        screen.blit(back_ground, (0, 0))

        # 背景音乐播放控制
        if not music_pause:
            screen.blit(unpause_image, pause_rect)
            # pygame.mixer.unpause()
            pygame.mixer.music.unpause()
        else:
            screen.blit(pause_image, pause_rect)
            # pygame.mixer.pause()
            pygame.mixer.music.pause()

        # 判断玩家飞机是否被击中
        if not player.is_hit:

            """
            玩家处理
            """
            # 更换图片索引，使飞机有动画效果
            # 结果为0或1，显示前两张飞机图片，显示飞机飞行动画
            player.img_index = player.shoot_index // ((player.shoot_frequency + 1) // 2)
            screen.blit(player.image[player.img_index], player.rect)

            player.draw_blood()

            # 根据频率发射子弹
            player.shoot_index += 1
            if player.shoot_index == player.shoot_frequency:
                player.shoot(player_bullet_img, player.rect.midtop, player_bullet_speed, player_main_bullet)
                player.shoot(enemy_bullet_img, (player.rect.midtop[0]-40, player.rect.midtop[1]+40), player_bullet_speed+5, player_side_bullet)
                player.shoot(enemy_bullet_img, (player.rect.midtop[0]+40, player.rect.midtop[1]+40), player_bullet_speed+5, player_side_bullet)
                player.shoot(enemy_bullet_img, (player.rect.midtop[0]-25, player.rect.midtop[1]+25), player_bullet_speed+3, player_side_bullet)
                player.shoot(enemy_bullet_img, (player.rect.midtop[0]+25, player.rect.midtop[1]+25), player_bullet_speed+3, player_side_bullet)
                shoot_sound.play()
                player.shoot_index = 0

            for bullet in player.bullets:
                # 以固定速度移动子弹
                bullet.move()
                # 移动出屏幕后删除子弹
                if bullet.rect.bottom < 0:
                    player.bullets.remove(bullet)
            # 显示子弹
            player.bullets.draw(screen)

            """
              敌机处理
            """
            # 根据频率生成敌机
            enemy_generate_index += 1
            if enemy_generate_index == enemy_generate_frequency:
                enemy_pos = [random.randint(0.5 * player.rect.width, SCREEN_WIDTH - 0.5 * player.rect.width), 0]
                enemy = Enemy(enemy_img, enemy_down_imgs, enemy_pos,enemy_speed, enemy_shoot_frequency)
                enemy.shoot(enemy_bullet_img, enemy.rect.midbottom, enemy_bullet_speed, enemy_main_bullet)
                enemy.shoot(enemy_bullet_img, enemy.rect.midbottom, enemy_bullet_speed, enemy_random_bullet)
                enemies.add(enemy)
                enemy_generate_index = 0

            for enemy in enemies:
                # 移动敌机
                enemy.move()
                enemy.draw_blood()

                # 敌机根据频率发射子弹
                enemy.shoot_index += 1
                if enemy.shoot_index == enemy.shoot_frequency:
                    enemy.shoot(enemy_bullet_img, enemy.rect.midbottom, enemy_bullet_speed, enemy_main_bullet)
                    enemy.shoot(enemy_bullet_img, enemy.rect.midbottom, enemy_bullet_speed, enemy_random_bullet)
                    enemy.shoot_index = 0

                for bullet in enemy.bullets:
                    # 移动敌机子弹
                    bullet.move()

                    # 敌机子弹与玩家飞机碰撞检测
                    if pygame.sprite.collide_rect(bullet, player):
                        boom_sound.play()
                        enemy.bullets.remove(bullet)
                        player.blood -= bullet.hurt
                        if player.blood <= 0:
                            player.is_hit = True
                            break

                    # 移动出屏幕后删除子弹
                    if not 0 < bullet.rect.centerx < SCREEN_WIDTH and 0 < bullet.rect.centery < SCREEN_HEIGHT:
                        enemy.bullets.remove(bullet)
     
                # 敌机子弹与玩家子弹碰撞检测，子弹碰撞互相消失
                pygame.sprite.groupcollide(enemy.bullets, player.bullets, True, True)

                # 显示敌机子弹
                enemy.bullets.draw(screen)

                # 敌机与玩家飞机碰撞检测
                if pygame.sprite.collide_rect(enemy, player):
                    enemies_down.add(enemy)  # enemies_down是炸毁的敌机
                    boom_sound.play()
                    enemies.remove(enemy)
                    player.blood -= 0.5 * player.max_blood
                    if player.blood <= 0:
                            player.is_hit = True
                            break
                # 移出屏幕后删除敌机
                if enemy.rect.top > SCREEN_HEIGHT:
                    enemies.remove(enemy)

            # 敌机与玩家子弹碰撞
            result = pygame.sprite.groupcollide(enemies, player.bullets, False, True)  
            # 统计碰撞敌机，遍历字典key值
            for enemy in result:
                enemy.blood -= result[enemy][0].hurt
                if enemy.blood <= 0:
                    # 添加销毁的敌机到列表
                    enemies_down.add(enemy)  # 将击中的敌机添加到炸毁敌机中
                    boom_sound.play()
                    enemies.remove(enemy)
                    tmp = random.random()
                    if tmp < 0.5:
                        item = Item(blood_img, [enemy.rect.centerx, enemy.rect.centery], blood_bottle_speed, blood_bottle)
                        items.add(item)

            result = pygame.sprite.spritecollide(player, items, True)
            for item in result:
                player.blood += item.recover
                if player.blood >= player.max_blood:
                    player.blood = player.max_blood

            for item in items:
                item.move()
                if item.rect.top > SCREEN_HEIGHT:
                    items.remove(item)

            items.draw(screen)


            # 敌机被子弹击中的效果展示
            for enemy_down in enemies_down:
                # 结果为0到3，显示4张敌机照片，显示敌机爆炸动画
                screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)

                enemy_down.down_index += 1
                if enemy_down.down_index > 7:
                    enemies_down.remove(enemy_down)
                    player.score += 100

            # 显示敌机
            enemies.draw(screen)

        else:
            # 玩机飞机被击中后的处理效果
            player.img_index = player.down_index // 16  # 结果为2到7，显示第3张到第8张飞机图片，显示飞机爆炸动画
            screen.blit(player.image[player.img_index], player.rect)
            player.down_index += 1

            if player.down_index > 112:
                # 击中效果处理完后游戏结束
                running = False

        # 绘制当前得分
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(str(player.score), True, (225, 0, 0))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10, 10]
        screen.blit(score_text, text_rect)

        # 更新屏幕
        pygame.display.update()

        # 处理游戏退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if pause_rect.left <= event.pos[0] <= pause_rect.right \
                        and pause_rect.top <= event.pos[1] <= pause_rect.bottom:
                    music_pause = not music_pause
            if event.type == KEYDOWN:
                if event.key == K_p:
                    game_pause = not game_pause

        # 获取键盘事件
        key_pressed = pygame.key.get_pressed()
        # 处理键盘事件
        if not player.is_hit:
            if key_pressed[K_w] or key_pressed[K_UP]:
                player.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                player.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                player.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                player.moveRight()

    draw_game_over(player.score)
    update_score_rank(player.score)


def draw_game_over(score):

    # 绘制游戏结束背景
    screen.blit(game_over, (0, 0))
    # 游戏 Game Over 后显示最终得分
    font = pygame.font.Font(None, 48)
    text = font.render('Score: ' + str(score), True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    screen.blit(text, text_rect)

    # 使用系统字体
    xtfont = pygame.font.SysFont('SimHei', 30)
    # 重新开始按钮
    textstart = xtfont.render('重新开始 ', True, (255, 255, 255))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 120
    screen.blit(textstart, text_rect)
    # 排行榜按钮
    textstart = xtfont.render('排行榜 ', True, (255, 255, 255))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 180
    screen.blit(textstart, text_rect)


def update_score_rank(score):

    # 判断得分更新排行榜
    # 临时的变量在到排行榜的时候使用
    j = 0
    # 获取文件中内容转换成列表使用mr分割开内容
    arrayscore = read_txt(score_path)[0].split('mr')

    # 循环分数列表在列表里排序
    for i in range(0, len(arrayscore)):
        # 判断当前获得的分数是否大于排行榜上的分数
        if score > int(arrayscore[i]):
            # 大于排行榜上的内容 把分数和当前分数进行替换
            j = arrayscore[i]
            arrayscore[i] = str(score)
            score = 0
        # 替换下来的分数下移动一位
        if int(j) > int(arrayscore[i]):
            k = arrayscore[i]
            arrayscore[i] = str(j)
            j = k

    #  循环分数列表 写入文档
    for i in range(0, len(arrayscore)):
        # 判断列表中第一个分数
        if i == 0:
            # 覆盖写入内容追加mr方便分割内容
            write_txt(arrayscore[i] + 'mr', 'w', score_path)
        else:
            # 判断是否为最后一个分数
            if i == 9:
                # 最近添加内容最后一个分数不添加mr
                write_txt(arrayscore[i], 'a', score_path)
            else:
                # 不是最后一个分数，添加的时候添加mr
                write_txt(arrayscore[i] + 'mr', 'a', score_path)


# 排行榜
def show_game_rank():
    screen2 = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 绘制背景
    screen2.fill(0)
    screen2.blit(back_ground, (0, 0))
    # 使用系统字体
    xtfont = pygame.font.SysFont('SimHei', 30)

    # 排行榜按钮
    textstart = xtfont.render('排行榜', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = 50
    screen.blit(textstart, text_rect)

    # 重新开始按钮
    textstart = xtfont.render('重新开始', True, (255, 0, 0))
    text_rect = textstart.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 120
    screen2.blit(textstart, text_rect)

    # 获取排行文档内容
    arrayscore = read_txt(score_path)[0].split('mr')
    # 循环排行榜文件显示排行
    for i in range(0, len(arrayscore)):
        # 游戏 Game Over 后显示最终得分
        font = pygame.font.Font(None, 48)
        # 排名重1到10
        k = i + 1
        text = font.render(str(k) + "  " + arrayscore[i], True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen2.get_rect().centerx
        text_rect.centery = 80 + 30 * k
        # 绘制分数内容
        screen2.blit(text, text_rect)


def write_txt(content, strim, path):
    """
    写入txt
    """
    f = codecs.open(path, strim, 'utf8')
    f.write(str(content))
    f.close()


def read_txt(path):
    """
    读取txt：
    """
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
    return lines


def main_game():
    start_game()
    # 判断点击位置以及处理游戏推出
    while True:
        for event in pygame.event.get():
            # 关闭页面游戏退出
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # 鼠标单击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 判断鼠标单击的位置是否为开始按钮位置范围内
                if screen.get_rect().centerx - 70 <= event.pos[0] <= screen.get_rect().centerx + 50 \
                        and screen.get_rect().centery + 100 <= event.pos[1] <= screen.get_rect().centery + 140:
                    # 重新开始游戏
                    main_game()
                # 判断鼠标是否单击排行榜按钮
                if screen.get_rect().centerx - 70 <= event.pos[0] <= screen.get_rect().centerx + 50 \
                        and screen.get_rect().centery + 160 <= event.pos[1] <= screen.get_rect().centery + 200:
                    # 显示排行榜
                    show_game_rank()
        # 更新界面
        pygame.display.update()


if __name__ == '__main__':
    main_game()
