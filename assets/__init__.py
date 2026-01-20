import pygame
import os

BASE = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE, "images")

IMAGES = {}

def load_images():
  for root, _, files in os.walk(IMAGE_DIR):
    for filename in files:
      if filename == ".DS_Store":
        continue
      if not filename.lower().endswith((".png")):
        continue

      path = os.path.join(root, filename)

      relative_path = os.path.relpath(root, IMAGE_DIR)
      name_body = os.path.splitext(filename)[0].lower()

      if relative_path == ".":
        key = name_body
      else:
        clean_folder = relative_path.replace(os.sep, ".").lower()
        key = f"{clean_folder}.{name_body}"

      IMAGES[key] = path

load_images()

class Assets:
  _images = {}

  @classmethod
  def image(cls, key, size=None):
    if key not in IMAGES:
      print(f"ERROR: Image key '{key}' not found!")
      return None
    
    path = IMAGES[key]
    cache_key = (key, size)

    if cache_key in cls._images:
      return cls._images[cache_key]
    
    try:
      img = pygame.image.load(path).convert_alpha()
      if size:
        img = pygame.transform.scale(img, size)
      cls._images[cache_key] = img
      return img
    except pygame.error as e:
      print(f"ERROR: Failed to load image: {path}\n{e}")
      return None