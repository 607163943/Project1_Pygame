# python第三方模块
import pygame as pg
# python内置模块
import random
# python自定义模块
from config import GameConfig


# 玩家类
class Player(pg.sprite.Sprite):
    # 初始化玩家实列
    def __init__(self,game,x,y):
        self.game=game
        # 添加到精灵组
        self.groups=self.game.all_sprite
        super().__init__(self.groups)
        # 创建玩家图像填充颜色
        self.image=self.game.image_dict.get("player")
        self.image.set_colorkey(GameConfig.BLACK)
        # 创建速度,位置向量并指定玩家在屏幕的初始位置
        self.rect=self.image.get_rect()
        self.pos=pg.math.Vector2(x,y)
        self.vel=pg.math.Vector2(0,0)
        self.rect.midbottom=self.pos
        # 指定玩家的碰撞半径
        self.radius = self.rect.width*0.3
        # 获取创建玩家时的时间
        self.last_shoot_update=pg.time.get_ticks()
        # 玩家生命
        self.life=100
        # 玩家火力等级
        self.level=1
        # 玩家护盾值
        self.shield=0
        # 玩家有盾时使用的护盾图像类型
        self.shield_type="low"
        # 是否有盾
        self.have_shield=False
        # 是否需要使用复活次数
        self.once_again=False
        # 玩家再次复活时的时间
        self.once_again_time=pg.time.get_ticks()
        # 玩家生命次数
        self.life_number=3

    # 更新数据
    def update(self):
        # 移动函数
        self.move()
        # 开火函数
        self.shoot()
        # 判断是否碰到敌人
        self.mob_hit()
        # 判断是否碰到道具
        self.power_hit()
        # 判断是否有盾
        self.is_shield()
        # 替换护盾图像
        self.shield_replace()
        # 判断是否消耗生命条数
        self.is_once_again()

    # 玩家移动
    def move(self):
        # 设置初始加速度
        self.vel=pg.math.Vector2(0,0)
        # 获取玩家按键事件
        key=pg.key.get_pressed()
        # 根据玩家按键移动飞船
        if key[pg.K_RIGHT]:
            self.vel.x=GameConfig.PLAYER_VEL_X
        if key[pg.K_LEFT]:
            self.vel.x=-GameConfig.PLAYER_VEL_X
        self.pos+=self.vel
        # 防止飞船穿过屏幕边界
        if self.pos.x<0+self.rect.width/2:
            self.pos.x=0+self.rect.width/2
        elif self.pos.x>GameConfig.WIDTH-self.rect.width/2:
            self.pos.x=GameConfig.WIDTH-self.rect.width/2
        # 将移动后的位置更新到屏幕上的玩家精灵中
        self.rect.midbottom=self.pos

    # 敌人碰撞判定
    def mob_hit(self):
        # 使用圆形碰撞判断玩家是否撞到敌人(圆形碰撞的判断依据是双方的radius属性值)
        hits:list[Mob]=pg.sprite.spritecollide(self,self.game.mobs,False,pg.sprite.collide_circle)
        if hits:
            for i in hits:
                # 更新碰撞敌人的状态(该状态下的敌人会重新在屏幕上方生成位置,实现碰撞后摧毁的效果)
                i.hit_over=True
                # 玩家生命值减去碰撞敌人半径的一半
                self.life-=hits[0].rect.width/2
                # 玩家耗尽生命,重置生命,火力等级,并减去一次生命
                if self.life<0:
                    if self.life_number>1:
                        self.life_number-=1
                        self.life=100
                        self.level=1
                        # 更新玩家复活时的时间
                        self.once_again_time=pg.time.get_ticks()
                        # 指定玩家为复活状态
                        self.once_again=True
                    else:
                        # 玩家耗尽生命数,做游戏结束处理
                        self.life=0
                        self.game.playing=False
                    break

    # 道具碰撞判定
    def power_hit(self):
        # 使用圆形碰撞判断上方是否装上
        hits=pg.sprite.spritecollide(self,self.game.powers,True,pg.sprite.collide_circle)
        if hits:
            # 根据碰到的道具类型获得对应增益
            for i in hits:
                # 在火力等级小于3时提升火力等级
                if i.type=="shoot_up":
                    if self.level<3:
                        self.level+=1
                    else:
                        self.level=3
                # 在生命小于100时,补充生命值
                elif i.type=="help":
                    if self.life<100:
                        self.life+=20
                    if self.life>100:
                        self.life=100
                # 在护盾值小于100时补充护盾值
                elif i.type=="shield":
                    if self.shield<100:
                        self.shield+=20
                    if self.shield>100:
                        self.shield=100

    # 开火函数
    def shoot(self):
        # 获取当前时间
        now=pg.time.get_ticks()
        # 判断是否满足开火间隔
        if now-self.last_shoot_update>300:
            # 更新上一次开火时间
            self.last_shoot_update=now
            # 根据火力等级发射对应子弹
            if self.level==1:
                Bullet(self.game, self.rect.centerx, self.rect.y)
            elif self.level==2:
                Bullet(self.game, self.rect.left + 12, self.rect.y + 10)
                Bullet(self.game, self.rect.right - 12, self.rect.y + 10)
            else:
                Bullet(self.game,self.rect.left+5,self.rect.y+15)
                Bullet(self.game,self.rect.right-5,self.rect.y+15)
                Bullet(self.game,self.rect.centerx,self.rect.y)

    # 判断是否有盾
    def is_shield(self):
        if self.shield>0 and not self.have_shield:
            self.temp_shield=Shield(self.game,self.pos.x,self.pos.y,self.shield_type)
            self.have_shield=True

    # 刚复活时处理函数
    def is_once_again(self):
        # 判断是否刚复活
        if self.once_again:
            # 获取当前时间
            now=pg.time.get_ticks()
            # 刚复活时玩家不会出现在屏幕中,过时后才会出现在屏幕上(防止玩家刚复活就撞上敌人)
            if now-self.once_again_time>3000:
                self.pos=pg.math.Vector2(GameConfig.WIDTH/2,GameConfig.HEIGHT)
                # 更新复活状态
                self.once_again=False
            else:
                self.pos=pg.math.Vector2(GameConfig.WIDTH/2,-300)

    # 替换护盾图像
    def shield_replace(self):
        # 根据玩家护盾情况替换护盾图像
        if self.shield<=40:
            self.shield_type="low"
        else:
            self.shield_type="normal"


# 子弹类
class Bullet(pg.sprite.Sprite):

    # 初始化子弹实列
    def __init__(self,game,x,y):
        self.game=game
        # 添加到精灵组
        self.groups=(self.game.all_sprite,self.game.bullets)
        super().__init__(self.groups)
        # 设置子弹图像并指定子弹的速度,位置向量
        self.image=self.game.image_dict.get("bullet")
        self.rect=self.image.get_rect()
        self.pos=pg.math.Vector2(x,y)
        self.vel=pg.math.Vector2(0,GameConfig.BULLET_VEL_Y)
        # 同步位置数据到屏幕上的图像位置
        self.rect.midbottom=self.pos

    # 更新子弹数据
    def update(self):
        # 更新子弹的位置向量并同步到屏幕上的图像上
        self.pos+=self.vel
        self.rect.midbottom=self.pos
class Shield(pg.sprite.Sprite):

    # 初始化护盾实列
    def __init__(self,game,x,y,type):
        self.game=game
        # 将添加到精灵组
        self.groups=self.game.all_sprite
        super().__init__(self.groups)
        # 护盾类型
        self.type=type
        # 设置护盾图像,位置向量
        self.image=self.game.image_dict.get("shield")[self.type]
        self.image.set_colorkey(GameConfig.BLACK)
        self.rect=self.image.get_rect()
        self.pos=pg.math.Vector2(x,y)
        # 同步位置数据到屏幕上的图像中
        self.rect.midbottom=self.pos
        # 指定碰撞半径
        self.radius=40

    # 更新数据
    def update(self):
        # 同步护盾位置到玩家上
        self.shield_move(self.game.player.pos.x,self.game.player.pos.y)
        # 判断是否碰撞敌人
        self.mob_hit()
        # 判断护盾是否消失
        self.is_over()

    # 移动护盾
    def shield_move(self,x,y):
        # 根据玩家护盾值情况获得护盾图像
        self.type=self.game.player.shield_type
        # 根据护盾类型更新使用的图像
        self.image = self.game.image_dict.get("shield")[self.type]
        self.image.set_colorkey(GameConfig.BLACK)
        self.rect=self.image.get_rect()
        self.pos=pg.math.Vector2(x,y)
        # 将替换前的图像位置设置给替换后的图像(保证图像替换不会使屏幕上的图像位置变动)
        self.rect.midbottom=self.pos

    # 判断护盾是否消失
    def is_over(self):
        # 如果玩家护盾小于0,存在的护盾对象去除
        if self.game.player.shield<=0:
            self.game.player.shield=0
            self.game.player.have_shield=False
            self.kill()

    # 敌人碰撞判定
    def mob_hit(self):
        # 使用圆形碰撞判断是否碰到敌人
        hits:list[Mob]=pg.sprite.spritecollide(self,self.game.mobs,False,pg.sprite.collide_circle)
        if hits:
            for i in hits:
                # 更新敌人状态
                i.hit_over=True
                # 根据碰到的敌人半径去减护盾值
                self.game.player.shield-=i.rect.width/2


# 道具类
class Power(pg.sprite.Sprite):
    # 初始化道具实列
    def __init__(self,game,x,y):
        self.game=game
        # 概率性选取道具类型
        temp_tuple=("shoot_up","help","shield")
        self.type=random.choice(temp_tuple)
        # 将该对象添加到精灵组中
        self.groups=(self.game.all_sprite,self.game.powers)
        super().__init__(self.groups)
        # 设置图像并指定位置,速度向量
        self.image=self.game.image_dict.get("power")[self.type]
        self.image.set_colorkey(GameConfig.BLACK)
        self.rect=self.image.get_rect()
        self.last_update=pg.time.get_ticks()
        self.pos=pg.math.Vector2(x,y)
        self.vel=pg.math.Vector2(random.randint(2,5),random.randint(2,5))
        # 更新位置数据到在屏幕上的图像
        self.rect.center=self.pos

    # 更新函数
    def update(self):
        self.move()  # 移动道具

    # 移动函数
    def move(self):
        # 根据道具位置改变对应的速度方向
        if self.wall_hit_x():
            self.vel.x=-self.vel.x
        if self.wall_hit_y():
            self.vel.y=-self.vel.y
        # 更新位置数据到屏幕上的图像
        self.pos+=self.vel
        self.rect.center=self.pos
        # 判断是否清除该道具
        if self.is_over():
            self.kill()

    # 水平边界撞判断
    def wall_hit_x(self):
        if self.rect.centerx>GameConfig.WIDTH or self.rect.centerx<0:
            return True
        return False

    # 竖直边界撞判断
    def wall_hit_y(self):
        if self.rect.centery>GameConfig.HEIGHT:
            return True
        elif self.rect.centery<0 and self.vel.y<0:
            return True
        return False

    # 判断是否消除道具
    def is_over(self):
        now=pg.time.get_ticks()
        if now-self.last_update>GameConfig.POWER_LIFE_TIME:
            return True
        return False


# 敌人类
class Mob(pg.sprite.Sprite):
    # 初始化敌人实列
    def __init__(self,game,x,y):
        self.game=game
        # 将敌人对象添加到精灵组中
        self.groups=(self.game.all_sprite,self.game.mobs)
        super().__init__(self.groups)
        # 存放敌人类型
        self.type=random.choice(GameConfig.MOB_TYPE_TUPLE)
        # 存放敌人生命上限
        self.max_life=GameConfig.MOB_LIFE_DICT.get(self.type)
        # 记录敌人当前生命值
        self.life=self.max_life
        # 存放初始图像(旋转图像用)
        self.start_image=random.choice(self.game.mob_dict.get(self.type))
        # 设置图像,位置,速度向量
        self.image=self.start_image
        self.image.set_colorkey(GameConfig.BLACK)
        self.rect=self.image.get_rect()
        self.vel=pg.math.Vector2(random.randint(-6,6),random.randint(1,6))
        self.pos=pg.math.Vector2(x,y)
        # 设置图像在屏幕上的位置
        self.rect.center=self.pos
        # 设置旋转角,旋转角度
        self.rot = 0
        self.rot_vel = random.randint(-6, 6)
        # 设置碰撞半径
        self.radius=self.rect.width*0.4
        # 判断是否碰到飞船,子弹,护盾
        self.hit_over=False

    # 更新数据
    def update(self):
        # 移动
        self.move()
        # 判断敌人是否应该从屏幕中清除
        if self.is_over() or self.hit_over:
            self.once_show()
        # 旋转图像
        self.image_rot()

    #  移动敌人
    def move(self):
        # 更新位置数据
        self.pos+=self.vel
        # 同步位置数据到屏幕中的图像
        self.rect.center=self.pos

    # 旋转图像
    def image_rot(self):
        # 根据旋转角移动图像
        self.rot=(self.rot+self.rot_vel)%360
        # 由于每次旋转都会损坏图像的像素因此每次都旋转初始图像,再将旋转后的图像替换原图像
        self.image=pg.transform.rotate(self.start_image,self.rot).convert()
        self.image.set_colorkey(GameConfig.BLACK)
        # 将原图像的位置数据同步到新图像中
        self.rect=self.image.get_rect()
        self.rect.center=self.pos

    # 判断敌人是否飞出屏幕边界(屏幕上方不判断)
    def is_over(self):
        if self.rect.x<-100 or self.rect.x>GameConfig.WIDTH+100:
            return True
        elif self.rect.y>GameConfig.HEIGHT+100:
            return True
        else:
            return False

    # 重新设置敌人的出现位置
    def once_show(self):
        # 重新指定敌人的速度,旋转角,旋转速度
        self.vel=pg.math.Vector2(random.randint(-6,6),random.randint(1,6))
        self.rot=0
        self.rot_vel = random.randint(-6, 6)
        # 指定敌人重新出现的位置
        x=random.randint(-50,GameConfig.WIDTH+50)
        y=random.randint(-100,-50)
        # 重新设置敌人的类型,生命上限,当前生命值,图像,位置向量,碰撞半径
        self.type=random.choice(GameConfig.MOB_TYPE_TUPLE)
        self.max_life = GameConfig.MOB_LIFE_DICT.get(self.type)
        self.life = self.max_life
        self.start_image = random.choice(self.game.mob_dict.get(self.type))
        self.image=self.start_image
        self.image.set_colorkey(GameConfig.BLACK)
        self.rect=self.image.get_rect()
        self.radius = self.rect.width*0.4
        self.pos = pg.math.Vector2(x, y)
        # 同步位置数据到屏幕的图像上
        self.rect.center=self.pos
        # 重置敌人的碰撞状态
        self.hit_over=False
