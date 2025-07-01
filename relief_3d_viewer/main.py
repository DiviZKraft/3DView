import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QFileDialog
from pages.home_page import HomePage
from pages.viewer_3d_page import Viewer3DPage
from pages.file_search_page import FileSearchPage
from utils.last_path import load_last_path, save_last_path
import os
from ui.theme_manager import ThemeManager

class MainWindow(QMainWindow):
    """
    Головне вікно програми з переходом між сторінками.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Переглядач")
        self.setGeometry(100, 100, 1200, 800)

        # Стек-виджет для організації сторінок
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Менеджер теми (синглтон)
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_current_theme()  # застосування теми при старті

        # --- Ініціалізація сторінок ---
        self.home_page = HomePage(
            open_file_callback=self.open_file_explorer,             # Відкрити діалог вибору файлу
            open_last_file_callback=self.open_last_file,             # Відкрити останній файл
            toggle_theme_callback=self.toggle_theme,                 # Перемкнути тему
            parent=self
        )
        self.viewer_page = Viewer3DPage(go_back_callback=self.switch_page)  # Сторінка 3D рендеру
        self.file_search_page = FileSearchPage(main_window=self)            # Пошук файлів

        # Додаємо сторінки до стеку
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.viewer_page)
        self.stacked_widget.addWidget(self.file_search_page)

        # Відразу показуємо домашню сторінку
        self.switch_page("home")

    def switch_page(self, name):
        """
        Перемикає сторінки за ключовою назвою.
        """
        if name == "home":
            self.stacked_widget.setCurrentWidget(self.home_page)
        elif name == "viewer":
            self.stacked_widget.setCurrentWidget(self.viewer_page)
        elif name == "search":
            self.stacked_widget.setCurrentWidget(self.file_search_page)

    def open_file_explorer(self):
        """
        Відкриває діалог вибору файлу моделі. Після вибору — перемикає на вікно перегляду.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Виберіть 3D модель", "", "OBJ/PLY файли (*.obj *.ply)"
        )
        if file_path:
            self.viewer_page.set_obj_file(file_path)
            save_last_path(file_path)
            self.switch_page("viewer")

    def open_last_file(self):
        """
        Відкриває останній файл моделі (якщо його шлях збережено).
        """
        last_path = load_last_path()
        if last_path:
            self.viewer_page.set_obj_file(last_path)
            self.switch_page("viewer")

    def toggle_theme(self):
        """
        Перемикає тему (темна/світла) за допомогою ThemeManager.
        """
        self.theme_manager.toggle_theme()


if __name__ == "__main__":
    # Старт додатку
    app = QApplication(sys.argv)
    theme_manager = ThemeManager()
    theme_manager.apply_current_theme()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
