import pygame as pg
# 通用配置类
class Config:
    # 初始化通用配置
    def __init__(self):
        self.width=480
        self.height=600
        self.fps=60
        self.title="兔子跳跃"
        font_start_name = "simHei"
        self.font_name = pg.font.match_font(font_start_name)
        self.load_rgb()

    # 加载颜色配置
    def load_rgb(self):
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)


# 开始界面配置类
class ConfigStart(Config):
    # 初始化开始界面配置数据
    def __init__(self):
        super().__init__()
        self.load_font_config()
        self.load_button_config()

    # 加载按钮配置
    def load_button_config(self):
        self.button_font_size=30
        self.button_color=(240,240,240)

    # 加载字体配置
    def load_font_config(self):
        self.title_font_size=50
        self.score_font_size=30


# 游戏界面配置类
class ConfigRun(Config):
    # 初始化运行界面配置数据
    def __init__(self):
        super().__init__()
        # 初始地板位置
        self.wall_start_list=[(0,self.height-40),(0,400),(self.width/2,250),(0,150),(self.width*2/3,50)]
        # 游戏天气场景类型
        self.weather_type_tuple=("grass","sand","snow")
        # 地板可能的类型
        self.wall_type_dict = {"grass":("grass","wood","stone"),
                               "sand":("sand","wood","stone"),
                               "snow":("snow","wood","stone")}
        # 植被可能的类型
        self.plant_type_dict={"grass":("grass","mushroom"),
                              "wood":("mushroom","grass_brown"),
                              "sand":("grass_brown","cactus"),"snow":("grass_brown",)}
        # 硬币可能的类型
        self.coin_type_tuple=("bronze","silver","gold")
        self.load_player_config()
        self.load_font_config()
        self.load_layer_config()

    # 加载字体配置
    def load_font_config(self):
        self.font_size = 30

    # 加载玩家配置
    def load_player_config(self):
        # 玩家移动加速度
        self.player_acc_x = 0.5
        self.player_acc_y = 0.8
        # 玩家水平摩擦力
        self.player_friction = 0.12
        # 玩家跳跃竖直方向初速度
        self.player_jump = -20
        # 玩家在弹簧上跳跃的竖直方向初速度
        self.player_spring_jump=-50
        # 玩家初始位置
        self.player_start_pos = (20, self.height - 100)

    # 加载绘制优先级配置
    def load_layer_config(self):
        # 设置的各类图像的绘制优先级(优先级越低越先绘制)
        self.player_layer = 6
        self.coin_layer = 6
        self.wall_layer = 5
        self.grass_layer = 3
        self.spring_layer=4


# 结束界面配置类
class ConfigOver(Config):
    # 初始化结束界面配置数据
    def __init__(self):
        super().__init__()
        self.load_font_config()
        self.load_button_config()

    # 加载按钮配置
    def load_button_config(self):
        self.button_font_size=30
        self.button_color=(240,240,240)

    # 加载字体配置
    def load_font_config(self):
        self.title_font_size=50
        self.score_font_size=30