import os

def load_obj_with_texture(path):
    vertices = []
    faces = []
    texture_file = None

    with open(path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                vertices.append(tuple(map(float, parts[1:4])))
            elif line.startswith('f '):
                parts = line.strip().split()
                face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                faces.append(face)
            elif line.startswith('mtllib'):
                mtl_file = line.strip().split()[1]
                mtl_path = os.path.join(os.path.dirname(path), mtl_file)
                try:
                    with open(mtl_path, 'r') as mtl:
                        for mtl_line in mtl:
                            if mtl_line.startswith('map_Kd'):
                                texture_file = mtl_line.strip().split()[1]
                                texture_path = os.path.join(os.path.dirname(path), texture_file)
                                return (vertices, faces), texture_path
                except:
                    continue
    return (vertices, faces), None

def load_fbx(path):
    # Заглушка — підтримка FBX потребує сторонньої бібліотеки (наприклад, Open3D, Assimp тощо)
    return [], []
