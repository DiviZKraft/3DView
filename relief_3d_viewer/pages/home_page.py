from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from ui.theme_manager import ThemeManager
from ui.constants import BUTTON_STYLE, LABEL_STYLE
from utils.last_path import load_last_path

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.theme_manager = ThemeManager()

        layout = QVBoxLayout()
        label = QLabel("Вітаємо у 3D Переглядачі!")
        label.setStyleSheet(LABEL_STYLE)
        layout.addWidget(label)

        open_button = QPushButton("Відкрити 3D модель")
        open_button.setStyleSheet(BUTTON_STYLE)
        open_button.clicked.connect(self.main_window.open_file_explorer)
        layout.addWidget(open_button)

        last_path = load_last_path()
        if last_path:
            open_last_btn = QPushButton("Відкрити останній файл")
            open_last_btn.setStyleSheet(BUTTON_STYLE)
            open_last_btn.clicked.connect(lambda: self.main_window.open_3d_viewer(last_path))
            layout.addWidget(open_last_btn)

        search_btn = QPushButton("Пошук файлів")
        search_btn.setStyleSheet(BUTTON_STYLE)
        search_btn.clicked.connect(lambda: self.main_window.switch_page("search"))
        layout.addWidget(search_btn)

        theme_btn = QPushButton("🌓 Перемкнути тему")
        theme_btn.setStyleSheet(BUTTON_STYLE)
        theme_btn.clicked.connect(self.theme_manager.toggle_theme)
        layout.addWidget(theme_btn)

        self.setLayout(layout)
        self.theme_manager.apply_current_theme()
