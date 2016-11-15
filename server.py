from flask import Flask, request, send_from_directory, session, make_response
from flask_socketio import SocketIO, emit, send
import socket, thread, json, sys

sys.path.append('code')

from constants import *

# Web Server
server = Flask(__name__, static_url_path='', static_folder='public')
server.secret_key = 'lol this is a secret key'
userIds = 0

# Root route to render index
@server.route("/")
def root():
  global server, userIds
  print("Asking for root")
  if not session.get("userId"):
    session["userId"] = userIds
    userIds += 1
  return server.send_static_file('index.html')

# Web Socket
socketio = SocketIO(server)
sendQueue = {}

@socketio.on('location')
def io_location(blob):
  emit('nextLocation')

  # Check if the server needs to send anything to this user
  if sendQueue.get(session["userId"]):
    messages = sendQueue[session["userId"]]
    for message in messages:
      if message['action'] == 'face':
        session['face'] = message['data']['face']

      emit(message['action'], message['data'])
    del sendQueue[session["userId"]]

  # Tell game the user's location
  sendMsg({
    "id": session["userId"],
    "type": "location",
    "location": blob
  })

@socketio.on('attack')
def io_attack():
  print("attack")
  # Tell game the user attacked
  sendMsg({
    "id": session["userId"],
    "type": "attack"
  })

@socketio.on('connect')
def io_connect():
  global userIds
  print('Client connected')
  emit('nextLocation')

  if session.get('face'):
    emit('face', {'face': session['face']})

  # Tell game we have a new user
  sendMsg({
    "id": session["userId"],
    "type": "connect"
  })

@socketio.on('disconnect')
def io_disconnect():
  global userIds
  print('Client disconnected')

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

    if not blob.get('id'):
      # Quit if the pygame client sends the quit command
      if blob.get('action') == 'quit':
        sys.exit()

      continue

    # Create a new sendQueue entry if we don't have a queued message yet
    if not sendQueue.get(blob['id']):
      sendQueue[blob['id']] = []

    # Add the message to the queue
    sendQueue[blob['id']].append(blob['blob'])

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

      data += req
      data = parseData(data)

    conn.close()


thread.start_new_thread(ServerThread, ())
if __name__ == '__main__':
  socketio.run(server, port=3000, host="0.0.0.0")