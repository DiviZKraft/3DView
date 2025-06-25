# === main.py ===
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QPalette, QColor

from pages.home_page import HomePage
from pages.file_search_page import FileSearchPage
from pages.viewer_3d_page import Viewer3DPage
from pages.relief_viewer_page import ReliefViewerPage
from pages.tif_viewer_page import TifViewerPage
from pages.shapefile_viewer_page import ShapefileViewerPage
from pages.geojson_viewer_page import GeoJSONViewerPage
from pages.kml_viewer_page import KMLViewerPage
from pages.pointcloud_viewer_page import PointCloudViewerPage
from pages.gpx_viewer_page import GPXViewerPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GeoData Viewer Pro")
        self.setGeometry(100, 100, 1280, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.home = HomePage(self.navigate_to)
        self.viewer3d = Viewer3DPage(self.navigate_to)
        self.relief_viewer = ReliefViewerPage(self.navigate_to)
        self.tif_viewer = TifViewerPage(self.navigate_to)
        self.shp_viewer = ShapefileViewerPage(self.navigate_to)
        self.geojson_viewer = GeoJSONViewerPage(self.navigate_to)
        self.kml_viewer = KMLViewerPage(self.navigate_to)
        self.pointcloud_viewer = PointCloudViewerPage(self.navigate_to)
        self.gpx_viewer = GPXViewerPage(self.navigate_to)

        self.search = FileSearchPage(
            self.navigate_to,
            self.viewer3d.set_obj_file,
            self.relief_viewer.set_relief_file,
            self.tif_viewer.set_tif_file,
            self.shp_viewer.set_shp_file,
            self.geojson_viewer.set_geojson_file,
            self.kml_viewer.set_kml_file,
            self.pointcloud_viewer.set_pointcloud_file,
            self.gpx_viewer.set_gpx_file
        )

        self.stack.addWidget(self.home)
        self.stack.addWidget(self.search)
        self.stack.addWidget(self.viewer3d)
        self.stack.addWidget(self.relief_viewer)
        self.stack.addWidget(self.tif_viewer)
        self.stack.addWidget(self.shp_viewer)
        self.stack.addWidget(self.geojson_viewer)
        self.stack.addWidget(self.kml_viewer)
        self.stack.addWidget(self.pointcloud_viewer)
        self.stack.addWidget(self.gpx_viewer)

        self.stack.setCurrentWidget(self.home)

    def navigate_to(self, page_name):
        pages = {
            "home": self.home,
            "search": self.search,
            "viewer": self.viewer3d,
            "relief_viewer": self.relief_viewer,
            "tif_viewer": self.tif_viewer,
            "shapefile_viewer": self.shp_viewer,
            "geojson_viewer": self.geojson_viewer,
            "kml_viewer": self.kml_viewer,
            "pointcloud_viewer": self.pointcloud_viewer,
            "gpx_viewer": self.gpx_viewer
        }
        widget = pages.get(page_name)
        if widget:
            self.stack.setCurrentWidget(widget)

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
