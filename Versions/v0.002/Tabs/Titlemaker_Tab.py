from PySide6.QtWidgets import (
    QGridLayout, QApplication, QMainWindow, QTabWidget, QWidget,
    QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout,
    QFileDialog, QTreeWidget, QTreeWidgetItem, QAbstractItemView, 
    QMenu, QProgressBar, QCheckBox, QGroupBox, QMessageBox,
    QLineEdit, QDialog, 
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QThread, Signal


class TitleMaker(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        self.temp = self.create_Main()
        layout.addWidget(self.temp,alignment = Qt.AlignCenter)
        self.setLayout(layout)



    def create_Main(self):
        label = QLabel("🚧 Under Construction 🚧")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                background-color: #FFD700;
                color: black;
                font-size: 24px;
                font-weight: bold;
                border: 2px dashed black;
                padding: 40px;
                margin: 20px;
            }
        """)
        return label