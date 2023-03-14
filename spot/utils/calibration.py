import json
import time
import os
from settings.settings import CALIBRATIONS_DIR

coord_nodes = json.load(open("{}/calibration_data_final.json".format(CALIBRATIONS_DIR))) if os.path.exists("{}/calibration_data_final.json".format(CALIBRATIONS_DIR)) else {
    "x": [0, 0, 400, 400],
    "y": [0, 300, 0, 300],
    "yaw": [-0.4, -0.4, 0.4, 0.4],
    "pitch": [-0.4, 0.4, -0.4, 0.4],
    "max_width": 400,
    "max_height": 300
}

MAX_WIDTH = coord_nodes["max_width"]
MAX_HEIGHT = coord_nodes["max_height"]

def centralize(xx, yy, all_segments):
    all_xx = [segment[0] for segment in all_segments]
    all_yy = [segment[1] for segment in all_segments]

    min_x = min(all_xx)
    min_y = min(all_yy)
    xx = [x - min_x for x in xx]
    yy = [y - min_y for y in yy]

    max_x = max(all_xx)
    max_y = max(all_yy)
    xx = [x * MAX_WIDTH / max_x for x in xx]
    yy = [y * MAX_HEIGHT / max_y for y in yy]
    return xx, yy

def calibration_movement(sc, get_spot_face_on_camera_coords):
    global MAX_WIDTH, MAX_HEIGHT, coord_nodes

    yaws = [(-1) ** (j % 2) * i / 10 for j in range(8) for i in range(-5, 6, 1)]
    pitches = [i / 10 for i in range(-5, 3, 1) for j in range(11)]
    rolls = [0] * len(yaws)

    calibration_result = {
        "x": [], "y": [], "yaw": [], "pitch": []
    }

    for i in range(len(yaws)):
        sc.move_head_in_points(yaws=yaws[i:i + 1], pitches=pitches[i:i + 1], rolls=rolls[i:i + 1])
        time.sleep(0.3)
        x, y = get_spot_face_on_camera_coords()
        calibration_result["x"].append(x)
        calibration_result["y"].append(y)
        calibration_result["yaw"].append(yaws[i])
        calibration_result["pitch"].append(pitches[i])
        time.sleep(0.3)

    print(calibration_result)

    with open('calibration_data_raw.json', 'w') as outfile:
        json_string = json.dumps(calibration_result)
        outfile.write(json_string)

    left_upper_x = max([calibration_result["x"][i] for i in range(len(calibration_result["x"]))
                        if calibration_result["yaw"][i] == min(yaws)])
    left_upper_y = max([calibration_result["y"][i] for i in range(len(calibration_result["y"]))
                        if calibration_result["pitch"][i] == min(pitches)])

    right_bottom_x = min([calibration_result["x"][i] for i in range(len(calibration_result["x"]))
                          if calibration_result["yaw"][i] == max(yaws)])
    right_bottom_y = min([calibration_result["y"][i] for i in range(len(calibration_result["y"]))
                          if calibration_result["pitch"][i] == max(pitches)])

    MAX_WIDTH = right_bottom_x - left_upper_x
    MAX_HEIGHT = right_bottom_y - left_upper_y

    calibration_result["x"] = [calibration_result["x"][i] - left_upper_x for i in range(len(calibration_result["x"]))]
    calibration_result["y"] = [calibration_result["y"][i] - left_upper_y for i in range(len(calibration_result["y"]))]

    coord_nodes = calibration_result
    coord_nodes["max_width"] = MAX_WIDTH
    coord_nodes["max_height"] = MAX_HEIGHT

    with open('{}/calibration_data_final.json'.format(CALIBRATIONS_DIR), 'w') as outfile:
        json_string = json.dumps(coord_nodes)
        outfile.write(json_string)

    sc.update_interpolator(coord_nodes)


