from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import json

from spot.spot_controller import get_spot_position
from utils.auth import check_if_admin, verify_token_sign
from settings.settings import INTERACTION_MODE

from scipy.interpolate import Rbf

import logging


def server(actions_queue, tasks_queue, robot_state):
    app = Flask(__name__)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.route("/current_state", methods=["GET"])
    def current_state():
        return {
            'queue_size': tasks_queue.qsize(),
            'robot_state': robot_state['state'],
            'last_session_id': robot_state['last_session_id'],
            'current_user': robot_state['current_user']
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
            tasks_queue.put(
                {
                    'task_type': 'drawing',
                    'segments': segments,
                    'payment_mode': data['payment_mode'],
                    'tx_id': data['tx_id']
                }
            )
        return {'status': 'started'}

    @app.route('/start_inspection', methods=['POST'])
    def start_inspection():
        print("GOT INSPECTION REQUEST")

        data = request.get_json()

        if check_if_admin(data['account']):
            tasks_queue.put(
                {
                    'task_type': 'inspection',
                    'account': data['account'],
                    'payment_mode': data['payment_mode'],
                    'tx_id': data['tx_id']
                }
            )
        return {'status': 'started'}

    @app.route('/command', methods=['POST'])
    def process_command():
        data = request.get_json()

        account = data['account']
        signed_token = data['signed_token']

        if not verify_token_sign(account, signed_token):
            return {"status": "wrong signature"}
        if account != robot_state['current_user']:
            return {"status": "no access"}
        actions_queue.empty()
        actions_queue.put({
            'action': 'move',
            'value': data['vel']
        })

    @app.route('/start_calibration', methods=['POST'])
    def start_calibration():
        print("GOT CALIBRATION REQUEST")

        data = request.get_json()
        account = data['account']

        signed_token = data['signed_token']
        if not verify_token_sign(account, signed_token):
            return {"status": "wrong signature"}
        if not check_if_admin(account):
            return {"status": "no access"}

        tasks_queue.put(
            {
                'task_type': 'drawing',
                'segments': [],
                'admin_action': True,
            }
        )
        return {'status': 'ok'}

    @app.route('/interaction_mode', methods=['GET'])
    def get_interaction_mode():
        return {'interaction_mode': INTERACTION_MODE}

    # @app.route('/go_to_point', methods=["POST"])
    # def go_to_point():
    #     print("GOT MOVEMENT REQUEST")
    #     data = request.get_json()
    #     nodes = robot_state['calibration_nodes']
    #
    #     coord_nodes = {k: [dic[k] for dic in nodes] for k in nodes[0]}
    #     robot_x_interpolate = Rbf(coord_nodes["camera_x"], coord_nodes["camera_y"], coord_nodes["robot_x"],
    #                               function="linear")
    #     robot_y_interpolate = Rbf(coord_nodes["camera_x"], coord_nodes["camera_y"], coord_nodes["robot_y"],
    #                               function="linear")
    #
    #     camera_point_coords = data['camera_point_coords']
    #     robot_x_aim = float(robot_x_interpolate(camera_point_coords[0], camera_point_coords[1]))
    #     robot_y_aim = float(robot_y_interpolate(camera_point_coords[0], camera_point_coords[1]))
    #     actions_queue.put([robot_x_aim, robot_y_aim])
    #     return {'status': 'ok'}

    app.run(host='0.0.0.0', port=1234)
