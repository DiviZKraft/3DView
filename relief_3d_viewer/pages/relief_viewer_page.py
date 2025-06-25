from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.mplot3d import Axes3D  # потрібно для 3D
from matplotlib import cm

class ReliefViewerPage(QWidget):
    def __init__(self, navigate_to):
        super().__init__()
        self.navigate_to = navigate_to

        self.layout = QVBoxLayout()
        self.label = QLabel("🌄 Рельєф не завантажено")
        self.layout.addWidget(self.label)

        # Полотно matplotlib для 3D
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.back_btn = QPushButton("← Назад")
        self.back_btn.clicked.connect(lambda: self.navigate_to("search"))
        self.layout.addWidget(self.back_btn)

        self.setLayout(self.layout)

    def set_relief_file(self, path):
        if not os.path.exists(path):
            self.label.setText("Файл не знайдено.")
            return

        self.label.setText(f"🌄 Відкрито: {os.path.basename(path)}")
        elevation_data = self.read_asc_file(path)

        if elevation_data is not None:
            self.plot_surface(elevation_data)
        else:
            self.label.setText("Помилка при читанні файлу рельєфу.")

    def read_asc_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                header = {}
                for _ in range(6):
                    line = f.readline()
                    key, value = line.strip().split()
                    header[key.lower()] = float(value)

                data = []
                for line in f:
                    row = [float(val) for val in line.strip().split()]
                    data.append(row)

                arr = np.array(data)
                arr[arr == header['nodata_value']] = np.nan
                return arr
        except Exception as e:
            print(f"Помилка при читанні .asc: {e}")
            return None

    def plot_surface(self, elevation):
        self.figure.clear()
        ax = self.figure.add_subplot(111, projection='3d')

        nrows, ncols = elevation.shape
        x = np.arange(ncols)
        y = np.arange(nrows)
        X, Y = np.meshgrid(x, y)

        ax.plot_surface(X, Y, elevation, cmap=cm.terrain, edgecolor='none')
        ax.set_title("3D-поверхня рельєфу")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Висота")
        self.canvas.draw()
