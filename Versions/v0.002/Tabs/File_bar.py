from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QAction, QFileDialog
import path

class FileBar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
            # Create Menu Bar
        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu("File")

            # File → Open
        open_action = QAction("Open PDF", self)
        open_action.triggered.connect(self.open_pdf)
        self.file_menu.addAction(open_action)

            # File → Save As
        save_action = QAction("Save As...", self)
        save_action.triggered.connect(self.save_pdf)
        self.file_menu.addAction(save_action)

            # File → Exit
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)  
   
    def open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open PDF", str(Path.home()), "PDF Files (*.pdf);;All Files (*)"
        )
        if path:
            self.bookmark_tab.local_path = path
            self.bookmark_tab.populate_tree_items()

    def save_pdf(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF With Bookmarks",
            str(Path.home() / "with_bookmarks.pdf"),
            "PDF Files (*.pdf);;All Files (*)"
        )
        if path:
            self.bookmark_tab.output_pdf(self.bookmark_tab.structure, path)
