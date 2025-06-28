from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog, QSlider, QToolBar, QAction, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import QSize


from widgets.simple_gl_widget import SimpleGLWidget


class Viewer3DPage(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()

        self.set_dark_theme()
        layout = QHBoxLayout(self)

        # Панель ліворуч (азимут)
        left_controls = QVBoxLayout()
        left_controls.addWidget(QLabel("☀️ Азимут"))
        self.az_slider = QSlider(Qt.Vertical)
        self.az_slider.setRange(0, 360)
        self.az_slider.setValue(45)
        self.az_slider.valueChanged.connect(lambda val: self.set_light_angle(val, 'az'))
        left_controls.addWidget(self.az_slider)
        layout.addLayout(left_controls)

        # Центральна область
        center_layout = QVBoxLayout()
        self.go_back_callback = go_back_callback

        # Панель інформації
        self.info_label = QLabel("ℹ️ Інформація про модель")
        self.info_label.setStyleSheet("font-size: 16px; padding: 4px;")
        center_layout.addWidget(self.info_label)

        # OpenGL-віджет
        self.gl_widget = SimpleGLWidget(self.info_label)
        self.gl_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout.addWidget(self.gl_widget)

        # Toolbar
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))

        wire_btn = QAction("🔳 Wireframe/Solid", self)
        wire_btn.triggered.connect(self.toggle_wireframe)
        toolbar.addAction(wire_btn)

        screenshot_btn = QAction("📸 Зберегти скрін", self)
        screenshot_btn.triggered.connect(self.save_screenshot)
        toolbar.addAction(screenshot_btn)

        export_btn = QAction("📝 Експорт", self)
        export_btn.triggered.connect(self.export_info)
        toolbar.addAction(export_btn)

        if self.go_back_callback:
            back_btn = QAction("⬅️ Назад", self)
            back_btn.triggered.connect(lambda: self.go_back_callback("home"))
            toolbar.addAction(back_btn)

        center_layout.addWidget(toolbar)
        layout.addLayout(center_layout)

        # Панель праворуч (висота)
        right_controls = QVBoxLayout()
        right_controls.addWidget(QLabel("🌄 Висота"))
        self.el_slider = QSlider(Qt.Vertical)
        self.el_slider.setRange(-90, 90)
        self.el_slider.setValue(45)
        self.el_slider.valueChanged.connect(lambda val: self.set_light_angle(val, 'el'))
        right_controls.addWidget(self.el_slider)
        layout.addLayout(right_controls)

        theme_btn = QAction("🌓 Змінити тему", self)
        theme_btn.triggered.connect(self.gl_widget.toggle_theme)
        toolbar.addAction(theme_btn)

    def toggle_wireframe(self):
        self.gl_widget.wireframe = not self.gl_widget.wireframe
        self.gl_widget.update()

    def save_screenshot(self):
        img = self.gl_widget.grabFramebuffer()
        file, _ = QFileDialog.getSaveFileName(self, "Зберегти скріншот", "model.png", "PNG (*.png)")
        if file:
            img.save(file)

    def export_info(self):
        vertices, faces = self.gl_widget.model
        with open("model_info.txt", "w", encoding="utf-8") as f:
            f.write(f"Вершин: {len(vertices)}\n")
            f.write(f"Граней: {len(faces)}\n")

    def set_light_angle(self, value, mode):
        if mode == 'az':
            self.gl_widget.light_azimuth = value
        elif mode == 'el':
            self.gl_widget.light_elevation = value
        self.gl_widget.update()

    def set_obj_file(self, file_path):
        self.gl_widget.load_model(file_path)

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#121212"))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#1e1e1e"))
        palette.setColor(QPalette.AlternateBase, QColor("#2e2e2e"))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#2e2e2e"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

