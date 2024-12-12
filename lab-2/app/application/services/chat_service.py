import threading
import random
import time
import json
from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from threading import Lock
import logging

# Configure logging for the application
logging.basicConfig(level=logging.INFO)

class ChatService:
    def __init__(self):
        self.active_connections: dict = {}
        self.lock = Lock()

    async def connect_to_room(self, websocket: WebSocket, room: str):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)
        logging.info(f"WebSocket connection established in room: {room}")
    
    async def disconnect_from_room(self, websocket: WebSocket, room: str):
        self.active_connections[room].remove(websocket)
        if not self.active_connections[room]:
            del self.active_connections[room]
        logging.info(f"WebSocket disconnection from room: {room}")

    async def handle_messages(self, websocket: WebSocket, room: str):
        try:
            while True:
                data = await websocket.receive_text()
                logging.info(f"Received data: {data}")

                # Process each command in a separate thread
                thread = threading.Thread(target=self.process_command, args=(data,))
                thread.start()

                await self.broadcast_message(data, websocket, room)
        except WebSocketDisconnect:
            await self.disconnect_from_room(websocket, room)

    async def broadcast_message(self, message: str, websocket: WebSocket, room: str):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                if connection != websocket:
                    await connection.send_text(f"Room {room}: {message}")

    def process_command(self, command: str):
        with self.lock:
            time.sleep(random.randint(1, 7))  # Random delay to simulate computation
            with open("chat_log.txt", "a") as f:
                f.write(f"Processed command: {command}\n")
            logging.info(f"Processed command: {command}")