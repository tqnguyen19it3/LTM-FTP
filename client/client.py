import socket

from PyQt5 import QtWidgets
import sys
from Worker.CommandLineWorker import CommandLineWorker
from GUI.ClientGUI import ClientGUI


def command_line():
    server_ip = input("Server ip: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Tạo một đối tượng socket truyền vào các hằng số mạng tương ứng (IPv4 và hằng số truyền tải theo định dạng luồng)
    client.connect((server_ip, 21)) # Kết nối với server thông qua địa chỉ IP và cổng (21) 
    print("Connect successfully!")

    handler = CommandLineWorker(client)
    handler.start() # bắt đầu thực thi worker để xử lý các lệnh từ command line


def gui(): # Tạo và Hiển Thị Cửa Sổ GUI
    app = QtWidgets.QApplication(sys.argv)

    window = ClientGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    gui()
