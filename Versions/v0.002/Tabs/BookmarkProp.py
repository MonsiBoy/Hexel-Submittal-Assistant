from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QPushButton, QGridLayout
from PySide6.QtCore import Qt

class EditBookmarkDialog(QDialog):
    def __init__(self, title: str, page: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Bookmark")

        # Widgets
        self.title_input = QLineEdit(title)
        self.page_input = QSpinBox()
        self.page_input.setRange(1, 99999999)
        self.page_input.setValue(page)

        # Layout
        layout = QGridLayout()

        layout.addWidget(QLabel("Property"), 0,0)
        layout.addWidget(QLabel("Value"), 0,1)

        layout.addWidget(QLabel("Bookmark Title:"), 1,0)
        layout.addWidget(self.title_input, 1,1)

        layout.addWidget(QLabel("Page Number:"), 2,0)
        layout.addWidget(self.page_input, 2,1)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout, 3,0, 1,2, alignment =  Qt.AlignHCenter)
        self.setLayout(layout)

    def get_values(self):
        return self.title_input.text(), self.page_input.value()