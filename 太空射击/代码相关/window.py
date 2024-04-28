# python第三方模块
import pygame as pg
# python内置模块
from os import path
import csv
# python自定义模块
from sprites import start_sprites
from sprites import over_sprites
from config import Config
from config import StartConfig
from config import OverConfig
import image
import game
import box


# 窗口类
class Window:

    # 初始化window实列
    def __init__(self):
        self.running=True
        # 创建屏幕
        self.screen = pg.display.set_mode((Config.WIDTH, Config.HEIGHT))
        # 指定标题
        pg.display.set_caption(Config.TITLE)
        # 创建工具类对象
        self.box = box.Box()
        # 创建图片对象
        self.image=image.Image()
        # 创建游戏对象
        self.game=game.Game(self)
        # 记录鼠标坐标
        self.mouse_x=0
        self.mouse_y=0
        # 记录最高分数
        self.max_score=0
        # 加载数据
        self.load_data()
        # 记录鼠标点击情况
        self.is_mouse=False

    # 加载数据
    def load_data(self):
        dir_path_base=""
        dir_data_path=path.join(dir_path_base,"data")
        try:
            with open(path.join(dir_data_path,"score.csv"),mode="r+",encoding="UTF-8")as f:
                f.seek(0)
                csv_f=csv.reader(f)
                for i in csv_f:
                    self.max_score=int(i[0])
        except ValueError as e:
            self.max_score=0

    # 将最新分数存到数据文件
    def __del__(self):
        dir_path_base=""
        dir_data_path=path.join(dir_path_base,"data")
        with open(path.join(dir_data_path,"score.csv"),mode="w+",encoding="UTF-8",newline="")as f:
            f.seek(0)
            csv_f=csv.writer(f)
            csv_f.writerow([self.max_score])

    # 初始化开始界面
    def start_new(self):
        self.start_all_sprite=pg.sprite.Group()
        self.start_buttons=pg.sprite.Group()
        self.start_labels=pg.sprite.Group()
        # 创建标签
        start_sprites.Label(self,200,60,StartConfig.BLACK,StartConfig.WIDTH//2,StartConfig.HEIGHT//4,
                            50,StartConfig.WHITE,StartConfig.TITLE)
        # 记录分数标签
        start_sprites.Label(self,480,60,StartConfig.BLACK,StartConfig.WIDTH//2,StartConfig.HEIGHT*3//7,
                            30,StartConfig.WHITE,f"最高纪录:{self.max_score}")
        # 创建按钮
        start_sprites.Button(self,180,60,StartConfig.GREY1,StartConfig.WIDTH//2,StartConfig.HEIGHT*2/3,
                             30,StartConfig.BLACK,"开始游戏")
        # 运行开始界面
        self.start_run()

    # 处理开始界面事件
    def start_event(self):
        for event in pg.event.get():
            # 判断是否点击窗口关闭按钮
            if event.type==pg.QUIT:
                if self.start_playing:
                    self.start_playing=False
                self.running=False
            # 判断是否按下鼠标
            elif event.type==pg.MOUSEBUTTONDOWN:
                self.is_mouse=True
            # 判断是否移动鼠标
            elif event.type==pg.MOUSEMOTION:
                self.mouse_x,self.mouse_y=pg.mouse.get_pos()

    # 更新开始界面数据
    def start_update(self):
        self.start_all_sprite.update()

    # 绘制开始界面
    def start_draw(self):
        self.screen.blit(self.image.start_image_dict.get("bg"),(0,0))
        self.start_all_sprite.draw(self.screen)
        pg.display.flip()

    # 运行开始界面
    def start_run(self):
        self.start_playing=True
        while self.start_playing:
            self.box.set_fps(StartConfig.FPS)
            self.start_event()
            self.start_update()
            self.start_draw()
        # 清空当前界面设置的精灵和鼠标状态
        self.start_all_sprite.empty()
        self.start_labels.empty()
        self.start_buttons.empty()
        self.mouse_x,self.mouse_y=0,0
        self.is_mouse=False

    # 初始化游戏界面
    def game_new(self):
        # 将鼠标隐藏
        pg.mouse.set_visible(False)
        self.game.new()

    # 初始化结束界面
    def over_new(self):
        # 判断游戏是否已通过关闭键退出
        if self.running:
            self.over_all_sprite=pg.sprite.Group()
            self.over_labels=pg.sprite.Group()
            self.over_buttons=pg.sprite.Group()
            # 创建标签
            over_sprites.Label(self,200,60,OverConfig.BLACK,OverConfig.WIDTH//2,OverConfig.HEIGHT // 4,
                                50, OverConfig.WHITE, "游戏结束")
            # 记录分数标签
            max_score_text=f"最高纪录:{self.max_score}"
            if self.game.score>self.max_score:
                self.max_score = self.game.score
                max_score_text = "新纪录!"
            over_sprites.Label(self, 480, 60, OverConfig.BLACK, OverConfig.WIDTH // 2,
                               OverConfig.HEIGHT * 2 // 5,
                               30, OverConfig.WHITE, max_score_text)
            over_sprites.Label(self, 480, 60, OverConfig.BLACK, OverConfig.WIDTH // 2,
                               OverConfig.HEIGHT // 2,
                               30, OverConfig.WHITE, f"本轮分数:{self.game.score}")
            # 创建按钮
            over_sprites.Button(self,180,60,OverConfig.GREY1,OverConfig.WIDTH//2,OverConfig.HEIGHT*2//3,
                                 30, OverConfig.BLACK, "重新开始")
            self.over_run()

    # 遍历结束界面
    def over_event(self):
        for event in pg.event.get():
            # 判断是否按下窗口关闭按钮
            if event.type==pg.QUIT:
                if self.over_playing:
                    self.over_playing=False
                self.running=False
            # 判断是否按下鼠标
            elif event.type==pg.MOUSEBUTTONDOWN:
                self.is_mouse=True
            # 判断鼠标是否移动
            elif event.type==pg.MOUSEMOTION:
                self.mouse_x,self.mouse_y=pg.mouse.get_pos()

    # 更新结束界面数据
    def over_update(self):
        self.over_all_sprite.update()

    # 绘制结束界面
    def over_draw(self):
        self.screen.blit(self.image.over_image_dict.get("bg"),(0,0))
        self.over_all_sprite.draw(self.screen)
        pg.display.flip()

    # 运行结束界面
    def over_run(self):
        self.over_playing=True
        while self.over_playing:
            self.box.set_fps(OverConfig.FPS)
            self.over_event()
            self.over_update()
            self.over_draw()
        # 清空当前界面设置的精灵和鼠标状态
        self.over_all_sprite.empty()
        self.over_labels.empty()
        self.over_buttons.empty()
        self.mouse_x,self.mouse_y=0,0
        self.is_mouse=False

    # 显示窗口
    def show(self):
        self.start_new()
        while self.running:
            self.game_new()
            self.over_new()