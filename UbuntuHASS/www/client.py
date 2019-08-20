#!/usr/bin/env python

# WS client example

import asyncio
import websockets
import sys

message = sys.argv[1]
async def hello():
    uri = "ws://localhost:7999"
    async with websockets.connect(uri) as websocket:
        #name = input("What's your name? ")

        #await websocket.send(name)
        print("Client send: " + message)
        await websocket.send(message)
        print(f"Client > {message}")

        greeting = await websocket.recv()
        print(f"Server < {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
#asyncio.get_event_loop().run_forever()
