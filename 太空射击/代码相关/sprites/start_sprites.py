# python第三方模块
import pygame as pg
# python自定义模块
from config import StartConfig


# 标签类
class Label(pg.sprite.Sprite):
    # 初始化标签实列
    def __init__(self,window,width,height,color,x,y,font_size,font_color,text):
        self.window=window
        # 将标签实列添加到精灵组
        self.groups=(self.window.start_all_sprite,self.window.start_labels)
        super().__init__(self.groups)
        self.image=pg.surface.Surface((width,height))
        # 填充背景色
        self.image.set_colorkey(StartConfig.BLACK)
        # 指定标签位置
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        # 绘制标签文本
        self.draw_text(font_size,font_color,text)

    # 绘制文本
    def draw_text(self,font_size,font_color,text):
        font=pg.font.Font(StartConfig.FONT_NAME,font_size)
        font_surface=font.render(text,True,font_color)
        font_rect=font_surface.get_rect()
        font_rect.center=(self.rect.width//2,self.rect.height//2)
        self.image.blit(font_surface,font_rect)


# 按钮类
class Button(pg.sprite.Sprite):
    # 初始化按钮实列
    def __init__(self,window,width,height,color,x,y,font_size,font_color,text):
        self.window=window
        # 将按钮添加到精灵组
        self.groups=(self.window.start_all_sprite,self.window.start_buttons)
        super().__init__(self.groups)
        # 绘制按钮图像
        self.image=pg.surface.Surface((width,height))
        self.image.fill(color)
        # 指定按钮位置
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        # 存放文本和字体信息
        self.font_tuple = (font_size, font_color, text)
        # 绘制文本
        self.draw_text(*self.font_tuple)

    # 绘制按钮文本
    def draw_text(self,font_size,font_color,text):
        font=pg.font.Font(StartConfig.FONT_NAME,font_size)
        # 创建字体绘制对象
        font_surface=font.render(text,True,font_color)
        # 指定文本相对按钮左上角的的位置
        font_rect=font_surface.get_rect()
        font_rect.center=(self.rect.width//2,self.rect.height//2)
        # 将字体绘制面添加到按钮绘制面上
        self.image.blit(font_surface,font_rect)

    # 更新按钮数据
    def update(self):
        # 判断鼠标对按钮的操作
        self.mouse()

    # 判断鼠标是否点击按钮
    def mouse(self):
        # 判断鼠标是否移到按钮上方
        if self.rect.collidepoint(self.window.mouse_x,self.window.mouse_y):
            # 判断鼠标是否点击按钮
            if self.window.is_mouse:
                self.window.start_playing=False
                self.window.is_mouse=False
            self.image.fill(StartConfig.WHITE)
            self.draw_text(*self.font_tuple)
        else:
            self.image.fill(StartConfig.GREY1)
            self.draw_text(*self.font_tuple)
        self.window.is_mouse=False
