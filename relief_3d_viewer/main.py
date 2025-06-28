import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QPalette, QColor

from pages.home_page import HomePage
from pages.file_search_page import FileSearchPage
from pages.viewer_3d_page import Viewer3DPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Переглядач Моделей")
        self.setGeometry(100, 100, 1200, 800)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f0f0f0"))
        self.setPalette(palette)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home_page = HomePage(self)
        self.search_page = FileSearchPage(self)
        self.viewer_page = Viewer3DPage(self)

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.search_page)
        self.stack.addWidget(self.viewer_page)

        self.stack.setCurrentWidget(self.home_page)

    def open_file_explorer(self):
        self.stack.setCurrentWidget(self.search_page)

    def open_3d_viewer(self, file_path):
        self.viewer_page.set_obj_file(file_path)
        self.stack.setCurrentWidget(self.viewer_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
