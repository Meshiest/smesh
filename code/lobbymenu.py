import pygame, pymunk, math
from constants import *
from gamemenu import *
from player import *
from font import *

class LobbyMenu(GameMenu):

  def __init__(self, players):
    GameMenu.__init__(self, players)

    # Things to remove so we don't remove during step
    self.removeQueue = []

    # Create a physics space
    self.space = pymunk.Space() 
    self.space.gravity = 0,GRAVITY

    self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
    self.body.position = (0, 0)
    self.nextMenu = ()
    minDim = min(WIDTH, HEIGHT)/2 + 5
    mapVerts = [(- minDim, HEIGHT)]

    numPolys = 20
    for i in range(0, numPolys):
      theta = math.pi * (1.0 * i / numPolys + 1.0)
      mapVerts.append([
        math.cos(theta) * minDim,
        math.sin(theta) * minDim
      ])

    mapVerts.append((minDim, HEIGHT))

    # Generate verticies for the bowl
    self.lines = []
    for i in range(len(mapVerts)):
      vert = mapVerts[i]
      nextVert = mapVerts[(i+1)%len(mapVerts)]
      line = pymunk.Segment(self.body, vert, nextVert, 5)
      line.friction = 0.4
      self.lines.append(line)

    self.space.add(self.lines)
    # Generate physics bodies for each player
    keys = self.players.keys()
    for id in keys:
      if not self.players.get(id): continue
      self.players[id].lobbyPlayer = LobbyPlayer(self.players[id], self.space)

    # Pre-render text that is displayed
    self.nextScreenText = fontBold80.render("Press Space When Ready!", 1, (160, 160, 250))
  
  def queueRemove(self, obj):
    self.removeQueue.append(obj)

  def tick(self, deltaTime):
    # Advance physics
    self.space.step(deltaTime)

    while len(self.removeQueue):
      self.space.remove(self.removeQueue.pop(0))

    keys = self.players.keys()
    for id in keys:
      if not self.players.get(id): continue
      if self.players[id].lobbyPlayer:
        self.players[id].lobbyPlayer.tick(deltaTime)
      else:
        # Generate physics bodies for each player or tick them
        self.players[id].lobbyPlayer = LobbyPlayer(self.players[id], self.space)

  def render(self, screen):
    minDim = min(WIDTH, HEIGHT)/2

    # Draw circle in background
    pygame.draw.circle(screen, (255, 255, 255), (WIDTH/2, HEIGHT/2), minDim)
    pygame.draw.rect(screen, (255, 255, 255), (WIDTH/2-minDim/2, 0, minDim, HEIGHT/2), minDim)

    keys = self.players.keys()
    for id in keys:
      if not self.players.get(id): continue
      pygame.draw.rect(screen, (255, 255, 0), (id * 50 + 50, 50, 20, 20))
      try:
        if self.players[id].lobbyPlayer:
          self.players[id].lobbyPlayer.render(screen)
      except Exception:
        pass

    screen.blit(self.nextScreenText, (WIDTH/2 - self.nextScreenText.get_width()/2, 40))

  def keyDown(self, key):
    pass
  
  def keyUp(self, key):
    pass