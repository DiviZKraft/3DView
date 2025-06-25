from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class GeoJSONViewerPage(QWidget):
    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to
        layout = QVBoxLayout()
        self.label = QLabel("🌐 GeoJSON не завантажено")
        layout.addWidget(self.label)
        back_btn = QPushButton("← Назад")
        back_btn.clicked.connect(lambda: self.navigate_to("search"))
        layout.addWidget(back_btn)
        self.setLayout(layout)

    def set_geojson_file(self, path):
        self.label.setText(f"🌐 Відкрито GeoJSON: {path}")
