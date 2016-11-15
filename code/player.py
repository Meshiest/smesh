import time, pygame, random, math, pymunk, json
from constants import *
from imagestore import *

class Player():
  id = -1
  theta = 0
  dist = 0
  attacking = False
  lastAttack = 0
  lobbyPlayer = None

  def __init__(self, id, conn):
    self.conn = conn
    self.id = id
    self.faceid = sampleIndex(faces)
    self.conn.send(json.dumps({
      'id': self.id,
      'blob': {
        'action': 'face',
        'data': {
          'face': self.faceid
        }
      }
    }) + "\n")
    print('sent face' + str(self.faceid))
    self.face = generateFace(self.faceid)

  def setLocation(self, theta, dist):
    self.theta = theta
    self.dist = dist

  def startAttack(self):
    self.lastAttack = time.time()
    self.attacking = True

  def createBody(self, position):
    pass

  def gameRender(self, screen):
    # for later
    print("Render game")

class LobbyPlayer():
  radius = 50

  def __init__(self, parentPlayer, space):
    self.parentPlayer = parentPlayer
    self.space = space
    self.body = pymunk.Body(1, 1)
    self.body.position = (random.random() - 0.5) * WIDTH / 4, HEIGHT/2
    self.poly = pymunk.Circle(self.body, self.radius)
    self.poly.friction = 0.2
    self.body.damping = 0.9
    self.theta = parentPlayer.theta
    self.dist = parentPlayer.dist
    space.add(self.body, self.poly)

  def tick(self, deltaTime):
    self.theta = math.atan2(
      math.sin(self.theta or 0) + math.sin(self.parentPlayer.theta or 0) * 5 * deltaTime,
      math.cos(self.theta or 0) + math.cos(self.parentPlayer.theta or 0) * 5 * deltaTime
    )

  def render(self, screen):
    newSurface = pygame.transform.rotate(
      self.parentPlayer.face,
      - self.theta / math.pi * 180 + 90
    )
    x = int(self.body.position[0] + WIDTH/2)
    y = int(-self.body.position[1] + HEIGHT/2)
    width = newSurface.get_width()
    height = newSurface.get_height()
    #pygame.draw.circle(screen, (255, 0, 0), (x, y), self.radius)
    screen.blit(newSurface, (
      x - width / 2,
      y - height / 2,
      width,
      height
    ))