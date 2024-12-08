import pygame.font

class Button:
    """按钮类"""
    def __init__(self, core_ball, msg):
        """初始化按钮的属性"""
        self.screen = core_ball.screen
        self.screen_rect = self.screen.get_rect()
        
        self.width, self.height = 150, 70
        self.button_color = core_ball.settings.button_color
        self.text_color = core_ball.settings.text_color
        self.font = pygame.font.SysFont(None, 60)
        
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        self._prep_msg(msg)
        
    def _prep_msg(self, msg):
        """将msg渲染为图像并居中"""
        self.msg_image = self.font.render(msg, True, self.text_color, 
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
