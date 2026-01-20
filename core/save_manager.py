import json
import os
from settings import SAVE_FILE

class SaveManager:
  @staticmethod
  def save_game(game):
    data = {
      "difficulty": game.difficulty,
      "money": game.money,
      "hp": game.hp,
      "wave": game.wave_manager.wave,
      "map_seed": game.map.seed, 
      "map_straightness": game.map.straightness,
      "towers": []
    }

    for tower in game.towers:
      data["towers"].append({
        "type": tower.name,
        "x": tower.rect.centerx,
        "y": tower.rect.centery,
      })

    try:
      with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
        return True
    except Exception as e:
      return False

  @staticmethod
  def load_game():
    if not os.path.exists(SAVE_FILE):
      return None
    
    try:
      with open(SAVE_FILE, "r") as f:
        return json.load(f)
    except Exception as e:
      print(f"Error loading save file: {e}")
      return None
    
  @staticmethod
  def has_save():
    return os.path.exists(SAVE_FILE)