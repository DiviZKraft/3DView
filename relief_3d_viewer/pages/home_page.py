from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class HomePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()

        label = QLabel("Вітаємо у 3D Переглядачі!")
        label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(label)

        open_button = QPushButton("Відкрити 3D модель")
        open_button.setStyleSheet("padding: 10px; font-size: 16px;")
        open_button.clicked.connect(self.main_window.open_file_explorer)
        layout.addWidget(open_button)

        self.setLayout(layout)
