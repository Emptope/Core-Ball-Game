import json

class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self, core_ball):
        """初始化统计信息"""
        self.settings = core_ball.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = self.load_high_score()
        
    def reset_stats(self):
        """初始化在游戏运行过程中变化的统计信息"""
        self.score = 0

    def load_high_score(self):
        """加载保存的最高分"""
        try:
            with open("high_score.json", "r") as f:
                return int(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
        
    def save_high_score(self):
        """保存最高分"""
        with open("high_score.json", "w") as f:
            json.dump(self.high_score, f)
            
    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
