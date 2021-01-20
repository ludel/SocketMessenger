from socket import socket


class CommandManager:
    current_socket: socket
    keep_connection: bool = True
    name: str

    def parse_message(self, msg):
        meta, body_msg = msg.split('>')
        client_id, command = meta.split(':')
        getattr(self, '_{}'.format(command), self.unknown_command)(client_id, body_msg, command)

    def _close(self, *args):
        print('Close connection')
        self.keep_connection = False
        self.current_socket.close()

    @staticmethod
    def unknown_command(*args):
        pass
