from PySide6.QtCore import QThread, Signal
from PySide6.QtCore import QObject, Signal, Slot, QThread
from Tabs.operations.Bookmark_Maker import BookMark

class WorkerThread(QThread):
    finished = Signal(object)
    progress = Signal(int)

    def __init__(self, file_path, mode):
        super().__init__()
        self.file_path = file_path
        self.mode      = mode

    @Slot()
    def run(self):
        def report_progress(value):
            self.progress.emit(value)
        
        bookmaker = BookMark()

        if self.mode == 1:
            result = bookmaker.read_pdf(self.file_path, progress_callback=report_progress)
            self.finished.emit(result)

        elif self.mode == 2:
            result = bookmaker.bookmark_gen(self.file_path, progress_callback=report_progress)
            self.finished.emit(result)

        elif self.mode == 3:
            bookmarks = bookmaker.read_pdf(self.file_path, progress_callback=report_progress)
            generated = bookmaker.bookmark_gen(self.file_path, progress_callback=report_progress)
            self.finished.emit((bookmarks, generated))

        else:
            # Send an error or None to indicate the mode is invalid
            self.finished.emit(None)


class ScanWorker(QObject):
    result_ready = Signal(str)
    error = Signal(str)
    finished = Signal()

    def __init__(self, image, mode):
        super().__init__()
        self.image = image
        self.mode = mode

    @Slot()
    def run(self):
        try:
            from easyocr import Reader
            import numpy as np
            import torch

            device = torch.cuda.is_available()
            reader = Reader(['en'], gpu=device)

            img_np = np.array(self.image)
            result = reader.readtext(img_np)
            text = "\n".join([r[1] for r in result])
            self.result_ready.emit(text)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()
