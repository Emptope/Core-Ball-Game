import pygame
from pygame.sprite import Sprite
import math

class Needle(Sprite):
    """针类"""
    def __init__(self, core_ball):
        super().__init__()
        self.screen = core_ball.screen
        self.screen_rect = core_ball.screen.get_rect()
        self.core_ball = core_ball

        # 针的属性
        self.color = core_ball.settings.needle_color
        self.width = 3
        self.height = 80
        self.tail_radius = 6

        # 创建一个矩形来表示针的位置
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = self.screen_rect.midbottom

        # 创建针尾部的小圆形
        self.tail_center = [self.rect.centerx, self.rect.bottom + self.tail_radius]

        # 标记针是否已附加到球上
        self.attached = False
        self.fired = False

        # 初始化角度和速度
        self.initial_angle = 0
        self.rotation_angle = 0
        self.speed = self.core_ball.settings.needle_speed

    def update(self):
        """更新针的位置并检查碰撞"""
        if self.fired and not self.attached:
            self.rect.y -= self.speed  # 使用发射速度
            self.tail_center[1] = self.rect.bottom + self.tail_radius

            # 检查与球的碰撞
            if self.rect.colliderect(self.core_ball.ball.rect):
                self.attached = True
                self.initial_angle = self.core_ball.ball.angle # 记录球的旋转角度
                self.core_ball.ball.attach_needle(self)
                self.core_ball.sb.increase_score()  # 增加分数
            else:
                # 检查与其他针的碰撞
                for needle in self.core_ball.ball.needles:
                    if self.rect.colliderect(needle.rect):
                        self.core_ball.stats.game_active = False
                        break

    def update_position(self, center, angle):
        """更新附加到球上的针的位置"""
        if self.attached:
            total_angle = angle - self.initial_angle + 90 # 使用碰撞时球的旋转角度
            radians = math.radians(total_angle)
            self.rect.centerx = center[0] + (self.core_ball.ball.radius + self.height / 2) * math.cos(radians)
            self.rect.centery = center[1] + (self.core_ball.ball.radius + self.height / 2) * math.sin(radians)

            # 更新针尾部小球的位置
            tail_radians = math.radians(total_angle)
            self.tail_center[0] = center[0] + (self.core_ball.ball.radius + self.height + self.tail_radius) * math.cos(tail_radians)
            self.tail_center[1] = center[1] + (self.core_ball.ball.radius + self.height + self.tail_radius) * math.sin(tail_radians)

            # 更新针的旋转角度
            self.rotation_angle = total_angle + 90

    def blitme(self):
        """在指定位置绘制针"""
        # 创建一个新的表面来绘制旋转后的针
        needle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        needle_surface.fill(self.color)
        rotated_image = pygame.transform.rotate(needle_surface, -self.rotation_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        self.screen.blit(rotated_image, rotated_rect)
        pygame.draw.circle(self.screen, self.color, self.tail_center, self.tail_radius)
