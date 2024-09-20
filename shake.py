import sys
import matplotlib.pyplot as plt
print(f"Python 执行路径: {sys.executable}")
print(f"Python 搜索路径: {sys.path}")

import pygame
import random

class 贪吃蛇:
    def __init__(self):
        pygame.init()
        self.宽度 = 800
        self.高度 = 600
        self.块大小 = 20
        self.窗口 = pygame.display.set_mode((self.宽度, self.高度))
        pygame.display.set_caption('优化版贪吃蛇游戏')

        self.白色 = (255, 255, 255)
        self.黑色 = (0, 0, 0)
        self.红色 = (255, 0, 0)
        self.绿色 = (0, 255, 0)

        # 尝试加载默认字体
        try:
            self.字体 = pygame.font.Font(pygame.font.get_default_font(), 35)
            print(f"成功加载默认字体: {pygame.font.get_default_font()}")
        except Exception as e:
            print(f"加载默认字体失败: {e}")
            self.字体 = None

        self.重置游戏()
        self.时钟 = pygame.time.Clock()
        print("游戏初始化完成")

    def 重置游戏(self):
        self.蛇 = [(self.宽度//2, self.高度//2)]
        self.方向 = 'RIGHT'
        self.食物 = self.生成食物()
        self.分数 = 0
        print(f"游戏重置 - 蛇头位置: {self.蛇[0]}, 食物位置: {self.食物}")

    def 生成食物(self):
        while True:
            食物 = (random.randrange(0, (self.宽度//self.块大小)) * self.块大小,
                    random.randrange(0, (self.高度//self.块大小)) * self.块大小)
            if 食物 not in self.蛇:
                return 食物

    def 画蛇和食物(self):
        self.窗口.fill(self.黑色)
        for 位置 in self.蛇:
            pygame.draw.rect(self.窗口, self.绿色, pygame.Rect(位置[0], 位置[1], self.块大小, self.块大小))
        pygame.draw.rect(self.窗口, self.红色, pygame.Rect(self.食物[0], self.食物[1], self.块大小, self.块大小))

    def 移动蛇(self):
        新头部 = list(self.蛇[0])
        if self.方向 == 'UP':
            新头部[1] -= self.块大小
        elif self.方向 == 'DOWN':
            新头部[1] += self.块大小
        elif self.方向 == 'LEFT':
            新头部[0] -= self.块大小
        elif self.方向 == 'RIGHT':
            新头部[0] += self.块大小
        self.蛇.insert(0, tuple(新头部))

    def 检查碰撞(self):
        头部 = self.蛇[0]
        return (
            头部[0] < 0 or 头部[0] >= self.宽度 or
            头部[1] < 0 or 头部[1] >= self.高度 or
            头部 in self.蛇[1:]
        )

    def 显示文本(self, 文本, 大小, 颜色, x, y):
        if self.字体 is None:
            print(f"无法显示文本 '{文本}': 字体未加载")
            return
        try:
            文本表面 = self.字体.render(文本, True, 颜色)
            文本矩形 = 文本表面.get_rect(center=(x, y))
            self.窗口.blit(文本表面, 文本矩形)
            print(f"显示文本: '{文本}' 在位置 ({x}, {y})")
        except Exception as e:
            print(f"显示文本 '{文本}' 失败: {e}")
            # 尝试使用 pygame.draw.rect 来显示文本位置
            pygame.draw.rect(self.窗口, 颜色, (x-50, y-25, 100, 50), 2)

    def 开始界面(self):
        self.窗口.fill(self.黑色)
        self.显示文本("贪吃蛇游戏", 64, self.白色, self.宽度//2, self.高度//3)
        self.显示文本("按空格键开始", 32, self.白色, self.宽度//2, self.高度//2)
        pygame.display.flip()
        print("显示开始界面")

        while True:
            for 事件 in pygame.event.get():
                if 事件.type == pygame.QUIT:
                    return False
                if 事件.type == pygame.KEYDOWN:
                    if 事件.key == pygame.K_SPACE:
                        print("用户按下空格键，开始游戏")
                        return True
                    elif 事件.key == pygame.K_q:
                        print("用户按下Q键，退出游戏")
                        return False

    def 结束界面(self):
        self.窗口.fill(self.黑色)
        self.显示文本(f"游戏结束! 得分: {self.分数}", 48, self.白色, self.宽度//2, self.高度//3)
        self.显示文本("按R键重新开始, 按Q键退出", 32, self.白色, self.宽度//2, self.高度//2)
        pygame.display.flip()
        print("显示结束界面")

        while True:
            for 事件 in pygame.event.get():
                if 事件.type == pygame.QUIT:
                    return False
                if 事件.type == pygame.KEYDOWN:
                    if 事件.key == pygame.K_r:
                        print("用户选择重新开始")
                        return True
                    elif 事件.key == pygame.K_q:
                        print("用户选择退出")
                        return False

    def 游戏循环(self):
        while True:
            for 事件 in pygame.event.get():
                if 事件.type == pygame.QUIT:
                    return False
                elif 事件.type == pygame.KEYDOWN:
                    if 事件.key == pygame.K_UP and self.方向 != 'DOWN':
                        self.方向 = 'UP'
                    elif 事件.key == pygame.K_DOWN and self.方向 != 'UP':
                        self.方向 = 'DOWN'
                    elif 事件.key == pygame.K_LEFT and self.方向 != 'RIGHT':
                        self.方向 = 'LEFT'
                    elif 事件.key == pygame.K_RIGHT and self.方向 != 'LEFT':
                        self.方向 = 'RIGHT'

            self.移动蛇()

            if self.蛇[0] == self.食物:
                self.分数 += 1
                self.食物 = self.生成食物()
            else:
                self.蛇.pop()

            if self.检查碰撞():
                return self.结束界面()

            self.画蛇和食物()
            self.显示文本(f"分数: {self.分数}", 35, self.白色, 70, 20)
            pygame.display.flip()
            self.时钟.tick(10)

    def 运行(self):
        print("游戏开始运行")
        while True:
            if not self.开始界面():
                break
            if not self.游戏循环():
                break
            self.重置游戏()
        pygame.quit()
        print("游戏结束")

if __name__ == "__main__":
    游戏 = 贪吃蛇()
    游戏.运行()
