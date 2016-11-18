import time, pygame, random, math, pymunk, json
from pymunk.vec2d import Vec2d
from constants import *
from imagestore import *
from audio import *
from utils import *

class Player():
  id = -1
  theta = math.pi / 2
  smoothTheta = math.pi / 2
  dist = 0
  smoothDist = 0
  attacking = False
  lastAttack = 0
  jumping = False
  lobbyPlayer = None
  direction = False
  grounded = False
  radius = 30
  footTheta = 0
  dead = False
  died = 0
  lastMove = 0

  def __init__(self, id, conn):
    self.conn = conn
    self.id = id
    self.faceid = sampleIndex(faces)
    self.face = generateFace(self.faceid)
    self.torso = generateTorso()
    self.foot = generateFoot()
    self.weapon = generateWeapon()
    self.lastMove = 0
    self.died = 0

  def setLocation(self, theta, dist):
    if theta != None:
      self.theta = theta
      self.lastMove = time.time()
    if dist != None:
      self.dist = dist

  # Called when a player taps the screen
  def startAttack(self):
    vert = math.sin(self.theta) * self.dist
    if vert < 0:
      self.tryJumping()
    else:
      self.lastAttack = time.time()
      self.attacking = True

  def tryJumping(self):
    self.jumping = True

  def createBody(self, space, position):
    self.space = space
    self.body = pymunk.Body(5, pymunk.inf)
    self.body.position = position[0], HEIGHT-position[1]
    self.poly = pymunk.Circle(self.body, self.radius)
    self.poly.friction = 0.1
    self.poly.collision_type = 1
    self.body.damping = 0.8
    self.space.add(self.body, self.poly)
    self.dead = False

  # Used to detect collisions between player and ground
  def raycastCallback(self, ray):
    contactPoint = ray.contact_point_set
    normal = -contactPoint.normal

    if normal.y > self.raycast_normal.y:
      self.raycast_normal = normal
      self.raycast_penetration = -contactPoint.points[0].distance
      self.raycast_body = ray.shapes[1].body
      self.raycast_impulse = ray.total_impulse
      self.raycast_position = contactPoint.points[0].point_b


  def tick(self, deltaTime):
    if self.body.position.y < -200:
      self.dead = True
      self.died = time.time()
      explosion.play()
      self.space.remove(self.body)
      self.space.remove(self.poly)
      return

    self.raycast_normal = Vec2d.zero()
    self.raycast_penetration = Vec2d.zero()
    self.raycast_impulse = Vec2d.zero()
    self.raycast_position = Vec2d.zero()
    self.raycast_body = None



    self.smoothTheta = math.atan2(
      math.sin(self.smoothTheta or 0) + math.sin(self.theta or 0) * 5 * deltaTime,
      math.cos(self.smoothTheta or 0) + math.cos(self.theta or 0) * 5 * deltaTime
    )

    self.smoothDist += (self.dist-self.smoothDist) * deltaTime * 5

    # Do raycasting to check for collisions beneath player
    self.body.each_arbiter(lambda ray: self.raycastCallback(ray))

    grounded = self.raycast_body != None and abs(self.raycast_normal.x / self.raycast_normal.y) < -PLAYER_GROUND_ACCEL/self.space.gravity.y
    self.grounded = grounded
    if grounded:
      self.footTheta += self.body.velocity.x * 0.1 * deltaTime + math.pi * 2
    elif self.jumping:
      self.jumping = False


    self.footTheta %= math.pi * 2

    if grounded and self.jumping:

      jumpVelocity = math.sqrt(2.0 * JUMP_HEIGHT * abs(GRAVITY))
      impulse = (0, self.body.mass * jumpVelocity)
      self.body.apply_impulse_at_local_point(impulse)
      self.jumping = False

    # Direction player is facing
    self.direction = self.body.velocity.x > 0

    vx = 0
    magnitude = math.cos(self.theta) * self.smoothDist

    if abs(magnitude) > 0.1:
      vx = PLAYER_VELOCITY * magnitude

    self.poly.surface_velocity = -vx, 0

    if self.raycast_body != None:
      self.poly.friction = -PLAYER_GROUND_ACCEL / GRAVITY
    else:
      self.poly.friction = 0
      # Air movement
      self.body.velocity.x = lerp(self.body.velocity.x, vx, PLAYER_AIR_ACCEL * deltaTime)

    # Falling max speed
    self.body.velocity.y = max(self.body.velocity.y, -FALL_VELOCITY)


  def render(self, screen):
    x = int(self.body.position[0])
    y = int(HEIGHT-self.body.position[1])

    #pygame.draw.circle(screen, (255, 0, 0), (x, y), self.radius)

    legHeight = 30 - self.radius
    neckLength = 20
    armLength = 50

    faceRight = abs(math.cos(self.theta) * self.dist) > 0.05 and math.cos(self.theta) * self.dist > 0
    rightMult = faceRight and -1 or 1

    # Draw Feet
    footWidth = self.foot.get_width()
    footHeight = self.foot.get_height()
    
    torsoWidth = self.torso.get_width()
    torsoHeight = self.torso.get_height()

    leftFoot = pygame.transform.flip(self.foot, faceRight, False)
    screen.blit(
      leftFoot,
      (
        x - footWidth / 2 + torsoWidth / 5 * math.cos(self.footTheta),
        y - legHeight + footHeight / 2 * math.sin(self.footTheta),
        footWidth,
        footHeight
      )
    )
    screen.blit(
      leftFoot,
      (
        x - footWidth / 2 + torsoWidth / 5 * math.cos(self.footTheta + math.pi),
        y - legHeight + footHeight / 2 * math.sin(self.footTheta + math.pi),
        footWidth,
        footHeight
      )
    )

    # Draw Torso
    screen.blit(
      pygame.transform.flip(self.torso, faceRight, False),
      (
        x - torsoWidth / 2,
        y - torsoHeight - legHeight,
        torsoWidth,
        torsoHeight
      )
    )

    # Draw Face
    theta = self.smoothTheta
    if faceRight:
      theta *= -1
      theta += math.pi
    faceSurface = pygame.transform.rotate(
      self.face,
      - theta / math.pi * 180 + 90
    )

    faceWidth = faceSurface.get_width()
    faceHeight = faceSurface.get_height()
    faceOffsetX = math.cos(self.smoothTheta + math.pi) * neckLength
    faceOffsetY = math.sin(self.smoothTheta + math.pi) * neckLength
    screen.blit(
      pygame.transform.flip(faceSurface, faceRight, False),
      (
        x - faceWidth / 2 + faceOffsetX,
        y - 160 - faceHeight / 2 - legHeight + faceOffsetY,
        faceWidth,
        faceHeight
      )
    )

    # Draw Weapon
    weaponImage = self.weapon['img']
    handPos = self.weapon['hand']
    now = time.time()
    attackMod = now - self.lastAttack < 0.5 and 3 or 1
    attackTimeMod = now - self.lastAttack < 0.5 and 10 or 1
    armTheta = (math.cos((now * attackTimeMod + self.id)  % (math.pi * 2))  + 1) * 0.2 * attackMod 
    weaponImage = pygame.transform.flip(weaponImage, not faceRight, False)
    weaponWidth = weaponImage.get_width()
    weaponHeight = weaponImage.get_height()
    screen.blit(
      weaponImage, (
        x - (torsoWidth / 3 + math.cos(armTheta) * armLength) * rightMult - weaponWidth/2,
        y - torsoHeight + 40 + math.sin(armTheta) * armLength - weaponHeight + handPos[1],
        weaponWidth, 
        weaponHeight,
      )
    )

    handTheta = (math.cos((now + self.id)  % (math.pi * 2))  + 1) * 0.2 - 1.2
    screen.blit(
        pygame.transform.flip(pygame.transform.rotate(hand_base,
          handTheta / math.pi * 180
        ), faceRight, False), (
        x - (-torsoWidth / 3 - math.cos(-handTheta) * armLength) * rightMult - hand_base.get_width()/2,
        y - torsoHeight + 40 + math.sin(-handTheta) * armLength - hand_base.get_height()/2,
        weaponWidth, 
        weaponHeight,
      )
    )


class LobbyPlayer():
  radius = 50

  def __init__(self, parentPlayer, space):
    self.parentPlayer = parentPlayer
    self.space = space
    self.body = pymunk.Body(1, 1)
    self.body.position = (random.random() - 0.5) * WIDTH / 4, HEIGHT/2
    self.poly = pymunk.Circle(self.body, self.radius)
    #self.body.damping = 0.8
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