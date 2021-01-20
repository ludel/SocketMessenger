import socket
import threading

from command import CommandManager


class Server(threading.Thread, CommandManager):
    def __init__(self, host, port):
        super(Server, self).__init__()

        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_sock.bind((host, port))
        self.tcp_sock.listen(10)

        self.current_socket, (self.ip, self.port) = self.tcp_sock.accept()
        self.client_connected = []
        self.name = 'server'

    def run(self):
        while self.keep_connection:
            msg = self.current_socket.recv(2048).decode()
            self.parse_message(msg)

    def _connection_client(self, client_id, *args):
        print('New user connected : {}'.format(client_id))
        self.client_connected.append(client_id)

    def _message_server(self, client_id, body, *args):
        msg = '<User {}> {}'.format(client_id, body)
        print(msg)
        self.current_socket.sendall(msg.encode())


if __name__ == '__main__':
    print('Staring server ...')
    server = Server(host='127.0.0.1', port=1234)
    server.start()
