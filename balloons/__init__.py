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
    def __init__(self, name, waypoints):
        data = BALLOON_DATA[name]
        super().__init__(
            color_name=name,
            hp=data["hp"],
            speed=data["speed"],
            damage=data["damage"],
            reward=data["reward"],
            waypoints=waypoints
        )
        self.child_type = CHILD_MAP.get(name)

def balloon_factory(name, waypoints):
    name = name.lower()
    if name not in BALLOON_DATA:
        name = "red"
    return ConcreteBalloon(name, waypoints)