from PySide6.QtWidgets import QGridLayout,QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QIcon
from Tabs.Bookmark_Tab import BookmarkTab
from Tabs.Titlemaker_Tab import TitleMaker
from Tabs.Tools_Tab import ToolTab
from Tabs.Utility.Utility_funcs import get_folder
import sys

class SplashScreen(QWidget):
    def __init__(self, image_path, duration=3000):
        super().__init__()
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        layout = QGridLayout()
        layout.setHorizontalSpacing(10)

        logo_pic = QPixmap(image_path)
        logo_label = QLabel()
        logo_label.setPixmap(logo_pic)
        logo_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(logo_label, 0,0,4,1)

        text_layout = QVBoxLayout()
        app_title     = QLabel("Submittal Assistant")
        version_label = QLabel("v0.002")
        creator_label = QLabel("Oscar Simon M. Velasco")
        email_label   = QLabel("simon@hexel.co.jp")
        app_title.setAlignment(Qt.AlignCenter)
        version_label.setAlignment(Qt.AlignCenter)
        creator_label.setAlignment(Qt.AlignCenter)
        email_label .setAlignment(Qt.AlignCenter)
        text_layout.addWidget(app_title)
        text_layout.addWidget(version_label)
        text_layout.addWidget(creator_label)
        text_layout.addWidget(email_label)

        text_widget = QWidget()
        text_widget.setLayout(text_layout)
        layout.addWidget(text_widget,0,1,4,1)

        self.setLayout(layout)
        self.setFixedSize(300,logo_pic.height()+100)

        QTimer.singleShot(duration, self.close)
class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Submittal Helper (PySide6)")
        self.setGeometry(100, 100, 1200, 1000)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_tabs()

    def create_tabs(self):
        # Placeholder tabs - will be replaced with actual ones
        title_tab = TitleMaker()
        bookmark_tab = BookmarkTab()
        tool_tab = ToolTab()
        self.tabs.addTab(title_tab, "Title Maker")
        self.tabs.addTab(bookmark_tab, "Bookmark Maker")
        self.tabs.addTab(tool_tab, "Tools")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(get_folder(Target = "Resources/Images/hexel_icon.ico"))
    app.setWindowIcon(QIcon(str(get_folder(Target = "Resources/Images/hexel_icon.ico"))))

    splsh_img = get_folder(Target = "Resources/Images/hexel_works.png")
    splash = SplashScreen(splsh_img)
    splash.show()

    main_window = MainApp()
    QTimer.singleShot(3000, main_window.show)

    sys.exit(app.exec())
