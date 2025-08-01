import asyncio
import os
from aiohttp import web

LOG_FILE = "log.txt"

async def handle_websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    with open(LOG_FILE, "rb") as f:
        f.seek(0, os.SEEK_END)
        size = f.tell()
        f.seek(max(size - 1024, 0))
        lines = f.readlines()[-10:]
        for line in lines:
            await ws.send_str(line.decode())

    with open(LOG_FILE, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                await ws.send_str(line)
            else:
                await asyncio.sleep(1)

    return ws

async def serve_html(request):
    return web.FileResponse("client/index.html")

app = web.Application()
app.router.add_get("/log", serve_html)
app.router.add_get("/ws", handle_websocket)

web.run_app(app, port=5000)
