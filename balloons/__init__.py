from .base import Balloon

BALLOON_DATA = {
    "purple": {"hp": 10, "speed": 1.5, "damage": 5, "reward": 20},
    "pink":   {"hp": 5,  "speed": 3.5, "damage": 2, "reward": 15},
    "cyan":   {"hp": 4,  "speed": 3.0, "damage": 1, "reward": 12},
    "yellow": {"hp": 3,  "speed": 2.5, "damage": 1, "reward": 10},
    "orange": {"hp": 2,  "speed": 2.0, "damage": 1, "reward": 5},
    "green":  {"hp": 2,  "speed": 1.8, "damage": 1, "reward": 4},
    "red":    {"hp": 1,  "speed": 1.5, "damage": 1, "reward": 2}
}

CHILD_MAP = {
    "purple": "pink",
    "pink":   "cyan",
    "cyan":   "yellow",
    "yellow": "orange",
    "orange": "green",
    "green":  "red",
    "red":    None
}

class ConcreteBalloon(Balloon):
    def __init__(self, name, waypoints, hp_m, speed_m, reward_m):
        data = BALLOON_DATA[name]
        
        final_hp = max(1, int(data["hp"] * hp_m))
        final_speed = data["speed"] * speed_m
        final_reward = int(data["reward"] * reward_m)

        super().__init__(
            color_name=name,
            hp=final_hp,
            speed=final_speed,
            damage=data["damage"],
            reward=final_reward,
            waypoints=waypoints
        )
        self.child_type = CHILD_MAP.get(name)

def balloon_factory(name, waypoints, difficulty="Normal"):
    name = name.lower()
    if name not in BALLOON_DATA:
        name = "red"
    
    diff_key = str(difficulty).strip().capitalize()

    diff_settings = {
        "Easy":   (0.7, 0.8, 1.3),
        "Normal": (1.0, 1.0, 1.0),
        "Hard":   (1.6, 1.4, 0.6)
    }
    
    hp_m, speed_m, reward_m = diff_settings.get(diff_key, (1.0, 1.0, 1.0))
    
    return ConcreteBalloon(name, waypoints, hp_m, speed_m, reward_m)