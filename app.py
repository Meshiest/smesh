import pygame, thread, time, sys, math, copy, socket, json
sys.path.append('code')
from constants import *

pygame.init()
pygame.mixer.init(frequency=22100, size=-16, channels=2, buffer=2048)
real_screen = pygame.display.set_mode([REAL_WIDTH, REAL_HEIGHT], pygame.HWSURFACE|pygame.DOUBLEBUF)
screen = pygame.Surface((WIDTH, HEIGHT))

from player import *
from font import *
from lobbymenu import *
from mapmenu import *
from fightmenu import *

# Pygame
players = {}
menus = [
  LobbyMenu(players),
  MapMenu(players),
  FightMenu(players),
]
# Constants for determining which menu to use
LOBBY_MENU = 0
MAP_MENU = 1
FIGHT_MENU = 2

currMenu = LOBBY_MENU
sockClient = None

def toMapMenu():
  global currMenu, playersCanJoin
  currMenu = MAP_MENU
  playersCanJoin = False

def toLobbyMenu():
  global currMenu, playersCanJoin
  currMenu = LOBBY_MENU
  playersCanJoin = True

def toFightMenu():
  global currMenu
  index = menus[MAP_MENU].selectedMap
  currMapBlob = menus[MAP_MENU].maps[index].blob
  menus[FIGHT_MENU].loadMap(blob)
  currMenu = FIGHT_MENU
  menus[FIGHT_MENU].start()

currTime = time.time()
gameRunning = True
playersCanJoin = True

# When a key is pressed
def onKeyPress(key):
  global currMenu, menus
  menus[currMenu].keyDown(key)
  if currMenu == LOBBY_MENU:
    if key == pygame.K_SPACE and len(players) > 0:
      toMapMenu()

  elif currMenu == MAP_MENU:
    if key == pygame.K_ESCAPE:
      toLobbyMenu()

  elif currMenu == FIGHT_MENU:
    if key == pygame.K_SPACE:
      toFightMenu()

# When a key is released
def onKeyRelease(key):
  global currMenu, menus
  menus[currMenu].keyUp(key)

def render():
  global screen, currMenu, menus, deltaTime

  pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))

  menus[currMenu].tick(deltaTime)
  menus[currMenu].render(screen)
  pygame.transform.scale(screen, 
    (REAL_WIDTH, REAL_HEIGHT),
    real_screen
  )


def gameLoop():
  global currTime, deltaTime, gameRunning, screen, WIDTH, HEIGHT

  # Get current unix time
  lastTime, currTime = currTime, time.time()
  deltaTime = currTime - lastTime

  keys = pygame.key.get_pressed()
  for event in pygame.event.get():

    # Detection for pressing exit button
    if event.type == pygame.QUIT:
      gameRunning = False
      if sockClient:
        sockClient.send(json.dumps({
          "action": "quit"
        }) + "\n")


    # When keys are pressed
    if event.type == pygame.KEYDOWN:
      onKeyPress(event.dict['key'])

    # When keys are released
    if event.type == pygame.KEYUP:
      onKeyRelease(event.dict['key'])

  render()
  pygame.display.update()


# Socket Thread
def ServerThread():
  global gameRunning, players, playersCanJoin, menus, sockClient

  sockClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sockClient.connect((TCP_HOST, TCP_PORT))
  sockClient.send(json.dumps({
    "action": "start"
  }) + "\n")
  data = ''
  while gameRunning:
    resp = sockClient.recv(BUFFER_SIZE)
    if not resp:
      gameRunning = False
      break
    data += resp
    print("Got: " + str(resp))
    messages = data.split("\n")
    data = messages[-1]
    for msg in messages[:-1]:
      blob = json.loads(str.decode(msg))

      # player reconnected without properly disconnecting
      if blob['type'] == 'connect' and players.get(blob['id']) and playersCanJoin:
        player = players[blob['id']]
        lobbyPlayer = player.lobbyPlayer
        menus[0].queueRemove(lobbyPlayer.body)
        menus[0].queueRemove(lobbyPlayer.poly)
        del players[blob['id']]

      # Handle creating new players
      if (blob['type'] == 'connect' or not players.get(blob['id'])) and playersCanJoin: # handle new players
        players[blob['id']] = Player(blob['id'], sockClient)

      if not players[blob['id']]:
        continue

      if blob['type'] == 'disconnect': # handle dropping players
        continue # jk lol no disconnections
        player = players[blob['id']]
        lobbyPlayer = player.lobbyPlayer
        if lobbyPlayer:
          menus[0].queueRemove(lobbyPlayer.body)
          menus[0].queueRemove(lobbyPlayer.poly)

        del players[blob['id']]

      if blob['type'] == 'location': # handle new player location
        players[blob['id']].setLocation(blob['location']['theta'], blob['location']['dist'])

      if blob['type'] == 'attack':
        players[blob['id']].startAttack()

    sockClient.send(json.dumps({
      "action": "ping"
    }) + "\n")

  sockClient.send(json.dumps({
    "action": "quit"
  }) + "\n")

  sockClient.close()

thread.start_new_thread(ServerThread, ())

# Starting Game
while gameRunning:
  gameLoop()

sys.exit()
