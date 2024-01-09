import os
import logging
import socket
import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication

from GUI.ServerGUI import ServerGUI
from settings import *
from Worker.ServerWorker import ServerWorker

# lấy địa chỉ IP của máy chủ và lưu vào biến HOST.
HOST = socket.gethostbyname(socket.gethostname())


# Start socket server
def server_listener():
    """
    # Hàm này tạo và khởi động một máy chủ socket ở địa chỉ và cổng được xác định trong file settings. Nó lắng nghe các kết nối đến và tạo một ServerWorker cho mỗi kết nối.
    """
    print('[SERVER] Starting...')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Sử dụng IPv4 và giao thức TCP
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Cấu hình socket để có thể sử dụng lại địa chỉ ngay cả khi socket đang lắng nghe.
    s.bind((HOST, PORT)) # Ghép địa chỉ và cổng vào socket.
    print("[SERVER] Server started, listening on {}".format(s.getsockname()))
    s.listen(5) # Bắt đầu lắng nghe, chấp nhận tối đa 5 kết nối đồng thời.
    print('[SERVER] Server is listening')

    while True: # Trong vòng lặp vô hạn, nó chấp nhận kết nối mới, tạo một ServerWorker cho mỗi kết nối và bắt đầu xử lý.
        client_socket, address = s.accept()
        print("Accept")
        handler = ServerWorker(address=address, socket=client_socket, host=HOST)
        handler.start()
        print("[SERVER] New connection from {}".format(address))


def gui():
    """
    # Hàm này sử dụng thư viện PyQt5 để tạo một giao diện người dùng phía sv
    """
    app = QApplication(sys.argv)
    ui = ServerGUI()
    ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # listener = Thread(target=server_listener)
    # listener.start()

    gui()
