from spot.spot_logic import spot_logic_process, robonomics_subscriber_process
from server.server import server

import multiprocessing
import json
import os

PROCESSES = []


def main():
    manager = multiprocessing.Manager()

    ctx = multiprocessing.get_context('spawn')
    tasks_queue = ctx.Queue()
    actions_queue = ctx.Queue()

    robot_state = manager.dict()
    robot_state['state'] = "idle"
    robot_state['last_session_id'] = None
    robot_state['calibration_nodes'] = json.load(open("movement_calibration_nodes.json")) if os.path.exists(
        "movement_calibration_nodes.json") else []
    robot_state['transactions'] = []  # list of transactions
    robot_state['current_user'] = None
    spot_controller_process = ctx.Process(target=spot_logic_process, args=(actions_queue, tasks_queue, robot_state))
    server_process = ctx.Process(target=server, args=(actions_queue, tasks_queue, robot_state))
    robonomics_process = ctx.Process(target=robonomics_subscriber_process, args=(robot_state, tasks_queue))

    PROCESSES.append(spot_controller_process)
    PROCESSES.append(server_process)
    PROCESSES.append(robonomics_process)

    for p in PROCESSES:
        p.start()

    for p in PROCESSES:
        p.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        for p in PROCESSES:
            p.terminate()
