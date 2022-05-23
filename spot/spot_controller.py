import time
import bosdyn.client
from bosdyn.client.robot_command import RobotCommandClient, RobotCommandBuilder, blocking_stand  # , blocking_sit
from bosdyn.geometry import EulerZXY
from bosdyn.api.spot import robot_command_pb2 as spot_command_pb2
from scipy.interpolate import Rbf
from bosdyn.client.frame_helpers import ODOM_FRAME_NAME
from bosdyn.api.basic_command_pb2 import RobotCommandFeedbackStatus


class SpotController:
    def __init__(self, username, password, robot_ip, coord_nodes):
        self.username = username
        self.password = password
        self.robot_ip = robot_ip

        self.coord_nodes = coord_nodes

        sdk = bosdyn.client.create_standard_sdk('ControllingSDK')

        self.robot = sdk.create_robot(robot_ip)
        id_client = self.robot.ensure_client('robot-id')

        self.robot.authenticate(username, password)

        self.command_client = self.robot.ensure_client(RobotCommandClient.default_service_name)
        self.lease_client = self.robot.ensure_client('lease')

        self.yaw_interpolate = Rbf(coord_nodes["x"], coord_nodes["y"], coord_nodes["yaw"], function="linear")
        self.pitch_interpolate = Rbf(coord_nodes["x"], coord_nodes["y"], coord_nodes["pitch"], function="linear")

        self.robot.logger.info("Authenticated")
        self.lease = None

    def update_interpolator(self, coord_nodes):
        self.coord_nodes = coord_nodes
        self.yaw_interpolate = Rbf(coord_nodes["x"], coord_nodes["y"], coord_nodes["yaw"], function="linear")
        self.pitch_interpolate = Rbf(coord_nodes["x"], coord_nodes["y"], coord_nodes["pitch"], function="linear")

    def move_head_in_points(self, yaws, pitches, rolls, body_height=-0.3, sleep_after_point_reached=0, timeout=3):
        for i in range(len(yaws)):
            footprint_r_body = EulerZXY(yaw=yaws[i], roll=rolls[i], pitch=pitches[i])
            params = RobotCommandBuilder.mobility_params(footprint_R_body=footprint_r_body, body_height=body_height)
            blocking_stand(self.command_client, timeout_sec=timeout, update_frequency=0.02, params=params)
            self.robot.logger.info("Moved to yaw={} rolls={} pitch={}".format(yaws[i], rolls[i], pitches[i]))

    def wait_until_action_complete(self, cmd_id, timeout=15):
        start_time = time.time()
        while time.time() - start_time < timeout:
            feedback = self.command_client.robot_command_feedback(cmd_id)
            mobility_feedback = feedback.feedback.synchronized_feedback.mobility_command_feedback
            if mobility_feedback.status != RobotCommandFeedbackStatus.STATUS_PROCESSING:
                print("Failed to reach the goal")
                return False
            traj_feedback = mobility_feedback.se2_trajectory_feedback
            if (traj_feedback.status == traj_feedback.STATUS_AT_GOAL and
                    traj_feedback.body_movement_status == traj_feedback.BODY_STATUS_SETTLED):
                print("Arrived at the goal.")
                return True
            time.sleep(0.5)

    def move_to_goal(self, goal_x, goal_y):
        cmd = RobotCommandBuilder.synchro_se2_trajectory_point_command(goal_x=goal_x, goal_y=goal_y, goal_heading=0,
                                                                       frame_name=ODOM_FRAME_NAME)
        cmd_id = self.command_client.robot_command(lease=None, command=cmd,
                                                   end_time_secs=time.time() + 10)
        self.wait_until_action_complete(cmd_id)

        self.robot.logger.info("Moved to x={} y={}".format(goal_x, goal_y))

    def lease_control(self):
        self.lease = self.lease_client.take()
        lease_keep_alive = bosdyn.client.lease.LeaseKeepAlive(self.lease_client, must_acquire=True)
        self.robot.logger.info("Lease acquired")

    def power_on_stand_up(self):
        self.robot.power_on(timeout_sec=20)
        assert self.robot.is_powered_on(), "Not powered on"
        self.robot.time_sync.wait_for_sync()
        blocking_stand(self.command_client, timeout_sec=10)

    def power_off_sit_down(self):
        self.lease_client.return_lease(self.lease)
        self.move_head_in_points(yaws=[0], pitches=[0], rolls=[0])
        self.robot.power_off(cut_immediately=False)

    def move_to_draw(self, start_drawing_trigger_handler, end_drawing_trigger_handler,
                     xx, yy, body_height=-0.3):

        coords = [self.interpolate_coords(xx[i], yy[i]) for i in range(len(xx))]
        yaws = [coord[0] for coord in coords]
        pitches = [coord[1] for coord in coords]
        rolls = [coord[2] for coord in coords]

        self.move_head_in_points(yaws=yaws[0:1], pitches=pitches[0:1], rolls=rolls[0:1], body_height=body_height)
        start_drawing_trigger_handler()
        self.move_head_in_points(yaws=yaws[1:], pitches=pitches[1:], rolls=rolls[1:], body_height=body_height)
        end_drawing_trigger_handler()

    def interpolate_coords(self, x, y):
        return float(self.yaw_interpolate(x, y)), float(self.pitch_interpolate(x, y)), 0
