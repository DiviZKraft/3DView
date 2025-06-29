import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QFileDialog
from pages.home_page import HomePage
from pages.viewer_3d_page import Viewer3DPage
from pages.file_search_page import FileSearchPage
from utils.last_path import load_last_path, save_last_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Переглядач")
        self.setGeometry(100, 100, 1200, 800)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_page = HomePage(main_window=self)
        self.viewer_page = Viewer3DPage(go_back_callback=self.switch_page)
        self.file_search_page = FileSearchPage(main_window=self)

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.viewer_page)
        self.stacked_widget.addWidget(self.file_search_page)
        self.switch_page("home")

    def switch_page(self, name):
        if name == "home":
            self.stacked_widget.setCurrentWidget(self.home_page)
        elif name == "viewer":
            self.stacked_widget.setCurrentWidget(self.viewer_page)
        elif name == "search":
            self.stacked_widget.setCurrentWidget(self.file_search_page)

    def open_file_explorer(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Виберіть 3D модель", "", "OBJ/FBX файли (*.obj *.fbx)"
        )
        if file_path:
            self.viewer_page.set_obj_file(file_path)
            save_last_path(file_path)
            self.switch_page("viewer")

    def open_3d_viewer(self, file_path):
        if file_path:
            self.viewer_page.set_obj_file(file_path)
            save_last_path(file_path)
            self.switch_page("viewer")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
