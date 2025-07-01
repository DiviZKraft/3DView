from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog,
    QSlider, QToolBar, QAction, QSizePolicy, QMessageBox, QColorDialog
)
from PyQt5.QtCore import Qt, QSize
from widgets.simple_gl_widget import SimpleGLWidget
from ui.theme_manager import ThemeManager
from ui.constants import BUTTON_STYLE, LABEL_STYLE
import os

class Viewer3DPage(QWidget):
    """
    Сторінка з 3D-рендером, керуванням камерою, експортом, зміною фону.
    """
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

        export_btn = QAction("💾 Експортувати як...", self)
        export_btn.triggered.connect(self.export_model_dialog)
        toolbar.addAction(export_btn)

        color_action = QAction("🎨 Колір фону", self)
        color_action.triggered.connect(self.change_bg_color)
        toolbar.addAction(color_action)

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

    def set_light_angle(self, value, mode):
        if mode == 'az':
            self.gl_widget.light_azimuth = value
        elif mode == 'el':
            self.gl_widget.light_elevation = value
        self.gl_widget.update()

    def set_obj_file(self, file_path):
        self.gl_widget.load_model(file_path)

    def change_bg_color(self):
        col = QColorDialog.getColor()
        if col.isValid():
            r, g, b, _ = col.getRgbF()
            self.gl_widget.set_background_color(r, g, b, 1.0)

    def export_model_dialog(self):
        vertices, faces = self.gl_widget.model
        if not vertices or not faces:
            QMessageBox.warning(self, "Експорт", "Модель не завантажена!")
            return
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Експортувати модель", "model",
            "OBJ файли (*.obj);;PLY файли (*.ply)"
        )
        if not file_path:
            return
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext == ".obj":
                self.export_obj(vertices, faces, file_path)
            elif ext == ".ply":
                self.export_ply(vertices, faces, file_path)
            else:
                QMessageBox.warning(self, "Експорт", "Непідтримуваний формат!")
                return
            QMessageBox.information(self, "Експорт", "Експорт виконано успішно!")
        except Exception as e:
            QMessageBox.critical(self, "Експорт", f"Помилка експорту: {e}")

    def export_obj(self, vertices, faces, file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            for v in vertices:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
            for face in faces:
                indices = [str(idx + 1) for idx in face]
                f.write(f"f {' '.join(indices)}\n")

    def export_ply(self, vertices, faces, file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("ply\nformat ascii 1.0\n")
            f.write(f"element vertex {len(vertices)}\n")
            f.write("property float x\nproperty float y\nproperty float z\n")
            f.write(f"element face {len(faces)}\n")
            f.write("property list uchar int vertex_indices\nend_header\n")
            for v in vertices:
                f.write(f"{v[0]} {v[1]} {v[2]}\n")
            for face in faces:
                f.write(f"{len(face)} {' '.join(str(idx) for idx in face)}\n")
