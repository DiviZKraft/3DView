from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class HomePage(QWidget):
    def __init__(self, open_file_callback, open_last_file_callback, toggle_theme_callback, parent=None):
        super().__init__(parent)
        self.setObjectName("HomePageBg")
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(35)
        layout.setContentsMargins(40, 50, 40, 50)

        # Іконка
        icon_label = QLabel()
        icon_label.setObjectName("HomeIcon")
        pixmap = QPixmap("relief_3d_viewer/ui/images/logo3d.png")
        if not pixmap.isNull():
            pixmap = pixmap.scaled(110, 110, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Заголовок
        title = QLabel("Вітаємо у 3D Переглядачі!")
        title.setObjectName("HomeTitle")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Підзаголовок
        subtitle = QLabel("Легко переглядайте, аналізуйте і працюйте з 3D-моделями у різних форматах.")
        subtitle.setObjectName("HomeSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Кнопки
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(18)

        btn_open = QPushButton("📁  Відкрити 3D модель")
        btn_open.setObjectName("MainButton")
        btn_open.setMinimumHeight(44)
        btn_open.clicked.connect(open_file_callback)
        btn_layout.addWidget(btn_open)

        btn_last = QPushButton("🕘  Відкрити останній файл")
        btn_last.setObjectName("MainButton")
        btn_last.setMinimumHeight(44)
        btn_last.clicked.connect(open_last_file_callback)
        btn_layout.addWidget(btn_last)

        btn_theme = QPushButton("🌗  Перемкнути тему")
        btn_theme.setObjectName("AccentButton")
        btn_theme.setMinimumHeight(40)
        btn_theme.setMaximumWidth(200)
        btn_theme.clicked.connect(toggle_theme_callback)
        btn_theme.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        btn_theme_layout = QHBoxLayout()
        btn_theme_layout.addStretch()
        btn_theme_layout.addWidget(btn_theme)
        btn_theme_layout.addStretch()
        btn_layout.addLayout(btn_theme_layout)

        layout.addLayout(btn_layout)
        layout.addStretch()
        self.setLayout(layout)
