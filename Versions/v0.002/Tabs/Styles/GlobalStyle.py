def apply_main_stylesheet(widget):
    widget.setStyleSheet("""
        QPushButton {
            background-color: #007ACC;
            color: white;
            border-radius: 5px;
            padding: 6px 12px;
        }
        QPushButton:hover {
            background-color: #005F99;
        }
        QPushButton:disabled {
            background-color: gray;
            color: white;
        }
        QTreeWidget {
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
        }
        QProgressBar {
            border: 1px solid #aaa;
            border-radius: 5px;
            height: 10px;
            text-align: center;
        }
        QProgressBar::chunk {
            background-color: #05B8CC;
            margin: 1px;
            border-radius: 3px;
        }
        QLabel {
            font-size: 13px;
        }
        QHeaderView::section {
            background-color: #007ACC;
            color: white;
            padding: 4px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-weight: bold;
        }
    """)
