import pygame, math, time, random
from constants import *
from gamemenu import *
from imagestore import *

class TitleMenu(GameMenu):

  def __init__(self, players):
    GameMenu.__init__(self, players)

    self.grass = load("menu/title_grass.png")
    self.sky = load("menu/title_sky.png")
    self.title = load("menu/title.png")
    self.pressSpace = load("menu/title_continue.png")

    self.heads = map(lambda i: {'face': generateFace(i), 'pos': self.genPos()}, range(len(faces)))

  # Generates a position for the head
  def genPos(self): 
    return [
      random.random() * (WIDTH + 100) - 100,
      random.random()
    ]

  def tick(self, deltaTime):
    for i in range(len(self.heads)):
      head = self.heads[i]
      head['pos'][0] += (head['pos'][1] * 500 + 20) * deltaTime
      if head['pos'][0] > WIDTH + 100:
        head['pos'][0] = -100

    self.heads = sorted(self.heads, key=lambda head: head['pos'][1]) 

  def render(self, screen):

    screen.blit(self.sky, (0, 0, WIDTH, HEIGHT))
    pos = - (time.time() * 800 % WIDTH)
    height = math.sin(time.time()) * HEIGHT/8 + HEIGHT/2
    screen.blit(self.grass, (pos + WIDTH, height, WIDTH, HEIGHT))
    screen.blit(self.grass, (pos, height, WIDTH, HEIGHT))

    freq = 180 / math.pi * 12
    for i in range(len(self.heads)):
      head = self.heads[i]
      scale = (head['pos'][1] * 1.1 + 1)
      img = pygame.transform.scale(head['face'], (
        int(head['face'].get_width() * scale),
        int(head['face'].get_height() * scale)
      ))
      img = pygame.transform.rotate(img, -(((time.time() + i) * freq) % 360))
      screen.blit(
        img, (
          head['pos'][0] - img.get_width() / 2,
          head['pos'][1] * HEIGHT / 2 + HEIGHT/10 + height - img.get_height() / 2
        )
      )

    title = pygame.transform.rotate(self.title, math.cos(time.time() * 0.5) * 5)
    screen.blit(title, (
      WIDTH / 2 - title.get_width() / 2,
      HEIGHT / 2 - title.get_height() / 2,
      title.get_width(),
      title.get_height()
    ))
