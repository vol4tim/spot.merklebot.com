from substrateinterface import SubstrateInterface
from datetime import datetime
import os, time
import subprocess
import requests

import multiprocessing
import shutil

import robonomicsinterface as RI
from pinatapy import PinataPy

from settings.settings import (
    VIDEOSERVER_URL,
    INTERACTION_MODE,
    PINATA_API_KEY,
    PINATA_SECRET_API_KEY,
    ESTUARY_TOKEN,
    ESTUARY_URL,
)
import signal


def get_account_nonce(address) -> int:
    substrate = SubstrateInterface(
        url="wss://kusama.rpc.robonomics.network/",
        ss58_format=32,
        type_registry_preset="substrate-node-template",
        type_registry={
            "types": {
                "Record": "Vec<u8>",
                "<T as frame_system::Config>::AccountId": "AccountId",
                "RingBufferItem": {
                    "type": "struct",
                    "type_mapping": [
                        ["timestamp", "Compact<u64>"],
                        ["payload", "Vec<u8>"],
                    ],
                },
            }
        }
    )
    return substrate.get_account_nonce(address)


def after_session_complete(
        record_folder_name,
        video_name,
        sender,
        session_id,
        created_at_str,
        launch_event_id,
):
    print("After session procedure for session {} started".format(session_id))
    video_path = "./traces/{}/{}".format(record_folder_name, video_name)
    h264_path = "./traces/{}/h264_{}".format(record_folder_name, video_name)
    os.system("ffmpeg -i {} -vcodec h264 {} ".format(video_path, h264_path))

    pinata = PinataPy(PINATA_API_KEY, PINATA_SECRET_API_KEY)
    folder = "/home/spot/davos.merklebot.com/spot/traces/{}".format(record_folder_name)
    pinata_resp = pinata.pin_file_to_ipfs(folder)
    print("Pinata response: {}".format(pinata_resp))

    robonomics = RI.RobonomicsInterface(seed=os.environ["MNENOMIC"])
    ipfs_cid = pinata_resp["IpfsHash"]
    datalog_extrinsic_hash = robonomics.record_datalog(ipfs_cid)
    requests.post("https://api.merklebot.com/robonomics-launch-traces", json={
        "sender": sender,
        "nonce": session_id,
        "created_at": created_at_str,
        "ipfs_cid": ipfs_cid,
        "launch_tx_id": launch_event_id,
        "datalog_tx_id": datalog_extrinsic_hash,
    })

    # Upload to Estuary Filecoin node
    tar = "{}/{}".format(folder, record_folder_name)
    shutil.make_archive(tar, "xztar", folder)
    time.sleep(0.3)
    with open("{}.tar.xz".format(tar)) as fd:
        resp = requests.post(f"{ESTUARY_URL}",
            headers={
                "Authorization": f"Bearer {ESTUARY_TOKEN}",
                "Content-Type": "multipart/form-data",
            },
            files={
                "data": fd,
            },
        )
        print("Estuary response: {}".format(resp))

    print("Session {} trace created with IPFS CID {}".format(session_id, ipfs_cid))


class RobonimicsHelper:
    def __init__(self, robot_state, execute_drawing_command, start_movement_session):
        self.execute_drawing_command = execute_drawing_command
        self.start_movement_sesstion = start_movement_session
        self.robot_state = robot_state

    def robonomics_transaction_callback(self, data, launch_event_id):
        """Execution sequence.

        1. Start robot state recording,
        2. Move the robot,
        3. Stop recording,
        4. Launch after session procedures in background.
        """

        sender, recipient, _ = data
        session_id = get_account_nonce(sender)
        created_at_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        record_folder_name = "user-{}-cps-{}-session-{}-{}".format(
            sender,
            recipient,
            session_id,
            created_at_str
        )

        bag_name = "state.bag"
        video_name = "camera.mp4"
        print("New launch, sender={}, recipient={}, session_id={}, bag={}".format(
            sender, recipient, session_id, bag_name))
        try:
            os.makedirs("./traces/{}".format(record_folder_name), exist_ok=True)

            # duration=5m limits max recoding time and prevents orphan processes keep recording forever
            recorder = subprocess.Popen(
                ["rosbag", "record", "--duration=5m", "--output-name={}".format(bag_name), "/tf", "/tf_static",
                 "/joint_states"],
                cwd="./traces/{}/".format(record_folder_name),  # directory to put files
            )

            # start recording stream from videoserver
            video_url = VIDEOSERVER_URL + "video"
            result_image_name = "result.jpg"
            video_recorder = subprocess.Popen(["python3", "video_recorder.py", "--video_url={}".format(video_url),
                                               "--output_file=./traces/{}/{}".format(record_folder_name, video_name),
                                               "--last_im_file=./traces/{}/{}".format(record_folder_name,
                                                                                      result_image_name)])
            if INTERACTION_MODE == 'drawing':
                self.execute_drawing_command(address=sender)
            elif INTERACTION_MODE == 'movement':
                self.start_movement_session()
        finally:
            time.sleep(2)  # wait for the robot to finish its movement
            recorder.terminate()
            video_recorder.send_signal(signal.SIGINT)
        time.sleep(5)  # wait while recorder process closes the file

        multiprocessing.Process(
            target=after_session_complete,
            args=(
                record_folder_name,
                video_name,
                sender,
                session_id,
                created_at_str,
                launch_event_id,
            )
        ).start()
        self.robot_state['last_session_id'] = session_id
        self.robot_state['state'] = "idle"
        print("Session {} complete, creating a trace".format(session_id))

    def start_subscriber(self):
        interface = RI.RobonomicsInterface()
        print("Robonomics subscriber starting...")
        subscriber = RI.Subscriber(interface, RI.SubEvent.NewLaunch, self.robonomics_transaction_callback,
                                   "4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j")
