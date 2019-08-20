#!/usr/bin/env python

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:7999"
    async with websockets.connect(uri) as websocket:
        message = "AAPH,80020001,1234,Hello world"
        await websocket.send(message)
        print(f"Client > {message}")
        greeting = await websocket.recv()
        print(f"Server < {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
