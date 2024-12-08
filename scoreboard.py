import pygame.font

class Scoreboard:
    """计分板类"""
    def __init__(self, core_ball):
        self.screen = core_ball.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = core_ball.stats
        self.settings = core_ball.settings
        self.text_color = self.settings.current_score_color
        self.font = pygame.font.SysFont(None, 48)

    def increase_score(self):
        """增加分数"""
        self.stats.score += 1
        self.stats.check_high_score()
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """将得分转换为渲染的图像"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, None)
        self.score_rect = self.score_image.get_rect()

    def prep_high_score(self):
        """将最高分转换为渲染的图像"""
        high_score_str = str(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.settings.high_score_color, None)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = self.screen_rect.midtop
        self.high_score_rect.top = 20

    def show_score(self, ball):
        """在屏幕上显示当前得分和最高分"""
        self.prep_score()
        self.prep_high_score()
        
        # 在球的中心显示当前得分
        self.score_rect.center = ball.rect.center
        self.screen.blit(self.score_image, self.score_rect)
        
        # 在屏幕右上角显示最高分
        self.screen.blit(self.high_score_image, self.high_score_rect)