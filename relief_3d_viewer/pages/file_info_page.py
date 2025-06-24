
# === pages/file_info_page.py ===
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class FileInfoPage(QWidget):
    def __init__(self, navigate_to):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("ℹ️ Інформація про вибраний файл"))

        back_btn = QPushButton("← Назад")
        back_btn.clicked.connect(lambda: navigate_to("home"))
        layout.addWidget(back_btn)

        self.setLayout(layout)