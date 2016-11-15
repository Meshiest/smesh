import pygame
from constants import *

class GameMenu:
  # Player array stored locally
  players = []

  def __init__(self, players):
    self.players = players

  # Called every frame, but before rendering
  def tick(self, deltaTime):
    pass

  # Called to render the current frame
  def render(self, screen):
    pass

  # Called when a key is pressed, works only when menu is visible
  def keyDown(self, key):
    pass
  
  # Called when a key is released, works only when menu is visible
  def keyUp(self, key):
    pass
