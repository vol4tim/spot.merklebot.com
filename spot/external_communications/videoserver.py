import requests
from settings.settings import VIDEOSERVER_URL, VIDEOSERVER_TOKEN

def send_command_to_videoserver(command_name):
    requests.post(VIDEOSERVER_URL + command_name, json={"token": VIDEOSERVER_TOKEN})


def get_spot_face_on_camera_coords():
    res = requests.get(VIDEOSERVER_URL + "get_spot_face_coords", json={"token": VIDEOSERVER_TOKEN})
    return res.json()['coords']


def notify_start_line():
    send_command_to_videoserver("start_line")


def notify_stop_line():
    send_command_to_videoserver("stop_line")