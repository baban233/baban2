import asyncio
import base64
import mss
import numpy as np
import cv2
import websockets

# Ersetze hier mit deiner Render-URL, z.B. wss://deinprojekt.onrender.com/socket.io/?EIO=4&transport=websocket
WS_URI = "wss://baban2.onrender.com/socket.io/?EIO=4&transport=websocket"

async def send_screen():
    async with websockets.connect(WS_URI) as websocket:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            while True:
                img = np.array(sct.grab(monitor))
                _, jpeg = cv2.imencode('.jpg', img[..., :3])
                frame_b64 = base64.b64encode(jpeg.tobytes()).decode('utf-8')
                await websocket.send(frame_b64)
                await asyncio.sleep(0.05)  # ca. 20 FPS

asyncio.run(send_screen())
