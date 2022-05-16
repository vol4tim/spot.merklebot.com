import uvicorn, asyncio, cv2
from vidgear.gears.asyncio import WebGear
from vidgear.gears.asyncio.helper import reducer
from detect import process_frame
from collections import deque
import numpy as np
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

# initialize WebGear app without any source
web = WebGear(logging=True)

TOKEN = "efbuhuj2n3f23cwt2"

cur_points = deque(maxlen=512)
segments = []
draw_line = False


async def frame_producer():
    global cur_points, draw_line
    stream = cv2.VideoCapture(0)
    stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        (grabbed, frame) = stream.read()
        if not grabbed:
            break

        frame = await reducer(frame, percentage=30, interpolation=cv2.INTER_AREA)  # reduce frame by 30%

        frame, obj = process_frame(frame)
        if obj and draw_line:
            cur_points.appendleft(obj)

        for segment_points in segments + [cur_points]:
            for i in range(1, len(segment_points)):
                if segment_points[i - 1] is None or segment_points[i] is None:
                    continue
                cv2.line(frame, segment_points[i - 1], segment_points[i], (0, 0, 255), 2)

        encodedImage = cv2.imencode(".jpg", frame)[1].tobytes()
        yield (b"--frame\r\nContent-Type:image/jpeg\r\n\r\n" + encodedImage + b"\r\n")
        await asyncio.sleep(0)
    stream.release()


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


async def clear_canvas(request: Request):
    global segments
    global cur_points
    data = await request.json()
    if data['token'] != TOKEN:
        return JSONResponse({"status": "error", "message": "Invalid token"})

    segments = []
    cur_points = deque(maxlen=512)
    return JSONResponse({"status": "ok"})


async def start_line(request: Request):
    global draw_line
    global segments
    global cur_points
    data = await request.json()
    if data['token'] != TOKEN:
        return JSONResponse({"status": "error", "message": "Invalid token"})

    cur_points = deque(maxlen=512)
    draw_line = True
    return JSONResponse({"status": "ok"})


async def stop_line(request: Request):
    global draw_line
    global segments
    global cur_points
    data = await request.json()
    if data['token'] != TOKEN:
        return JSONResponse({"status": "error", "message": "Invalid token"})
    segments += [cur_points]
    cur_points = deque(maxlen=512)
    draw_line = False
    return JSONResponse({"status": "ok"})


web.routes.append(Route("/clear_canvas", endpoint=clear_canvas, methods=["POST"]))
web.routes.append(Route("/start_line", endpoint=start_line, methods=["POST"]))
web.routes.append(Route("/stop_line", endpoint=stop_line, methods=["POST"]))

# run this app on Uvicorn server at address http://localhost:8000/
uvicorn.run(web(), host="0.0.0.0", port=8000)

# close app safely
web.shutdown()
