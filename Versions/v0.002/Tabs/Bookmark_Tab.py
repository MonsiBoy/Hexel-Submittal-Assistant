from PySide6.QtWidgets import (
    QGridLayout, QWidget, QLabel, QFrame, QPushButton, QHBoxLayout,
    QFileDialog, QProgressBar, QCheckBox, QGroupBox, QMessageBox,
    QLineEdit, QDialog, QVBoxLayout, QMenu
)
from PySide6.QtCore import Qt,Signal
from pathlib import Path
from Tabs.operations.Bookmark_Maker import BookMark
from Tabs.Thread.ThreadWorker import WorkerThread
from Tabs.BookmarkProp import EditBookmarkDialog
from Tabs.UI.TreeUI import BookmarkTree
from Tabs.Styles.GlobalStyle import apply_main_stylesheet

class BookmarkTab(QWidget):
    file_pick = Signal(bool)
    def __init__(self):
        super().__init__()
        self.worker = None
        self.picked_file = None
        self.read = False
        self.scan = False
        self.both = False
        self.bp1 = False
        self.bp2 = False
        self.setup_ui()

    def setup_ui(self):
        apply_main_stylesheet(self)
        

        layout = QGridLayout(self)
        self.bar = self.create_progress_bar()
        self.sidebar_frame = self.create_sidebar()
        self.tree = BookmarkTree(header_title="Bookmarks")
        self.drop_area = self.create_drop_area()
        self.option_area = self.create_option_frame()
        self.preview = self.create_PDFPreview()
        self.confirm_bypass()

        layout.addWidget(self.sidebar_frame, 0, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.tree, 0, 1, 10, 1, alignment=Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(self.preview, 0, 2, 20, 10, alignment=Qt.AlignCenter)

        layout.setRowStretch(1, 1)
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 1)

    def create_progress_bar(self):
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setFixedWidth(150)
        bar.setTextVisible(False)
        bar.setVisible(False)
        return bar

    def create_sidebar(self):
        frame = QFrame()
        frame.setFixedWidth(350)
        self.sidebar_layout = QGridLayout(frame)
        return frame

    def create_drop_area(self):
        canvas = QFrame()
        canvas.setObjectName("DropArea")
        canvas.setStyleSheet("#DropArea {background-color: white; border: 1px solid black;}")
        canvas.setFixedSize(300, 300)

        self.drop_layout = QVBoxLayout(canvas)
        self.file_label = QLabel("Drop your PDF here\nor")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.pick_file_handle)

        self.drop_layout.addSpacing(100)
        self.drop_layout.addWidget(self.file_label)
        self.drop_layout.addWidget(self.browse_button, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.drop_layout.addWidget(self.bar, alignment=Qt.AlignCenter)
        self.drop_layout.addStretch()

        self.sidebar_layout.addWidget(canvas, 0, 0, 1, 2)

        canvas.setAcceptDrops(True)
        canvas.dragEnterEvent = self.drag_enter_event
        canvas.dropEvent = self.handle_file_drop
        return canvas

    def create_option_frame(self):
        self.option_frame = QFrame()
        layout = QVBoxLayout(self.option_frame)

        container_layout = QHBoxLayout()
        container_layout.addStretch()
        container_layout.addWidget(self.option_frame)
        container_layout.addStretch()
        self.sidebar_layout.addLayout(container_layout, 1, 0, 5, 1)

        self.group_box = QGroupBox("Mode Selection")
        self.ReadOnlyCheck = QCheckBox("Read Only")
        self.ScanOnlyCheck = QCheckBox("Scan Only")
        self.ReadScanCheck = QCheckBox("Scan and Read")

        check_layout = QHBoxLayout()
        check_layout.addWidget(self.ReadOnlyCheck)
        check_layout.addWidget(self.ScanOnlyCheck)
        check_layout.addWidget(self.ReadScanCheck)
        self.group_box.setLayout(check_layout)

        self.ReadOnlyCheck.stateChanged.connect(self.update_states)
        self.ScanOnlyCheck.stateChanged.connect(self.update_states)
        self.ReadScanCheck.stateChanged.connect(self.update_states)

        self.save_group = QGroupBox("Save Destination")
        self.find_dest = QPushButton("Browse")
        self.show_dest = QLineEdit("Choose Destination Folder")
        self.show_dest.setEnabled(False)
        save_layout = QHBoxLayout()
        save_layout.addWidget(self.find_dest)
        save_layout.addWidget(self.show_dest)
        self.save_group.setLayout(save_layout)
        self.find_dest.clicked.connect(self.save_dest_handle)

        self.scan_button = QPushButton("Scan")
        self.confirm_button = QPushButton("Confirm")
        self.scan_button.clicked.connect(self.populate_tree_items)
        self.confirm_button.clicked.connect(self.produce_pdf)

        layout.addWidget(self.group_box)
        layout.addWidget(self.scan_button)
        layout.addWidget(self.save_group)
        layout.addWidget(self.confirm_button)

        self.scan_button.setEnabled(False)
        self.confirm_button.setEnabled(False)
        self.find_dest.setEnabled(False)

    def create_PDFPreview(self):
        label = QLabel("🚧 PDF Preview\nUnder Construction 🚧")
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

    def update_states(self):
        self.read = self.ReadOnlyCheck.isChecked()
        self.scan = self.ScanOnlyCheck.isChecked()
        self.both = self.ReadScanCheck.isChecked()

        self.ReadScanCheck.setEnabled(not (self.read or self.scan))
        self.ReadOnlyCheck.setEnabled(not (self.scan or self.both))
        self.ScanOnlyCheck.setEnabled(not (self.read or self.both))

        self.scan_button.setEnabled(bool((self.read or self.scan or self.both) and self.picked_file))

    def populate_tree_items(self):
        if self.worker and self.worker.isRunning():
            msg = QMessageBox()
            msg.setWindowTitle("Scan Still Running")
            msg.setText("Scanning In Progress: Please wait 😊")
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            self.browse_button.setEnabled(False)
            msg.exec()
            return

        self.bar.setVisible(True)
        self.tree.clear()
        self.browse_button.setEnabled(False)

        self.mode = 1 if self.read else 2 if self.scan else 3 if self.both else 0

        self.worker = WorkerThread(self.picked_file, self.mode)
        self.worker.finished.connect(self.on_scan_complete)
        self.worker.progress.connect(self.bar.setValue)
        self.worker.start()

    def on_scan_complete(self, data):
        self.tree.populate_items(data, mode=self.mode)
        self.bar.setVisible(False)
        self.bar.setValue(0)
        self.worker.deleteLater()
        self.worker = None

        self.browse_button.setEnabled(True)
        self.find_dest.setEnabled(True)
        self.tree.expandAll()
        self.tree.setVisible(True)
        self.structure = self.tree.refresh_structure()

    def produce_pdf(self):
        bookmaker = BookMark()
        self.structure = self.tree.refresh_structure()
        bookmaker.output_pdf(self.structure, self.picked_file, self.save_dest)

    def pick_file_handle(self):
        self.picked_file = self.browse_for_file()
        if self.picked_file:
            self.file_pick.emit(True)

    def save_dest_handle(self):
        self.save_dest = self.browse_for_path()
        self.show_dest.setText(str(self.save_dest))
        self.confirm_button.setEnabled(True)

    def browse_for_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", str(Path.home()), "PDF Files (*.pdf);;All Files (*)"
        )
        if path:
            truncated = Path(*Path(path).parts[-2:])
            self.file_name = Path(path).stem
            self.file_label.setText(f"Chosen File:\n...{truncated}")
            self.scan_button.setEnabled(bool(self.read or self.scan or self.both))
        return path

    def browse_for_path(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save as", f"{self.file_name}_withBookmarks", "PDF Files (*.pdf);;All Files (*)"
        )
        path = Path(path)
        return path.with_suffix(".pdf") if path.suffix.lower() != ".pdf" else path

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def handle_file_drop(self, event):
        for url in event.mimeData().urls():
            self.picked_file = url.toLocalFile()
            truncated = Path(*Path(self.picked_file).parts[-2:])
            self.file_name = Path(self.picked_file).stem
            self.file_label.setText(f"Dropped File:\n...{truncated}")
        self.scan_button.setEnabled(bool(self.read or self.scan or self.both))
        self.file_pick.emit(True)

    def confirm_bypass(self):
        self.tree.structure_chg.connect(self.handle_structure_ready)
        self.file_pick.connect(self.handle_file_ready)
    
    def handle_structure_ready(self,value):
        self.bp1 = value
        self.bypass_comp()
    
    def handle_file_ready(self,value):
        self.bp2 = value
        self.bypass_comp()

    def bypass_comp(self):
        if all([self.bp1, self.bp2]):
            self.confirm_button.setEnabled(True)
    
    
