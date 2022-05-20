import bosdyn.client
from bosdyn.client.graph_nav import GraphNavClient
from bosdyn.client.recording import GraphNavRecordingServiceClient

robot_ip = "192.168.50.3"
username = "admin"
password = "2zqa8dgw7lor"


sdk = bosdyn.client.create_standard_sdk('ControllingSDK')
robot = sdk.create_robot(robot_ip)
robot.authenticate(username, password)

lease_client = robot.ensure_client('lease')
lease = lease_client.take()
lease_keep_alive = bosdyn.client.lease.LeaseKeepAlive(lease_client, must_acquire=True)

recording_client = robot.ensure_client(GraphNavRecordingServiceClient.default_service_name)
graph_nav_client = robot.ensure_client(GraphNavClient.default_service_name)

recording_client.stop_recording()
graph_nav_client.clear_graph()
