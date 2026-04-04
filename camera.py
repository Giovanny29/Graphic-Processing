from src.Ponto import Ponto
from src.Vetor import Vetor
from utils.Scene.sceneSchema import CameraData

class Camera:
    def __init__(self, cam_data: CameraData):
        # Dados originais importados pelo parser
        self.C = cam_data.lookfrom
        self.M = cam_data.lookat
        self.Vup = cam_data.up_vector
        self.d = cam_data.screen_distance
        
        self.hres = cam_data.image_width
        self.vres = cam_data.image_height
        
        # --- Construção da Base Ortonormal ---
        # W: Oposto à direção de visão (C - M)
        direcao_w = self.C - self.M
        self.W = direcao_w.normalize()
        
        # U: Eixo X local (Direita). Obtido via produto vetorial de Vup e W
        direcao_u = self.Vup.cross(self.W)
        self.U = direcao_u.normalize()
        
        # V: Eixo Y local (Cima). Obtido garantindo que seja perpendicular a W e U
        self.V = self.W.cross(self.U)
        
        # --- Geometria da Tela ---
        self.pixel_size = 1.0 / self.hres
        screen_width = 1.0
        screen_height = self.vres * self.pixel_size
        
        # Centro da tela fica à distância 'd' na direção oposta de W
        self.screen_center = self.C - (self.W * self.d)
        
        # Ponto no espaço 3D correspondente ao canto superior esquerdo da tela
        self.upper_left = self.screen_center - (self.U * (screen_width / 2.0)) + (self.V * (screen_height / 2.0))
        
    def get_ray_direction(self, i: int, j: int) -> Vetor:
        """Calcula a direção do raio que parte do centro da câmera e passa pelo pixel (i, j)."""
        # (i + 0.5) e (j + 0.5) garante que o raio passe exatamente pelo meio do pixel
        deslocamento_x = self.U * ((i + 0.5) * self.pixel_size)
        deslocamento_y = self.V * ((j + 0.5) * self.pixel_size)
        
        # No eixo Y subtraímos porque a imagem cresce de cima para baixo
        pixel_center = self.upper_left + deslocamento_x - deslocamento_y
        
        # Vetor Direção: Ponto de destino (Pixel) - Origem (Câmera)
        direcao = pixel_center - self.C
        return direcao.normalize()
