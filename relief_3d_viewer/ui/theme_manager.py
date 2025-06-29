import os
from PyQt5.QtWidgets import QApplication

class ThemeManager:
    def __init__(self):
        self.dark_mode = True

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_current_theme()

    def apply_current_theme(self):
        if self.dark_mode:
            self.apply_dark_qss()
        else:
            self.apply_light_theme()

    def apply_dark_qss(self):
        qss_path = os.path.join(os.path.dirname(__file__), "styles.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())

    def apply_light_theme(self):
        QApplication.instance().setStyleSheet("")
        palette = QApplication.style().standardPalette()
        QApplication.instance().setPalette(palette)
