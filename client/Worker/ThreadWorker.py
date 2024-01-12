import time
import sys
import traceback

from PyQt5.QtCore import Qt, QThread, QRunnable, pyqtSlot, QObject, pyqtSignal


class ThreadWorker(QRunnable): #Là một worker thread cơ bản, thừa kế từ QRunnable của PyQt5.
    """
    Worker Thread
    """

    @pyqtSlot()
    def run(self):
        print("Thread started")
        time.sleep(6)
        print("Thread stop")


class WorkerSignals(QObject): # Là một lớp QObject để định nghĩa các tín hiệu (signals) mà worker thread có thể phát ra.
    """
    Xác định các tín hiệu có sẵn từ một luồng công việc đang chạy.

    Các tín hiệu được hỗ trợ là:
        finished
            Không có dữ liệu

        error
            bộ dữ liệu (loại exc, giá trị, traceback.format_exc())

        Result
            dữ liệu đối tượng được trả về từ quá trình xử lý, bất cứ thứ gì

        progress
            dữ liệu hiện tại (Tải xuống/tải lên)
    """

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int, str)


class DownloadWorker(QRunnable): #Là một worker thread được thiết kế để thực hiện tác vụ download
    """
    Download worker thread
    """

    def __init__(self, file_name, file_size, source_file, destination_file, ftp, *args, **kwargs):
        super(DownloadWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.file_name = file_name
        self.file_size = file_size
        self.source_file = source_file
        self.destination_file = destination_file
        self.ftp = ftp
        # Signal
        self.signals = WorkerSignals()
        self.kwargs["progress_callback"] = self.signals.progress

    @pyqtSlot()
    def run(self):
        """
            Thực hiện quá trình download bằng cách sử dụng ftp.retrbinary và gọi callback function để ghi dữ liệu vào tập tin đích
        """
        try:
            with open(self.destination_file, "wb") as file:
                def callback(data):
                    file.write(data)
                    self.signals.progress.emit(len(data), self.source_file)

                self.ftp.retrbinary("RETR " + self.file_name, callback=callback)

            self.ftp.quit()
        except Exception as e:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()

class UploadWorker(QRunnable): #  là một worker thread được thiết kế để thực hiện tác vụ upload.
    """
    Upload worker thread
    """

    def __init__(self, file_name, file_size, source_file, destination_file, ftp, *args, **kwargs):
        super(UploadWorker, self).__init__()
        self.args = args
        self.kwargs = kwargs
        self.file_name = file_name
        self.file_size = file_size
        self.source_file = source_file
        self.destination_file = destination_file
        self.ftp = ftp
        # Signal
        self.signals = WorkerSignals()
        self.kwargs["progress_callback"] = self.signals.progress

    @pyqtSlot()
    def run(self): # thực hiện quá trình upload bằng cách sử dụng ftp.storbinary và gọi callback function để đọc dữ liệu từ tập tin nguồn.
        try:
            with open(self.source_file, "rb") as file:
                def callback(data):
                    self.signals.progress.emit(len(data), self.source_file)

                self.ftp.storbinary("STOR " + self.file_name, fp=file, callback=callback)

            self.ftp.quit()
        except Exception as e:
            print(e)
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()
