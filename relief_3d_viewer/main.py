# === main.py ===
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from pages.home_page import HomePage
from pages.file_search_page import FileSearchPage
from pages.viewer_3d_page import Viewer3DPage
from pages.file_info_page import FileInfoPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Переглядач 3D-моделей (.obj)")
        self.setGeometry(100, 100, 1280, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.viewer = Viewer3DPage(self.navigate_to)  # Передаємо navigate_to

        self.search = FileSearchPage(self.navigate_to, self.viewer.set_obj_file)
        self.home = HomePage(self.navigate_to)
        self.info = FileInfoPage(self.navigate_to)

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.search)
        self.stack.addWidget(self.viewer)
        self.stack.addWidget(self.info)

    def navigate_to(self, page_name):
        pages = {
            "home": self.home,
            "search": self.search,
            "viewer": self.viewer,
            "info": self.info
        }
        widget = pages.get(page_name)
        if widget:
            self.stack.setCurrentWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
