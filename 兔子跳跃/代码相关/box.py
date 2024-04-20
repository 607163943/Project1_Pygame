# python的第三方模块
import pygame as pg


# 工具类
class Box:
    # 初始化工具对象数据
    def __init__(self):
        # 生成计时器类工具对象(用于设置FPS)
        self.clock=pg.time.Clock()

    # 设置FPS
    def set_FPS(self,FPS):
        self.clock.tick(FPS)

    # 绘制文本
    def draw_text(self, surface:pg.surface.Surface,
                  font_name:str, font_size:int,font_color:tuple[int,int,int],x, y,text):
        # 创建字体对象
        temp = pg.font.Font(font_name, font_size)
        # 绘制字体表面,并指定字体颜色和文本
        font_surface = temp.render(text, True, font_color)
        # 获取字体表面的控制矩形(用来设置字体的出现位置)
        font_rect = font_surface.get_rect()
        # 指定文本出现位置
        font_rect.center = (x, y)
        # 将绘制的字体文本显示在屏幕中
        surface.blit(font_surface, font_rect)

    # 在指定图像上绘制图标
    def draw_icon(self,window_surface:pg.surface.Surface,icon_surface:pg.surface.Surface,x,y):
        icon_rect=icon_surface.get_rect()
        icon_rect.center=(x,y)
        window_surface.blit(icon_surface,icon_rect)