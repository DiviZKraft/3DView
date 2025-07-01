import sys
import os
from PyQt5.QtWidgets import QApplication

class ThemeManager:
    """
    Singleton для перемикання теми (dark/light) для всього додатку.
    """
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
            cb(self.dark_mode)

    def apply_current_theme(self):
        if self.dark_mode:
            self.apply_qss("ui/styles_dark.qss")
        else:
            self.apply_qss("ui/styles_light.qss")

    def apply_qss(self, filename):
        qss_path = get_resource_path(filename)
        # Для діагностики:
        # print("Шукаємо QSS тут:", qss_path)
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())
        else:
            # Для діагностики, якщо файл не знайдено
            print(f"Файл стилю не знайдено: {qss_path}")

def get_resource_path(filename):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
         # PyInstaller
        base_path = sys._MEIPASS
    else:
         # Запуск із папки — шлях до exe або .py
         base_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    return os.path.join(base_path, filename)

