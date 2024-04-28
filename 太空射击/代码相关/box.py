import pygame as pg


# 工具类
class Box:
    # 初始化工具实列
    def __init__(self):
        self.clock=pg.time.Clock()

    # 设置FPS
    def set_fps(self,fps):
        self.clock.tick(fps)