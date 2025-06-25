from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QOpenGLWidget, QHBoxLayout, QFileDialog, QSlider, QMessageBox
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os
import math
from utils.model_loader import load_obj_with_texture

class SimpleGLWidget(QOpenGLWidget):
    def __init__(self, info_label):
        super().__init__()
        self.target = [0.0, 0.0, 0.0]
        self.distance = 5.0
        self.azimuth = 0.0
        self.elevation = 20.0
        self.model = ([], [])
        self.texture_id = None
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
        self.last_x = 0
        self.last_y = 0
        self.middle_button_pressed = False
        self.shift_pressed = False
        self.wireframe = False
        self.info_label = info_label

        self.light_azimuth = 45
        self.light_elevation = 45

    def load_model(self, path):
        try:
            self.model, texture_path = load_obj_with_texture(path)
            self.reset_view_to_model()
            self.update_info()
            if texture_path and os.path.exists(texture_path):
                self.load_texture(texture_path)
            else:
                self.texture_id = None
            self.update()
        except Exception as e:
            QMessageBox.critical(self, "Помилка моделі", str(e))

    def reset_view_to_model(self):
        vertices, _ = self.model
        if not vertices:
            return
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        zs = [v[2] for v in vertices]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        min_z, max_z = min(zs), max(zs)
        self.target = [
            (min_x + max_x) / 2,
            (min_y + max_y) / 2,
            (min_z + max_z) / 2
        ]
        size = max(max_x - min_x, max_y - min_y, max_z - min_z)
        self.distance = size * 1.5 if size > 0 else 5.0

    def load_texture(self, image_path):
        image = Image.open(image_path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGB").tobytes()
        width, height = image.size

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    def update_info(self):
        vertices, faces = self.model
        self.info_label.setText(f"Вершин: {len(vertices)} | Граней: {len(faces)}")

    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)  # світлий фон
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w / h if h != 0 else 1, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        eye = self.get_camera_position()
        gluLookAt(*eye, *self.target, 0, 1, 0)

        self.update_light()

        vertices, faces = self.model
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if self.wireframe else GL_FILL)
        for face in faces:
            glBegin(GL_TRIANGLES if len(face) == 3 else GL_QUADS if len(face) == 4 else GL_POLYGON)
            face_vertices = [vertices[i] for i in face]
            normal = self.compute_face_normal(face_vertices)
            glNormal3fv(normal)
            for v in face_vertices:
                glVertex3fv(v)
            glEnd()

    def get_camera_position(self):
        phi = math.radians(self.azimuth)
        theta = math.radians(self.elevation)
        x = self.distance * math.cos(theta) * math.sin(phi)
        y = self.distance * math.sin(theta)
        z = self.distance * math.cos(theta) * math.cos(phi)
        return [self.target[0] + x, self.target[1] + y, self.target[2] + z]

    def compute_face_normal(self, verts):
        if len(verts) < 3:
            return [0, 0, 1]
        v1 = [verts[1][i] - verts[0][i] for i in range(3)]
        v2 = [verts[2][i] - verts[0][i] for i in range(3)]
        normal = [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ]
        length = math.sqrt(sum(n * n for n in normal))
        return [n / length for n in normal] if length else [0, 0, 1]

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_button_pressed = True
        self.last_x = event.x()
        self.last_y = event.y()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middle_button_pressed = False

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_x
        dy = event.y() - self.last_y
        if self.middle_button_pressed:
            if self.shift_pressed:
                self.pan_camera(dx, dy)
            else:
                self.azimuth += dx * 0.5
                self.elevation += dy * 0.5
                self.elevation = max(-89, min(89, self.elevation))
            self.update()
        self.last_x = event.x()
        self.last_y = event.y()

    def pan_camera(self, dx, dy):
        right = [math.cos(math.radians(self.azimuth)), 0, -math.sin(math.radians(self.azimuth))]
        scale = 0.01 * self.distance
        self.target[0] -= right[0] * dx * scale
        self.target[1] += dy * scale
        self.target[2] -= right[2] * dx * scale

    def wheelEvent(self, event):
        self.distance *= 0.9 if event.angleDelta().y() > 0 else 1.1
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = True

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Shift:
            self.shift_pressed = False

    def update_light(self):
        az = math.radians(self.light_azimuth)
        el = math.radians(self.light_elevation)
        x = math.cos(el) * math.cos(az)
        y = math.sin(el)
        z = math.cos(el) * math.sin(az)
        glLightfv(GL_LIGHT0, GL_POSITION, [x * 10, y * 10, z * 10, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])












class Viewer3DPage(QWidget):
    def __init__(self, go_back_callback):
        super().__init__()
        layout = QHBoxLayout()

        left_controls = QVBoxLayout()
        az_slider = QSlider(Qt.Vertical)
        az_slider.setMinimum(0)
        az_slider.setMaximum(360)
        az_slider.setValue(45)
        az_slider.valueChanged.connect(lambda val: self.set_light_angle(val, 'az'))
        left_controls.addWidget(QLabel("\u2600\ufe0f Азимут"))
        left_controls.addWidget(az_slider)
        layout.addLayout(left_controls)

        center_layout = QVBoxLayout()
        self.go_back_callback = go_back_callback
        self.info_label = QLabel("\u2139\ufe0f Інформація про модель")
        center_layout.addWidget(self.info_label)

        self.gl_widget = SimpleGLWidget(self.info_label)
        center_layout.addWidget(self.gl_widget, stretch=1)

        controls = QHBoxLayout()

        wire_btn = QPushButton("\ud83d\udd33 Wireframe/Solid")
        wire_btn.clicked.connect(self.toggle_wireframe)
        controls.addWidget(wire_btn)

        screenshot_btn = QPushButton("\ud83d\udcf7 Зберегти скрін")
        screenshot_btn.clicked.connect(self.save_screenshot)
        controls.addWidget(screenshot_btn)

        if self.go_back_callback:
            back_btn = QPushButton("\u2b05\ufe0f Назад")
            back_btn.clicked.connect(lambda: self.go_back_callback("home"))
            controls.addWidget(back_btn)

        center_layout.addLayout(controls)
        layout.addLayout(center_layout)

        right_controls = QVBoxLayout()
        el_slider = QSlider(Qt.Vertical)
        el_slider.setMinimum(-90)
        el_slider.setMaximum(90)
        el_slider.setValue(45)
        el_slider.valueChanged.connect(lambda val: self.set_light_angle(val, 'el'))
        right_controls.addWidget(QLabel("\ud83c\udf05 Висота"))
        right_controls.addWidget(el_slider)
        layout.addLayout(right_controls)

        self.setLayout(layout)

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
