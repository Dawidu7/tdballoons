from .basic import BasicTower

TOWERS = {
  "basic": BasicTower
}

def tower_factory(name, x, y):
    tower = TOWERS.get(name.lower(), BasicTower)
    return tower(x, y)