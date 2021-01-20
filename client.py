import socket
import threading
import time
from uuid import uuid4

from command import CommandManager


class Client(threading.Thread, CommandManager):
    def __init__(self, host: str, port: int):
        super().__init__()
        self.current_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.current_socket.connect((host, port))
        self.name = uuid4().hex[:5]
        print('Connected')

    def run(self):
        while self.keep_connection:
            print(self.current_socket.recv(2048).decode())

    def send_message(self, msg):
        command = 'message_server'
        if msg.startswith('$'):
            command = msg.split('$')[-1]
        self.send_server(self.name, command, msg)

    def connection(self):
        self.send_server(self.name, 'connection_client', '')

    def send_server(self, name, command: str, body: str):
        command_msg = '{}:{}>{}'.format(name, command, body)
        self.current_socket.send(command_msg.encode())
        self.parse_message(command_msg)


if __name__ == '__main__':
    client = Client(host='127.0.0.1', port=1234)
    client.connection()
    client.start()

    while client.keep_connection:
        time.sleep(2)
        message = input('Message : ')
        client.send_message(message)
