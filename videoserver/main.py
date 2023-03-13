import multiprocessing

import uvicorn, asyncio, cv2
from vidgear.gears.asyncio import WebGear
from vidgear.gears.asyncio.helper import reducer
from detect import process_frame
from collections import deque
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.responses import StreamingResponse

import os, io
import numpy as np
from dotenv import load_dotenv
import pyfakewebcam
import hashlib
import datetime
from substrateinterface import Keypair, KeypairType

from camera_control import CameraControl

load_dotenv()

TOKEN = os.environ.get('VIDEOSERVER_TOKEN', "token")  # token to access this server's drawing functions

PROCESSES = []

SPOT_MOVING = os.getenv("SPOT_MOVING", 0)
FOLLOW_SPOT = os.getenv('FOLLOW_SPOT', 0)
DETECT_SPOT = os.getenv('DETECT_SPOT', 1)
FAKE_CAMERA = os.getenv('FAKE_CAMERA', '/dev/video2')
AUTH_SECRET = os.getenv('AUTH_SECRET', 'abcdefg')
ADMIN_WALLETS = os.getenv('ADMIN_WALLETS', '4HY2Mb4fpsyz6vyWHd3xGPgnHC983junioxhT2Cnfa5Kok5b').split(',')


def generate_auth_token(account):
    today = datetime.datetime.now().date()
    token = hashlib.sha1((AUTH_SECRET + str(today) + account).encode()).hexdigest()
    return token


def verify_token_sign(address, token, signed_token):
    keypair_public = Keypair(ss58_address=address,
                             crypto_type=KeypairType.SR25519)
    is_verified = keypair_public.verify(token, signed_token)
    return is_verified


def run_server(im, state):
    async def frame_producer():
        while True:
            frame, obj = im[0], im[1]

            frame = await reducer(frame, percentage=40, interpolation=cv2.INTER_AREA)  # reduce frame by 30%

            encodedImage = cv2.imencode(".jpg", frame)[1].tobytes()
            yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
            await asyncio.sleep(0.033)
        stream.release()

    async def stream_blackboard(request: Request):
        cv2img = im[2]
        res, im_jpeg = cv2.imencode(".jpeg", cv2img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        return StreamingResponse(io.BytesIO(im_jpeg.tobytes()), media_type="image/jpeg")

    async def clear_canvas(request: Request):
        data = await request.json()
        if data['token'] != TOKEN:
            return JSONResponse({"status": "error", "message": "Invalid token"})

        state['segments'] = []
        state['cur_points'] = []
        return JSONResponse({"status": "ok"})

    async def start_line(request: Request):
        data = await request.json()
        if data['token'] != TOKEN:
            return JSONResponse({"status": "error", "message": "Invalid token"})
        state['cur_points'] = []
        state['draw_line'] = True

        return JSONResponse({"status": "ok"})

    async def stop_line(request: Request):
        data = await request.json()
        if data['token'] != TOKEN:
            return JSONResponse({"status": "error", "message": "Invalid token"})
        state['segments'] += [state['cur_points']]
        state['cur_points'] = []
        state['draw_line'] = False
        return JSONResponse({"status": "ok"})

    async def get_obj_coords(request: Request):
        data = await request.json()
        if data['token'] != TOKEN:
            return JSONResponse({"status": "error", "message": "Invalid token"})
        return JSONResponse({"status": "ok", "coords": state['obj_coords']})

    async def get_auth_token(request: Request):
        data = await request.json()
        account = data['account']
        token = generate_auth_token(account)

        return JSONResponse({"status": "ok", "token": token})

    async def control_camera(request: Request):
        data = await request.json()
        account = data['account']
        signed_token = data['signed_token']
        token = generate_auth_token(account)
        is_verified = verify_token_sign(account, token, signed_token)
        if not is_verified:
            return JSONResponse({"status": "wrong signature"})
        if account not in ADMIN_WALLETS:
            return JSONResponse({"status": "no access"})

        camera_control = CameraControl()
        if data['control_name'] == 'move':
            camera_control.move(data['velocity'])
        elif data['control_name'] == 'zoom':
            camera_control.set_zoom(data['zoom_absolute'])

        return JSONResponse({"status": "ok"})

    web = WebGear(logging=True)

    web.middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    web.config["generator"] = frame_producer

    web.routes.append(Route("/clear_canvas", endpoint=clear_canvas, methods=["POST"]))
    web.routes.append(Route("/start_line", endpoint=start_line, methods=["POST"]))
    web.routes.append(Route("/stop_line", endpoint=stop_line, methods=["POST"]))
    web.routes.append(Route("/get_spot_face_coords", endpoint=get_obj_coords, methods=["GET"]))
    web.routes.append(Route("/token", endpoint=get_auth_token, methods=["GET", "POST"]))
    web.routes.append(Route("/control", endpoint=control_camera, methods=["POST"]))
    web.routes.append(Route("/blackboard", endpoint=stream_blackboard, methods=["GET"]))

    uvicorn.run(web(), host="0.0.0.0", port=8000)

    web.shutdown()


def run_camera(im, state):
    stream = cv2.VideoCapture(0)
    stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera_control = CameraControl()
    camera_control.set_zoom(173)

    fake_camera = pyfakewebcam.FakeWebcam(FAKE_CAMERA, 1280, 720)

    while True:
        (grabbed, frame) = stream.read()
        if not grabbed:
            break

        # frame = await reducer(frame, percentage=30, interpolation=cv2.INTER_AREA)  # reduce frame by 30%
        spot_coords = {}
        obj = None
        if DETECT_SPOT:
            frame, obj = process_frame(frame)

        if SPOT_MOVING and obj:
            spot_coords['x'] = obj[0]
            spot_coords['y'] = obj[1]

        if spot_coords:
            # print(f"Found spot = {spot_coords['x']}, {spot_coords['y']}")
            if FOLLOW_SPOT:
                # print("Following spot")
                vel = {
                    'x': 0,
                    'y': 0
                }
                frame_center_x = frame.shape[1] // 2
                frame_center_y = frame.shape[0] // 2
                x_diff = spot_coords['x'] - frame_center_x
                y_diff = spot_coords['y'] - frame_center_y
                if x_diff > 200:
                    vel['x'] = 1
                elif x_diff < -200:
                    vel['x'] = -1
                if y_diff > 100:
                    vel['y'] = -1
                elif y_diff < -100:
                    vel['y'] = 1
                # print(f"x_diff = {x_diff}, y_diff = {y_diff}")
                camera_control.move(vel, time_interval=0.05)

        blackboard = np.zeros(frame.shape, np.uint8)
        # blackboard[:] = (255, 255, 255)
        if obj:
            state['obj_coords'] = obj.copy()
        if obj and state['draw_line']:
            state['cur_points'] = [obj.copy()] + state['cur_points']
        for segment_points in state['segments'] + [state['cur_points']]:
            for i in range(1, len(segment_points)):
                if segment_points[i - 1] is None or segment_points[i] is None:
                    continue
                cv2.line(blackboard, segment_points[i - 1], segment_points[i], (0, 0, 255), 5)
        glow_strength = 0.6
        glow_radius = 17

        blackboard_blurred = cv2.GaussianBlur(blackboard, (glow_radius, glow_radius), 1)
        blackboard_blended = cv2.addWeighted(frame, 1, blackboard_blurred, glow_strength, 0)
        blackboard_blended = cv2.addWeighted(blackboard_blended, 1, blackboard, 1, 0)
        im_rgb = cv2.cvtColor(blackboard_blended, cv2.COLOR_BGR2RGB)

        fake_camera.schedule_frame(im_rgb)
        im[0] = blackboard_blended
        im[1] = obj
        im[2] = blackboard


def main():
    manager = multiprocessing.Manager()
    lst = manager.list()
    state = manager.dict()

    lst.append(None)
    lst.append(None)
    lst.append(None)

    state['cur_points'] = []
    state['segments'] = []
    state['obj_coords'] = [0, 0]
    state['draw_line'] = False
    server_process = multiprocessing.Process(target=run_server, args=(lst, state))
    camera_process = multiprocessing.Process(target=run_camera, args=(lst, state))

    PROCESSES.append(camera_process)
    PROCESSES.append(server_process)

    for p in PROCESSES:
        p.start()

    for p in PROCESSES:
        p.join()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        for p in PROCESSES:
            p.terminate()
