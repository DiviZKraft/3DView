import os
import math
from PyQt5.QtWidgets import QOpenGLWidget, QMessageBox
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from utils.model_loader import load_obj_with_texture, load_fbx

class SimpleGLWidget(QOpenGLWidget):
    def __init__(self, info_label):
        super().__init__()
        self.model = ([], [])
        self.texture_id = None
        self.wireframe = False
        self.show_normals = False
        self.show_texture = True
        # Колір фону окремо, незалежно від теми
        self.background_color = (0.1, 0.1, 0.1, 1.0)

        self.target = [0.0, 0.0, 0.0]
        self.distance = 5.0
        self.azimuth = 0.0
        self.elevation = 20.0
        self.light_azimuth = 45
        self.light_elevation = 45
        self.middle_button_pressed = False
        self.shift_pressed = False
        self.last_x = 0
        self.last_y = 0
        self.info_label = info_label
        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

    def set_background_color(self, r, g, b, a=1.0):
        """Змінити колір фону сцени OpenGL."""
        self.background_color = (r, g, b, a)
        self.update()

    def load_model(self, path):
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".obj":
                self.model, texture_path = load_obj_with_texture(path)
                if texture_path and os.path.exists(texture_path):
                    self.load_texture(texture_path)
                else:
                    self.texture_id = None
            elif ext == ".fbx":
                self.model = load_fbx(path)
                self.texture_id = None
            else:
                raise ValueError("Непідтримуваний формат файлу.")
            self.reset_view_to_model()
            self.update_info()
            self.update()
        except Exception as e:
            QMessageBox.critical(self, "Помилка моделі", str(e))

    def load_texture(self, image_path):
        try:
            image = Image.open(image_path).transpose(Image.FLIP_TOP_BOTTOM)
            img_data = image.convert("RGB").tobytes()
            width, height = image.size
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        except Exception:
            self.texture_id = None

    def update_info(self):
        vertices, faces = self.model
        self.info_label.setText(f"Вершин: {len(vertices)} | Граней: {len(faces)}")

    def reset_view_to_model(self):
        vertices, _ = self.model
        if not vertices:
            return
        xs, ys, zs = zip(*vertices)
        self.target = [(min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, (min(zs) + max(zs)) / 2]
        size = max(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))
        self.distance = size * 1.5 if size > 0 else 5.0

    def initializeGL(self):
        self.set_clear_color()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w / h if h != 0 else 1, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        self.set_clear_color()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        eye = self.get_camera_position()
        gluLookAt(*eye, *self.target, 0, 1, 0)
        self.update_light()
        vertices, faces = self.model
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if self.wireframe else GL_FILL)
        for face in faces:
            if len(face) < 3: continue
            glBegin(GL_POLYGON)
            face_vertices = [vertices[i] for i in face]
            normal = self.compute_face_normal(face_vertices)
            glNormal3fv(normal)
            if self.show_normals:
                glColor3f(0.6, 0.6, 1.0) if normal[2] >= 0 else glColor3f(1.0, 0.4, 0.4)
            else:
                glColor3f(0.8, 0.8, 0.8)
            for v in face_vertices:
                glVertex3fv(v)
            glEnd()

    def set_clear_color(self):
        r, g, b, a = self.background_color
        glClearColor(r, g, b, a)

    def get_camera_position(self):
        phi = math.radians(self.azimuth)
        theta = math.radians(self.elevation)
        x = self.distance * math.cos(theta) * math.sin(phi)
        y = self.distance * math.sin(theta)
        z = self.distance * math.cos(theta) * math.cos(phi)
        return [self.target[0] + x, self.target[1] + y, self.target[2] + z]

    def compute_face_normal(self, verts):
        if len(verts) < 3: return [0, 0, 1]
        v1 = [verts[1][i] - verts[0][i] for i in range(3)]
        v2 = [verts[2][i] - verts[0][i] for i in range(3)]
        normal = [
            v1[1]*v2[2] - v1[2]*v2[1],
            v1[2]*v2[0] - v1[0]*v2[2],
            v1[0]*v2[1] - v1[1]*v2[0]
        ]
        length = math.sqrt(sum(n * n for n in normal))
        return [n / length for n in normal] if length else [0, 0, 1]

    def update_light(self):
        az = math.radians(self.light_azimuth)
        el = math.radians(self.light_elevation)
        x = math.cos(el) * math.cos(az)
        y = math.sin(el)
        z = math.cos(el) * math.sin(az)
        glLightfv(GL_LIGHT0, GL_POSITION, [x * 10, y * 10, z * 10, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

    def toggle_normals(self):
        self.show_normals = not self.show_normals
        self.update()

    def toggle_textures(self):
        self.show_texture = not self.show_texture
        self.update()

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
