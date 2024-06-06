import asyncio
import websockets 
import base64
import json 

connected_clients = {}

async def send_frames(camera_id, frame):
    if camera_id in connected_clients:
        encoded_frame = base64.b64decode(frame).decode('utf-8')
        await asyncio.gather(*(client.send(encoded_frame) for client in connected_clients[camera_id]))

async def handler(websocket, path):
    async for message in websocket:
        camera_id=message
        if camera_id not in connected_clients:
            connected_clients[camera_id] = set()
        connected_clients[camera_id].add(websocket)

        try:
            await websocket.wait_closed()
        finally:
            connected_clients[camera_id].remove(websocket)

start_server = websockets.serve(handler, "localhost", 3001)

async def cors_wrapper(websocket, path):
    origin = websocket.request_headers.get("Origin")
    if origin in ["http://localhost:3000"]: 
        response = await handler(websocket, path)

        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        return response
    else:
        return websockets.Response(status=403)

start_server = websockets.serve(cors_wrapper, "localhost", 3001)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()