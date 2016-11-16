import pygame, math, pymunk
from pymunk.vec2d import Vec2d
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
    # Tick all the players
    keys = self.players.keys()
    for id in keys:
      if not self.players.get(id): continue
      self.players[id].tick(deltaTime)

    # Step the physics space
    self.space.step(deltaTime)

  def render(self, screen):
    # Render the background and middleground
    if self.mapBackground:
      screen.blit(self.mapBackground, (0, 0, WIDTH, HEIGHT))
    if self.mapMiddleground:
      screen.blit(self.mapMiddleground, (0, 0, WIDTH, HEIGHT))

    # Render all the players
    keys = self.players.keys()
    for id in keys:
      if not self.players.get(id): continue
      self.players[id].render(screen)

    #for line in self.staticLines:
    #  pygame.draw.line(screen, (255, 0, 0), line[0], line[1], 5)

    #for line in self.platformLines:
    #  pygame.draw.line(screen, (255, 255, 0), line[0], line[1], 5)



    # Render the foreground
    if self.mapForeground:
      screen.blit(self.mapForeground, (0, 0, WIDTH, HEIGHT))

  # Load in map information from the json blob
  def loadMap(self, blob):
    self.mapForeground = load("map/" + blob["foreground"])
    self.mapMiddleground = load("map/" + blob["middleground"])
    self.mapBackground = load("map/" + blob["background"])

    self.staticLines = self.statics = blob["segments_static"]
    self.platformLines = self.platforms = blob["segments_platform"]
    self.spawnpoints = blob["spawnpoints"]
    self.hasInit = False

  def createSegment(self, seg, isPlatform):
    seg = [(seg[0][0], HEIGHT - seg[0][1]),
           (seg[1][0], HEIGHT - seg[1][1])]

    segment = pymunk.Segment(self.space.static_body, seg[0], seg[1], 5)
    segment.friction = 1.
    print("Creating " + str(isPlatform and "platform" or "static") + " at " + str(seg))
    if isPlatform:
      segment.collision_type = 2
      segment.filter = pymunk.ShapeFilter(categories=0b1000)
    else:
      segment.group = 1
    return segment

  def start(self):
    # Don't let the fight menu init itself twice on the same map
    if self.hasInit:
      return

    # Create a physics space for the map
    self.space = pymunk.Space() 
    self.space.gravity = 0,GRAVITY
    self.space.add_collision_handler(1,2).begin = passthrough_handler

    # Create segments from the json blob
    self.statics = map(
      lambda seg: self.createSegment(seg, False),
      self.statics
    )
    self.platforms = map(
      lambda seg: self.createSegment(seg, True),
      self.platforms
    )

    # Add the segments to the world
    self.space.add(self.statics)
    self.space.add(self.platforms)

    # Create each player physics object at the spawnpoints
    keys = self.players.keys()
    for id in keys:
      if not self.players.get(id): continue
      self.players[id].createBody(self.space, sample(self.spawnpoints))

    self.hasInit = True

  def keyDown(self, key):
    pass
  
  def keyUp(self, key):
    pass

# For platforms that let players jump through them
def passthrough_handler(arbiter, space, data):
  return arbiter.shapes[0].body.velocity.y < 0