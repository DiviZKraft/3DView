# === pages/file_search_page.py ===
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog

class FileSearchPage(QWidget):
    def __init__(self, navigate_to, set_obj_callback):
        super().__init__()
        self.navigate_to = navigate_to
        self.set_obj_callback = set_obj_callback
        layout = QVBoxLayout()
        layout.addWidget(QLabel("🔍 Сторінка пошуку файлів"))

        btn = QPushButton("Обрати .obj файл")
        btn.clicked.connect(self.open_file_dialog)
        layout.addWidget(btn)

        back_btn = QPushButton("← Назад")
        back_btn.clicked.connect(lambda: navigate_to("home"))
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Обрати модель .obj", "", "OBJ файли (*.obj)")
        if file_name:
            print(f"Обрано файл: {file_name}")
            self.set_obj_callback(file_name)
            self.navigate_to("viewer")