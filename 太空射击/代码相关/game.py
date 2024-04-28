# python第三方模块
import pygame as pg
# python内置模块
import random
# python自定义模块
from sprites import game_sprite
from config import GameConfig
import box


# 游戏类
class Game:
    # 初始化游戏类数据
    def __init__(self,window):
        self.window=window
        # 存放加载的图片
        self.image_dict=self.window.image.game_image_dict
        # 存放加载敌人图片
        self.mob_dict=self.window.image.game_mob_dict
        self.clock = pg.time.Clock()  # 创建pygame的时钟对象控制内层的定时循环
        # 创建窗口并设置大小和标题
        self.screen:pg.surface.Surface=self.window.screen
        # 记录游戏分数
        self.score=0
        self.box:box.Box=self.window.box

    # 初始化游戏数据
    def new(self):
        # 创建游戏使用的精灵组
        self.all_sprite=pg.sprite.Group()
        self.mobs=pg.sprite.Group()
        self.bullets=pg.sprite.Group()
        self.powers=pg.sprite.Group()
        # 初始化分数
        self.score=0
        # 创建玩家精灵
        self.player= game_sprite.Player(self, GameConfig.WIDTH / 2, GameConfig.HEIGHT)
        # 创建多个敌人精灵
        for i in range(8):
            game_sprite.Mob(self, random.randint(-50, GameConfig.WIDTH + 50), random.randint(-100, -50))
        self.run()  # 开始游戏

    # 处理游戏界面事件
    def event(self):
        # 获取所有事件
        for event in pg.event.get():
            # 判断是否按下窗口关闭按钮
            if event.type==pg.QUIT:
                # 结束内外层循环
                if self.playing:
                    self.playing=False
                self.window.running=False

    # 更新数据
    def update(self):
        self.all_sprite.update()  # 更新所有精灵数据
        hits=pg.sprite.groupcollide(self.bullets,self.mobs,True,False) # 检测子弹与敌人的碰撞情况
        # 指定一个子弹只能消灭一个敌人,并根据消灭的敌人数增加游戏分数,分数由消灭的敌人半径决定
        for i in hits.values():
            temp: game_sprite.Mob=i[0]
            temp.life-=GameConfig.BULLET_DAMAGE
            if temp.life<=0:
                temp.life=0
                temp.hit_over=True
                self.score+=temp.max_life
        # 概率性在屏幕上方产出道具
        if random.uniform(0,100)<0.3:
            x=random.randint(0,GameConfig.WIDTH)
            y=random.randint(-100,-50)
            game_sprite.Power(self, x, y)

    # 绘制图像
    def draw(self):
        # 绘制背景图
        self.screen.blit(self.image_dict["bg"],(0,0))
        # 绘制所有精灵
        self.all_sprite.draw(self.screen)
        # 绘制分数文本
        self.draw_text(str(self.score),GameConfig.WIDTH/2,20)
        # 绘制敌人生命条
        self.draw_mob_life()
        # 绘制玩家生命条
        self.draw_player_life()
        # 绘制玩家护盾条
        self.draw_shield()
        # 绘制玩家的复活次数(图像表示)
        self.draw_life_number()
        # 将绘制好的屏幕翻转呈现在屏幕上
        pg.display.flip()

    # 绘制文本
    def draw_text(self,text:str,x,y):
        # 创建pygame字体并指定字体的控制矩形和在屏幕上的位置
        font=pg.font.Font(GameConfig.FONT_NAME,GameConfig.FONT_SIZE)
        font_surface=font.render(text,True,GameConfig.WHITE)
        font_rect=font_surface.get_rect()
        font_rect.center=(x,y)
        # 将字体绘制到屏幕上
        self.screen.blit(font_surface,font_rect)

    # 绘制敌人生命条
    def draw_mob_life(self):
        for i in self.mobs:
            if i.life<i.max_life:
                life_surface=pg.surface.Surface(((i.radius+40)*(i.life/i.max_life),5))
                life_rect=life_surface.get_rect()
                life_rect.center=i.rect.center
                life_rect.centery+=20
                pg.draw.rect(self.screen,GameConfig.GREEN,life_rect)

    # 绘制玩家生命条
    def draw_player_life(self):
        # 创建生命条框
        life_frame=pg.surface.Surface((120,15))
        life_frame_rect=life_frame.get_rect()
        life_frame_rect.topleft=(10,10)
        # 在屏幕上绘制该生命条框
        pg.draw.rect(self.screen,GameConfig.WHITE,life_frame_rect,3)
        # 创建当前生命条
        life=114*(self.player.life/100)
        life_bar=pg.surface.Surface((life,9))
        life_bar_rect=life_bar.get_rect()
        life_bar_rect.topleft=(13,13)
        # 在屏幕上绘制当前生命条
        pg.draw.rect(self.screen,GameConfig.GREEN,life_bar_rect)

    # 绘制复活次数
    def draw_life_number(self):
        for i in range(self.player.life_number):
            temp:pg.surface.Surface=self.image_dict.get("player_life")
            temp.set_colorkey(GameConfig.BLACK)
            # 在屏幕上绘制复活次数图像
            self.screen.blit(temp,(GameConfig.WIDTH*6/7+20*i,10))

    # 绘制护盾条
    def draw_shield(self):
        # 绘制护盾条框
        shield_frame_surface=pg.surface.Surface((120,10))
        shield_frame_rect=shield_frame_surface.get_rect()
        shield_frame_rect.topleft=(10,25)
        pg.draw.rect(self.screen,GameConfig.WHITE,shield_frame_rect,3)
        # 绘制护盾条
        shield_bar=114*(self.player.shield/100)
        shield_bar_surface=pg.surface.Surface((shield_bar,4))
        shield_bar_rect=shield_bar_surface.get_rect()
        shield_bar_rect.topleft=(13,28)
        pg.draw.rect(self.screen,GameConfig.BLUE,shield_bar_rect)

    # 运行游戏界面
    def run(self):
        self.playing=True
        while self.playing:
            # 设置定时长运行循环
            self.box.set_fps(GameConfig.FPS)
            self.event()
            self.update()
            self.draw()
        # 清空当前界面设置的精灵和鼠标状态
        self.all_sprite.empty()
        self.mobs.empty()
        self.bullets.empty()
        self.powers.empty()
        self.window.mouse_x,self.window.mouse_y=0,0
        self.window.is_mouse=False
        # 显示隐藏的鼠标
        pg.mouse.set_visible(True)
