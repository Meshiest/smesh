import pygame, math, json
from constants import *
from gamemenu import *
from font import *
from imagestore import *

def loadMap(name):
  return MapPreview(name)

class MapMenu(GameMenu):

  def __init__(self, players):
    GameMenu.__init__(self, players)
    self.selectedMap = 0
    self.maps = map(loadMap, [
      "demo",
      "demo2",
      "demo2",
      "demo",
    ])

    self.select_image = load("menu/map_select.png")
    self.translateOffset = 0

  def tick(self, deltaTime):
    self.translateOffset -= 10 * deltaTime * self.translateOffset

  def render(self, screen):
    screen.fill((0, 0, 0))

    # Render Preview
    preview = self.maps[self.selectedMap].preview
    screen.blit(
      preview,
      (
        WIDTH/2 - preview.get_width()/2,
        HEIGHT/4 - preview.get_height()/2, 
        WIDTH,
        HEIGHT/2
      )
    )

    # Fill the bottom half
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT/2, WIDTH, HEIGHT/2))


    # Render Map Name and overlay
    font = self.maps[self.selectedMap].font

    transOverlay = pygame.Surface((WIDTH, font.get_height() + 10))
    transOverlay.fill((0, 0, 0))
    transOverlay.set_alpha(100)
    screen.blit(transOverlay, (0, 0))

    screen.blit(
      font,
      (WIDTH/2 - font.get_width()/2 - self.translateOffset * 50, 5)
    )

    # Render icons
    numMaps = len(self.maps)
    for i in range(5):
      index = (i + self.selectedMap - 2 + numMaps) % numMaps
      icon = self.maps[index].icon

      if i == 0:
        icon = icon.copy()
        icon.set_alpha(min(abs(self.translateOffset * 255), 255))

      self.maps[index].render(
        screen,
        icon,
        (
          WIDTH/2 - (-i + 2 + self.translateOffset) * 250,
          HEIGHT*3/4
        )
      )

    screen.blit(self.select_image, (
      WIDTH/2 - self.select_image.get_width() / 2,
      HEIGHT*3/4 - self.select_image.get_height() / 2
    ))


  def keyDown(self, key):
    # Prev Map
    if key == pygame.K_a:
      self.selectedMap = (self.selectedMap + len(self.maps) - 1) % len(self.maps)
      self.translateOffset += 1      

    # Next Map
    if key == pygame.K_d:
      self.selectedMap = (self.selectedMap + 1) % len(self.maps)
      self.translateOffset -= 1
  
  def keyUp(self, key):
    pass

class MapPreview:
  def __init__(self, filename):
    blob = ""
    # Open file in map directory
    with open("./public/res/map/" + filename + ".json") as f:
      content = f.read()
      blob = json.loads(content)
      self.blob = blob

    # Only load in the preview and icon data
    self.name = blob["name"]
    self.font = fontBold80.render(blob["name"], 1, (255, 255, 0))
    self.preview = load("map/" + blob["preview"])
    self.icon = load("map/" + blob["icon"])

  def render(self, screen, icon, pos):
    width = icon.get_width()
    height = icon.get_height()
    screen.blit(icon, (
      pos[0] - width/2,
      pos[1] - height/2,
      width,
      height
    ))
