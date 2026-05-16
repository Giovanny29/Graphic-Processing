from src.Ponto import Ponto
from src.Vetor import Vetor


# ============================================================
# LIGHT
# ============================================================

class Light:
    """
    Luz pontual da cena
    """
    def __init__(self, position, color):

        self.pos = Ponto(
                position.x,
                position.y,
                position.z
            )

        self.color = Vetor(
                color.r,
                color.g,
                color.b
            )


# ============================================================
# AMBIENT LIGHT
# ============================================================

class AmbientLight:
    def __init__(self, color):
        self.color = Vetor(color.r, color.g, color.b)

# ============================================================
# HIT STRUCT
# ============================================================
class Hit:
    def __init__(self, point: Ponto, normal: Vetor, obj, t: float, index: int = -1):
        self.point = point
        self.normal = normal
        self.obj = obj
        self.t = t
        self.index = index

    def __repr__(self):
        return f"Hit(t={self.t:.4f}, obj={self.obj.obj_type})"
    
# ============================================================
# SHADOW
# ============================================================

def is_in_shadow(
    hit: Hit,
    light: Light,
    scene_objects: list,
    intersect_fn
) -> bool:

    EPSILON = 1e-2

    # direção até a luz
    light_vec = light.pos - hit.point

    light_distance = light_vec.magnitude()

    light_dir = light_vec.normalize()

    # evita acne
    shadow_origin = (
        hit.point
        + hit.normal * EPSILON
    )

    for obj in scene_objects:

        t, _ = intersect_fn(
            obj,
            shadow_origin,
            light_dir
        )

        if EPSILON < t < light_distance:
            return True

    return False


# ============================================================
# PHONG SHADING
# ============================================================

def phong_shading(
    hit: Hit,
    lights: list,
    ambient_light: AmbientLight,
    camera_pos: Ponto,
    scene_objects: list,
    intersect_fn
) -> Vetor:

    material = hit.obj.material

    # ========================================================
    # COEFICIENTES
    # ========================================================

    ka = Vetor(
        material.ka.r,
        material.ka.g,
        material.ka.b
    )

    kd = Vetor(
        material.color.r,
        material.color.g,
        material.color.b
    )

    ks = Vetor(
        material.ks.r,
        material.ks.g,
        material.ks.b
    )

    ns = material.ns

    # ========================================================
    # COMPONENTE AMBIENTE
    # ========================================================

    ambient = Vetor(
        ka.x * ambient_light.color.x,
        ka.y * ambient_light.color.y,
        ka.z * ambient_light.color.z
    )

    color = ambient

    # ========================================================
    # DIREÇÃO DA CÂMERA
    # ========================================================

    V = (
        camera_pos
        - hit.point
    ).normalize()

    N = hit.normal.normalize()

    # ========================================================
    # LUZES
    # ========================================================

    for light in lights:

        # sombra
        if is_in_shadow(
            hit,
            light,
            scene_objects,
            intersect_fn
        ):
            continue

        # direção até luz
        L = (
            light.pos
            - hit.point
        ).normalize()

        # ====================================================
        # DIFUSO
        # ====================================================

        N_dot_L = max(
            0.0,
            N.dot(L)
        )

        diffuse = Vetor(
            kd.x * light.color.x * N_dot_L,
            kd.y * light.color.y * N_dot_L,
            kd.z * light.color.z * N_dot_L
        )

        # ====================================================
        # ESPECULAR
        # ====================================================

        R = (
            N * (2.0 * N.dot(L))
            - L
        ).normalize()

        R_dot_V = max(
            0.0,
            R.dot(V)
        )

        spec_factor = R_dot_V ** ns

        specular = Vetor(
            ks.x * light.color.x * spec_factor,
            ks.y * light.color.y * spec_factor,
            ks.z * light.color.z * spec_factor
        )

        # acumula
        color = (
            color
            + diffuse
            + specular
        )

    return color.clamp(0.0, 1.0)