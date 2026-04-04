import numpy as np
from src.Ponto import Ponto
from src.Vetor import Vetor

def intersect_sphere(origem: Ponto, direcao: Vetor, centro: Ponto, raio: float) -> float:
    """
    Retorna a distância 't' da interseção do raio com a esfera.
    Se não houver interseção, retorna infinito.
    """
    v = origem - centro  # Ponto - Ponto = Vetor
    
    v_dot_d = v.dot(direcao)
    v_dot_v = v.dot(v)
    r2 = raio * raio
    
    # Discriminante (o que fica dentro da raiz quadrada)
    discriminant = (v_dot_d ** 2) - (v_dot_v - r2)
    
    if discriminant < 0:
        return float('inf')  # Não intersecta
        
    sqrt_disc = np.sqrt(discriminant)
    
    # As duas raízes da equação (pontos de entrada e saída da esfera)
    t1 = -v_dot_d - sqrt_disc
    t2 = -v_dot_d + sqrt_disc
    
    # Retornamos o menor 't' positivo (o ponto mais próximo na frente da câmera)
    # Usamos 0.001 em vez de 0 para evitar o "shadow acne" (problema de precisão flutuante)
    if t1 > 0.001: return t1
    if t2 > 0.001: return t2
    
    return float('inf')

def intersect_plane(origem: Ponto, direcao: Vetor, p0: Ponto, normal: Vetor) -> float:
    """
    Retorna a distância 't' da interseção do raio com o plano.
    Se não houver interseção, retorna infinito.
    """
    denom = direcao.dot(normal)
    
    # Se o denominador for muito próximo de zero, o raio é paralelo ao plano
    if abs(denom) > 1e-6:
        p0_origem = p0 - origem  # Ponto - Ponto = Vetor
        t = p0_origem.dot(normal) / denom
        
        if t > 0.001:
            return t
            
    return float('inf')