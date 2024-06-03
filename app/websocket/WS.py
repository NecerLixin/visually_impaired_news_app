import asyncio
import websockets

class WS:
    async def handler(self,websocket, path):
        print(f"Client connected from {websocket.remote_address}")
        try:
            async for message in websocket:
                print(f"Received message from client: {message}")
                response = f"Echo: {message}"
                await websocket.send(response)
                print(f"Sent response to client: {response}")
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Client disconnected: {e}")

    async def main(self):
        server = await websockets.serve(self.handler, "localhost", 8765)
        print("WebSocket server started on ws://localhost:8765")
        await server.wait_closed()
ws = WS()
if __name__ == "__main__":
    # asyncio.run(main())
    ws = WS()
    asyncio.run(ws.main())
    
