import pygame, math, pymunk
from gamemenu import *
from constants import *
from player import *
from font import *
from imagestore import *

class FightMenu(GameMenu):
  players = []

  def __init__(self, players):
    GameMenu.__init__(self, players)
    self.hasInit = False

  def tick(self, deltaTime):
    pass

  def render(self, screen):
    pass

  # Load in map information from the json blob
  def loadMap(self, blob):
    self.mapForeground = load("map/" + blob["foreground"])
    self.mapBackground = load("map/" + blob["background"])
    self.mapMiddleground = load("map/" + blob["middleground"])
    self.segments = blob["segments"]
    self.spawnponts = blob["spawnpoints"]
    self.hasInit = False

  def start(self):
    # Don't let the fight menu init itself twice on the same map
    if self.hasInit:
      return

    # Create a physics space for the map
    self.space = pymunk.Space() 
    self.space.gravity = 0,GRAVITY
    self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
    self.body.position = (0, 0)

    # Create segments from the json blob
    self.segments = map(
      lambda seg: pymunk.Segment(self.body, seg[0], seg[1], 5),
      self.segments
    )

    # Add the segments to the world
    space.add(self.segments)

    # Create each player physics object
    keys = self.players.keys()
    for id in keys:
      if not self.players.get(id): continue
      self.players[id].lobbyPlayer = LobbyPlayer(self.players[id], self.space)

    self.hasInit = True

  def keyDown(self, key):
    pass
  
  def keyUp(self, key):
    pass
