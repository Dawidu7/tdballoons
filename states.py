from abc import ABC, abstractmethod

class GameState(ABC):
  @abstractmethod
  def handle_event(self, event):
    pass

  @abstractmethod
  def update(self, dt):
    pass

  @abstractmethod
  def draw(self):
    pass