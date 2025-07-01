import os
import math
import numpy as np
from PyQt5.QtWidgets import QOpenGLWidget, QMessageBox
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import *
from utils.model_loader import load_obj_with_texture, load_ply

class SimpleGLWidget(QOpenGLWidget):
    def __init__(self, info_label):
        super().__init__()
        self.model = ([], [])
        self.texture_id = None
        self.wireframe = False
        self.smooth_shading = True
        self.background_color = (0.93, 1, 0.93, 1.0)
        self.target = [0.0, 0.0, 0.0]
        self.distance = 5.0
        self.azimuth = 45.0
        self.elevation = 20.0
        self.light_azimuth = 45
        self.light_elevation = 45
        self.middle_button_pressed = False
        self.shift_pressed = False
        self.last_x = 0
        self.last_y = 0
        self.info_label = info_label
        self.model_rotation_y = 0.0

        # Flat and smooth geometry arrays
        self._vertex_array = None
        self._normal_array = None
        self._tri_index_array = None
        self._quad_index_array = None

        # FLAT SHADING arrays
        self._flat_tri_vertex_array = None
        self._flat_tri_normal_array = None
        self._flat_quad_vertex_array = None
        self._flat_quad_normal_array = None

        self.view_mode = 0

        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

    def set_background_color(self, r, g, b, a=1.0):
        self.background_color = (r, g, b, a)
        self.update()

    def load_model(self, path):
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".obj":
                self.model, _ = load_obj_with_texture(path)
            elif ext == ".ply":
                self.model = load_ply(path)
            else:
                raise ValueError("Непідтримуваний формат файлу.")
            self.reset_view_to_model()
            self.prepare_arrays()
            self.update_info()
            self.update()
        except Exception as e:
            QMessageBox.critical(self, "Помилка моделі", str(e))

    def prepare_arrays(self):
        vertices, faces = self.model
        if not vertices or not faces:
            self._vertex_array = None
            self._normal_array = None
            self._tri_index_array = None
            self._quad_index_array = None
            self._flat_tri_vertex_array = None
            self._flat_tri_normal_array = None
            self._flat_quad_vertex_array = None
            self._flat_quad_normal_array = None
            return

        self._vertex_array = np.array(vertices, dtype=np.float32)
        triangles = []
        quads = []
        for f in faces:
            if len(f) == 3:
                triangles.append(f)
            elif len(f) == 4:
                quads.append(f)
            elif len(f) > 4:
                # Багатокутники — триангуляція (залишаємо як трикутники)
                for i in range(1, len(f)-1):
                    triangles.append([f[0], f[i], f[i+1]])
        self._tri_index_array = np.array(triangles, dtype=np.uint32).flatten() if triangles else None
        self._quad_index_array = np.array(quads, dtype=np.uint32).flatten() if quads else None

        # Гладкі нормалі (vertex normals)
        vertex_normals = [np.zeros(3, dtype=np.float32) for _ in vertices]
        for f in faces:
            verts = [np.array(vertices[i]) for i in f]
            if len(verts) < 3: continue
            v1 = verts[1] - verts[0]
            v2 = verts[2] - verts[0]
            n = np.cross(v1, v2)
            n = n / (np.linalg.norm(n) if np.linalg.norm(n) > 0 else 1)
            for idx in f:
                vertex_normals[idx] += n
        vertex_normals = [n / (np.linalg.norm(n) if np.linalg.norm(n) > 0 else 1) for n in vertex_normals]
        self._normal_array = np.array(vertex_normals, dtype=np.float32)

        # FLAT: окремо для трикутників і чотирикутників
        flat_tri_vertices = []
        flat_tri_normals = []
        flat_quad_vertices = []
        flat_quad_normals = []
        for f in faces:
            verts = [np.array(vertices[i]) for i in f]
            if len(f) == 3:
                v1 = verts[1] - verts[0]
                v2 = verts[2] - verts[0]
                n = np.cross(v1, v2)
                n = n / (np.linalg.norm(n) if np.linalg.norm(n) > 0 else 1)
                for i in range(3):
                    flat_tri_vertices.append(vertices[f[i]])
                    flat_tri_normals.append(n)
            elif len(f) == 4:
                v1 = verts[1] - verts[0]
                v2 = verts[2] - verts[0]
                n = np.cross(v1, v2)
                n = n / (np.linalg.norm(n) if np.linalg.norm(n) > 0 else 1)
                for i in range(4):
                    flat_quad_vertices.append(vertices[f[i]])
                    flat_quad_normals.append(n)
            elif len(f) > 4:
                # багатокутники — трикутники (fan)
                for i in range(1, len(f)-1):
                    tri = [f[0], f[i], f[i+1]]
                    tri_verts = [np.array(vertices[idx]) for idx in tri]
                    v1 = tri_verts[1] - tri_verts[0]
                    v2 = tri_verts[2] - tri_verts[0]
                    n = np.cross(v1, v2)
                    n = n / (np.linalg.norm(n) if np.linalg.norm(n) > 0 else 1)
                    for idx in tri:
                        flat_tri_vertices.append(vertices[idx])
                        flat_tri_normals.append(n)
        self._flat_tri_vertex_array = np.array(flat_tri_vertices, dtype=np.float32) if flat_tri_vertices else None
        self._flat_tri_normal_array = np.array(flat_tri_normals, dtype=np.float32) if flat_tri_normals else None
        self._flat_quad_vertex_array = np.array(flat_quad_vertices, dtype=np.float32) if flat_quad_vertices else None
        self._flat_quad_normal_array = np.array(flat_quad_normals, dtype=np.float32) if flat_quad_normals else None

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
        glShadeModel(GL_SMOOTH if self.smooth_shading else GL_FLAT)
        self.setup_materials()

    def setup_materials(self):
        diffuse = [0.82, 0.82, 0.82, 1.0]
        ambient = [0.32, 0.32, 0.32, 1.0]
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 1)

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
        glRotatef(self.model_rotation_y, 0, 1, 0)

        glShadeModel(GL_SMOOTH if self.smooth_shading else GL_FLAT)

        if self.smooth_shading:
            # Smoothing: стандартний рендер (vertex + normal + індекси)
            if self._vertex_array is not None:
                glEnableClientState(GL_VERTEX_ARRAY)
                glVertexPointer(3, GL_FLOAT, 0, self._vertex_array)
                glEnableClientState(GL_NORMAL_ARRAY)
                glNormalPointer(GL_FLOAT, 0, self._normal_array)
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if self.wireframe else GL_FILL)
                if self._tri_index_array is not None:
                    glDrawElements(GL_TRIANGLES, len(self._tri_index_array), GL_UNSIGNED_INT, self._tri_index_array)
                if self._quad_index_array is not None:
                    glDrawElements(GL_QUADS, len(self._quad_index_array), GL_UNSIGNED_INT, self._quad_index_array)
                glDisableClientState(GL_NORMAL_ARRAY)
                glDisableClientState(GL_VERTEX_ARRAY)
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            # FLAT: рендеримо окремо трикутники і чотирикутники з дубльованими нормалями
            if self._flat_tri_vertex_array is not None:
                glEnableClientState(GL_VERTEX_ARRAY)
                glEnableClientState(GL_NORMAL_ARRAY)
                glVertexPointer(3, GL_FLOAT, 0, self._flat_tri_vertex_array)
                glNormalPointer(GL_FLOAT, 0, self._flat_tri_normal_array)
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if self.wireframe else GL_FILL)
                glDrawArrays(GL_TRIANGLES, 0, len(self._flat_tri_vertex_array))
                glDisableClientState(GL_NORMAL_ARRAY)
                glDisableClientState(GL_VERTEX_ARRAY)
            if self._flat_quad_vertex_array is not None:
                glEnableClientState(GL_VERTEX_ARRAY)
                glEnableClientState(GL_NORMAL_ARRAY)
                glVertexPointer(3, GL_FLOAT, 0, self._flat_quad_vertex_array)
                glNormalPointer(GL_FLOAT, 0, self._flat_quad_normal_array)
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if self.wireframe else GL_FILL)
                glDrawArrays(GL_QUADS, 0, len(self._flat_quad_vertex_array))
                glDisableClientState(GL_NORMAL_ARRAY)
                glDisableClientState(GL_VERTEX_ARRAY)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

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
        direction = [x, y, z, 0.0]
        glLightfv(GL_LIGHT0, GL_POSITION, direction)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.23, 0.23, 0.23, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])

    # --- Управління камерою ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton or event.button() == Qt.LeftButton:
            self.middle_button_pressed = True
        self.last_x = event.x()
        self.last_y = event.y()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton or event.button() == Qt.LeftButton:
            self.middle_button_pressed = False

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_x
        dy = event.y() - self.last_y
        if self.middle_button_pressed:
            if self.shift_pressed:
                self.pan_camera(dx, dy)
            else:
                self.azimuth += dx * 0.5
                if self.view_mode == 0:
                    self.elevation += dy * 0.5
                    self.elevation = max(-35, min(35, self.elevation))
                else:
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

    def set_shadow(self, enabled):
        pass

    def rotate_y(self, angle):
        self.model_rotation_y = (self.model_rotation_y + angle) % 360
        self.update()

    def set_view_mode(self, mode):
        self.view_mode = mode
        if mode == 0:
            self.set_perspective_camera()
        elif mode == 1:
            self.set_top_view()
        elif mode == 2:
            self.set_bottom_view()
        elif mode == 3:
            self.set_side_view()
        self.update()

    def set_perspective_camera(self):
        self.azimuth = 45
        self.elevation = 20
        self.distance = 5.0

    def set_top_view(self):
        self.azimuth = 0
        self.elevation = 90
        self.distance = 5.0

    def set_bottom_view(self):
        self.azimuth = 0
        self.elevation = -90
        self.distance = 5.0

    def set_side_view(self):
        self.azimuth = 90
        self.elevation = 0
        self.distance = 5.0

    # --- Перемикач шейдингу ---
    def toggle_smooth_shading(self):
        self.smooth_shading = not self.smooth_shading
        self.update()
