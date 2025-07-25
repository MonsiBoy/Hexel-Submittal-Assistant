from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QGroupBox, QGridLayout,  QCheckBox,
    QComboBox, QFileDialog, QMessageBox,QTreeWidgetItem,
    QTreeWidget
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from pathlib import Path
import os
import json
import shutil
from Tabs.UI.UnifiedScanner import UnifiedScanner
from Tabs.Styles.GlobalStyle import apply_main_stylesheet
from Tabs.UI.TreeUI import BookmarkTree
from Tabs.operations.Bookmark_Maker import BookMark
from Tabs.Utility.Utility_funcs import get_folder


class ToolTab(QWidget):
    def __init__(self):
        super().__init__()
        self.standard_map = {
        "ANSI": get_folder("Resources/Standards/ANSI"),
        "IEEE": get_folder("Resources/Standards/IEEE"),
        "NFPA": get_folder("Resources/Standards/NFPA"),
        }
        self.setup_ui()

    def setup_ui(self):
        apply_main_stylesheet(self)
        self.bookmake = BookMark()
        
        self.master_lay = QGridLayout()
        self.setLayout(self.master_lay)

        self.QR = self.create_qr_scanner()
        self.TEXT = self.create_text_scanner()
        self.DIR = self.create_directory()

        self.master_lay.addWidget(self.QR, 0, 0)
        self.master_lay.addWidget(self.TEXT, 1, 0)
        self.master_lay.addWidget(self.DIR, 0, 1, 3, 6)


    def create_directory(self):
        self.create_addtl_ref()
        self.add_box.hide()

        self.directory_group = QGroupBox("Directory Maker")
        self.tree = BookmarkTree(header_title="Directory", context1 = "Add Folder", context2 = "Edit Folder Properties", master_mode = 2)

        layout = QGridLayout()
        self.tmpl_pick = QComboBox()
        self.tmpl_pick.setPlaceholderText("Choose Template Here")
        self.populate_template_combobox()
        self.tmpl_pick.currentIndexChanged.connect(lambda index:self.handle_template_selection(index))
        
        self.secondary_layout =  QVBoxLayout()
        

        sub_layout1 = QHBoxLayout()
        self.include_ref = QCheckBox("Include Standard References")
        self.include_ref.stateChanged.connect(self.show_addtl_ref)
        self.include_custom = QCheckBox("Include Custom Items")
        self.include_custom.setEnabled(False)
        sub_layout1.addWidget(self.include_ref)
        sub_layout1.addWidget(self.include_custom)


        sub_layout2 = QHBoxLayout()
        self.set_dir = QPushButton("Browse")
        self.set_dir.clicked.connect(self.pick_directory)
        self.dir = QLineEdit()
        self.dir.setPlaceholderText("Root Directory will appear here")
        sub_layout2.addWidget(self.set_dir)
        sub_layout2.addWidget(self.dir)

        self.generate = QPushButton("Generate Folder Tree")
        self.generate.clicked.connect(self.generate_folder_tree)

      
        self.secondary_layout.addWidget(self.tmpl_pick)
        self.secondary_layout.addLayout(sub_layout1)
        self.secondary_layout.addWidget(self.add_box)
        self.secondary_layout.addLayout(sub_layout2)
        self.secondary_layout.addWidget(self.generate)

        layout.addWidget(self.tree,0,1,3,5, alignment = Qt.AlignVCenter | Qt.AlignTop)
        layout.addLayout(self.secondary_layout,0,0)

        self.directory_group.setLayout(layout)

        return self.directory_group

    def create_addtl_ref(self):
        self.add_box = QGroupBox("Additional items")

        ref_layout = QVBoxLayout()
        self.all_check  = QCheckBox("Include all")
        self.all_check.stateChanged.connect(self.include_all)
        
        self.ANSI_check = QCheckBox("ANSI")
        self.ANSI_check.stateChanged.connect(self.add_ref_ANSI)
        self.IEEE_check = QCheckBox("IEEE")
        self.IEEE_check.stateChanged.connect(self.add_ref_IEEE)
        self.NFPA_check = QCheckBox("NFPA")
        self.NFPA_check.stateChanged.connect(self.add_ref_NFPA)

        ref_layout.addWidget(self.all_check)
        ref_layout.addWidget(self.ANSI_check)
        ref_layout.addWidget(self.IEEE_check)
        ref_layout.addWidget(self.NFPA_check)

        self.add_box.setLayout(ref_layout)
    
    def show_addtl_ref(self,state):
        self.add_box.setVisible(state)
        
    def include_all(self, state):
        self.ANSI_check.setChecked(state)
        self.IEEE_check.setChecked(state)
        self.NFPA_check.setChecked(state)
    
    def add_ref_ANSI(self):
        if self.ANSI_check.checkState() == Qt.Checked:
            ANSI_folder = get_folder(Target = "Resources/Standards/ANSI")
            root_item = QTreeWidgetItem([ANSI_folder.name])
            root_item.setFlags(root_item.flags() | Qt.ItemIsEditable)
            root_item.setData(0, Qt.UserRole, "ANSI") 
            self.tree.addTopLevelItem(root_item)
            self._add_folder_to_tree(ANSI_folder, root_item)
            
    def add_ref_IEEE(self):
        if self.IEEE_check.checkState() == Qt.Checked:
            IEEE_folder = get_folder(Target = "Resources/Standards/IEEE")
            root_item = QTreeWidgetItem([IEEE_folder.name])
            root_item.setFlags(root_item.flags() | Qt.ItemIsEditable)
            root_item.setData(0, Qt.UserRole, "IEEE")
            self.tree.addTopLevelItem(root_item)
            self._add_folder_to_tree(IEEE_folder, root_item)

    def add_ref_NFPA(self):
        if self.NFPA_check.checkState() == Qt.Checked:
            NFPA_folder = get_folder(Target = "Resources/Standards/NFPA")
            root_item = QTreeWidgetItem([NFPA_folder.name])
            root_item.setFlags(root_item.flags() | Qt.ItemIsEditable)
            root_item.setData(0, Qt.UserRole, "NFPA")
            self.tree.addTopLevelItem(root_item)
            self._add_folder_to_tree(NFPA_folder, root_item)


    def _add_folder_to_tree(self, folder_path: Path, parent_item):
        for item in folder_path.iterdir():
            child_item = QTreeWidgetItem([item.name])
            child_item.setFlags(child_item.flags() | Qt.ItemIsEditable)

            # Store original file path
            child_item.setData(0, Qt.UserRole, item)  # 👈 store Path object

            if parent_item is None:
                self.tree.addTopLevelItem(child_item)
            else:
                parent_item.addChild(child_item)

            if item.is_dir():
                self._add_folder_to_tree(item, child_item)  # recursive


    def create_qr_scanner(self):
        self.qr_group = QGroupBox("QR Scanner")
        self.qr_result = QLineEdit()
        self.qr_result.setPlaceholderText("Link will appear here")
        self.qr_search_btn = QPushButton("Search")
        self.qr_scan_btn = QPushButton("Open Scanner")
        self.qr_startqr_btn = QPushButton("Scan QR")
        self.qr_close_btn = QPushButton("Close QR")
        self.qr_close_btn.setEnabled(False)

        self.qr_startqr_btn.clicked.connect(self.run_qr_scan)
        self.qr_scan_btn.clicked.connect(self.start_qr_scan)
        self.qr_close_btn.clicked.connect(self.close_qr_scan)
        self.qr_search_btn.clicked.connect(self.open_qr_browser)

        self.qr_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.qr_shortcut.activated.connect(self.start_qr_scan)

        layout = QGridLayout()
        layout.addWidget(self.qr_scan_btn, 0, 0)
        layout.addWidget(self.qr_close_btn, 0, 1)
        layout.addWidget(self.qr_startqr_btn, 1, 0)
        layout.addWidget(self.qr_search_btn, 1, 1)
        layout.addWidget(self.qr_result, 1, 2)
        self.qr_group.setLayout(layout)
        return self.qr_group

    def create_text_scanner(self):
        self.text_group = QGroupBox("Text Scanner")
        self.text_results = QTextEdit()
        self.text_results.setPlaceholderText("Scanned text will appear here")

        self.text_scan_btn = QPushButton("Open Text Scanner")
        self.text_trigger_btn = QPushButton("Scan Text Now")
        self.text_close_btn = QPushButton("Close Text Scanner")
        self.choose_model = QComboBox()
        self.choose_model.addItems(["EasyOCR", "PaddleOCR (UNDER CONSTRUCTION)"])

        model = self.choose_model.model()
        item = model.item(1)
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)

        self.clear_on_scan = QCheckBox("Clear text before scan")
        self.append_on_scan = QCheckBox("Append text")


        self.text_close_btn.setEnabled(False)

        self.text_scan_btn.clicked.connect(self.open_text_scanner)
        self.text_trigger_btn.clicked.connect(lambda: self.trigger_text_scan(self.choose_model.currentText()))
        self.text_close_btn.clicked.connect(self.close_text_scanner)

        self.text_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        self.text_shortcut.activated.connect(lambda: self.trigger_text_scan(self.choose_model.currentText()))

        scan_opt = QHBoxLayout()
        scan_opt.addWidget(self.text_scan_btn)
        scan_opt.addWidget(self.choose_model)

       
        layout = QVBoxLayout()
        layout.addLayout(scan_opt)
        layout.addWidget(self.text_trigger_btn)
        layout.addWidget(self.text_close_btn)

     

        options = QHBoxLayout()
        options.addWidget(self.clear_on_scan)
        options.addWidget(self.append_on_scan)


        layout.addLayout(options)
        layout.addWidget(self.text_results)

        self.text_group.setLayout(layout)
        return self.text_group

    def start_qr_scan(self):
        self.qr_inst = UnifiedScanner(mode="qr")
        self.qr_window = self.qr_inst.getScanner()
        self.qr_inst.qr_detected.connect(self.qr_result.setText)


        self.qr_window.show()
        self.qr_scan_btn.setEnabled(False)
        self.qr_close_btn.setEnabled(True)

    def run_qr_scan(self):
        self.qr_inst.scan_area()

    def close_qr_scan(self):
        if hasattr(self, 'qr_window'):
            self.qr_window.close()
            self.qr_inst.qr_detected.disconnect()
        if hasattr(self, 'qr_timer'):
             self.scan_time.stop()
        self.qr_scan_btn.setEnabled(True)
        self.qr_close_btn.setEnabled(False)

    def open_qr_browser(self):
        import webbrowser
        webbrowser.open(self.qr_result.text())

    def open_text_scanner(self):
        self.text_inst = UnifiedScanner(mode="text")
        self.text_window = self.text_inst.getScanner()
        self.text_inst.text_detected.connect(self.update_text_result)
        self.text_window.show()
        self.text_scan_btn.setEnabled(False)
        self.text_close_btn.setEnabled(True)

    def close_text_scanner(self):
        if hasattr(self, 'text_window'):
            self.text_window.close()
        self.text_scan_btn.setEnabled(True)
        self.text_close_btn.setEnabled(False)

    def trigger_text_scan(self, mode):
        try:
            if hasattr(self, 'text_inst'):
                self.text_inst.trigger_text_scan(mode)
                QMessageBox.information(self, "Success", "Text Scanned!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to scan text:\n{e}")

    def update_text_result(self, text):
        if self.clear_on_scan.isChecked():
            self.text_results.clear()
        if self.append_on_scan.isChecked():
            self.text_results.append(text)
        else:
            self.text_results.setPlainText(text)


    def populate_template_combobox(self):
        self.template_folder = get_folder(Target = "FolderTemplates")
        self.tmpl_pick.clear()
        if self.template_folder.exists():
            for file in self.template_folder.glob("*.json"):
                self.tmpl_pick.addItem(file.stem, file)
            

    def handle_template_selection(self, index):
        file_path =  self.template_folder / f"{self.tmpl_pick.currentText()}.json"
        if not file_path:
            return

        with open(file_path, "r", encoding="utf-8") as f:
            structure = json.load(f)

        self.tree.clear()
        for node in structure:
            self._insert_node_recursive(node, self.tree)

    def _insert_node_recursive(self, node, parent):
        item = QTreeWidgetItem(parent, [node["title"]])
        item.setFlags(item.flags() | Qt.ItemIsEditable)
        if "children" in node:
            for child_node in node["children"]:
                self._insert_node_recursive(child_node, item)



    def pick_directory(self):
        self.main_folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            "/home"  # or use str(Path.home()) for cross-platform default
        )
        if self.main_folder:
            self.dir.setText(self.main_folder)

    def generate_folder_tree(self):
        try:
            for i in range(self.tree.topLevelItemCount()):
                item = self.tree.topLevelItem(i)
                self._create_folder_recursive(item, self.main_folder)
            QMessageBox.information(self, "Success", "Folder structure created successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create folders:\n{e}")

    def _create_folder_recursive(self, item, current_path):
        folder_name = item.text(0).strip()
        safe_folder = self._sanitize_folder_name(folder_name)
        new_path = os.path.join(current_path, safe_folder)

        if item.childCount() > 0:
            # Has children → it's a folder
            os.makedirs(new_path, exist_ok=True)
            for i in range(item.childCount()):
                child = item.child(i)
                self._create_folder_recursive(child, new_path)
        else:
            # No children → try to treat as file, else fallback to empty folder
            source_file = self._resolve_original_file_path(item)
            if source_file and source_file.exists():
                os.makedirs(current_path, exist_ok=True)
                dest_file = os.path.join(current_path, safe_folder)
                shutil.copy2(source_file, dest_file)
            else:
                # Fallback: treat as empty folder
                os.makedirs(new_path, exist_ok=True)

    
    def _resolve_original_file_path(self, item):
        path_data = item.data(0, Qt.UserRole)
        if isinstance(path_data, Path) and path_data.exists():
            return path_data
        return None


    def _copy_folder_contents(self, src_path: Path, dst_path: str):
        for item in src_path.iterdir():
            dst_item_path = os.path.join(dst_path, item.name)
            if item.is_dir():
                shutil.copytree(item, dst_item_path, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dst_item_path)    


    def _sanitize_folder_name(self, name):
        # Remove illegal characters for folder names (basic version)
        invalid = r'\/:*?"<>|'
        return "".join(c for c in name if c not in invalid).strip()