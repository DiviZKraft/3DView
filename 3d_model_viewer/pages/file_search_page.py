from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from ui.constants import BUTTON_STYLE, LABEL_STYLE

class FileSearchPage(QWidget):
    """
    Сторінка для ручного вибору файлу (OBJ/PLY) у файловій системі.
    """

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        # Текстове пояснення
        label = QLabel("Оберіть файл .obj або .ply для перегляду")
        label.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label)

        # Кнопка вибору файлу
        choose_button = QPushButton("Обрати файл")
        choose_button.setStyleSheet(BUTTON_STYLE)
        choose_button.clicked.connect(self.choose_file)
        layout.addWidget(choose_button)

        self.setLayout(layout)

    def choose_file(self):
        """
        Відкриває файловий діалог та передає обраний файл у головне вікно для перегляду.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Виберіть файл", "", "OBJ/PLY Files (*.obj *.ply)")
        if file_path:
            self.main_window.open_3d_viewer(file_path)
