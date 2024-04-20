# python第三方模块
import pygame as pg
# python内置模块
from os import path
import random
# 自己编写的python模块
from sprite import run_sprite
from setting import ConfigRun


# 游戏类
class Game:
    # 初始化游戏对象数据
    def __init__(self,box,window):
        # 加载游戏界面配置
        self.run_config = ConfigRun()
        # 存放各种加载图片
        self.image_dict={"player":{"stand":[],"walk_l":[],"walk_r":[]},"bg":[]}
        # 存放加载的弹簧图片
        self.image_spring_dict={}
        # 存放加载地板图片
        self.image_wall_dict={"grass":[],"wood":[],"sand":[],"snow":[],"stone":[]}
        # 存放加载的背景地形图片
        self.image_plant_dict={"grass":[], "mushroom":[],"grass_brown":[],"cactus":[]}
        # 存放加载的硬币图片
        self.image_coin_dict={"bronze":[],"silver":[],"gold":[]}
        # 存放收集硬币图像
        self.image_coin_icon_dict={}
        self.music_dict={}  # 存放各种加载的音乐文件对象
        # 加载图片
        self.load_image()
        # 加载音乐
        self.load_music()
        # 匹配字体名并使用
        self.font_name=pg.font.match_font(self.run_config.font_name)
        # 记录游戏分数
        self.score=0
        # 记录收集的各种硬币数量
        self.bronze_number=0
        self.silver_number=0
        self.gold_number=0
        # 存放工具类对象
        self.box=box
        # 存放窗口对象
        self.window=window
        self.screen:pg.surface.Surface=window.screen

    # 加载图片
    def load_image(self):
        dir_path_base=""
        dir_image_path=path.join(dir_path_base,"image")
        dir_PNG_path=path.join(dir_image_path,"PNG")
        dir_Background_path=path.join(dir_PNG_path,"Background")
        # 加载背景图
        for i in range(1,5):
            # 将背景图加载并缩放到与窗口等大后存放
            self.image_dict.get("bg").append(pg.transform.scale(
                pg.image.load(file=path.join(dir_Background_path,f"bg_layer{i}.png")).convert_alpha(),
                (self.run_config.width,self.run_config.height)))

        dir_Players_path = path.join(dir_PNG_path, "Players")
        # 加载玩家图
        # 将人物图片加载并缩放到0.4倍后存放
        temp_tuple = ("ready", "stand")
        for i in temp_tuple:
            self.image_dict.get("player").get("stand").append(pg.transform.scale_by(
                pg.image.load(file=path.join(dir_Players_path, f"bunny1_{i}.png")).convert_alpha(),
                0.4
            ))

        temp_tuple = ("walk1", "walk2")
        for i in temp_tuple:
            self.image_dict.get("player").get("walk_r").append(pg.transform.scale_by(
                pg.image.load(path.join(dir_Players_path, f"bunny1_{i}.png")).convert_alpha(),
                0.4
            ))

        self.image_dict.get("player")["jump"] = pg.transform.scale_by(
            pg.image.load(path.join(dir_Players_path, "bunny1_jump.png")).convert_alpha(),
            0.4
        )

        # 将所有人物向右行走的图片进行绕x轴翻转后向左行走的图片存放
        for i in self.image_dict.get("player").get("walk_r"):
            self.image_dict.get("player").get("walk_l").append(
                pg.transform.flip(i, True, False).convert_alpha()
            )

        dir_Environment_path=path.join(dir_PNG_path,"Environment")
        # 加载地形图
        temp_type_tuple=("grass","wood","sand","snow","stone")
        temp_tuple=("","_small")
        for i in temp_type_tuple:
            for j in temp_tuple:
                self.image_wall_dict.get(i).append(
                    pg.transform.scale_by(
                        pg.image.load(path.join(dir_Environment_path, f"ground_{i}{j}.png")).convert_alpha(),
                        0.4
                    )
                )
        # 加载植被图
        # 加载草图像
        temp_tuple=("grass","grass_brown")
        for i in temp_tuple:
            for j in range(1,3):
                self.image_plant_dict.get(i).append(
                    pg.transform.scale_by(
                        pg.image.load(file=path.join(dir_Environment_path, f"{i}{j}.png")).convert_alpha(),
                        0.4
                    )
                )
        # 加载蘑菇图像
        temp_tuple=("brown","red")
        for i in temp_tuple:
            self.image_plant_dict.get("mushroom").append(
                pg.transform.scale_by(
                    pg.image.load(file=path.join(dir_Environment_path, f"mushroom_{i}.png")).convert_alpha(),
                    0.4
                )
            )
        # 加载仙人掌图像
        self.image_plant_dict.get("cactus").append(
            pg.transform.scale_by(
                pg.image.load(file=path.join(dir_Environment_path, "cactus.png")).convert_alpha(),
                0.4
            )
        )
        dir_Items_path = path.join(dir_PNG_path, "Items")
        # 加载各种硬币
        temp_tuple=("bronze","silver","gold")
        for i in temp_tuple:
            # 将加载的图像缩放到0.4倍后存放
            for j in range(1,5):
                self.image_coin_dict.get(i).append(pg.transform.scale_by(
                    pg.image.load(path.join(dir_Items_path,f"{i}_{j}.png")).convert_alpha(),
                    0.4
                ))
            # 添加部分图像绕X轴旋转生成的新图像
            for j in range(2,0,-1):
                self.image_coin_dict.get(i).append(pg.transform.flip(
                    self.image_coin_dict.get(i)[j],True,False
                ).convert_alpha())
        for i in temp_tuple:
            self.image_coin_icon_dict[i]=pg.transform.scale_by(
                pg.image.load(path.join(dir_Items_path,f"{i}_1.png")).convert_alpha(),
                0.3
            )
        # 加载弹簧图像
        temp_type_tuple=("normal","up")
        temp_tuple=("","_out")
        for i in range(2):
            self.image_spring_dict[temp_type_tuple[i]]=pg.transform.scale_by(
                pg.image.load(path.join(dir_Items_path,f"spring{temp_tuple[i]}.png")).convert_alpha(),
                0.4
            )

    # 加载音乐
    def load_music(self):
        dir_path_base=""
        dir_music_path=path.join(dir_path_base,"music")
        dir_bg_music_path=path.join(dir_music_path,"bg_music")
        # 存放加载的背景乐
        self.music_dict["bg"]=path.join(dir_bg_music_path,"bg.wav")

    # 初始化游戏(初始化后会进入游戏)
    def new(self):
        # 创建精灵组
        # 创建总精灵组并指定优先级绘制
        self.all_sprite=pg.sprite.LayeredUpdates()
        self.walls=pg.sprite.Group()
        self.plants=pg.sprite.Group()
        self.coins=pg.sprite.Group()
        self.springs=pg.sprite.Group()
        # 随机指定天气场景类型
        self.weather_type=random.choice(self.run_config.weather_type_tuple)
        # 创建玩家精灵
        self.player=run_sprite.Player(self,*self.run_config.player_start_pos)
        # 创建初始地板
        for i in self.run_config.wall_start_list:
            run_sprite.Wall(self,*i)
        # 加载背景乐并播放
        pg.mixer.music.load(self.music_dict.get("bg"))
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=-1)
        # 初始化分数
        self.score = 0
        # 重置收集的各种硬币数量
        self.bronze_number = 0
        self.silver_number = 0
        self.gold_number = 0
        # 运行游戏
        self.run()

    # 处理事件
    def event(self):
        # 获取自上一次获取事件函数后出现的事件
        for event in pg.event.get():
            # 判断是否点击窗口关闭按钮
            if event.type==pg.QUIT:
                # 判断是否已开始游戏(内层循环)
                if self.playing:
                    self.playing=False
                # 退出游戏
                self.window.running=False

    # 更新游戏数据
    def update(self):
        # 执行所有继承自pygame精灵类子类的update方法
        self.all_sprite.update()
        # 判断玩家在窗口的位置是否在自上到下四分之一处
        if self.player.pos.y<self.run_config.height/4:
            # 执行将玩家和地板向下移动(视觉和感觉上的地板向下,玩家向上移动)
            self.player.pos.y+=max(abs(self.player.vel.y),2)  # 移动玩家
            # 向下移动各精灵,如果有精灵超过了屏幕下方一定距离就移除该精灵
            for i in self.walls:
                i.rect.centery+=max(abs(self.player.vel.y),2)
                if i.rect.top>self.run_config.height +50:
                    i.kill()
            for i in self.plants:
                i.rect.centery+=max(abs(self.player.vel.y),2)
                if i.rect.top>self.run_config.height+50:
                    i.kill()
            for i in self.coins:
                i.rect.centery+=max(abs(self.player.vel.y),2)
                if i.rect.top>self.run_config.height+50:
                    i.kill()
            for i in self.springs:
                i.rect.centery+=max(abs(self.player.vel.y),2)
                if i.rect.top>self.run_config.height+50:
                    i.kill()
        # 判断玩家是否遇到金币
        hits=pg.sprite.spritecollide(self.player,self.coins,True)
        # 遇到金币加分
        if hits:
            for i in hits:
                match i.type:
                    case "bronze":
                        self.score+=10
                        self.bronze_number+=1
                    case "silver":
                        self.score+=50
                        self.silver_number+=1
                    case "gold":
                        self.score+=100
                        self.gold_number+=1
        # 在窗口上方生成地板维持地图中存在的地板数量不低于5
        while len(self.walls)<5:
            run_sprite.Wall(self,
                        x=random.randrange(0,self.run_config.width*2/3),
                        y=random.randrange(-10,0))

    # 绘制图像
    def draw(self):
        # 背景图底图
        temp=self.image_dict.get("bg")[0]
        # 将其余背景图层依次添加到背景图底图上形成完整背景图
        for i in range(1,4):
            temp.blit(self.image_dict.get("bg")[i],(0,0))
        # 将背景图绘制到屏幕上
        self.window.screen.blit(temp, (0, 0))
        # 将所有精灵绘制到屏幕上
        self.all_sprite.draw(self.window.screen)
        # 绘制玩家游戏分数
        self.box.draw_text(self.window.screen,
                           self.font_name,self.run_config.font_size,self.run_config.white,
                           self.run_config.width/2,20,str(self.score))
        # 绘制硬币收集图像
        self.draw_coin_icon()
        # 将绘制好的新游戏屏幕显示电脑窗口上
        pg.display.flip()

    # 绘制硬币收集图像
    def draw_coin_icon(self):
        temp_tuple=("gold","silver","bronze")
        temp_coin_number_dict={"gold":self.gold_number,"silver":self.silver_number,"bronze":self.bronze_number}
        x=self.run_config.width-50
        y=20
        # 将各种硬币和数量绘制到屏幕上
        for i in temp_tuple:
            # 绘制硬币图像
            self.box.draw_icon(self.screen,self.image_coin_icon_dict.get(i),x,y)
            # 绘制硬币数量
            self.box.draw_text(self.screen,self.font_name,self.run_config.font_size,self.run_config.white,
                               x+30,y,str(temp_coin_number_dict.get(i)))
            y+=30

    # 游戏运行循环
    def run(self):
        # 游戏运行循环
        self.playing=True
        while self.playing:
            self.box.set_FPS(self.run_config.fps)  # 设置定时长完成循环
            self.event()  # 更新事件
            self.update()  # 更新各精灵
            self.draw()  # 绘制新图像
        # 清空精灵组中的精灵
        self.all_sprite.empty()
        # 重置鼠标位置
        self.window.mouse_x,self.window.mouse_y=0,0