# === main.py ===
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QPalette, QColor

from pages.home_page import HomePage
from pages.file_search_page import FileSearchPage
from pages.viewer_3d_page import Viewer3DPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Model Viewer")
        self.setGeometry(100, 100, 1280, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home = HomePage(self.navigate_to)
        self.viewer3d = Viewer3DPage(self.navigate_to)

        self.search = FileSearchPage(
            self.navigate_to,
            self.viewer3d.set_obj_file
        )

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.search)
        self.stack.addWidget(self.viewer3d)

        self.stack.setCurrentWidget(self.home)

    def navigate_to(self, page_name):
        if page_name == "home":
            self.stack.setCurrentWidget(self.home)
        elif page_name == "search":
            self.stack.setCurrentWidget(self.search)
        elif page_name == "viewer":
            self.stack.setCurrentWidget(self.viewer3d)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
    palette.setColor(QPalette.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
    palette.setColor(QPalette.Text, QColor(0, 0, 0))
    palette.setColor(QPalette.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(0, 0, 255))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
