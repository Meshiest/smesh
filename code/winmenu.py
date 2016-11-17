import pygame, math
from constants import *
from gamemenu import *
from font import *

class WinMenu(GameMenu):

  def __init__(self, players):
    GameMenu.__init__(self, players)
    self.winner = None
    self.theta = math.pi/2
    self.winFont = fontBold120.render("Winner", 1, (255, 255, 255))

  def setWinner(self, playerId):
    self.winner = self.players[playerId]
    self.theta = math.pi/2

  # Called every frame, but before rendering
  def tick(self, deltaTime):
    self.theta = math.atan2(
      math.sin(self.theta) + math.sin(self.winner.theta or 0) * 5 * deltaTime,
      math.cos(self.theta) + math.cos(self.winner.theta or 0) * 5 * deltaTime
    )

  # Called to render the current frame
  def render(self, screen):
    minDim = min(WIDTH, HEIGHT)
    newSurface = pygame.transform.rotate(
      pygame.transform.scale(self.winner.face, (minDim, minDim)),
      - self.theta / math.pi * 180 + 90
    )

    width = newSurface.get_width()
    height = newSurface.get_height()
    #pygame.draw.circle(screen, (255, 0, 0), (x, y), self.radius)
    screen.blit(newSurface, (
      WIDTH / 2 - width / 2,
      HEIGHT / 2 - height / 2,
      width,
      height
    ))

    screen.blit(self.winFont, (
      WIDTH/2 - self.winFont.get_width()/2,
      20
    ))