# python第三方模块
import pygame as pg
# python内置模块
from os import path
# python自定义模块
from config import StartConfig
from config import GameConfig
from config import OverConfig


# 图片类
class Image:
    # 初始化图片实列数据
    def __init__(self):
        # 存放初始图片
        self.image_dict={"power":{},"shield":{}}
        self.mob_dict={"big":[], "med":[], "small":[], "tiny":[]}
        # 存放开始界面图片
        self.start_image_dict = {"power":{},"shield":{}}
        # 存放运行界面图片
        self.game_image_dict={"power":{},"shield":{}}
        self.game_mob_dict={"big":[], "med":[], "small":[], "tiny":[]}
        # 存放结束界面图片
        self.over_image_dict = {"power":{},"shield":{}}
        # 加载初始图片
        self.load_image()
        # 加载开始界面图像
        self.load_start_image()
        # 加载运行界面图像
        self.load_game_image()
        # 加载结束界面图像
        self.load_over_image()

    # 加载初始图片
    def load_image(self):
        # 图片总路径
        dir_image_path_base = ""
        # 使用到的子文件夹路径
        dir_image_path = path.join(dir_image_path_base, "image")

        dir_Backgrounds_path = path.join(dir_image_path, "Backgrounds")
        self.image_dict["bg"] = pg.image.load(file=path.join(dir_Backgrounds_path, "black.png")).convert()

        dir_PNG_path = path.join(dir_image_path, "PNG")
        self.image_dict["player"] = pg.image.load(file=path.join(dir_PNG_path, "playerShip1_blue.png")).convert()

        dir_Meteors_path = path.join(dir_PNG_path, "Meteors")
        temp_tuple = ("big1", "big2", "big3", "big4", "med1", "med3", "small1", "small2", "tiny1", "tiny2")
        for i in temp_tuple:
            self.mob_dict.get(i[:-1]).append(
                pg.image.load(path.join(dir_Meteors_path, f"meteorBrown_{i}.png")).convert()
            )

        dir_Lasers_path = path.join(dir_PNG_path, "Lasers")
        self.image_dict["bullet"] = pg.image.load(file=path.join(dir_Lasers_path, "laserBlue01.png")).convert()

        dir_Power_ups_path = path.join(dir_PNG_path, "Power-ups")
        temp_tuple = ("pill_blue", "powerupBlue_bolt", "powerupBlue_shield")
        name_tuple = ("help", "shoot_up", "shield")
        for i in range(len(temp_tuple)):
            image_name = temp_tuple[i]
            self.image_dict.get("power")[name_tuple[i]] =pg.image.load(
                path.join(dir_Power_ups_path, f"{image_name}.png")).convert()

        dir_Effects_path = path.join(dir_PNG_path, "Effects")
        temp_tuple = ("low", "normal")
        for i in range(1, len(temp_tuple) + 1):
            self.image_dict.get("shield")[temp_tuple[i - 1]] =pg.image.load(
                path.join(dir_Effects_path, f"shield{i}.png")).convert()

        dir_UI_path = path.join(dir_PNG_path, "UI")
        self.image_dict["player_life"] =pg.image.load(
            path.join(dir_UI_path, "playerLife1_blue.png")).convert()

    # 生成开始界面图像
    def load_start_image(self):
        # 背景图
        self.start_image_dict["bg"] = pg.transform.scale(
            self.image_dict.get("bg"), (StartConfig.WIDTH, StartConfig.HEIGHT)
        ).convert()

    # 生成运行界面图像
    def load_game_image(self):
        # 背景图
        self.game_image_dict["bg"]=pg.transform.scale(
            self.image_dict.get("bg"),(GameConfig.WIDTH,GameConfig.HEIGHT)
        ).convert()
        # 玩家图像
        self.game_image_dict["player"]=pg.transform.scale_by(
            self.image_dict.get("player"),0.65
        ).convert()
        # 岩石图像
        temp_tuple=("big","med","small","tiny")
        for i in temp_tuple:
            for j in self.mob_dict.get(i):
                self.game_mob_dict.get(i).append(
                    pg.transform.scale_by(j,1).convert()
                )
        self.game_image_dict["bullet"]=pg.transform.scale_by(
            self.image_dict.get("bullet"),1
        ).convert()
        # 加载道具图像
        temp_tuple = ("help", "shoot_up", "shield")
        for i in temp_tuple:
            self.game_image_dict.get("power")[i]=pg.transform.scale_by(
                self.image_dict.get("power")[i],1
            ).convert()
        # 加载护盾图像
        temp_tuple = ("low", "normal")
        for i in temp_tuple:
            self.game_image_dict.get("shield")[i]=pg.transform.scale_by(
                self.image_dict.get("shield")[i],0.6
            ).convert()
        # 加载玩家生命图像
        self.game_image_dict["player_life"]=pg.transform.scale_by(
            self.image_dict.get("player_life"),0.6
        ).convert()

    # 生成结束界面图像
    def load_over_image(self):
        # 背景图
        self.over_image_dict["bg"] = pg.transform.scale(
            self.image_dict.get("bg"), (OverConfig.WIDTH, OverConfig.HEIGHT)
        ).convert()
