
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAbstractItemView, QDialog
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from Tabs.BookmarkProp import EditBookmarkDialog

class BookmarkTree(QTreeWidget):
    structure_chg = Signal(bool)

    def __init__(self, header_title = "Bookmarks", context1 = "Add Blank", context2 = "Edit Bookmark", master_mode = 1):
        super().__init__()
        self.context1 = context1
        self.context2 = context2
        self.master_mode = master_mode
        self.setHeaderLabels([header_title])
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setFixedHeight(500)
        self.setFixedWidth(300)
        self.itemChanged.connect(self.on_item_changed)
        self.customContextMenuRequested.connect(self.open_context_menu)
        self.dropEvent = self._wrap_drop_event(self.dropEvent)
        self.structure = []

    def _wrap_drop_event(self, original_drop_event):
        def wrapper(event):
            original_drop_event(event)
            self.refresh_structure()
        return wrapper

    def populate_items(self, data, mode=None):
        self.clear()
        self.item_lookup = {}

        if mode == 1:
            # Mode 1: Parent-child mapping (read-only bookmarks)
            for entry in data:
                for page, title in entry[0].items():
                    parent_title = entry[1]
                    parent_item = self.item_lookup.get(parent_title)
                    item = QTreeWidgetItem(parent_item if parent_item else self, [title])
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    item.setData(0, Qt.UserRole, page)
                    self.item_lookup[title] = item

        elif mode == 2:
            # Mode 2: Flat structure (OCR only)
            for page, title in data.items():
                item = QTreeWidgetItem(self, [title])
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setData(0, Qt.UserRole, page)

        elif mode == 3:
            # Mode 3: Combine both parented and OCR-based
            # Part 1: parented structure
            for entry in data[0]:
                for page, title in entry[0].items():
                    parent_title = entry[1]
                    parent_item = self.item_lookup.get(parent_title)
                    item = QTreeWidgetItem(parent_item if parent_item else self, [title])
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                    item.setData(0, Qt.UserRole, page)
                    self.item_lookup[title] = item

            # Part 2: flat OCR-based
            for page, title in data[1].items():
                item = QTreeWidgetItem(self, [title])
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setData(0, Qt.UserRole, page)

        else:
            # Default fallback: flat structure
            for page, title in data.items():
                item = QTreeWidgetItem(self, [title])
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setData(0, Qt.UserRole, page)


    def refresh_structure(self):
        def build_tree(item):
            if self.master_mode == 1:
                return {
                    "title": item.text(0),
                    "page": item.data(0, Qt.UserRole),
                    "children": [build_tree(item.child(i)) for i in range(item.childCount())]
                }
            elif self.master_mode == 2:
                return {
                    "title": item.text(0),
                    "children": [build_tree(item.child(i)) for i in range(item.childCount())]
                }


        self.structure = []
        for i in range(self.topLevelItemCount()):
            self.structure.append(build_tree(self.topLevelItem(i)))

        self.structure_chg.emit(True)
        return self.structure

    def add_blankmark(self):
        if self.master_mode == 1:
            item = QTreeWidgetItem(self, ["Untitled "])
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            item.setData(0, Qt.UserRole, 999999)
            self.refresh_structure()
        elif self.master_mode == 2:
            item = QTreeWidgetItem(self, ["Untitled "])
            item.setFlags(item.flags() | Qt.ItemIsEditable)

    def delete_selected_items(self):
        for item in self.selectedItems():
            parent = item.parent()
            if parent:
                parent.removeChild(item)
            else:
                index = self.indexOfTopLevelItem(item)
                if index != -1:
                    self.takeTopLevelItem(index)

    def edit_bookmark(self, item):
        current_title = item.text(0)
        current_page = item.data(0, Qt.UserRole) or 0
        dialog = EditBookmarkDialog(current_title, current_page, self)
        if dialog.exec() == QDialog.Accepted:
            new_title, new_page = dialog.get_values()
            item.setText(0, new_title)
            item.setData(0, Qt.UserRole, new_page-1)
            self.refresh_structure()


    def on_item_changed(self):
        self.refresh_structure()

    def open_context_menu(self, position):
        item = self.itemAt(position)
        
        menu = QMenu()

        if item:

            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(self.delete_selected_items)

            rename_action = QAction("Rename", self)
            rename_action.triggered.connect(lambda: self.editItem(item))
            
            page_action = QAction(self.context2, self)
            page_action.triggered.connect(lambda: self.edit_bookmark(item))

            menu.addAction(page_action)
            menu.addAction(rename_action)
            menu.addAction(delete_action)
        
        else:

            add_action = QAction(self.context1, self)
            add_action.triggered.connect(self.add_blankmark)
            menu.addAction(add_action)
            
            menu.addSeparator()
            
            menu.addAction("Expand All", self.expandAll)
            menu.addAction("Collapse All", self.collapseAll)


        menu.exec(self.viewport().mapToGlobal(position))
