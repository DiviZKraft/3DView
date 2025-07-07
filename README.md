
# 3DModelViewer

**3DModelViewer** — це сучасний десктопний застосунок для перегляду та аналізу тривимірних моделей у форматах OBJ та PLY. Програма створена на Python з використанням PyQt5 і OpenGL, має зручний інтерфейс та дозволяє легко працювати з 3D-об’єктами.

## Основні можливості

* Відкриття та перегляд 3D-моделей у форматах `.obj` і `.ply`
* Інтерактивне керування камерою: обертання, масштабування, панорамування
* Перемикання між темною та світлою темами інтерфейсу
* Відображення/приховування нормалей та текстур (у перспективі — покращена підтримка текстур)
* Інформаційна панель із відображенням основних параметрів моделі: кількість вершин, полігонів, габарити
* Збереження скриншоту поточного вигляду 3D-сцени
* Історія відкритих файлів для швидкого доступу до нещодавно переглянутих моделей
* Підтримка drag-and-drop для відкриття моделей

## Архітектура

Проєкт побудовано за модульним принципом:

* **main.py** — точка входу до застосунку
* **pages/** — сторінки інтерфейсу (головна, пошук файлів, 3D-перегляд)
* **widgets/** — кастомні віджети (наприклад, SimpleGLWidget для OpenGL-відображення)
* **utils/** — допоміжні утиліти (завантажувач моделей, менеджер історії)
* **ui/** — стилі (QSS) та менеджер тем
* **vertex/** — шейдери для рендерингу
* **icons/** — графічні ресурси

## Встановлення та запуск

### Необхідні залежності

* Python 3.9+
* PyQt5
* PyOpenGL
* trimesh
* numpy

Встановити залежності можна командою:

```bash
pip install -r requirements.txt
```

### Запуск програми

```bash
python main.py
```

### Системні вимоги

* ОС: Windows, Linux, MacOS
* Відеокарта з підтримкою OpenGL 3.3+

## Перспективи розвитку

* Додати підтримку інших форматів (FBX, STL, GLTF)
* Покращити роботу з текстурами (візуалізація матеріалів, карт нормалей)
* Додати функції вимірювання, анотацій, анімації моделей

## Скріншоти
![Снимок экрана 2025-07-01 215147](https://github.com/user-attachments/assets/31af22dc-5d03-454e-b6da-370a044290cd)

![Снимок экрана 2025-07-01 215227](https://github.com/user-attachments/assets/91019a5d-4a17-4d71-9e43-4917b869e198)


## Ліцензія

MIT License

---

**Автор:** Винник Д.В. (StelSuy), 2025


Sure! Here’s the **README.md** in English for your **3DModelViewer** project:

---

# 3DModelViewer

**3DModelViewer** is a modern desktop application for viewing and analyzing 3D models in OBJ and PLY formats. The program is written in Python using PyQt5 and OpenGL, featuring a user-friendly interface for easy interaction with 3D objects.

## Key Features

* Open and view 3D models in `.obj` and `.ply` formats
* Interactive camera controls: rotate, zoom, pan
* Switch between dark and light UI themes
* Show/hide normals and textures (improved texture support coming soon)
* Information panel with key model stats: vertex count, face count, bounding box dimensions
* Save screenshots of the current 3D scene
* History of opened files for quick access to recent models
* Drag-and-drop support for model loading

## Architecture

The project is organized in a modular way:

* **main.py** — application entry point
* **pages/** — UI pages (Home, File Search, 3D Viewer)
* **widgets/** — custom widgets (e.g., SimpleGLWidget for OpenGL rendering)
* **utils/** — utilities (model loader, history manager)
* **ui/** — styles (QSS) and theme manager
* **vertex/** — rendering shaders
* **icons/** — graphical assets

## Installation & Launch

### Required Dependencies

* Python 3.9+
* PyQt5
* PyOpenGL
* trimesh
* numpy

Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

### System Requirements

* OS: Windows, Linux, or MacOS
* Graphics card with OpenGL 3.3+ support

## Roadmap

* Support for additional formats (FBX, STL, GLTF)
* Advanced texture rendering (materials, normal maps)
* Tools for measurements, annotations, model animations

## Screenshots

> *(Insert screenshots of your program here)*

## License

MIT License

---
**Author:** D.V. Vynnyk (StelSuy), 2025
---

