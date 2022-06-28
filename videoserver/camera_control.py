import subprocess
from enum import Enum
import time

V4L2CTLEXEC = "/usr/bin/v4l2-ctl"


class CameraControl:
    def __init__(self):
        self.velocity = {
            'x': 0,
            'y': 0
        }

    def control(self, control_name, value):
        """
        control: control variable name
        value: control variable value
        """
        return subprocess.check_output([V4L2CTLEXEC, "-c", f"{control_name}={value}"])

    def set_velocity(self, vel_x, vel_y):
        self.velocity['x'] = vel_x
        self.velocity['y'] = vel_y

    def move(self, velocity, time_interval=0.1):
        self.control('pan_speed', velocity['x'])
        self.control('tilt_speed', velocity['y'])
        time.sleep(time_interval)
        self.control('pan_speed', 0)
        self.control('tilt_speed', 0)

    def set_zoom(self, zoom_absolute):
        self.control('zoom_absolute', zoom_absolute)
