from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog,
    QSlider, QToolBar, QAction, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette, QColor
from widgets.simple_gl_widget import SimpleGLWidget


class Viewer3DPage(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()

        self.set_dark_theme()
        self.go_back_callback = go_back_callback

        main_layout = QVBoxLayout(self)

        # === Верхній тулбар (навігація) ===
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))

        screenshot_btn = QAction("📸 Зберегти скрін", self)
        screenshot_btn.triggered.connect(self.save_screenshot)
        toolbar.addAction(screenshot_btn)

        export_btn = QAction("📝 Експорт", self)
        export_btn.triggered.connect(self.export_info)
        toolbar.addAction(export_btn)

        theme_btn = QAction("🌓 Тема", self)
        theme_btn.triggered.connect(self.toggle_theme)
        toolbar.addAction(theme_btn)

        if self.go_back_callback:
            back_btn = QAction("⬅️ Назад", self)
            back_btn.triggered.connect(lambda: self.go_back_callback("home"))
            toolbar.addAction(back_btn)

        main_layout.addWidget(toolbar)

        # === Центр: 3D сцена і повзунки ===
        content_layout = QHBoxLayout()

        # Лівий слайдер (Азимут)
        left_controls = QVBoxLayout()
        left_controls.addWidget(QLabel("☀️ Азимут"))
        self.az_slider = QSlider(Qt.Vertical)
        self.az_slider.setRange(0, 360)
        self.az_slider.setValue(45)
        self.az_slider.valueChanged.connect(lambda val: self.set_light_angle(val, 'az'))
        left_controls.addWidget(self.az_slider)
        content_layout.addLayout(left_controls)

        # Центр: сцена + info + нижні кнопки
        center_layout = QVBoxLayout()
        self.info_label = QLabel("ℹ️ Інформація про модель")
        self.info_label.setStyleSheet("font-size: 16px; padding: 4px;")
        center_layout.addWidget(self.info_label)

        self.gl_widget = SimpleGLWidget(self.info_label)
        self.gl_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout.addWidget(self.gl_widget)

        # Нижні кнопки (режими перегляду)
        bottom_controls = QHBoxLayout()
        normal_btn = QPushButton("🧭 Нормалі")
        normal_btn.clicked.connect(self.gl_widget.toggle_normals)
        bottom_controls.addWidget(normal_btn)

        texture_btn = QPushButton("🖼️ Текстура")
        texture_btn.clicked.connect(self.gl_widget.toggle_textures)
        bottom_controls.addWidget(texture_btn)

        wire_btn = QPushButton("🔳 Wireframe/Solid")
        wire_btn.clicked.connect(self.toggle_wireframe)
        bottom_controls.addWidget(wire_btn)

        center_layout.addLayout(bottom_controls)
        content_layout.addLayout(center_layout)

        # Правий слайдер (Висота)
        right_controls = QVBoxLayout()
        right_controls.addWidget(QLabel("🌄 Висота"))
        self.el_slider = QSlider(Qt.Vertical)
        self.el_slider.setRange(-90, 90)
        self.el_slider.setValue(45)
        self.el_slider.valueChanged.connect(lambda val: self.set_light_angle(val, 'el'))
        right_controls.addWidget(self.el_slider)
        content_layout.addLayout(right_controls)

        main_layout.addLayout(content_layout)

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

    def toggle_theme(self):
        self.gl_widget.toggle_theme()

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