import os

def load_obj_with_texture(path):
    """
    Завантажує OBJ-модель: вершини, грані та текстуру з .mtl (якщо є).
    Повертає ((vertices, faces), texture_path або None).
    """
    print(f"[DEBUG] OBJ loader. Спроба відкрити: {path}")
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
                print(f"[DEBUG] OBJ: знайдено mtllib: {mtl_path}")
                try:
                    with open(mtl_path, 'r') as mtl:
                        for mtl_line in mtl:
                            if mtl_line.startswith('map_Kd'):
                                texture_file = mtl_line.strip().split()[1]
                                texture_path = os.path.join(os.path.dirname(path), texture_file)
                                print(f"[DEBUG] OBJ: знайдено map_Kd: {texture_path}")
                                return (vertices, faces), texture_path
                except Exception as e:
                    print(f"[DEBUG] OBJ: Помилка при читанні MTL: {e}")
                    continue
    print(f"[DEBUG] OBJ: Вершин {len(vertices)}, Граней {len(faces)}, текстури немає.")
    return (vertices, faces), None

def load_ply(path):
    """
    Завантажує PLY-файл (вершини, грані) через trimesh.
    """
    print(f"[DEBUG] PLY loader. Спроба відкрити: {path}")
    try:
        import trimesh
        mesh = trimesh.load(path, file_type='ply')
        vertices = mesh.vertices.tolist()
        faces = mesh.faces.tolist()
        print(f"[DEBUG] PLY: Вершин {len(vertices)}, Граней {len(faces)}")
        return vertices, faces
    except Exception as e:
        print(f"[PLY ERROR] {e}")
        return [], []
