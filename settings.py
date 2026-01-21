FPS = 60
GRID_SIZE = 10

SCREEN_HEIGHT = 800 
MAP_SIZE = SCREEN_HEIGHT

SIDEBAR_WIDTH = 200 
SCREEN_WIDTH = MAP_SIZE + SIDEBAR_WIDTH

WIDTH = SCREEN_WIDTH
HEIGHT = SCREEN_HEIGHT

TILE_SIZE = MAP_SIZE // GRID_SIZE
TILE_GRASS = 0
TILE_PATH = 1
TILE_START = 2
TILE_END = 3

MENU_BUTTON_COLOR = (0, 100, 0)
MENU_BUTTON_HOVER_COLOR = (0, 180, 0)

BALLOON_SIZE = (30, 40)

SAVE_FILE = "save.json"

DIFFICULTIES = {
  "easy": {
    "start_money": 150,
    "start_hp": 150,
    "map_straightness": 0.05,
    "enemy_hp_mult": 0.7,
    "enemy_speed_mult": 0.8,
    "reward_mult": 1.2,
    "wave_count_mult": 0.7,
    "wave_interval_mult": 1.5,
    "child_spawn_mult": 0.8
  },
  "normal": {
    "start_money": 100,
    "start_hp": 100,
    "map_straightness": 0.4,
    "enemy_hp_mult": 1.0,
    "enemy_speed_mult": 1.0,
    "reward_mult": 1.0,
    "wave_count_mult": 1.0,
    "wave_interval_mult": 1.0,
    "child_spawn_mult": 1.0
  },
  "hard": {
    "start_money": 75,
    "start_hp": 50,
    "map_straightness": 0.8,
    "enemy_hp_mult": 0.7,
    "enemy_speed_mult": 0.8,
    "reward_mult": 1.2,
    "wave_count_mult": 1.5,
    "wave_interval_mult": 0.7,
    "child_spawn_mult": 1.5
  },
}