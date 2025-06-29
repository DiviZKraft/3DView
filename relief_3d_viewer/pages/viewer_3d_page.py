from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog, QSlider, QToolBar, QAction, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from widgets.simple_gl_widget import SimpleGLWidget
from ui.theme_manager import ThemeManager
from ui.constants import BUTTON_STYLE, LABEL_STYLE

class Viewer3DPage(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback
        self.theme_manager = ThemeManager()

        main_layout = QVBoxLayout(self)
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))

        screenshot_btn = QAction("📸 Зберегти скрін", self)
        screenshot_btn.triggered.connect(self.save_screenshot)
        toolbar.addAction(screenshot_btn)

        export_btn = QAction("📝 Експорт", self)
        export_btn.triggered.connect(self.export_info)
        toolbar.addAction(export_btn)

        theme_btn = QAction("🌓 Тема", self)
        theme_btn.triggered.connect(self.theme_manager.toggle_theme)
        toolbar.addAction(theme_btn)

        if self.go_back_callback:
            back_btn = QAction("⬅️ Назад", self)
            back_btn.triggered.connect(lambda: self.go_back_callback("home"))
            toolbar.addAction(back_btn)

        main_layout.addWidget(toolbar)
        content_layout = QHBoxLayout()

        # --- Left Controls (Azimuth) ---
        left_controls = QVBoxLayout()
        az_label = QLabel("☀️ Азимут")
        az_label.setStyleSheet(LABEL_STYLE)
        left_controls.addWidget(az_label)
        self.az_slider = QSlider(Qt.Vertical)
        self.az_slider.setRange(0, 360)
        self.az_slider.setValue(45)
        self.az_slider.valueChanged.connect(lambda val: self.set_light_angle(val, 'az'))
        left_controls.addWidget(self.az_slider)
        content_layout.addLayout(left_controls)

        # --- Center (3D) ---
        center_layout = QVBoxLayout()
        self.info_label = QLabel("ℹ️ Інформація про модель")
        self.info_label.setStyleSheet(LABEL_STYLE)
        center_layout.addWidget(self.info_label)

        self.gl_widget = SimpleGLWidget(self.info_label)
        self.gl_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout.addWidget(self.gl_widget)

        # --- Bottom Controls (Buttons) ---
        bottom_controls = QHBoxLayout()
        self.normal_btn = QPushButton("🧭 Нормалі")
        self.normal_btn.setStyleSheet(BUTTON_STYLE)
        self.normal_btn.setCheckable(True)
        self.normal_btn.clicked.connect(self.toggle_normals)
        bottom_controls.addWidget(self.normal_btn)

        self.texture_btn = QPushButton("🖼️ Текстура")
        self.texture_btn.setStyleSheet(BUTTON_STYLE)
        self.texture_btn.setCheckable(True)
        self.texture_btn.clicked.connect(self.toggle_textures)
        bottom_controls.addWidget(self.texture_btn)

        self.wire_btn = QPushButton("🔳 Wireframe/Solid")
        self.wire_btn.setStyleSheet(BUTTON_STYLE)
        self.wire_btn.setCheckable(True)
        self.wire_btn.clicked.connect(self.toggle_wireframe)
        bottom_controls.addWidget(self.wire_btn)

        center_layout.addLayout(bottom_controls)
        content_layout.addLayout(center_layout)

        # --- Right Controls (Elevation) ---
        right_controls = QVBoxLayout()
        el_label = QLabel("🌄 Висота")
        el_label.setStyleSheet(LABEL_STYLE)
        right_controls.addWidget(el_label)
        self.el_slider = QSlider(Qt.Vertical)
        self.el_slider.setRange(-90, 90)
        self.el_slider.setValue(45)
        self.el_slider.valueChanged.connect(lambda val: self.set_light_angle(val, 'el'))
        right_controls.addWidget(self.el_slider)
        content_layout.addLayout(right_controls)

        main_layout.addLayout(content_layout)

    def toggle_wireframe(self):
        self.gl_widget.wireframe = not self.gl_widget.wireframe
        self.wire_btn.setChecked(self.gl_widget.wireframe)
        self.gl_widget.update()

    def toggle_normals(self):
        self.gl_widget.toggle_normals()
        self.normal_btn.setChecked(self.gl_widget.show_normals)

    def toggle_textures(self):
        self.gl_widget.toggle_textures()
        self.texture_btn.setChecked(self.gl_widget.show_texture)

    def save_screenshot(self):
        img = self.gl_widget.grabFramebuffer()
        file, _ = QFileDialog.getSaveFileName(self, "Зберегти скріншот", "model.png", "PNG (*.png)")
        if file:
            img.save(file)

    def export_info(self):
        vertices, faces = self.gl_widget.model
        file, _ = QFileDialog.getSaveFileName(self, "Експортувати інфо", "model_info.txt", "Text (*.txt)")
        if file:
            with open(file, "w", encoding="utf-8") as f:
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
