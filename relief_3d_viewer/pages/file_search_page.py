import os
import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileSystemModel, QTreeView, QListWidget, QSplitter, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QModelIndex

HISTORY_FILE = "history.json"

class FileSearchPage(QWidget):
    def __init__(
        self, navigate_to,
        set_obj_callback,
        set_relief_callback,
        set_tif_callback,
        set_shp_callback,
        set_geojson_callback,
        set_kml_callback,
        set_pointcloud_callback,
        set_gpx_callback
    ):
        super().__init__()
        self.navigate_to = navigate_to
        self.set_obj_callback = set_obj_callback
        self.set_relief_callback = set_relief_callback
        self.set_tif_callback = set_tif_callback
        self.set_shp_callback = set_shp_callback
        self.set_geojson_callback = set_geojson_callback
        self.set_kml_callback = set_kml_callback
        self.set_pointcloud_callback = set_pointcloud_callback
        self.set_gpx_callback = set_gpx_callback
        self.history = []

        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("🔍 Оберіть файл геоданих"))

        splitter = QSplitter(Qt.Horizontal)
        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath("")
        self.dir_view = QTreeView()
        self.dir_view.setModel(self.dir_model)
        self.dir_view.setRootIndex(self.dir_model.index(""))
        self.dir_view.clicked.connect(self.on_tree_clicked)
        splitter.addWidget(self.dir_view)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_clicked)
        splitter.addWidget(self.history_list)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter)

        btn = QPushButton("📂 Вибрати файл вручну")
        btn.clicked.connect(self.open_file_dialog)
        main_layout.addWidget(btn)

        back_btn = QPushButton("← Назад")
        back_btn.clicked.connect(lambda: self.navigate_to("home"))
        main_layout.addWidget(back_btn)

        self.setLayout(main_layout)
        self.load_history()

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Оберіть файл", "", "Геодані (*.obj *.asc *.tif *.shp *.geojson *.kml *.xyz *.las *.gpx);;Всі файли (*.*)")
        if file_name:
            self.set_any_file(file_name)

    def on_tree_clicked(self, index: QModelIndex):
        file_path = self.dir_model.filePath(index)
        if os.path.isfile(file_path):
            self.set_any_file(file_path)

    def on_history_clicked(self, item):
        self.set_any_file(item.text())

    def set_any_file(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext == '.obj':
            self.set_obj_callback(path)
            self.navigate_to("viewer")
        elif ext == '.asc':
            self.set_relief_callback(path)
            self.navigate_to("relief_viewer")
        elif ext in ['.tif', '.tiff']:
            self.set_tif_callback(path)
            self.navigate_to("tif_viewer")
        elif ext == '.shp':
            self.set_shp_callback(path)
            self.navigate_to("shapefile_viewer")
        elif ext == '.geojson':
            self.set_geojson_callback(path)
            self.navigate_to("geojson_viewer")
        elif ext == '.kml':
            self.set_kml_callback(path)
            self.navigate_to("kml_viewer")
        elif ext in ['.xyz', '.las']:
            self.set_pointcloud_callback(path)
            self.navigate_to("pointcloud_viewer")
        elif ext == '.gpx':
            self.set_gpx_callback(path)
            self.navigate_to("gpx_viewer")
        else:
            QMessageBox.warning(self, "Невідомий формат", f"Формат {ext} не підтримується.")
            return

        if path not in self.history:
            self.history.append(path)
            self.history_list.addItem(path)
            self.save_history()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                for path in self.history:
                    if os.path.exists(path):
                        self.history_list.addItem(path)
            except Exception as e:
                print(f"Помилка при читанні історії: {e}")

    def save_history(self):
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Помилка при збереженні історії: {e}")
