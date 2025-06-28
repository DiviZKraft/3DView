# === pages/home_page.py ===
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class HomePage(QWidget):
    def __init__(self, navigate_to):
        super().__init__()
        layout = QVBoxLayout()

        label = QLabel("<h1>🏠 Головна сторінка</h1>")
        layout.addWidget(label)

        btn1 = QPushButton("🔍 Пошук 3D-моделі")
        btn1.clicked.connect(lambda: navigate_to("search"))
        layout.addWidget(btn1)

        btn2 = QPushButton("👁️ Перегляд 3D-моделі")
        btn2.clicked.connect(lambda: navigate_to("viewer"))
        layout.addWidget(btn2)

        self.setLayout(layout)
