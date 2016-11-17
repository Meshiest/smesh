from flask import Flask, request, send_from_directory, session, make_response
from flask_socketio import SocketIO, emit, send
from flask_redis import FlaskRedis
import socket, thread, json, sys, eventlet, random
eventlet.monkey_patch(socket=True)

sys.path.append('code')

from constants import *

# Web Server
server = Flask(__name__, static_folder='public', static_url_path='/public')
server.secret_key = 'lol this is a secret key'
redis_store = FlaskRedis(server)

redis_store.flushall()
redis_store.set('seed', random.randint(0,100000))
print("Set seed to " + str(redis_store.get("seed")))
redis_store.set("userIds", 1)

# Root route to render index
@server.route("/")
def root():
  global server
  print("Asking for root " + str(session.get("userId")))

  seed = redis_store.get("seed")
  if session.get("userId") == None or session.get('seed') != seed:
    session['seed'] = seed
    userId = int(redis_store.get("userIds"))
    print(str(userId) + " id")
    session["userId"] = userId
    redis_store.set("userIds", str(userId + 1))

  return server.send_static_file('index.html')

# Web Socket
#socketio = SocketIO(server)
# eventlet does not pass a flask instance
socketio = SocketIO(server, message_queue='redis://localhost:6379')
@socketio.on('location')
def io_location(blob):
  emit('nextLocation')

  # Check if the server needs to send anything to this user
  face = redis_store.get("face_" + str(session["userId"]))
  if session.get('face') != face and face != None:
    session["face"] = int(face)
    emit('face', {'face': session['face']})

  # Tell game the user's location
  sendMsg({
    "id": session["userId"],
    "type": "location",
    "location": blob
  })

@socketio.on('attack')
def io_attack():
  # Tell game the user attacked
  sendMsg({
    "id": session["userId"],
    "type": "attack"
  })

@socketio.on('connect')
def io_connect():
  print('Client connected')

  seed = redis_store.get("seed")
  if session.get("userId") == None or session.get('seed') != seed:
    session['seed'] = seed
    userId = int(redis_store.get("userIds"))
    print(str(userId) + " id")
    session["userId"] = userId
    redis_store.set("userIds", str(userId + 1))

  face = redis_store.get("face_" + str(session["userId"]))
  if session.get('face') != face and face != None:
    session["face"] = int(face)
    emit('face', {'face': session['face']})

@socketio.on('game_connect')
def io_game_connect():

  emit('nextLocation')

  seed = redis_store.get("seed")
  if session.get("userId") == None or session.get('seed') != seed:
    session['seed'] = seed
    userId = int(redis_store.get("userIds"))
    print(str(userId) + " id")
    session["userId"] = userId
    redis_store.set("userIds", str(userId + 1))

  # Tell game we have a new user
  sendMsg({
    "id": session["userId"],
    "type": "connect"
  })

@socketio.on('disconnect')
def io_disconnect():
  print('Client disconnected ' + str(session.get("userId")))

  # Tell game we have lost a user
  sendMsg({
    "id": session["userId"],
    "type": "disconnect"
  })


sockServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockServer.bind((TCP_HOST, TCP_PORT))
conn = None

def sendMsg(blob):
  global conn

  if not conn:
    return

  conn.send(str.encode(json.dumps(blob) + "\n"))

def parseData(data):
  items = data.split('\n')
  blobs = items[:-1]
  for blob in blobs:
    blob = json.loads(blob)

    if blob.get('id') == None:
      # Quit if the pygame client sends the quit command
      if blob.get('action') == 'quit':
        sys.exit()
      continue

  return items[-1]

# Starting Socket Server
def ServerThread():
  global conn
  sockServer.listen(1)
  # Keep listening until progam is stopped
  while True:
    conn, addr = sockServer.accept()
    print("Connected to Pygame")
    data = ''

    while True:
      req = conn.recv(BUFFER_SIZE)
      if not req: # Terminating connections on empty string
        break 
      req = str.decode(req)
      print("Got " + req)

      data += req
      data = parseData(data)

    conn.close()


thread.start_new_thread(ServerThread, ())
if __name__ == '__main__':
  socketio.run(server, port=3000, host="0.0.0.0")