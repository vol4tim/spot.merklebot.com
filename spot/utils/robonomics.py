import os

from substrateinterface import SubstrateInterface
import robonomicsinterface
import datadog

from settings.settings import INTERACTION_MODE
from utils.logger import logger

def get_account_nonce(address) -> int:
    substrate = SubstrateInterface(
        url="wss://kusama.rpc.robonomics.network",
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


def record_datalog(ipfs_cid):
    account = robonomicsinterface.Account(os.environ["MNEMONIC"])
    datalog = robonomicsinterface.Datalog(account)
    datalog_extrinsic_hash = datalog.record(ipfs_cid)
    return datalog_extrinsic_hash


class RobonimicsHelper:
    def __init__(self, robot_state):
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

        try:
            datadog.statsd.event(
                "Launch",
                "Launch, sender={}, nonce={}, recipient={}".format(sender, session_id, recipient),
            )
        except Exception as e:
            logger.error("Datadog statsd error: {}".format(e))

        if INTERACTION_MODE == 'drawing':
            self.robot_state['transactions'] = self.robot_state['transactions'] + [{'tx_id': launch_event_id, 'sender': sender, 'recipient': recipient, 'session_id': session_id}]
            # self.execute_drawing_command(address=sender)
        elif INTERACTION_MODE == 'movement':
            pass

        logger.info("Session {} complete, creating a trace".format(session_id))

    def start_subscriber(self):
        while True:
            try:
                logger.info("Robonomics subscriber starting...")
                account = robonomicsinterface.Account(remote_ws="wss://kusama.rpc.robonomics.network")
                robonomicsinterface.Subscriber(
                    account,
                    robonomicsinterface.SubEvent.NewLaunch,
                    self.robonomics_transaction_callback,
                    pass_event_id=True,
                    addr="4FNQo2tK6PLeEhNEUuPePs8B8xKNwx15fX7tC2XnYpkC8W1j",
                )
            except:
                logger.error("Error while connecting to robonomics, restart subscriber...")
