import stat
import os
import time
import stat
import platform
import socket
import re
import uuid
import psutil

"""
    UNIX system only
"""

def get_file_properties(file_path):
    """
    # Hàm này nhận đường dẫn tới một tệp và trả về các thuộc tính của tệp đó.
    :return:
    """
    _stat = os.stat(file_path) # lấy thông tin về tệp được chỉ định bởi file_path và lưu vài biến _stat
    message = []

    def _get_file_mode(): # hàm sử dụng các hằng số của module stat và các phép toán bitwise để kiểm tra các bit quyền truy cập của tệp.
        modes = [
            stat.S_IRUSR,  # ~ Owner has read permission.
            stat.S_IWUSR,  # ~ Owner has write permission.
            stat.S_IXUSR,  # ~ Owner has execute permission.
            stat.S_IRGRP,  # ~ Group has read permission.
            stat.S_IWGRP,  # ~ Group has write permission
            stat.S_IXGRP,  # ~ Group has execute permission.
            stat.S_IROTH,  # ~ Others have read permission.
            stat.S_IWOTH,  # ~ Others have write permission.
            stat.S_IXOTH,  # ~ Others have execute permission.
        ]

        mode = _stat.st_mode
        full_mode = ""
        full_mode += "d" if os.path.isdir(file_path) else "-"

        for i in range(9):
            full_mode += bool(mode & modes[i]) and 'rwxrwxrwx'[i] or '-'
        return full_mode


    def _get_size(): # Trả về kích thước của tệp theo byte dưới dạng chuỗi.
        return str(_stat.st_size)

    def _get_last_time(): # Trả về thời gian sửa đổi cuối cùng của tệp dưới dạng chuỗi đã định dạng.
        return time.strftime("%b %d %H:%M", time.gmtime(_stat.st_mtime))

    # lặp qua ba hàm nội bộ trên, in kết quả của chúng và thêm vào một danh sách gọi là message.
    for function in ("_get_file_mode()", "_get_size()", "_get_last_time()"):
        print(eval(function))
        message.append(eval(function))

    # Thêm tên cơ bản của tệp (không bao gồm đường dẫn) vào danh sách message.
    message.append(os.path.basename(file_path))
    # dùng join để nối các pt trong ds message và trả về 1 chuỗi thuộc tính tệp
    return " ".join(message)


def get_sys_info():
    """
    # Hàm thu thập thông tin về hệ thống (chủ yếu là cho máy chủ đang chạy).
    :return:
    """
    try:
        # tạo 1 dictionary info với các thông tin liên quan đến hệ thống
        info = {'platform': platform.system(),
                'platform-release': platform.release(),
                'platform-version': platform.version(),
                'architecture': platform.machine(),
                'hostname': socket.gethostname(),
                'ip-address': socket.gethostbyname(socket.gethostname()),
                'mac-address': ':'.join(re.findall('..', '%012x' % uuid.getnode())),
                'processor': platform.processor(),
                'ram': str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"}

        return info
    except Exception as e:
        print(e)
