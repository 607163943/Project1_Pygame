import pygame as pg


# 基础配置类
class Config:
    # 屏幕宽高
    WIDTH = 480
    HEIGHT = 600
    # 屏幕标题
    TITLE = "太空射击"
    # 游戏FPS
    FPS = 60
    # 使用到的rbg颜色
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    GREY1=(200, 200, 200)


# 开始界面配置
class StartConfig(Config):
    # 字体配置
    START_FONT_NAME = "simHei"
    FONT_NAME = pg.font.match_font(START_FONT_NAME)


# 游戏界面配置
class GameConfig(Config):
    # 字体配置
    START_FONT_NAME="simHei"
    FONT_NAME=pg.font.match_font(START_FONT_NAME)
    FONT_SIZE=30
    # 玩家配置
    PLAYER_VEL_X = 5
    # 敌人类型
    MOB_TYPE_TUPLE=("big","med","small","tiny")
    # 不同类型的敌人生命上限
    MOB_LIFE_DICT={"big":160,"med":80,"small":40,"tiny":20}
    # 子弹配置
    BULLET_VEL_Y = -12
    BULLET_DAMAGE = 20
    # 道具配置
    POWER_LIFE_TIME=10000


# 结束界面配置
class OverConfig(Config):
    # 字体配置
    START_FONT_NAME = "simHei"
    FONT_NAME = pg.font.match_font(START_FONT_NAME)
