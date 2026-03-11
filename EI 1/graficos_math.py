import math
from typing import Tuple, Optional, Union, List

class Ponto2D:
    """Ponto no plano (x, y)."""
    def __init__(self, x: float, y: float):
        self.x, self.y = x, y
    def __repr__(self):
        return f"Ponto2D({self.x}, {self.y})"
    def distancia(self, outro: 'Ponto2D') -> float:
        return math.sqrt((self.x - outro.x)**2 + (self.y - outro.y)**2)

class Ponto3D:
    """Ponto no espaço (x, y, z)."""
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z
    def __repr__(self):
        return f"Ponto3D({self.x}, {self.y}, {self.z})"
    def distancia(self, outro: 'Ponto3D') -> float:
        return math.sqrt((self.x-outro.x)**2 + (self.y-outro.y)**2 + (self.z-outro.z)**2)

def multiplicar_matriz_2x2(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def multiplicar_matriz_3x3(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def multiplicar_matriz_4x4(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def comprimento_segmento_2d(p1: Union[Ponto2D, Tuple], p2: Union[Ponto2D, Tuple]) -> float:
    p1 = Ponto2D(p1[0], p1[1]) if isinstance(p1, tuple) else p1
    p2 = Ponto2D(p2[0], p2[1]) if isinstance(p2, tuple) else p2
    return p1.distancia(p2)

def comprimento_segmento_3d(p1: Union[Ponto3D, Tuple], p2: Union[Ponto3D, Tuple]) -> float:
    p1 = Ponto3D(p1[0], p1[1], p1[2]) if isinstance(p1, tuple) else p1
    p2 = Ponto3D(p2[0], p2[1], p2[2]) if isinstance(p2, tuple) else p2
    return p1.distancia(p2)

def _orientacao(a: Ponto2D, b: Ponto2D, c: Ponto2D) -> float:
    return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)

def _no_segmento(p: Ponto2D, a: Ponto2D, b: Ponto2D) -> bool:
    return min(a.x, b.x) <= p.x <= max(a.x, b.x) and min(a.y, b.y) <= p.y <= max(a.y, b.y)

def interseccao_segmentos_2d(a1, a2, b1, b2) -> Optional[Ponto2D]:
    def to_p(p):
        return Ponto2D(p[0], p[1]) if isinstance(p, tuple) else p
    a1, a2, b1, b2 = to_p(a1), to_p(a2), to_p(b1), to_p(b2)

    d1, d2 = _orientacao(a1, a2, b1), _orientacao(a1, a2, b2)
    d3, d4 = _orientacao(b1, b2, a1), _orientacao(b1, b2, a2)

    if d1 * d2 < 0 and d3 * d4 < 0:
        ax, ay = a2.x - a1.x, a2.y - a1.y
        denom = ax * (b2.y - b1.y) - ay * (b2.x - b1.x)
        if abs(denom) < 1e-10:
            return None
        t = ((b1.x - a1.x) * (b2.y - b1.y) - (b1.y - a1.y) * (b2.x - b1.x)) / denom
        return Ponto2D(a1.x + t * ax, a1.y + t * ay)

    if d1 == 0 and _no_segmento(b1, a1, a2): return b1
    if d2 == 0 and _no_segmento(b2, a1, a2): return b2
    if d3 == 0 and _no_segmento(a1, b1, b2): return a1
    if d4 == 0 and _no_segmento(a2, b1, b2): return a2
    return None

def imprimir_matriz(m: List[List[float]], nome: str = "M") -> None:
    print(f"{nome} ="); [print(" ", linha) for linha in m]; print()