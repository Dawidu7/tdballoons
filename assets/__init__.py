import pygame
import os

BASE = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE, "images")
SOUND_DIR = os.path.join(BASE, "sounds")

IMAGES = {}
SOUNDS = {}

def load_assets():
    for root, _, files in os.walk(IMAGE_DIR):
        for filename in files:
            if filename.lower().endswith(".png"):
                path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, IMAGE_DIR)
                name_body = os.path.splitext(filename)[0].lower()
                key = name_body if relative_path == "." else f"{relative_path.replace(os.sep, '.')}.{name_body}"
                IMAGES[key.lower()] = path

    if os.path.exists(SOUND_DIR):
        for root, _, files in os.walk(SOUND_DIR):
            for filename in files:
                if filename.lower().endswith((".wav", ".mp3")):
                    path = os.path.join(root, filename)
                    relative_path = os.path.relpath(root, SOUND_DIR)
                    name_body = os.path.splitext(filename)[0].lower()
                    key = name_body if relative_path == "." else f"{relative_path.replace(os.sep, '.')}.{name_body}"
                    SOUNDS[key.lower()] = path

if not pygame.mixer.get_init():
    pygame.mixer.init()
load_assets()

class Assets:
    _images = {}
    _sounds = {}

    @classmethod
    def image(cls, key, size=None):
        key = key.lower()
        if key not in IMAGES:
            print(f"ERROR: Image key '{key}' not found!")
            return None
        
        cache_key = (key, size)
        if cache_key in cls._images:
            return cls._images[cache_key]
        
        try:
            img = pygame.image.load(IMAGES[key]).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            cls._images[cache_key] = img
            return img
        except pygame.error as e:
            print(f"ERROR: Failed to load image: {IMAGES[key]}\n{e}")
            return None

    @classmethod
    def sound(cls, key, volume=1.0):
        key = key.lower()
        if key not in SOUNDS:
            print(f"ERROR: Sound key '{key}' not found!")
            return None

        if key not in cls._sounds:
            try:
                cls._sounds[key] = pygame.mixer.Sound(SOUNDS[key])
            except pygame.error as e:
                print(f"ERROR: Failed to load sound: {SOUNDS[key]}\n{e}")
                return None
        
        sound_obj = cls._sounds[key]
        sound_obj.set_volume(volume)
        return sound_obj