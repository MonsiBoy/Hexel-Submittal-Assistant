from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QPainter, QColor, QPen, QMouseEvent, QGuiApplication, QCursor
from pyzbar.pyzbar import decode
from PIL import Image
from PIL.ImageQt import ImageQt
import torch
import numpy as np

from Tabs.Thread.ThreadWorker import ScanWorker


class UnifiedScanner(QWidget):
    qr_detected = Signal(str)
    text_detected = Signal(str)

    def __init__(self, mode="qr"):
        super().__init__()
        self.mode = mode  # "qr" or "text"

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(200, 150)
        self.resize(400, 300)

        screen = QGuiApplication.screenAt(QCursor.pos())
        if screen:
            screen_geometry = screen.geometry()
            center_x = screen_geometry.x() + (screen_geometry.width() - self.width()) // 2
            center_y = screen_geometry.y() + (screen_geometry.height() - self.height()) // 2
            self.move(center_x, center_y)

        self._drag_pos = None
        self._resizing = False
        self._resize_margin = 8
        self._resize_direction = None

        self.setMouseTracking(True)

    def getScanner(self):
        return self

    def trigger_text_scan(self, engine="EasyOCR"):
        if self.mode != "text":
            return

        image = self._capture_screen_area()
        if image is None:
            return

        # Threaded OCR using ScanWorker
        self.thread = QThread()
        self.worker = ScanWorker(image, engine)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.result_ready.connect(self.text_detected.emit)
        self.worker.error.connect(lambda msg: print(f"❌ Error: {msg}"))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def scan_area(self, engine="EasyOCR"):
        image = self._capture_screen_area()
        if image is None:
            return

        if self.mode == "qr":
            results = decode(image)
            for result in results:
                self.qr_detected.emit(result.data.decode("utf-8"))

        elif self.mode == "text" and engine == "EasyOCR":
            from easyocr import Reader
            reader = Reader(["en"], gpu=torch.cuda.is_available())
            result = reader.readtext(np.array(image))
            text = "\n".join([item[1] for item in result])
            if text.strip():
                self.text_detected.emit(text)

    def _capture_screen_area(self):
        global_pos = self.mapToGlobal(self.rect().topLeft())
        screen = QGuiApplication.screenAt(global_pos)

        if not screen:
            print("⚠️ Could not detect screen for this widget.")
            return None

        # DPI check
        logical_dpi = screen.logicalDotsPerInch()
        physical_dpi = screen.physicalDotsPerInch()
        if int(logical_dpi) != int(physical_dpi):
            print(f"⚠️ DPI Scaling Detected! Logical: {logical_dpi}, Physical: {physical_dpi}\n⚠️ Please ensure all displays are set to 100% scaling for accurate scanning.")

        x = global_pos.x()
        y = global_pos.y()
        w = self.width()
        h = self.height()

        try:
            pixmap = screen.grabWindow(0, x, y, w, h)
            return Image.fromqimage(pixmap.toImage())
        except Exception as e:
            print(f"❌ Failed to capture screen: {e}")
            return None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 50))
        pen = QPen(QColor(0, 255, 0), 3)
        painter.setPen(pen)
        painter.drawRect(10, 10, self.width() - 20, self.height() - 20)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            self._resize_direction = self._get_resize_direction(event.pos())
            self._resizing = bool(self._resize_direction)
            self._moving = not self._resizing
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._resizing:
            self._resize_window(event.globalPosition().toPoint())
        elif self._drag_pos and not self._resize_direction:
            self.move(self.pos() + event.globalPosition().toPoint() - self._drag_pos)
            self._drag_pos = event.globalPosition().toPoint()
        else:
            self._update_cursor(event.pos())
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self._resizing = False
        self._moving = False
        self._drag_pos = None
        self._resize_direction = None
        self.setCursor(Qt.ArrowCursor)

    def _update_cursor(self, pos):
        direction = self._get_resize_direction(pos)
        cursors = {
            "left": Qt.SizeHorCursor,
            "right": Qt.SizeHorCursor,
            "top": Qt.SizeVerCursor,
            "bottom": Qt.SizeVerCursor,
            "top_left": Qt.SizeFDiagCursor,
            "bottom_right": Qt.SizeFDiagCursor,
            "top_right": Qt.SizeBDiagCursor,
            "bottom_left": Qt.SizeBDiagCursor,
        }
        self.setCursor(cursors.get(direction, Qt.ArrowCursor))

    def _get_resize_direction(self, pos):
        x, y, w, h = pos.x(), pos.y(), self.width(), self.height()
        m = self._resize_margin

        if y <= m and x <= m:
            return "top_left"
        if y <= m and x >= w - m:
            return "top_right"
        if y >= h - m and x <= m:
            return "bottom_left"
        if y >= h - m and x >= w - m:
            return "bottom_right"
        if y <= m:
            return "top"
        if y >= h - m:
            return "bottom"
        if x <= m:
            return "left"
        if x >= w - m:
            return "right"
        return None

    def _resize_window(self, global_pos):
        delta = global_pos - self._drag_pos
        rect = self.geometry()
        direction = self._resize_direction

        if "left" in direction:
            rect.setLeft(rect.left() + delta.x())
        if "right" in direction:
            rect.setRight(rect.right() + delta.x())
        if "top" in direction:
            rect.setTop(rect.top() + delta.y())
        if "bottom" in direction:
            rect.setBottom(rect.bottom() + delta.y())

        self.setGeometry(rect.normalized())
        self._drag_pos = global_pos
