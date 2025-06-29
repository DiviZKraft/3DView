from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

class FileSearchPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        label = QLabel("Оберіть файл .obj для перегляду")
        label.setStyleSheet("font-size: 18px;")
        layout.addWidget(label)

        choose_button = QPushButton("Обрати файл")
        choose_button.clicked.connect(self.choose_file)
        layout.addWidget(choose_button)

        self.setLayout(layout)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Виберіть файл", "", "OBJ Files (*.obj)")
        if file_path:
            self.main_window.open_3d_viewer(file_path)