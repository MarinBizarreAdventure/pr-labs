from fastapi import APIRouter, Depends, WebSocket
from app.domain.security.jwt_utils import get_current_user
from app.application.services.chat_service import ChatService
import logging
import socket
import threading, time, random


class ChatRouter:
    def __init__(self, chat_service: ChatService):
        self.router = APIRouter()
        self.chat_service = chat_service
        self.setup_routes()

    def setup_routes(self):
        @self.router.websocket("/ws/{room}")
        async def chat_websocket(websocket: WebSocket, room: str):
            await self.chat_service.connect_to_room(websocket, room)
            await self.chat_service.handle_messages(websocket, room)



logging.basicConfig(level=logging.INFO)

file_lock = threading.Lock()
coordination_lock = threading.Lock()
write_completion_event = threading.Event()

def tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9090))
    server_socket.listen()
    logging.info("TCP server started on port 9090...")

    while True:
        client_socket, addr = server_socket.accept()
        logging.info(f"New client connected from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()


def handle_client(client_socket):
    with client_socket:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode()
            logging.info(f"Received message via TCP: {message}")

            if message.lower().startswith("write"):
                threading.Thread(target=process_write_command, args=(message,)).start()
            elif message.lower().startswith("read"):
                logging.info("Waiting for all writes to complete before reading...")
                coordination_lock.acquire()
                threading.Thread(target=process_read_command).start()
                coordination_lock.release()
            else:
                logging.warning("Unknown command received")

def process_write_command(command):
    with file_lock:
        logging.info(f"Processing write command: {command}")
        time.sleep(random.randint(1, 7))  
        with open("shared_file.txt", "a") as f:
            f.write(f"{command}\n")
        logging.info(f"Write command completed: {command}")
    write_completion_event.set() 

def process_read_command():
    write_completion_event.wait()  
    with file_lock:
        logging.info("Processing read command")
        time.sleep(random.randint(1, 7)) 
        with open("shared_file.txt", "r") as f:
            contents = f.read()
        logging.info("Read contents from shared file")
        print(f"Contents of the file:\n{contents}")