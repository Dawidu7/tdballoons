WIDTH, HEIGHT = 1280, 720
DIFFICULTIES = {
    "Easy": {"hp_mult": 0.8, "speed_mult": 0.9, "reward_mult": 1.2},
    "Normal": {"hp_mult": 1.0, "speed_mult": 1.0, "reward_mult": 1.0},
    "Hard": {"hp_mult": 1.5, "speed_mult": 1.2, "reward_mult": 0.8}
}
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
FPS = 60

GRID_SIZE = 15
MAP_SIZE = SCREEN_HEIGHT
SIDEBAR_WIDTH = SCREEN_WIDTH - MAP_SIZE

TILE_SIZE = MAP_SIZE // GRID_SIZE
TILE_GRASS = 0
TILE_PATH = 1
TILE_START = 2
TILE_END = 3
