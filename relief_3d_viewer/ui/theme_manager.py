import os
from PyQt5.QtWidgets import QApplication

class ThemeManager:
    """
    Singleton для перемикання теми (dark/light) для всього додатку.
    Забезпечує єдиний спосіб змінити стилі інтерфейсу у всіх вікнах.
    """
    _instance = None
    _callbacks = []

    def __new__(cls):
        # Реалізація singleton — завжди повертає один і той же екземпляр
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
            cls._instance.dark_mode = True  # Початково — темна тема
        return cls._instance

    def register(self, callback):
        """
        Додає функцію, яка буде викликана при зміні теми.
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unregister(self, callback):
        """
        Видаляє зареєстрований колбек.
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def toggle_theme(self):
        """
        Перемикає тему між темною та світлою. Оновлює QSS та викликає колбеки.
        """
        self.dark_mode = not self.dark_mode
        self.apply_current_theme()
        for cb in self._callbacks:
            cb(self.dark_mode)

    def apply_current_theme(self):
        """
        Застосовує поточну тему (темна/світла) до всього додатку.
        """
        if self.dark_mode:
            self.apply_dark_qss()
        else:
            self.apply_light_theme()

    def apply_dark_qss(self):
        """
        Завантажує та застосовує стилі для темної теми.
        """
        qss_path = os.path.join(os.path.dirname(__file__), "styles_dark.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())

    def apply_light_theme(self):
        """
        Завантажує та застосовує стилі для світлої теми.
        """
        qss_path = os.path.join(os.path.dirname(__file__), "styles_light.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())
