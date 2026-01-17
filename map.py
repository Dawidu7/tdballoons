from settings import GRID_SIZE, TILE_SIZE, TILE_GRASS, TILE_PATH, TILE_START, TILE_END
import random
import pygame

class Map:
  def __init__(self, straightness, seed=None):
    self.grid = []
    self.waypoints = []

    self.straightness = straightness
    self.rng = random.Random(seed)

    self._generate_path()

  def draw(self, surface):
    colors = {
      TILE_GRASS: (34, 139, 34),
      TILE_PATH: (200, 200, 200),
      TILE_START: (0, 200, 255),
      TILE_END: (255, 100, 0),
    }

    for row in range(GRID_SIZE):
      for col in range(GRID_SIZE):
        tile = self.grid[row][col]
        color = colors.get(tile, (0, 0, 0))
        x = col * TILE_SIZE
        y = row * TILE_SIZE
        pygame.draw.rect(surface, color, (x, y, TILE_SIZE, TILE_SIZE))

  def can_place_tower(self, x, y):
    col = x // TILE_SIZE
    row = y // TILE_SIZE
    if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
      return False
    return self.grid[row][col] == TILE_GRASS

  def _generate_path(self):
    self.grid = [[TILE_GRASS for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    self.waypoints = []

    sides = ("W", "E", "N", "S")
    start_side = self.rng.choice(sides)

    u = 0
    v = self.rng.randint(1, GRID_SIZE - 2)
    last_v = 0

    self._place_tile(u, v, start_side, TILE_START)

    while u < GRID_SIZE - 1:
      moves = ["FORWARD"]

      if u > 0:
        if v > 1 and last_v != 1:
          moves.append("LEFT")

        if v < GRID_SIZE - 2 and last_v != -1:
          moves.append("RIGHT")

      moves = [m for m in moves if self._is_valid_step(u, v, m, start_side)]

      if not moves:
        break

      move = self._choose_move(moves)

      match move:
        case "FORWARD":
          u += 1
          last_v = 0
        case "LEFT":
          v -= 1
          last_v = -1
        case "RIGHT":
          v += 1
          last_v = 1

      if u == GRID_SIZE - 1:
        break
      
      self._place_tile(u, v, start_side, TILE_PATH)

    self._place_tile(u, v, start_side, TILE_END)

    start = pygame.Vector2(self.waypoints[0])
    next = pygame.Vector2(self.waypoints[1])
    start_dir = (start - next).normalize()
    self.waypoints.insert(0, tuple(start + start_dir * TILE_START))

    end = pygame.Vector2(self.waypoints[-1])
    prev = pygame.Vector2(self.waypoints[-2])
    end_dir = (end - prev).normalize()
    self.waypoints.append(tuple(end + end_dir * TILE_SIZE))

  def _place_tile(self, u, v, start_side, tile):
    row, col = 0, 0

    match start_side:
      case "W":
        row, col = v, u
      case "E":
        row, col = v, GRID_SIZE - 1 - u
      case "N":
        row, col = u, v
      case "S":
        row, col = u, GRID_SIZE - 1 - v

    self.grid[row][col] = tile

    x = col * TILE_SIZE + TILE_SIZE // 2
    y = row * TILE_SIZE + TILE_SIZE // 2
    self.waypoints.append((x, y))

  def _choose_move(self, moves):
    if len(moves) == 1:
      return moves[0]
    
    if self.rng.random() < self.straightness:
      return "FORWARD"
    
    return self.rng.choice([move for move in moves if move != "FORWARD"])

  def _is_valid_step(self, u, v, move, start_side):
    nu, nv = u, v
    if move == "FORWARD":
      nu += 1
    elif move == "LEFT":
      nv -= 1
    elif move == "RIGHT":
      nv += 1

    if not (0 <= nu < GRID_SIZE and 0 <= nv < GRID_SIZE):
      return False

    row, col = 0, 0
    match start_side:
      case "W":
        row, col = nv, nu
      case "E":
        row, col = nv, GRID_SIZE - 1 - nu
      case "N":
        row, col = nu, nv
      case "S":
        row, col = nu, GRID_SIZE - 1 - nv

    if self.grid[row][col] != TILE_GRASS:
      return False

    def is_path(r, c):
      if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
        return self.grid[r][c] in (TILE_PATH, TILE_START, TILE_END)
      return False

    cur_row, cur_col = 0, 0
    match start_side:
      case "W":
        cur_row, cur_col = v, u
      case "E":
        cur_row, cur_col = v, GRID_SIZE - 1 - u
      case "N":
        cur_row, cur_col = u, v
      case "S":
        cur_row, cur_col = u, GRID_SIZE - 1 - v

    neighbors = [(row-1,col),(row+1,col),(row,col-1),(row,col+1)]
    for r, c in neighbors:
      if is_path(r, c) and not (r == cur_row and c == cur_col):
        return False

    return True