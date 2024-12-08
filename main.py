import pygame
import sys
# 导入其他模块
from ball import Ball
from button import Button
from game_stats import GameStats
from needle import Needle
from scoreboard import Scoreboard
from settings import Settings

class CoreBall:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏资源"""
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("见缝插针 by Emptope")

        self.screen_rect = self.screen.get_rect()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ball = Ball(self)
        self.needles = pygame.sprite.Group()
        self.play_button = Button(self, "Start")
        
        # 创建一根针并设置其位置为屏幕的 midbottom
        self.initial_needle = Needle(self)
        self.initial_needle.rect.midbottom = self.screen_rect.midbottom
        self.needles.add(self.initial_needle)

        # 标志针是否发射
        self.needle_fired = False

        # 控制帧率
        self.clock = pygame.time.Clock()

        # 音乐
        self._load_music()
        
    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self._update_needles()
                self.ball.update()
            self._update_screen()
            # 设置帧率
            self.clock.tick(240) # FPS
        
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if not self.stats.game_active:
                        self._check_play_button(mouse_x, mouse_y)
                    else:
                        self._fire_needle()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.stats.game_active:
                        self._start_game()
                    else:
                        self._fire_needle()

    def _check_play_button(self, mouse_x, mouse_y):
        """在玩家点击Play按钮时开始新游戏"""
        if self.play_button.rect.collidepoint(mouse_x, mouse_y):
            self._start_game()

    def _start_game(self):
        """开始新游戏"""
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_high_score()
        self._start_music()
        self._set_volume(0.5)
        
        # 重置游戏中的其他元素
        self.needles.empty()
        self.ball = Ball(self)
        
        # 将 initial_needle 添加到 needles 组中
        self.initial_needle = Needle(self)
        self.initial_needle.rect.midbottom = self.screen_rect.midbottom
        self.needles.add(self.initial_needle)
        self.needle_fired = False
    
    def _load_music(self):
        """加载背景音乐"""
        pygame.mixer.music.load("sounds/bgm.mp3")
        
    def _start_music(self):
        """开始播放背景音乐"""
        pygame.mixer.music.play(-1)
        
    def _stop_music(self):
        """停止播放背景音乐"""
        pygame.mixer.music.stop()
        
    def _set_volume(self, volume):
        """设置音量"""
        pygame.mixer.music.set_volume(volume)

    def _fire_needle(self):
        """发射一根针"""
        if not self.needle_fired:
            self.needle_fired = True
            self.initial_needle.fired = True
            self._create_new_needle()

    def _create_new_needle(self):
        """在底部创建一根新的针"""
        self.initial_needle = Needle(self)
        self.initial_needle.rect.midbottom = self.screen_rect.midbottom
        self.needles.add(self.initial_needle)
        self.needle_fired = False

    def _update_needles(self):
        """更新所有针的位置并检查碰撞"""
        self.needles.update()
        for needle in self.needles.copy():
            if needle.rect.bottom <= 0:
                self.needles.remove(needle)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        if self.stats.game_active:
            self.ball.draw_ball()
            for needle in self.needles.sprites():
                needle.blitme()
            self.sb.show_score(self.ball)
        else:
            if self.stats.score > 0:
                self._game_over()
            else:
                self.play_button.draw_button()
                self._draw_start_message()
        pygame.display.flip()

    def _draw_start_message(self):
        """在游戏开始界面上绘制信息"""
        font = pygame.font.Font("Font/SimHei.ttf", 90)
        message = "见缝插针"
        message_image = font.render(message, True, self.settings.black)
        message_rect = message_image.get_rect()
        message_rect.center = self.screen_rect.center
        message_rect.top = self.play_button.rect.bottom - 200
        self.screen.blit(message_image, message_rect)

    def _game_over(self):
        """游戏结束"""
        # 停止播放背景音乐
        self._stop_music()
        
        # 显示游戏结束信息
        font = pygame.font.SysFont(None, 100)
        game_over_image = font.render("Game Over!", True, self.settings.game_over_msg_color, self.settings.bg_color)
        game_over_rect = game_over_image.get_rect()
        game_over_rect.center = self.screen_rect.center
        game_over_rect.top -= 100
        self.screen.blit(game_over_image, game_over_rect)
        
        # 显示最终得分
        score_font = pygame.font.SysFont(None, 60)
        score_image = score_font.render("Score: " + str(self.stats.score), True, self.settings.game_over_msg_color, self.settings.bg_color)
        score_rect = score_image.get_rect()
        score_rect.center = self.screen_rect.center
        score_rect.top = game_over_rect.bottom + 20
        self.screen.blit(score_image, score_rect)

        # 显示提示信息
        info_font = pygame.font.SysFont(None, 48)
        info_image = info_font.render("Press SPACE or Click to Restart", True, self.settings.game_over_msg_color, self.settings.bg_color)
        info_rect = info_image.get_rect()
        info_rect.center = self.screen_rect.center
        info_rect.top = game_over_rect.bottom + 120
        self.screen.blit(info_image, info_rect)

if __name__ == '__main__':
    cb = CoreBall()
    cb.run_game()

