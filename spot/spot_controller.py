import time
import bosdyn.client
from bosdyn.client.robot_command import RobotCommandClient, RobotCommandBuilder, blocking_stand  # , blocking_sit
from bosdyn.geometry import EulerZXY
from bosdyn.api.spot import robot_command_pb2 as spot_command_pb2
import picture_to_coods_data as ptc
from scipy.interpolate import interp2d


class SpotController:
    def __init__(self, username, password, robot_ip):
        self.username = username
        self.password = password
        self.robot_ip = robot_ip

        sdk = bosdyn.client.create_standard_sdk('ControllingSDK')

        self.robot = sdk.create_robot(robot_ip)
        id_client = self.robot.ensure_client('robot-id')

        self.robot.authenticate(username, password)

        self.command_client = self.robot.ensure_client(RobotCommandClient.default_service_name)
        self.yaw_interpolate = interp2d(x=ptc.coord_nodes["x"], y=ptc.coord_nodes["y"],
                                                     z=ptc.coord_nodes["yaw"], kind="linear")

        self.pitch_interpolate = interp2d(x=ptc.coord_nodes["x"], y=ptc.coord_nodes["y"],
                                                     z=ptc.coord_nodes["pitch"], kind="linear")

        self.robot.logger.info("Authenticated")

    def move_head_in_points(self, yaws, pitches, rolls, body_height=-0.3, sleep_after_point_reached=0, timeout=3):
        for i in range(len(yaws)):
            footprint_r_body = EulerZXY(yaw=yaws[i], roll=rolls[i], pitch=pitches[i])
            params = RobotCommandBuilder.mobility_params(footprint_R_body=footprint_r_body, body_height=body_height)
            blocking_stand(self.command_client, timeout_sec=timeout, update_frequency=0.1, params=params)
            self.robot.logger.info("Moved to yaw={} rolls={} pitch={}".format(yaws[i], rolls[i], pitches[i]))
            # cmd = RobotCommandBuilder.synchro_stand_command()
            # self.command_client.robot_command(cmd)

    def lease_control(self):
        lease_client = self.robot.ensure_client('lease')
        lease = lease_client.take()
        lease_keep_alive = bosdyn.client.lease.LeaseKeepAlive(lease_client, must_acquire=True)
        self.robot.logger.info("Lease acquired")

    def power_on_stand_up(self):
        self.robot.power_on(timeout_sec=20)
        assert self.robot.is_powered_on(), "Not powered on"
        self.robot.time_sync.wait_for_sync()
        blocking_stand(self.command_client, timeout_sec=10)

    def power_off_sit_down(self):
        self.robot.power_off(cut_immediately=False)

    def move_to_draw(self, start_drawing_trigger_handler, end_drawing_trigger_handler,
                     xx, yy, body_height=-0.3):

        coords = [self.interpolate_coords(xx[i], yy[i]) for i in range(len(xx))]
        yaws = [coord[0] for coord in coords]
        pitches = [coord[1] for coord in coords]
        rolls = [coord[2] for coord in coords]

        self.lease_control()
        # self.power_on_stand_up()

        self.move_head_in_points(yaws=yaws[0:1], pitches=pitches[0:1], rolls=rolls[0:1], body_height=body_height)
        start_drawing_trigger_handler()
        self.move_head_in_points(yaws=yaws[1:], pitches=pitches[1:], rolls=rolls[1:], body_height=body_height)
        end_drawing_trigger_handler()

        # self.power_off_sit_down()

    def interpolate_coords(self, x, y):
        return self.yaw_interpolate(x, y), self.pitch_interpolate(x, y), 0


# yaws = [(-1) ** (j % 2) * i / 10 for j in range(11) for i in range(-5, 6, 1)]
# pitches = [i / 10 for i in range(-5, 6, 1) for j in range(11)]
# rolls = [0] * len(yaws)