import requests


def create_launch_trace(sender, session_id, created_at_str, launch_event_id):
    res = requests.post("https://api.merklebot.com/robonomics-launch-traces", json={
        "sender": sender,
        "nonce": session_id,
        "created_at": created_at_str,
        "launch_tx_id": launch_event_id,
    })
    return res.json()


def update_launch_trace(launch_id, new_data):
    requests.patch(f"https://api.merklebot.com/robonomics-launch-traces/{launch_id}", json=new_data)
