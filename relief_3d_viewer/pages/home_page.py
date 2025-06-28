from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication
from PyQt5.QtCore import Qt
import os

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.dark_mode = True  # Початкова тема

        layout = QVBoxLayout()

        label = QLabel("Вітаємо у 3D Переглядачі!")
        layout.addWidget(label)

        open_button = QPushButton("Відкрити 3D модель")
        open_button.clicked.connect(self.main_window.open_file_explorer)
        layout.addWidget(open_button)

        theme_btn = QPushButton("🌓 Перемкнути тему")
        theme_btn.clicked.connect(self.toggle_app_theme)
        layout.addWidget(theme_btn)

        self.setLayout(layout)

        # Застосувати початкову тему
        self.apply_dark_qss()

    def toggle_app_theme(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_qss()
        else:
            self.apply_light_qss()

    def apply_dark_qss(self):
        qss_path = os.path.join("ui", "styles.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())

    def apply_light_qss(self):
        QApplication.instance().setStyleSheet("")
