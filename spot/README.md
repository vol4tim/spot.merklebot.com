# Davos Spot Robot Control

## How to run

Set env variables:
``` bash
export SPOT_IP=192.168.50.3 # Ip of connected Spot robot instance
export SPOT_USERNAME=admin # username for Spot robot
export SPOT_PASSWORD=admin # password for Spot robot
export VIDEOSERVER_URL=http://10.200.0.8:8000/ # url of videoserver instance
export VIDEOSERVER_TOKEN=token # access token to control videoserver output canvas
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Run server with:
```bash
python main.py
```
