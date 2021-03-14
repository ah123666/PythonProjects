# import pygame

# #初始化pygame
# pygame.init()
# # 设置屏幕大小
# SCREEN_WIDTH = 600
# SCREEN_HEIGHT = 600
# # 设置游戏界面大小
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# screen.fill((255,255,255))
# for i in range(300, 400):
#     for j in range(300, 400):
#         screen.set_at([i, j], (255,0,0))
# pygame.display.update()
# while True:
#     # 处理游戏退出
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             exit()

a = {"1":1, "2":2, "3":3}
for key in a:
    print(key, type(key))
    print(a[key], type(a[key]))
print(type(a))