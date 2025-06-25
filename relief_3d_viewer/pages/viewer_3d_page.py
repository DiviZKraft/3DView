from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QOpenGLWidget, QHBoxLayout, QFileDialog, QSlider, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import os
import math
from utils.model_loader import load_obj_with_texture

class SimpleGLWidget(QOpenGLWidget):
    def __init__(self, info_label):
        super().__init__()
        self.camera_pos = [0.0, 0.0, 5.0]
        self.camera_rot = [0.0, 0.0]
        self.model = ([], [])
        self.texture_id = None
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)
        self.last_x = 0
        self.last_y = 0
        self.mouse_pressed = False
        self.wireframe = False
        self.info_label = info_label

        self.light_azimuth = 45
        self.light_elevation = 45

    def load_model(self, path):
        try:
            self.model, texture_path = load_obj_with_texture(path)
            self.update_info()
            if texture_path and os.path.exists(texture_path):
                self.load_texture(texture_path)
            else:
                self.texture_id = None
            self.update()
        except Exception as e:
            QMessageBox.critical(self, "Помилка моделі", str(e))

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
        gluPerspective(45.0, w / h if h != 0 else 1, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(-self.camera_pos[0], -self.camera_pos[1], -self.camera_pos[2])
        glRotatef(self.camera_rot[0], 1.0, 0.0, 0.0)
        glRotatef(self.camera_rot[1], 0.0, 1.0, 0.0)

        self.update_light()

        vertices, faces = self.model
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if self.wireframe else GL_FILL)
        glBegin(GL_TRIANGLES)
        for face in faces:
            if len(face) >= 3:
                v0 = vertices[face[0]]
                v1 = vertices[face[1]]
                v2 = vertices[face[2]]
                normal = self.compute_face_normal([v0, v1, v2])
                glNormal3fv(normal)
                glVertex3fv(v0)
                glVertex3fv(v1)
                glVertex3fv(v2)
        glEnd()

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
        self.mouse_pressed = True
        self.last_x = event.x()
        self.last_y = event.y()

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            dx = event.x() - self.last_x
            dy = event.y() - self.last_y
            self.camera_rot[0] += dy * 0.5
            self.camera_rot[1] += dx * 0.5
            self.update()
        self.last_x = event.x()
        self.last_y = event.y()

    def wheelEvent(self, event):
        self.camera_pos[2] -= event.angleDelta().y() / 240
        self.update()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_W:
            self.camera_pos[2] -= 0.2
        elif key == Qt.Key_S:
            self.camera_pos[2] += 0.2
        elif key == Qt.Key_A:
            self.camera_pos[0] -= 0.2
        elif key == Qt.Key_D:
            self.camera_pos[0] += 0.2
        elif key == Qt.Key_Q:
            self.camera_pos[1] -= 0.2
        elif key == Qt.Key_E:
            self.camera_pos[1] += 0.2
        self.update()

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
        left_controls.addWidget(QLabel("☀️ Азимут"))
        left_controls.addWidget(az_slider)
        layout.addLayout(left_controls)

        center_layout = QVBoxLayout()
        self.go_back_callback = go_back_callback
        self.info_label = QLabel("ℹ️ Інформація про модель")
        center_layout.addWidget(self.info_label)

        self.gl_widget = SimpleGLWidget(self.info_label)
        center_layout.addWidget(self.gl_widget, stretch=1)

        controls = QHBoxLayout()

        wire_btn = QPushButton("🔳 Wireframe/Solid")
        wire_btn.clicked.connect(self.toggle_wireframe)
        controls.addWidget(wire_btn)

        screenshot_btn = QPushButton("📷 Зберегти скрін")
        screenshot_btn.clicked.connect(self.save_screenshot)
        controls.addWidget(screenshot_btn)

        export_btn = QPushButton("📄 Експорт інфо")
        export_btn.clicked.connect(self.export_info)
        controls.addWidget(export_btn)

        if self.go_back_callback:
            back_btn = QPushButton("⬅️ Назад")
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
        right_controls.addWidget(QLabel("🌅 Висота"))
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
