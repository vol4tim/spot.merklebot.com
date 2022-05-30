from spot_controller import SpotController
import json

coord_nodes = json.load(open("calibration_data_final.json")) if os.path.exists("calibration_data_final.json") else {
    "x": [0, 0, 400, 400],
    "y": [0, 300, 0, 300],
    "yaw": [-0.4, -0.4, 0.4, 0.4],
    "pitch": [-0.4, 0.4, -0.4, 0.4],
    "max_width": 400,
    "max_height": 300
}

with SpotController("admin", "2zqa8dgw7lor", "192.168.50.3", coord_nodes) as sc:
    yaws = [(-1) ** (j % 2) * i / 10 for j in range(8) for i in range(-5, 6, 1)]
    pitches = [i / 10 for i in range(-5, 3, 1) for j in range(11)]
    rolls = [0] * len(yaws)
    sc.move_head_in_points(yaws, pitches, rolls)