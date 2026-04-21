import sys
from utils.Scene.sceneParser import SceneJsonLoader
from utils.MeshReader.ObjReader import ObjReader
from camera import Camera
from geometria import intersect_sphere, intersect_plane, intersect_triangle


def main():
    """
    Programa de ray casting básico.

    Recebe como argumento um arquivo de cena (.json), carrega os dados
    utilizando o parser fornecido e configura a câmera.

    Para cada pixel da imagem:
    - Gera um raio a partir da câmera na direção correspondente ao pixel
    - Testa interseção desse raio com todos os objetos da cena (esferas e planos)
    - Seleciona o objeto mais próximo (menor t positivo)
    - Atribui ao pixel a cor difusa do objeto atingido
    - Caso não haja interseção, o pixel recebe cor preta

    As cores dos objetos estão no intervalo [0,1] e são convertidas para
    o intervalo [0,255] antes de serem escritas, conforme exigido pelo
    formato PPM (P3).

    A imagem é escrita no formato PPM diretamente na saída padrão,
    permitindo redirecionamento para um arquivo.

    Mensagens de progresso são enviadas para stderr para não interferir
    no arquivo de saída.
    """
    if len(sys.argv) < 2:
        print("Use: python main.py <caminho_para_cena.json> > out.ppm", file=sys.stderr)
        sys.exit(1)

    scene_file = sys.argv[1]
    scene_data = SceneJsonLoader.load_file(scene_file)
    cam = Camera(scene_data.camera)
    
# --- PRÉ-CARREGAMENTO DE MALHAS ---
    # Guarda os ObjReaders na memória para não reler o arquivo a cada pixel
    loaded_meshes = {}
    for obj in scene_data.objects:
        if obj.obj_type == "mesh":
            # Pega o caminho do arquivo (Ajuste a string "filename" se o seu JSON usar outro nome, ex: "file")
            obj_path = obj.get_property("path") 
            if obj_path not in loaded_meshes:
                print(f"Carregando malha: {obj_path}...", file=sys.stderr)
                loaded_meshes[obj_path] = ObjReader(obj_path)
    # ----------------------------------

    print(f"P3\n{cam.hres} {cam.vres}\n255")
    
    for j in range(cam.vres):
        print(f"Renderizando linha {j}/{cam.vres}...", file=sys.stderr, end='\r')
        
        for i in range(cam.hres):
            ray_dir = cam.get_ray_direction(i, j)
            
            closest_t = float('inf')
            hit_color = None
            
            for obj in scene_data.objects:
                t = float('inf')
                
                if obj.obj_type == "sphere":
                    centro = obj.relative_pos
                    raio = obj.get_num("radius")
                    t = intersect_sphere(cam.C, ray_dir, centro, raio)
                    
                elif obj.obj_type == "plane":
                    ponto_plano = obj.relative_pos
                    normal = obj.get_vetor("normal").normalize()
                    t = intersect_plane(cam.C, ray_dir, ponto_plano, normal)
                
                elif obj.obj_type == "mesh":
                    # Busca a malha pré-carregada na memória
                    mesh_reader = loaded_meshes[obj.get_property("path")]
                    
                    # Testa interseção com CADA triângulo da malha
                    for face_pts in mesh_reader.get_face_points():
                        t = intersect_triangle(cam.C, ray_dir, face_pts[0], face_pts[1], face_pts[2])

                if t < closest_t:
                    closest_t = t
                    hit_color = obj.material.color
            
            if hit_color is not None:
                r = int(255.999 * hit_color.r)
                g = int(255.999 * hit_color.g)
                b = int(255.999 * hit_color.b)  
            else:
                r, g, b = 0, 0, 0
                
            print(f"{r} {g} {b}")
            
    print("\nRenderização concluída com sucesso!", file=sys.stderr)


if __name__ == "__main__":
    main()
