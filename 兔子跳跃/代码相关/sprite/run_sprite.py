# python第三方模块
import pygame as pg
# python内置模块
import random
import game


# 玩家类
class Player(pg.sprite.Sprite):
    # 初始化玩家对象数据
    def __init__(self,game,x,y):
        self.game=game  # 存放游戏类
        self._layer = self.game.run_config.player_layer  # 指定玩家图像的绘制优先级
        self.groups=self.game.all_sprite
        super().__init__(self.groups)  # 将玩家精灵添加到指定的精灵组中
        self.update_index = 0  # 存放玩家当前所用的图片列表中的图片对象的索引
        # 设置玩家在屏幕上所用的图像(默认使用站立的第一张图像)
        self.image=self.game.image_dict.get("player").get("stand")[self.update_index]
        self.rect=self.image.get_rect()  # 获取玩家图像的控制矩形(通过设置矩形在屏幕位置可以改变玩家在屏幕的位置)
        self.pos=pg.math.Vector2(x,y)  # 存放位置向量
        self.vel=pg.math.Vector2(0,0)  # 存放速度向量
        self.acc=pg.math.Vector2(0,0)  # 存放加速度向量
        self.rect.center=self.pos  # 设置玩家的起始位置
        self.last_update_time=pg.time.get_ticks()  # 存放玩家创建时的其实时间(这个时间是从pygame开始运行时计算的)
        self.walking=False  # 存放玩家是否走路的标志
        self.jumping=False  # 存放玩家是否跳跃的标志

    # 更新玩家数据
    def update(self):
        self.move()  # 玩家移动函数
        self.image_replace()  # 替换玩家使用图像的函数

    # 玩家移动
    def move(self):
        self.acc=pg.math.Vector2(0,self.game.run_config.player_acc_y)  # 设置初始加速度
        key=pg.key.get_pressed()  # 获取玩家按下的键
        # 判断玩家是否左右移动
        if key[pg.K_RIGHT]:
            self.acc.x=self.game.run_config.player_acc_x
        if key[pg.K_LEFT]:
            self.acc.x=-self.game.run_config.player_acc_x
        # 判断玩家是否跳跃
        if key[pg.K_SPACE]:
            self.jump()
        # 计算摩擦力影响下的玩家实际水平加速度(忽略竖直方向摩擦力的影响)
        self.acc.x-=self.vel.x*self.game.run_config.player_friction
        self.vel+=self.acc  # 更新玩家的速度
        # 判断玩家是否处于行走状态,速度低于一定值将直接速度归零,不行走则处于站立状态
        if abs(self.vel.x)<0.2:
            self.vel.x=0
            self.walking=False
        else:
            self.walking=True
        # 更新玩家的位置向量
        self.pos+=self.vel+0.5*self.acc
        # 判断玩家是否遇到左右边界,若从左边界进入则从有边界出来,若从右边界进入,则从左边界出来
        if self.pos.x>self.game.run_config.width+self.rect.width/2:
            self.pos.x=0-self.rect.width/2
        elif self.pos.x<0-self.rect.width/2:
            self.pos.x=self.game.run_config.width+self.rect.width/2
        # 更新玩家在屏幕上的位置
        self.rect.center=self.pos
        # 判断玩家是否掉出屏幕下方
        if self.rect.y>self.game.run_config.height+100:
            self.game.playing=False
        else:
            # 先判断玩家是否遇到地板
            self.wall_hit()
            # 再判断玩家是否遇到弹簧
            self.spring_hit()

    # 跳跃函数
    def jump(self):
        # 避免pygame的帧检查机制对地板碰撞的影响设置的临时移动(保证玩家站在地板上能被检测到遇到地板)
        self.rect.centery+=1
        # 判断玩家是否遇到了地板
        wall_hits=pg.sprite.spritecollide(self,self.game.walls,False)
        spring_hits:list[Spring]=pg.sprite.spritecollide(self,self.game.springs,False)
        if not self.jumping:
            # 判断玩家是否站在地板上
            if wall_hits:
                # 更新玩家的是否跳跃状态
                self.jumping=True
                # 指定玩家的初始竖直方向的速度
                self.vel.y=self.game.run_config.player_jump
            # 判断玩家是否站在弹簧上
            elif spring_hits:
                self.jumping=True
                self.vel.y=self.game.run_config.player_spring_jump
                spring_hits[0].last_update=pg.time.get_ticks()
                spring_hits[0].state="up"
            # 清除临时移动的位置
        self.rect.centery-=1

    # 检测墙的碰撞
    def wall_hit(self):
        # 判断玩家是否在下落(遇到墙才会站在墙上,上升则会忽略它)
        if self.vel.y>0:
            # 判断玩家是否与墙精灵组中的任意精灵有碰撞
            hits:list[Wall]=pg.sprite.spritecollide(self,self.game.walls,False)
            # 判断是否下落时是否遇到墙
            if hits:
                # 判断玩家是否在地板上方(地板在玩家下方才会让玩家站在上面)
                if self.rect.bottom<hits[0].rect.bottom:
                    # 判断玩家与碰撞墙的水平位置(玩家处在地板水平范围内部在会让玩家站在上面)
                    if self.rect.left>hits[0].rect.left-38 and self.rect.right<hits[0].rect.right+38:
                        # 玩家竖直速度归零
                        self.vel.y=0
                        # 更新玩家位置向量
                        self.pos.y=hits[0].rect.top-self.rect.height/2
                        # 更新玩家在屏幕上的位置
                        self.rect.center=self.pos
                        # 如果玩家是跳到地板上的,更新跳跃状态
                        if self.jumping:
                            self.jumping=False

    # 检测弹簧的碰撞
    def spring_hit(self):
        # 判断玩家是否在下落(遇到弹簧才会站在弹簧上,上升则会忽略它)
        if self.vel.y>0:
            # 判断玩家是否与弹簧精灵组中的任意精灵有碰撞
            hits:list[Spring]=pg.sprite.spritecollide(self,self.game.springs,False)
            # 判断是否下落时是否遇到弹簧
            if hits:
                # 判断玩家是否在弹簧的竖直位置指定距离上方(避免因为竖直方向速度误差导致玩家从地板上闪现到弹簧上面)
                if self.rect.bottom<hits[0].rect.bottom-hits[0].rect.height/3:
                    # 判断玩家与碰撞弹簧的水平位置(玩家处在弹簧水平范围内部在会让玩家站在上面)
                    if self.rect.left>hits[0].rect.left-35 and self.rect.right<hits[0].rect.right+35:
                        # 玩家竖直速度归零
                        self.vel.y=0
                        # 更新玩家位置向量
                        self.pos.y=hits[0].rect.top-self.rect.height/2
                        # 更新玩家在屏幕上的位置
                        self.rect.center=self.pos
                        # 如果玩家是跳到弹簧上的,更新跳跃状态
                        if self.jumping:
                            self.jumping=False
                        hits[0].last_update=pg.time.get_ticks()

    # 替换玩家图像
    def image_replace(self):
        now=pg.time.get_ticks()  # 判断当前时间
        # 在对应状态下达到一定时间间隔更新图片索引来替换使用的图片,并更新上一次更新的时间
        # 替换图像时,会先保留该图像在屏幕上的位置并设置到新图像中,保证图像替换不会影响到玩家在屏幕上的位置变化
        if now-self.last_update_time>450 and not self.walking and not self.jumping:
            self.last_update_time=now
            self.update_index=(self.update_index+1)%len(
                self.game.image_dict.get("player").get("stand"))
            temp=self.rect.center
            self.image=self.game.image_dict.get("player").get("stand")[self.update_index]
            self.rect=self.image.get_rect()
            self.rect.center=temp
        elif now-self.last_update_time>200 and self.walking and not self.jumping:
            self.last_update_time=now
            self.update_index=(self.update_index+1)%len(
                self.game.image_dict.get("player").get("walk_r")
            )
            temp=self.rect.center
            # 判断玩家行走的方向
            if self.vel.x>0:
                self.image=self.game.image_dict.get("player").get("walk_r")[self.update_index]
            else:
                self.image=self.game.image_dict.get("player").get("walk_l")[self.update_index]
            self.rect=self.image.get_rect()
            self.rect.center=temp
        elif self.jumping:
            temp=self.rect.center
            self.image=self.game.image_dict.get("player").get("jump")
            self.rect=self.image.get_rect()
            self.rect.center=temp


# 墙类
class Wall(pg.sprite.Sprite):
    # 初始化墙对象数据
    def __init__(self,game,x,y):
        self.game = game
        # 指定地板的绘制优先级
        self._layer=self.game.run_config.wall_layer
        # 将该对象添加到指定精灵组中
        self.groups=(self.game.all_sprite,self.game.walls)
        super().__init__(self.groups)
        # 随机产生一个地板的类型
        self.type=random.choice(self.game.run_config.wall_type_dict.get(self.game.weather_type))
        # 随机使用一张地板图像
        self.image=random.choice(self.game.image_wall_dict.get(self.type))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)  # 设置图像在屏幕上的位置
        # 设置地板上的植被
        self.set_grass()
        # 设置地板上的金币对象
        self.set_coin()
        # 设置地板上的弹簧对象
        self.set_spring()

    # 设置植被
    def set_grass(self):
        # 随机产生草颗数
        grass_number = random.choices([0, 1, 2, 3], weights=[4, 3, 2, 1], k=1)[0]
        while grass_number > 0:
            if self.type!="stone":
                x = random.randint(int(self.rect.left) + 5, int(self.rect.right) - 5)
                temp=int(self.rect.top)
                y = random.randint(temp+1,temp+5)
                Plant(self.game, x, y,self.type)
            grass_number -= 1

    # 设置金币对象
    def set_coin(self):
        # 随机产生金币数
        coin_number=random.choices([0,1,2],weights=[3,2,1],k=1)[0]
        while coin_number>0:
            x = random.randint(int(self.rect.left) + 5, int(self.rect.right) - 5)
            Coin(self.game, x, self.rect.top)
            coin_number-=1

    # 设置弹簧对象
    def set_spring(self):
        if random.randint(0,100)<20:
            x = random.randint(int(self.rect.left) + 7, int(self.rect.right) - 7)
            Spring(self.game,x,self.rect.top+2)


# 植被类
class Plant(pg.sprite.Sprite):
    # 初始化植被对象数据
    def __init__(self,game,x,y,wall_type):
        self.game = game
        # 指定植被类的绘制优先级
        self._layer=self.game.run_config.grass_layer
        # 将该对象添加到指定的精灵组中
        self.groups=(self.game.all_sprite,self.game.plants)
        super().__init__(self.groups)
        # 随机获取对应地板下能使用的植被类型
        self.type=random.choice(self.game.run_config.plant_type_dict.get(wall_type))
        # 随机使用植被类型对应图片
        self.image=random.choice(self.game.image_plant_dict.get(self.type))
        self.rect=self.image.get_rect()
        # 设置图像在屏幕上的位置
        self.rect.midbottom=(x,y)


# 硬币类
class Coin(pg.sprite.Sprite):
    # 初始化硬币对象数据
    def __init__(self,game,x,y):
        self.game=game
        # 指定硬币类的绘制优先级
        self._layer=self.game.run_config.coin_layer
        # 将硬币对象添加到精灵组
        self.groups=(self.game.all_sprite,self.game.coins)
        super().__init__(self.groups)
        # 随机指定产生硬币类型
        self.type=random.choices(self.game.run_config.coin_type_tuple,weights=[3,2,1],k=1)[0]
        # 记录使用的图像列表中对应图像的索引值
        self.current = 0
        # 设置图像
        self.image=self.game.image_coin_dict.get(self.type)[self.current]
        # 设置图像的位置
        self.rect=self.image.get_rect()
        self.rect.midbottom=(x,y)
        # 获取该硬币对象创建时的时间(从pygame启动开始计时)
        self.last_update=pg.time.get_ticks()
        # 存放硬币对象旋转一周用的图像数
        self.length=len(self.game.image_coin_dict.get(self.type))

    # 更新硬币数据
    def update(self):
        self.image_replace()  # 替换金币使用的图像

    # 替换硬币图像
    def image_replace(self):
        now=pg.time.get_ticks()  # 获取当前的时间
        # 满足指定的时间差后使用下一张硬币图像
        if now-self.last_update>100:
            self.last_update=now
            self.current=(self.current+1)%self.length
            temp=self.rect.midbottom
            # 如果使用的是最后一张图,则取余使用开头的图像
            self.image=self.game.image_coin_dict.get(self.type)[self.current]
            # 设置将原图像在屏幕上的位置设置给新图像
            self.rect=self.image.get_rect()
            self.rect.midbottom=temp


# 弹簧类
class Spring(pg.sprite.Sprite):
    # 初始化弹簧对象数据
    def __init__(self,game,x,y):
        self.game=game
        self._layer=self.game.run_config.spring_layer
        self.groups=(self.game.all_sprite,self.game.springs)
        super().__init__(self.groups)
        self.state="normal"
        self.last_update=pg.time.get_ticks()
        self.image=self.game.image_spring_dict.get(self.state)
        self.rect=self.image.get_rect()
        self.rect.midbottom=(x,y)

    # 更新弹簧对象数据
    def update(self):
        # 替换图片
        self.image_replace()
        # 恢复弹簧状态
        self.state_reset()

    # 替换图片
    def image_replace(self):
        temp_rect=self.rect
        self.image=self.game.image_spring_dict.get(self.state)
        self.rect=self.image.get_rect()
        self.rect.midbottom=temp_rect.midbottom

    # 恢复弹簧状态
    def state_reset(self):
        now=pg.time.get_ticks()
        if now-self.last_update>300:
            self.last_update=now
            self.state="normal"