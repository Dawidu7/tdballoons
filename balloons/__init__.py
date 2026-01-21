from dataclasses import dataclass
from typing import Optional
from .base import Balloon

@dataclass(frozen=True)
class BalloonConfig:
    name: str
    hp: int
    speed: float
    damage: int
    reward: int
    child_type: Optional[str] = None
    child_count: int = 0

BALLOON_DATA = {
    "purple": BalloonConfig("purple", 10, 1.5, 5, 20, "pink", 2),
    "pink":   BalloonConfig("pink", 5, 3.5, 2, 15, "cyan", 2),
    "cyan":   BalloonConfig("cyan", 4, 3.0, 1, 12, "yellow", 2),
    "yellow": BalloonConfig("yellow", 3, 2.5, 1, 10, "orange", 2),
    "orange": BalloonConfig("orange", 2, 2.0, 1, 5, "green", 2),
    "green":  BalloonConfig("green", 2, 1.8, 1, 4, "red", 2),
    "red":    BalloonConfig("red", 1, 1.5, 1, 2),
}

def balloon_factory(name, waypoints, current_waypoint=0, current_pos=None):
    name = name.lower()
    if name not in BALLOON_DATA:
        name = "red"

    cfg = BALLOON_DATA[name]
    
    balloon = Balloon(
        color_name=name,
        hp=cfg.hp,
        speed=cfg.speed,
        damage=cfg.damage,
        reward=cfg.reward,
        waypoints=waypoints,
        current_waypoint=current_waypoint,
        current_pos=current_pos
    )
    balloon.child_type = cfg.child_type
    balloon.child_count = cfg.child_count

    return balloon