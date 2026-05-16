import numpy as np
from src.Ponto import Ponto
from src.Vetor import Vetor

def garantir_ponto(p):
    """Converte array numpy para Ponto se necessário."""
    if isinstance(p, np.ndarray):
        return Ponto(p[0], p[1], p[2])
    return p

def garantir_vetor(v):
    """Converte array numpy para Vetor se necessário."""
    if isinstance(v, np.ndarray):
        return Vetor(v[0], v[1], v[2])
    return v

def intersect_sphere(origem, direcao, centro, raio: float) -> float:
    """
    Calcula a interseção entre um raio e uma esfera.
    """
    origem = garantir_ponto(origem)
    direcao = garantir_vetor(direcao)
    centro = garantir_ponto(centro)

    v = origem - centro
    
    v_dot_d = v.dot(direcao)
    v_dot_v = v.dot(v)
    r2 = raio * raio
    
    discriminant = (v_dot_d ** 2) - (v_dot_v - r2)
    
    if discriminant < 0:
        return float('inf')
        
    sqrt_disc = np.sqrt(discriminant)
    
    t1 = -v_dot_d - sqrt_disc
    t2 = -v_dot_d + sqrt_disc
    
    if t1 > 0.001: return t1
    if t2 > 0.001: return t2
    
    return float('inf')

def intersect_plane(origem, direcao, p0, normal) -> float:
    """
    Calcula a interseção entre um raio e um plano.
    """
    origem = garantir_ponto(origem)
    direcao = garantir_vetor(direcao)
    p0 = garantir_ponto(p0)
    normal = garantir_vetor(normal)

    denom = direcao.dot(normal)
    
    # Agora denom é garantidamente um float, abs() funcionará
    if abs(denom) > 1e-6:
        p0_origem = p0 - origem
        t = p0_origem.dot(normal) / denom
        
        if t > 0.001:
            return t
            
    return float('inf')

def intersect_triangles_numpy(origem: Ponto, direcao: Vetor,
                               v0: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> tuple:
    """
    Möller–Trumbore vetorizado — retorna (menor t, índice do triângulo).
    Se não houver interseção: (inf, -1)
    """

    EPSILON = 1e-8

    orig = np.array([origem.x, origem.y, origem.z])
    dire = np.array([direcao.x, direcao.y, direcao.z])

    aresta1 = v1 - v0          # (N, 3)
    aresta2 = v2 - v0          # (N, 3)

    h = np.cross(dire, aresta2)                         # (N, 3)
    a = np.einsum('ij,ij->i', aresta1, h)               # (N,)

    mask = np.abs(a) > EPSILON

    f = np.where(mask, 1.0 / np.where(mask, a, 1), 0)

    s = orig - v0                                       # (N, 3)
    u = f * np.einsum('ij,ij->i', s, h)                # (N,)
    mask &= (u >= 0.0) & (u <= 1.0)

    q = np.cross(s, aresta1)                            # (N, 3)
    v = f * (q @ dire)                                  # (N,)
    mask &= (v >= 0.0) & ((u + v) <= 1.0)

    t = f * np.einsum('ij,ij->i', aresta2, q)          # (N,)
    mask &= (t > 0.001)

    # ============================================================
    # RESULTADO
    # ============================================================

    if not np.any(mask):
        return float('inf'), -1

    valid_indices = np.where(mask)[0]

    idx_local = np.argmin(t[mask])
    idx_global = valid_indices[idx_local]

    return float(t[idx_global]), int(idx_global)