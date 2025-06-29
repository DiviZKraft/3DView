import os
from PyQt5.QtWidgets import QApplication

class ThemeManager:
    _instance = None
    _callbacks = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
            cls._instance.dark_mode = True
        return cls._instance

    def register(self, callback):
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unregister(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_current_theme()
        for cb in self._callbacks:
            cb(self.dark_mode)   # Повідомляємо всіх віджетів про зміну теми

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
