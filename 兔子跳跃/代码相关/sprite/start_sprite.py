import pygame as pg
class Button(pg.sprite.Sprite):
    # 初始化按钮对象数据
    def __init__(self,window,width,height,x,y):
        self.window=window
        self.groups=(self.window.start_all_sprite)
        super().__init__(self.groups)
        self.image=pg.surface.Surface((width,height))
        self.image.fill(self.window.start_config.button_color)
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)

    # 更新按钮数据
    def update(self):
        if self.is_select():
            self.window.start_playing=False

    # 判断是否点击该按钮
    def is_select(self):
        return self.rect.collidepoint(self.window.mouse_x,self.window.mouse_y)