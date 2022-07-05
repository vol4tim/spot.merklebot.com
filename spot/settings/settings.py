import os
from dotenv import load_dotenv

load_dotenv()


# Constants to access spot robot
SPOT_USERNAME = os.environ.get("SPOT_USERNAME", "admin")
SPOT_PASSWORD = os.environ.get("SPOT_PASSWORD", "2zqa8dgw7lor")
SPOT_IP = os.environ.get("SPOT_IP", "192.168.50.3")

INTERACTION_MODE = os.environ.get("INTERACTION_MODE", "movement")

# Videoserver url
VIDEOSERVER_URL = os.environ.get("VIDEOSERVER_IP", "http://10.200.0.8:8000/")

# Security token to execute video server commands
VIDEOSERVER_TOKEN = os.environ.get("VIDEOSERVER_TOKEN", "")

USE_ROBONOMICS = os.environ.get("USE_ROBONOMICS", 1)
ROBONOMICS_LISTEN_ROBOT_ACCOUNT = os.environ.get("ROBONOMICS_LISTEN_ROBOT_ACCOUNT",
                                                 "4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j")
PINATA_API_KEY = os.environ["PINATA_API_KEY"]
PINATA_SECRET_API_KEY = os.environ["PINATA_SECRET_API_KEY"]

ESTUARY_URL = os.environ["ESTUARY_URL"]
ESTUARY_TOKEN = os.environ["ESTUARY_TOKEN"]

MOVEMENT_SESSION_DURATION_TIME = 120

DEMO_API_URL = os.environ.get('DEMO_API_URL', 'https://api.merklebot.com/spot-demo')

ADMIN_ACCOUNTS = os.environ.get('ADMIN_ACCOUNTS', '4HVVtYPQ8hu7XGKQPmwjhTTHK5crSsiitJpLsA4B4PQV1PNr,4G1SKuxjYkm7AtbMzjpZZnXdt3sShj7nrvEB9dxLcVYJe87P,4HY2Mb4fpsyz6vyWHd3xGPgnHC983junioxhT2Cnfa5Kok5b').split(',')

MNEMONIC = os.environ["MNEMONIC"]
