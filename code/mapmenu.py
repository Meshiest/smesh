import pygame, math, json, glob, os
from constants import *
from gamemenu  import *
from font import *
from imagestore import *
from audio import *


def loadMap(name):
  return MapPreview(name)

class MapMenu(GameMenu):

  def __init__(self, players):
    GameMenu.__init__(self, players)
    self.selectedMap = 0
    self.maps = map(loadMap, glob.glob("public/res/map/*.json"))

    self.select_image = load("menu/map_select.png")
    self.translateOffset = 0

  def tick(self, deltaTime):
    self.translateOffset -= 10 * deltaTime * self.translateOffset

  def render(self, screen):
    screen.fill((0, 0, 0))

    # Render icons for the maps, 2 to the left, 2 to the right
    numMaps = len(self.maps)
    for i in range(7):
      index = (i + self.selectedMap - 3 + numMaps) % numMaps

      offset = -i + 3 + self.translateOffset
      self.maps[index].render(
        screen,
        (
          WIDTH/2 - (offset) * 270,
          HEIGHT*3/4
        )
      )
      if(abs(offset) > 1): continue
      # Render Preview
      preview = self.maps[index].preview
      screen.blit(
        preview,
        (
          WIDTH/2 - preview.get_width()/2 - offset * WIDTH,
          HEIGHT/4 - preview.get_height()/2, 
          WIDTH,
          HEIGHT/2
        )
      )

      # Render Map Name and overlay
      font = self.maps[self.selectedMap].font

      transOverlay = pygame.Surface((WIDTH, font.get_height() + 10))
      transOverlay.fill((0, 0, 0))
      transOverlay.set_alpha(100)
      screen.blit(transOverlay, (-offset * WIDTH, 0))

      screen.blit(
        font,
        (WIDTH/2 - font.get_width()/2 - offset * WIDTH, 5)
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
      menu_select.play()   

    # Next Map
    if key == pygame.K_d:
      self.selectedMap = (self.selectedMap + 1) % len(self.maps)
      self.translateOffset -= 1
      menu_select.play()   
  
  def keyUp(self, key):
    pass

class MapPreview:
  def __init__(self, filename):
    blob = ""
    # Open file in map directory
    with open(filename) as f:
      content = f.read()
      blob = json.loads(content)
      import os
      blob['filename'] = os.path.basename(os.path.splitext(filename)[0])
      self.blob = blob

    # Only load in the preview and icon data
    self.name = blob["name"]
    self.font = fontBold80.render(blob["name"], 1, (255, 255, 0))
    self.preview = load("map/" + blob["preview"])
    self.icon = load("map/" + blob["icon"])

  # Render the icon for the map
  def render(self, screen, pos):
    width = self.icon.get_width()
    height = self.icon.get_height()
    screen.blit(self.icon, (
      pos[0] - width/2,
      pos[1] - height/2,
      width,
      height
    ))
