from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class PointCloudViewerPage(QWidget):
    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to
        layout = QVBoxLayout()
        self.label = QLabel("☁ Хмара точок не завантажена (.xyz/.las)")
        layout.addWidget(self.label)
        back_btn = QPushButton("← Назад")
        back_btn.clicked.connect(lambda: self.navigate_to("search"))
        layout.addWidget(back_btn)
        self.setLayout(layout)

    def set_pointcloud_file(self, path):
        self.label.setText(f"☁ Відкрито хмару точок: {path}")
