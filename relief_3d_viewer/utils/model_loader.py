import os

def load_obj_with_texture(file_path):
    vertices = []
    faces = []
    texture_file = None

    mtl_file = None
    base_dir = os.path.dirname(file_path)

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('mtllib'):
                mtl_file = line.strip().split()[1]
            elif line.startswith('v '):
                parts = line.strip().split()
                vertices.append(tuple(map(float, parts[1:4])))
            elif line.startswith('f '):
                parts = line.strip().split()
                face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                faces.append(face)

    if mtl_file:
        mtl_path = os.path.join(base_dir, mtl_file)
        if os.path.exists(mtl_path):
            with open(mtl_path, 'r') as mtl:
                for line in mtl:
                    if line.startswith('map_Kd'):
                        texture_file = line.strip().split()[1]
                        break

    texture_path = os.path.join(base_dir, texture_file) if texture_file else None
    return (vertices, faces), texture_path
