import sys
import socket
from settings import PORT
from functools import partial
import datetime
import os
from Worker.ServerWorker import ServerWorker
from Worker.UserWorker import get_all_user, delete_user
from Worker.UserWorker import create_user, update_user, check_user
class GuiRunner():
    """
    Start server worker thread
    """
    clients = []
    is_kill = False

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = None


    def run(self):
        while not self.is_kill:
            print("[SERVER] Starting...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            print("[SERVER] Server started, listening on {}".format(self.socket.getsockname()))
            self.socket.listen(5)
            while not self.is_kill:
                try:
                    client_socket, address = self.socket.accept()
                except OSError:
                    break
                # print("Accept")
                handler = ServerWorker(address=address, socket=client_socket, host=self.host)
                handler.start()

                self.clients.append(handler)
                # print("[SERVER] New connection from {}".format(address))
                print("[SERVER] New connection from {}".format(address))
                if self.is_kill:
                    break

    def stop(self):
        self.is_kill = True
        self.socket.close()
        # self.requestInterruption()
        for client in self.clients:
            client.terminate()
        print("[SERVER] Server stopped!")
        # self.terminate()


if __name__ == '__main__':
    server_gui = GuiRunner('192.168.1.4', 21)
    server_gui.run()
