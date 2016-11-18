# Starting Smesh on the Server

## Windows Run

1. Clone
2. Install python and pygame from installers folder
3. cd to clone folder, start 3 terminals (I will call them A, B, and C)
4. A - `pip install -r requirements.txt`
5. A - `cd redis`
6. A - `redis-server.exec conf\\redis.conf`
7. B - `python server.py`
8. C - `python app.py`

## Linux Run

1. Clone
2. `sudo apt install python2.7 python-pygame python-pip redis-server`
3. `cd clone/redis` -> `service redis-server start conf/redis.conf`
4. `python server.py`
5. `python app.py` in a new terminal

# Connecting

1. Open `[LOCALIP]:3000` on any device on the same network where `[LOCALIP]` is the ip given by `ipconfig` or `ifconfig` in a cmd/shell

# More Info

Checkout `MAP_README.md` for Map editor instructions

Change resolution under `WIDTH` and `HEIGHT` in `code/constants.py`, do **not** change `REAL_WIDTH` and `REAL_HEIGHT`