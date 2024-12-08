class Settings:
    """存储游戏的所有设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        self.screen_width = 900
        self.screen_height = 700
        
        # 颜色
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.purple = (255, 0, 255)
        self.cyan = (0, 255, 255)
        self.orange = (255, 165, 0)
        self.gray = (128, 128, 128)
        self.brown = (165, 42, 42)
        self.pink = (255, 192, 203)
        self.sky_blue = (135, 206, 235)
        self.dark_green = (0, 100, 0)
        self.dark_blue = (0, 0, 139)
        self.dark_red = (139, 0, 0)
        self.dark_yellow = (139, 139, 0)
        self.dark_purple = (139, 0, 139)
        self.dark_cyan = (0, 139, 139)
        self.dark_orange = (255, 140, 0)
        self.dark_gray = (169, 169, 169)
        self.dark_brown = (139, 69, 19)
        self.dark_pink = (255, 20, 147)
        self.dark_sky_blue = (0, 206, 209)
        
        # 设置背景颜色
        self.bg_color = self.gray
        
        # 设置 Play 按钮的颜色
        self.button_color = (120, 120, 120)
        
        # 设置 Play 按钮的文本颜色
        self.text_color = self.black

        # 设置球的颜色
        self.ball_color = self.black
        
        # 设置针的颜色
        self.needle_color = self.black
        
        # 设置当前得分的颜色
        self.current_score_color = self.white
        
        # 设置最高分的颜色
        self.high_score_color = self.black
        
        # 设置游戏结束时信息的颜色
        self.game_over_msg_color = self.black
        
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.needle_speed = 2
        self.ball_speed = 0.2
        self.score = 0
        
    def increase_speed(self):
        """提高速度设置"""
        self.needle_speed += 0.1
        self.ball_speed += 0.02
