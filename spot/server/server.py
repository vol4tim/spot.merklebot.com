from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import json

from spot.spot_controller import get_spot_position

from settings.settings import INTERACTION_MODE

from scipy.interpolate import Rbf

import logging




def server(movement_queue, drawing_queue, robot_state):
    app = Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/current_state", methods=["GET"])
    def current_state():
        return {
            'queue_size': drawing_queue.qsize(),
            'robot_state': robot_state['state'],
            'last_session_id': robot_state['last_session_id'],
        }

    @app.route("/odom", methods=["GET"])
    def odom():
        position = get_spot_position()
        return {
            'position': {
                'x': position.x,
                'y': position.y
            }
        }

    @app.route('/set_movement_calibration_nodes', methods=['POST'])
    def set_movement_calibration_nodes():
        data = request.get_json()
        robot_state['calibration_nodes'] = data['calibration_nodes']
        with open('movement_calibration_nodes.json', 'w') as f:
            json.dump(data['calibration_nodes'], f)

        return {
            'status': 'ok'
        }

    @app.route('/draw_figure', methods=['POST'])
    def draw_figure():
        print("GOT DRWAWING REQUEST")

        data = request.get_json()

        if 'segments' in data:
            segments = data['segments']
            drawing_queue.put(
                {
                    'segments': segments,
                    'payment_mode': data['payment_mode'],
                    'tx_id': data['tx_id']
                }
            )
        return {'status': 'started'}

    @app.route('/interaction_mode', methods=['GET'])
    def get_interaction_mode():
        return {'interaction_mode': INTERACTION_MODE}

    @app.route('/go_to_point', methods=["POST"])
    def go_to_point():
        print("GOT MOVEMENT REQUEST")
        data = request.get_json()
        nodes = robot_state['calibration_nodes']

        coord_nodes = {k: [dic[k] for dic in nodes] for k in nodes[0]}
        robot_x_interpolate = Rbf(coord_nodes["camera_x"], coord_nodes["camera_y"], coord_nodes["robot_x"],
                                  function="linear")
        robot_y_interpolate = Rbf(coord_nodes["camera_x"], coord_nodes["camera_y"], coord_nodes["robot_y"],
                                  function="linear")

        camera_point_coords = data['camera_point_coords']
        robot_x_aim = float(robot_x_interpolate(camera_point_coords[0], camera_point_coords[1]))
        robot_y_aim = float(robot_y_interpolate(camera_point_coords[0], camera_point_coords[1]))
        movement_queue.put([robot_x_aim, robot_y_aim])
        return {'status': 'ok'}

    app.run(host='0.0.0.0', port=1234)
