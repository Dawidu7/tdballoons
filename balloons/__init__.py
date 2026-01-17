from .base import Balloon

BALLOON_DATA = {
    "red":     {"hp": 1,  "speed": 2,   "damage": 1,  "reward": 2,   "color": (255, 0, 0)},
    "blue":    {"hp": 2,  "speed": 3,   "damage": 1,  "reward": 5,   "color": (0, 0, 255)},
    "green":   {"hp": 3,  "speed": 4,   "damage": 1,  "reward": 8,   "color": (0, 255, 0)},
    "yellow":  {"hp": 4,  "speed": 5,   "damage": 2,  "reward": 12,  "color": (255, 255, 0)},
    "pink":    {"hp": 1,  "speed": 7,   "damage": 1,  "reward": 15,  "color": (255, 192, 203)},
    "black":   {"hp": 10, "speed": 1.5, "damage": 5,  "reward": 25,  "color": (30, 30, 30)},
    "lead":    {"hp": 25, "speed": 1,   "damage": 10, "reward": 50,  "color": (120, 120, 120)},
    "rainbow": {"hp": 50, "speed": 2,   "damage": 20, "reward": 100, "color": (255, 0, 255)},
}

def balloon_factory(name, waypoints):
    stats = BALLOON_DATA.get(name.lower(), BALLOON_DATA["red"]).copy()
    
    color = stats.pop("color")
    
    balloon = Balloon(waypoints=waypoints, **stats)
    balloon.image.fill(color)
    
    return balloon