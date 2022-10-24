import multiprocessing
import traceback
from datetime import datetime
import os, time
import pathlib
import subprocess
import signal
import shutil
import requests

from pinatapy import PinataPy
from substrateinterface import SubstrateInterface, Keypair
import datadog

from utils.robonomics import record_datalog

from external_communications.merklebot import create_launch_trace, update_launch_trace, make_helloween_nft

from settings.settings import (
    VIDEOSERVER_URL,
    PINATA_API_KEY,
    PINATA_SECRET_API_KEY,
    ESTUARY_URL,
    ESTUARY_TOKEN,
    MNEMONIC,
    TRACES_DIR,
)


def after_session_complete(
        record_folder_name,
        video_name,
        sender,
        session_id,
        created_at_str,
        launch_event_id,
        record_video
):
    res_record_create = create_launch_trace(sender, session_id, created_at_str, launch_event_id)
    record_id = res_record_create['id']
    print("After session procedure for session {} started".format(session_id))

    if record_video:
        video_path = "{}/{}/{}".format(TRACES_DIR, record_folder_name, video_name)
        h264_path = "{}/{}/h264_{}".format(TRACES_DIR, record_folder_name, video_name)
        os.system("ffmpeg -loglevel error -i {} -vcodec h264 {} ".format(video_path, h264_path))

    pinata = PinataPy(PINATA_API_KEY, PINATA_SECRET_API_KEY)
    folder = "{}/{}".format(TRACES_DIR, record_folder_name)
    print("Record folder {}".format(folder))
    pinata_resp = pinata.pin_file_to_ipfs(folder)
    print("Pinata response: {}".format(pinata_resp))

    ipfs_cid = pinata_resp["IpfsHash"]
    update_launch_trace(record_id, {'ipfs_cid': ipfs_cid})
    make_helloween_nft(customer_address=sender, launch_tx_hash=launch_event_id,
                       image_url=f"https://merklebot.mypinata.cloud/ipfs/{ipfs_cid}/{record_folder_name}/helloween.jpg")
    datalog_extrinsic_hash = record_datalog(ipfs_cid)
    update_launch_trace(record_id, {'datalog_tx_id': datalog_extrinsic_hash})

    try:
        datadog.statsd.increment("trace.bytes", int(pinata_resp["PinSize"]))
    except Exception as e:
        pass

    # Pin to Crust Network
    try:
        size = pinata_resp["PinSize"]
        crust = SubstrateInterface(
            url="wss://rpc.crust.network",
            ss58_format=66,
            type_registry_preset="crust",
        )
        call = crust.compose_call(
            call_module="Market",
            call_function="place_storage_order",
            call_params=dict(
                cid=ipfs_cid,
                reported_file_size=size,
                tips=0,
                _memo="",
            )
        )
        keypair = Keypair.create_from_mnemonic(MNEMONIC)
        extrinsic = crust.create_signed_extrinsic(
            call=call,
            keypair=keypair,
        )
        receipt = crust.submit_extrinsic(extrinsic, wait_for_finalization=True)
        update_launch_trace(record_id, {'crust_tx_id': receipt.extrinsic_hash})
    except Exception as e:
        print(f"Crust Network exception: {e=}")

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
    update_launch_trace(record_id, {'filecoin_cid': estuary_resp.json()["cid"]})

    print("Session {} trace created with IPFS CID {}".format(session_id, ipfs_cid))


class DataRecorder:
    def __init__(self, transaction, record_video=True):
        self.sender = transaction['sender']
        self.recipient = transaction['recipient']
        self.session_id = transaction['session_id']
        self.tx_id = transaction['tx_id']
        self.recorder = None
        self.video_recorder = None
        self.record_folder_name = None
        self.video_name = None
        self.created_at_str = None
        self.record_video = record_video

    def start_data_recording(self):
        self.created_at_str = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        self.record_folder_name = "user-{}-cps-{}-session-{}-{}".format(
            self.sender,
            self.recipient,
            self.session_id,
            self.created_at_str
        )

        bag_name = "state.bag"
        self.video_name = "camera.mp4"
        print("New launch, sender={}, recipient={}, session_id={}, bag={}".format(
            self.sender, self.recipient, self.session_id, bag_name))

        os.makedirs("{}/{}".format(TRACES_DIR, self.record_folder_name), exist_ok=True)

        # duration=5m limits max recoding time and prevents orphan processes keep recording forever
        self.recorder = subprocess.Popen(
            ["rosbag", "record", "--duration=5m", "--output-name={}".format(bag_name), "/tf", "/tf_static",
             "/joint_states"],
            cwd="{}/{}/".format(TRACES_DIR, self.record_folder_name),  # directory to put files
        )
        if self.record_video:
            # start recording stream from videoserver
            video_url = VIDEOSERVER_URL + "video"
            result_image_name = "result.jpg"
            result_drawing_name = "drawing.jpg"
            result_helloween_name = "helloween.jpg"
            self.video_recorder = subprocess.Popen(
                ["python3.8", "video_recorder.py", "--video_url={}".format(video_url),
                 "--output_file={}/{}/{}".format(TRACES_DIR, self.record_folder_name,
                                                 self.video_name),
                 "--last_im_file={}/{}/{}".format(TRACES_DIR, self.record_folder_name,
                                                  result_image_name),
                 "--last_drawing_file={}/{}/{}".format(TRACES_DIR, self.record_folder_name,
                                                       result_drawing_name),
                 "--helloween_drawing_file={}/{}/{}".format(TRACES_DIR, self.record_folder_name,
                                                            result_helloween_name)
                 ])

    def stop_data_recording(self):
        time.sleep(2)  # wait for the robot to finish its movement
        self.recorder.terminate()
        if self.record_video:
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
                self.record_video
            )
        ).start()
