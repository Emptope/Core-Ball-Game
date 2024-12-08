import pygame
from pygame.sprite import Sprite

class Ball(Sprite):
    """球类"""
    def __init__(self, core_ball):
        """初始化球的属性并设置其初始位置"""
        super().__init__()
        self.screen = core_ball.screen
        self.screen_rect = core_ball.screen.get_rect()
        self.settings = core_ball.settings
        
        # 初始化动态设置
        self.settings.initialize_dynamic_settings()
        
        # 设置球的颜色和半径
        self.color = core_ball.settings.ball_color
        self.radius = 120
        
        # 创建一个矩形来表示球的位置
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.rect.center = self.screen_rect.center
        
        # 旋转角度
        self.angle = 0
        self.rotation_speed = self.settings.ball_speed
        self.needles = []

    def update(self):
        """更新球的旋转"""
        self.angle = (self.angle + self.rotation_speed) % 360
        for needle in self.needles:
            needle.update_position(self.rect.center, self.angle)

    def draw_ball(self):
        """在屏幕上绘制球"""
        pygame.draw.circle(self.screen, self.color, self.rect.center, self.radius)
        for needle in self.needles:
            needle.blitme()

    def attach_needle(self, needle):
        """将针附加到球上"""
        needle.attached = True
        needle.initial_angle = self.angle
        self.needles.append(needle)
        self.settings.increase_speed()
        self.rotation_speed = self.settings.ball_speed