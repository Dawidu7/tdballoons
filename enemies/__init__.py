from .base import Balloon
from settings import DIFFICULTIES

class RedBalloon(Balloon):
    def __init__(self, path, mults):
        super().__init__(hp=1, speed=2, damage=1, reward=2, path=path, multipliers=mults, child_type=None)
        self.image.fill((255, 0, 0))

class BlueBalloon(Balloon):
    def __init__(self, path, mults):
        super().__init__(hp=2, speed=3, damage=1, reward=5, path=path, multipliers=mults, child_type="red")
        self.image.fill((0, 0, 255))

class GreenBalloon(Balloon):
    def __init__(self, path, mults):
        super().__init__(hp=3, speed=4, damage=1, reward=8, path=path, multipliers=mults, child_type="blue")
        self.image.fill((0, 255, 0))

class YellowBalloon(Balloon):
    def __init__(self, path, mults):
        super().__init__(hp=4, speed=5, damage=2, reward=12, path=path, multipliers=mults, child_type="green")
        self.image.fill((255, 255, 0))

class PinkBalloon(Balloon):
    def __init__(self, path, mults):
        super().__init__(hp=1, speed=7, damage=1, reward=15, path=path, multipliers=mults, child_type="yellow")
        self.image.fill((255, 192, 203))

class BlackBalloon(Balloon):
    def __init__(self, path, mults):
        super().__init__(hp=10, speed=1.5, damage=5, reward=25, path=path, multipliers=mults, child_type="pink")
        self.image.fill((30, 30, 30))

class LeadBalloon(Balloon):
    def __init__(self, path, mults):
        super().__init__(hp=25, speed=1, damage=10, reward=50, path=path, multipliers=mults, child_type="black")
        self.image.fill((120, 120, 120))

class RainbowBalloon(Balloon):
    def __init__(self, path, mults):
        super().__init__(hp=50, speed=2, damage=20, reward=100, path=path, multipliers=mults, child_type="lead")
        self.image.fill((255, 0, 255))

def balloon_factory(name, path, difficulty_level="Normal"):

    mults = DIFFICULTIES.get(difficulty_level, {"hp_mult": 1.0, "speed_mult": 1.0, "reward_mult": 1.0})
    
    balloon_types = {
        "red": RedBalloon,
        "blue": BlueBalloon,
        "green": GreenBalloon,
        "yellow": YellowBalloon,
        "pink": PinkBalloon,
        "black": BlackBalloon,
        "lead": LeadBalloon,
        "rainbow": RainbowBalloon
    }
    
    balloon_class = balloon_types.get(name.lower(), RedBalloon)
    return balloon_class(path, mults)