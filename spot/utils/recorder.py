import multiprocessing
from datetime import datetime
import os, time
import subprocess
import signal
import shutil
import requests

from pinatapy import PinataPy

from utils.robonomics import record_datalog

from settings.settings import VIDEOSERVER_URL, PINATA_API_KEY, PINATA_SECRET_API_KEY, ESTUARY_URL, ESTUARY_TOKEN


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

    ipfs_cid = pinata_resp["IpfsHash"]
    datalog_extrinsic_hash = record_datalog(ipfs_cid)

    # Upload to Estuary Filecoin node
    tar = "{}/{}".format(folder, record_folder_name)
    shutil.make_archive(tar, "xztar", folder)
    time.sleep(0.3)
    with open("{}.tar.xz".format(tar), "rb") as fd:
        estuary_resp = requests.post(f"{ESTUARY_URL}/content/add",
                                     headers={
                                         "Authorization": f"Bearer {ESTUARY_TOKEN}",
                                     },
                                     files={
                                         "data": fd,
                                     },
                                     )
        print("Estuary response: {}".format(estuary_resp.text))

    requests.post("https://api.merklebot.com/robonomics-launch-traces", json={
        "sender": sender,
        "nonce": session_id,
        "created_at": created_at_str,
        "ipfs_cid": ipfs_cid,
        "launch_tx_id": launch_event_id,
        "datalog_tx_id": datalog_extrinsic_hash,
        "filecoin_cid": estuary_resp.json()["cid"],
    })
    print("Session {} trace created with IPFS CID {}".format(session_id, ipfs_cid))


class DataRecorder:
    def __init__(self, transaction):
        self.sender = transaction['sender']
        self.recipient = transaction['recipient']
        self.session_id = transaction['session_id']
        self.tx_id = transaction['tx_id']
        self.recorder = None
        self.video_recorder = None
        self.record_folder_name = None
        self.video_name = None
        self.created_at_str = None

    def start_data_recording(self):
        created_at_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        self.record_folder_name = "user-{}-cps-{}-session-{}-{}".format(
            self.sender,
            self.recipient,
            self.session_id,
            created_at_str
        )

        bag_name = "state.bag"
        self.video_name = "camera.mp4"
        print("New launch, sender={}, recipient={}, session_id={}, bag={}".format(
            self.sender, self.recipient, self.session_id, bag_name))

        os.makedirs("./traces/{}".format(self.record_folder_name), exist_ok=True)

        # duration=5m limits max recoding time and prevents orphan processes keep recording forever
        self.recorder = subprocess.Popen(
            ["rosbag", "record", "--duration=5m", "--output-name={}".format(bag_name), "/tf", "/tf_static",
             "/joint_states"],
            cwd="./traces/{}/".format(self.record_folder_name),  # directory to put files
        )

        # start recording stream from videoserver
        video_url = VIDEOSERVER_URL + "video"
        result_image_name = "result.jpg"
        self.video_recorder = subprocess.Popen(["python3", "video_recorder.py", "--video_url={}".format(video_url),
                                                "--output_file=./traces/{}/{}".format(self.record_folder_name,
                                                                                      self.video_name),
                                                "--last_im_file=./traces/{}/{}".format(self.record_folder_name,
                                                                                       result_image_name)])

    def stop_data_recording(self):
        time.sleep(2)  # wait for the robot to finish its movement
        self.recorder.terminate()
        self.video_recorder.send_signal(signal.SIGINT)
        time.sleep(10)

    def start_data_uploading(self):
        multiprocessing.Process(
            target=after_session_complete,
            args=(
                self.record_folder_name,
                self.video_name,
                self.sender,
                self.session_id,
                self.created_at_str,
                self.tx_id,
            )
        ).start()

