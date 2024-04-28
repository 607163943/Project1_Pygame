# python第三方模块
import pygame as pg
# python自定义模块
import window


# 程序入口
def main():
    # 初始化pygame模块
    pg.init()
    pg.mixer.init()
    window_example=window.Window()
    window_example.show()


if __name__=="__main__":
    main()