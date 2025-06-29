from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from ui.constants import BUTTON_STYLE, LABEL_STYLE

class FileSearchPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        label = QLabel("Оберіть файл .obj або .fbx для перегляду")
        label.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label)

        choose_button = QPushButton("Обрати файл")
        choose_button.setStyleSheet(BUTTON_STYLE)
        choose_button.clicked.connect(self.choose_file)
        layout.addWidget(choose_button)

        self.setLayout(layout)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Виберіть файл", "", "OBJ/FBX Files (*.obj *.fbx)")
        if file_path:
            self.main_window.open_3d_viewer(file_path)
