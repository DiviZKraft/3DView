# === pages/file_search_page.py ===
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileSystemModel, QTreeView, QListWidget, QSplitter, QFileDialog
)
from PyQt5.QtCore import Qt, QModelIndex
import os

class FileSearchPage(QWidget):
    def __init__(self, navigate_to, set_obj_callback):
        super().__init__()
        self.navigate_to = navigate_to
        self.set_obj_callback = set_obj_callback
        self.history = []

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("🔍 Пошук моделей .obj"))

        splitter = QSplitter(Qt.Horizontal)

        # Ліва панель — дерево файлової системи (всі диски)
        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath("")
        self.dir_view = QTreeView()
        self.dir_view.setModel(self.dir_model)
        self.dir_view.setRootIndex(self.dir_model.index(""))  # Показати всі диски
        self.dir_view.clicked.connect(self.on_tree_clicked)
        splitter.addWidget(self.dir_view)

        # Права панель — історія відкритих файлів
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_clicked)
        splitter.addWidget(self.history_list)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)

        # Нижні кнопки
        btn = QPushButton("📂 Обрати .obj файл вручну")
        btn.clicked.connect(self.open_file_dialog)
        main_layout.addWidget(btn)

        back_btn = QPushButton("← Назад")
        back_btn.clicked.connect(lambda: self.navigate_to("home"))
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Обрати модель .obj", "", "OBJ файли (*.obj)"
        )
        if file_name:
            self.set_obj_file(file_name)

    def on_tree_clicked(self, index: QModelIndex):
        file_path = self.dir_model.filePath(index)
        if file_path.lower().endswith(".obj"):
            self.set_obj_file(file_path)

    def on_history_clicked(self, item):
        self.set_obj_file(item.text())

    def set_obj_file(self, path):
        self.set_obj_callback(path)
        self.navigate_to("viewer")

        if path not in self.history:
            self.history.append(path)
            self.history_list.addItem(path)
