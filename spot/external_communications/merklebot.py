import requests


def create_launch_trace(sender, session_id, created_at_str, launch_event_id):
    res = requests.post("https://api.merklebot.com/robonomics-launch-traces", json={
        "sender": sender,
        "nonce": session_id,
        "created_at": created_at_str,
        "launch_tx_id": launch_event_id,
    })
    return res.json()


def create_halloween_nft_order(customer_address: str, launch_tx_hash: str, image_url: str):
    res = requests.post(f"https://api.merklebot.com/spot-demo/nft/orders", json={
        "customer_account_address": customer_address,
        "robot_launch_extrinsic_hash": launch_tx_hash,
        "image_url": image_url
    })
    return res.json()


def update_launch_trace(launch_id, new_data):
    requests.patch(f"https://api.merklebot.com/robonomics-launch-traces/{launch_id}", json=new_data)
