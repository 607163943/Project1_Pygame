# python的第三方模块
import pygame as pg
# python内置的模块
from os import path
import csv
# 编写的python模块
from sprite import start_sprite
from sprite import over_sprite
from setting import Config
from setting import ConfigStart
from setting import ConfigOver
import game
import box
class Window:
    # 初始化窗口对象数据
    def __init__(self):
        # 初始化pygame模块
        pg.init()
        pg.mixer.init()
        # 创建工具对象
        self.box=box.Box()
        # 窗口界面循环
        self.running = True
        # 加载通用配置
        self.config=Config()
        # 加载开始界面配置
        self.start_config=ConfigStart()
        # 加载结束界面配置
        self.over_config=ConfigOver()
        # 设置窗口大小
        self.screen = pg.display.set_mode((self.config.width, self.config.height))
        # 设置窗口标题
        pg.display.set_caption(self.config.title)
        # 实列化游戏对象
        self.game=game.Game(self.box,self)
        # 记录最高分数
        self.max_score=0
        # 记录是否更新最高分数
        self.is_update_score=False
        self.mouse_x=0
        self.mouse_y=0
        # 加载最高记录数据
        self.load_data()

    # 加载最高记录
    def load_data(self):
        dir_path_base=""
        dir_data_path=path.join(dir_path_base,"data")
        with open(path.join(dir_data_path,"data.csv"),mode="r+",encoding="UTF-8")as f:
            # 将数据读取,若没有数据,则使用默认的0值
            csv_f=csv.reader(f)
            for i in csv_f:
                self.max_score=int(i[0])
                break

    # 将最新的最高记录写入csv文件
    def __del__(self):
        dir_path_base = ""
        dir_data_path = path.join(dir_path_base, "data")
        with open(path.join(dir_data_path, "data.csv"), mode="w+", encoding="UTF-8") as f:
            csv_f=csv.writer(f)
            csv_f.writerow([self.max_score])

    # 显示开始界面
    def show_start_game(self):
        self.start_game_new()

    # 初始化开始界面数据
    def start_game_new(self):
        self.start_all_sprite=pg.sprite.Group()
        start_sprite.Button(self, 150, 60, self.start_config.width / 2, self.start_config.height * 2 / 3)
        self.start_game_run()

    # 处理开始界面事件
    def start_game_event(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                if self.start_playing:
                    self.start_playing=False
                self.running=False
            elif event.type==pg.MOUSEBUTTONDOWN:
                self.mouse_x,self.mouse_y=pg.mouse.get_pos()
            elif event.type==pg.KEYDOWN:
                self.start_playing=False

    # 更新开始界面数据
    def start_game_update(self):
        self.start_all_sprite.update()

    # 绘制开始界面图像
    def start_game_draw(self):
        # 填充窗口颜色
        self.screen.fill(self.start_config.black)
        # 绘制窗口文本
        self.box.draw_text(self.screen,self.start_config.font_name,self.start_config.title_font_size,
                           self.start_config.white,self.start_config.width/2,self.start_config.height/4,"兔子跳跃")
        self.box.draw_text(self.screen,self.start_config.font_name,self.start_config.score_font_size,
                           self.start_config.white,self.start_config.width/2,self.start_config.height/2-50,
                           f"最高纪录:{self.max_score}")
        # 绘制精灵
        self.start_all_sprite.draw(self.screen)
        # 绘制按钮文本
        self.box.draw_text(self.screen,self.start_config.font_name,self.start_config.button_font_size,
                           self.start_config.black,self.start_config.width/2,self.start_config.height*2/3,
                           "开始游戏")
        # 将绘制好的图像显示到窗口上
        pg.display.flip()

    # 运行开始界面
    def start_game_run(self):
        self.start_playing=True
        while self.start_playing:
            self.box.set_FPS(self.start_config.fps)
            self.start_game_event()
            self.start_game_update()
            self.start_game_draw()
        # 退出本循环后会进入下一个窗口,因此要清除所有精灵
        self.start_all_sprite.empty()
        self.mouse_x,self.mouse_y=0,0

    # 显示游戏界面
    def show_run_game(self):
        self.game.new()

    # 显示结束界面
    def show_over_game(self):
        # 判断玩家是否通过窗口关闭按钮直接关闭游戏
        if not self.running:
            return None
        # 设置背景乐音量变小止停止背景乐的时间
        pg.mixer.music.stop()
        self.over_game_new()

    # 初始化结束界面数据
    def over_game_new(self):
        self.over_all_sprite=pg.sprite.Group()
        over_sprite.Button(self, 150, 60, self.start_config.width / 2, self.start_config.height * 2 / 3)
        self.over_game_run()

    # 处理结束界面事件
    def over_game_event(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.over_playing=False
                self.running=False
            elif event.type==pg.MOUSEBUTTONDOWN:
                self.mouse_x,self.mouse_y=pg.mouse.get_pos()
            elif event.type == pg.KEYDOWN:
                self.over_playing = False

    # 更新结束界面数据
    def over_game_update(self):
        self.over_all_sprite.update()

    # 绘制结束界面图像
    def over_game_draw(self):
        # 填充窗口
        self.screen.fill(self.over_config.black)
        # 绘制窗口文本
        self.box.draw_text(self.screen, self.over_config.font_name, self.over_config.title_font_size,
                           self.over_config.white, self.over_config.width / 2, self.over_config.height // 4,
                           "游戏结束")
        # 根据本轮得分显示对应文本
        if self.game.score<=self.max_score:
            self.box.draw_text(self.screen, self.over_config.font_name, self.over_config.score_font_size,
                               self.over_config.white, self.over_config.width / 2, self.over_config.height / 2 - 50,
                               f"最高纪录:{self.max_score}")
            self.box.draw_text(self.screen, self.over_config.font_name, self.over_config.score_font_size,
                               self.over_config.white, self.over_config.width / 2, self.over_config.height / 2,
                               f"本次得分:{self.game.score}")
        else:
            self.box.draw_text(self.screen, self.over_config.font_name, self.over_config.score_font_size,
                               self.over_config.white, self.over_config.width / 2, self.over_config.height / 2 - 50,
                               f"新纪录!")
            self.box.draw_text(self.screen, self.over_config.font_name, self.over_config.score_font_size,
                               self.over_config.white, self.over_config.width / 2, self.over_config.height / 2,
                               f"本次得分:{self.game.score}")
            self.is_update_score=True
        # 绘制精灵
        self.over_all_sprite.draw(self.screen)
        # 绘制按钮文本
        self.box.draw_text(self.screen, self.over_config.font_name, self.over_config.button_font_size,
                           self.over_config.black, self.over_config.width / 2, self.over_config.height * 2 / 3,
                           "重新开始")
        # 将绘制好的图像显示到窗口上
        pg.display.flip()

    # 运行结束界面
    def over_game_run(self):
        # 游戏结束界面循环
        self.over_playing=True
        while self.over_playing:
            self.box.set_FPS(self.over_config.fps)
            self.over_game_event()
            self.over_game_update()
            self.over_game_draw()
        # 切换界面或者关闭窗口时清空所有精灵
        self.over_all_sprite.empty()
        if self.is_update_score:
            self.max_score=self.game.score
            self.is_update_score=False
        # 重置鼠标位置
        self.mouse_x, self.mouse_y = 0, 0

    # 显示窗口并进入窗口界面切换循环
    def show(self):
        # 显示开始游戏界面
        self.show_start_game()
        # 进入游戏状态切换循环
        while self.running:
            # 显示游戏界面
            self.show_run_game()
            # 显示游戏结束界面
            self.show_over_game()