from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFileDialog,
    QSlider, QToolBar, QAction, QSizePolicy, QMessageBox, QColorDialog
)
from PyQt5.QtCore import Qt, QSize, QTimer
from widgets.simple_gl_widget import SimpleGLWidget
from ui.theme_manager import ThemeManager
from ui.constants import LABEL_STYLE
import os

BASEDIR = os.path.dirname(os.path.abspath(__file__))
STYLE_DARK_PATH = os.path.join(BASEDIR, "ui", "styles_dark.qss")
STYLE_LIGHT_PATH = os.path.join(BASEDIR, "ui", "styles_light.qss")

class Viewer3DPage(QWidget):
    """
    Сторінка з 3D-рендером, керуванням камерою, експортом, зміною фону та теми.
    """

    def __init__(self, go_back_callback):
        super().__init__()
        self.go_back_callback = go_back_callback    # Колбек для повернення на попередню сторінку
        self.theme_mode = "dark"                   # Поточний режим теми

        self.shadow_enabled = False                # (зарезервовано під тіні)
        self.auto_rotate_enabled = False           # Автоматичне обертання моделі
        self.current_view_mode = 0                 # Режим камери (0 - перспектива, 1 - top...)

        # Таймер для автоповороту моделі
        self.rotate_timer = QTimer(self)
        self.rotate_timer.timeout.connect(self.rotate_model)

        main_layout = QVBoxLayout(self)
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))

        # --- Кнопки тулбара ---
        screenshot_btn = QAction("📸 Зберегти скрін", self)
        screenshot_btn.triggered.connect(self.save_screenshot)
        toolbar.addAction(screenshot_btn)

        export_btn = QAction("💾 Експортувати як...", self)
        export_btn.triggered.connect(self.export_model_dialog)
        toolbar.addAction(export_btn)

        color_action = QAction("🎨 Колір фону", self)
        color_action.triggered.connect(self.change_bg_color)
        toolbar.addAction(color_action)

        # Кнопка повернення назад (якщо є)
        if self.go_back_callback:
            back_btn = QAction("⬅️ Назад", self)
            back_btn.triggered.connect(lambda: self.go_back_callback("home"))
            toolbar.addAction(back_btn)

        main_layout.addWidget(toolbar)
        content_layout = QHBoxLayout()

        # --- Праві контролери (Elevation - підйом джерела світла) ---
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

        # --- Центр (OpenGL віджет + кнопки керування) ---
        center_layout = QVBoxLayout()
        self.info_label = QLabel("ℹ️ Інформація про модель")
        self.info_label.setStyleSheet(LABEL_STYLE)
        center_layout.addWidget(self.info_label)

        self.gl_widget = SimpleGLWidget(self.info_label)
        self.gl_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout.addWidget(self.gl_widget)

        # --- Нижні кнопки (керування переглядом) ---
        bottom_controls = QHBoxLayout()
        bottom_controls.setSpacing(12)

        self.view_btn = QPushButton("👁️ Перспектива")
        self.view_btn.setObjectName("MainButton")
        self.view_btn.clicked.connect(self.cycle_view_mode)
        bottom_controls.addWidget(self.view_btn)

        self.wire_btn = QPushButton("🔳 Wireframe/Solid")
        self.wire_btn.setObjectName("MainButton")
        self.wire_btn.setCheckable(True)
        self.wire_btn.setChecked(False)
        self.wire_btn.clicked.connect(self.toggle_wireframe)
        bottom_controls.addWidget(self.wire_btn)

        self.smooth_btn = QPushButton("🟢 Гладке освітлення")
        self.smooth_btn.setObjectName("MainButton")
        self.smooth_btn.setCheckable(True)
        self.smooth_btn.setChecked(True)
        self.smooth_btn.clicked.connect(self.toggle_smooth_shading)
        bottom_controls.addWidget(self.smooth_btn)

        self.btn_rotate = QPushButton("🔄 Автовертіння")
        self.btn_rotate.setObjectName("MainButton")
        self.btn_rotate.setCheckable(True)
        self.btn_rotate.setChecked(False)
        self.btn_rotate.clicked.connect(self.toggle_auto_rotate)
        bottom_controls.addWidget(self.btn_rotate)

        center_layout.addLayout(bottom_controls)
        content_layout.addLayout(center_layout)

        # --- Ліві контролери (Azimuth - азимут світла) ---
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

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
        # --- Тема встановлюється менеджером при старті ---


    # --- Логіка та обробники кнопок ---

    def cycle_view_mode(self):
        """
        Перемикає режими камери (перспектива, зверху, знизу, збоку).
        """
        self.current_view_mode = (self.current_view_mode + 1) % 4
        if self.current_view_mode == 0:
            self.view_btn.setText("👁️ Перспектива")
        elif self.current_view_mode == 1:
            self.view_btn.setText("⬆️ Зверху")
        elif self.current_view_mode == 2:
            self.view_btn.setText("⬇️ Знизу")
        elif self.current_view_mode == 3:
            self.view_btn.setText("➡️ Збоку")
        if hasattr(self, 'gl_widget'):
            self.gl_widget.set_view_mode(self.current_view_mode)

    def toggle_auto_rotate(self):
        """
        Вмикає/вимикає автоматичне обертання моделі.
        """
        self.auto_rotate_enabled = not self.auto_rotate_enabled
        self.btn_rotate.setChecked(self.auto_rotate_enabled)
        if self.auto_rotate_enabled:
            self.rotate_timer.start(20)
        else:
            self.rotate_timer.stop()

    def rotate_model(self):
        """
        Кожен таймер-тік — обертає модель (для автовертіння).
        """
        if hasattr(self, 'gl_widget'):
            self.gl_widget.rotate_y(2)
            self.gl_widget.update()

    def toggle_wireframe(self):
        """
        Перемикає рендер між solid/wireframe.
        """
        self.gl_widget.wireframe = not self.gl_widget.wireframe
        self.wire_btn.setChecked(self.gl_widget.wireframe)
        self.gl_widget.update()

    def save_screenshot(self):
        """
        Зберігає знімок вікна з моделлю у PNG.
        """
        img = self.gl_widget.grabFramebuffer()
        file, _ = QFileDialog.getSaveFileName(self, "Зберегти скріншот", "model.png", "PNG (*.png)")
        if file:
            img.save(file)

    def set_light_angle(self, value, mode):
        """
        Встановлює кут освітлення (азимут або підйом).
        """
        if mode == 'az':
            self.gl_widget.light_azimuth = value
        elif mode == 'el':
            self.gl_widget.light_elevation = value
        self.gl_widget.update()

    def set_obj_file(self, file_path):
        """
        Завантажує модель для перегляду у OpenGL-віджет.
        """
        self.gl_widget.load_model(file_path)

    def change_bg_color(self):
        """
        Відкриває діалог вибору кольору для фону 3D сцени.
        """
        col = QColorDialog.getColor()
        if col.isValid():
            r, g, b, _ = col.getRgbF()
            self.gl_widget.set_background_color(r, g, b, 1.0)

    def export_model_dialog(self):
        """
        Діалог експорту моделі у .obj або .ply (викликає відповідний метод).
        """
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
        """
        Експортує модель у формат OBJ.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            for v in vertices:
                f.write(f"v {v[0]} {v[1]} {v[2]}\n")
            for face in faces:
                indices = [str(idx + 1) for idx in face]
                f.write(f"f {' '.join(indices)}\n")

    def export_ply(self, vertices, faces, file_path):
        """
        Експортує модель у формат PLY.
        """
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

    def toggle_smooth_shading(self):
        """
        Перемикає між гладким та плоским шейдингом.
        """
        self.gl_widget.toggle_smooth_shading()
        if self.gl_widget.smooth_shading:
            self.smooth_btn.setText("🟢 Гладке освітлення")
            self.smooth_btn.setChecked(True)
        else:
            self.smooth_btn.setText("🔲 Плоске освітлення")
            self.smooth_btn.setChecked(False)
