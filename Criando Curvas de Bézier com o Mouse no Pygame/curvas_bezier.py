"""
Curvas de Bézier Dinâmicas - Pygame
Clique para adicionar pontos | Arraste para mover | Clique dir: remover
ENTER: nova curva | R: limpar | D: De Casteljau

Referência: AZEVEDO, Eduardo. Computação gráfica: geração de imagens.
            Rio de Janeiro: Campos, 2003. (Seção 3.1.7)
"""

import pygame
import math

LARGURA, ALTURA = 800, 600
COR_FUNDO = (25, 28, 35)
COR_PONTOS, COR_ARRAS = (255, 180, 80), (255, 100, 100)
COR_POLIGONO, COR_LINHA, COR_CURVA = (120, 120, 140), (80, 180, 255), (120, 255, 160)
COR_CASTELJAU, COR_INFO = (255, 220, 100), (180, 200, 220)
RAIO_PONTO, RAIO_CLIQUE = 7, 15
NUM_SEGMENTOS = 80
TRAÇO, ESPAÇO = 8, 6


def ponto_bezier(pontos, t):
    """Ponto B(t) na curva - fórmula de Bernstein."""
    n = len(pontos)
    if n <= 1:
        return pontos[0] if pontos else (0, 0)
    x = y = 0.0
    g = n - 1
    for i in range(n):
        b = math.comb(g, i)
        w = b * (1 - t) ** (g - i) * t ** i
        x += w * pontos[i][0]
        y += w * pontos[i][1]
    return (x, y)


def de_casteljau(pontos, t):
    """De Casteljau: retorna (ponto B(t), níveis para visualização)."""
    if len(pontos) < 2:
        return (pontos[0] if pontos else (0, 0)), [list(pontos)]
    niveis = [list(pontos)]
    atual = list(pontos)
    for _ in range(len(pontos) - 1):
        prox = [(1 - t) * atual[i][0] + t * atual[i + 1][0],
                (1 - t) * atual[i][1] + t * atual[i + 1][1]
                for i in range(len(atual) - 1)]
        atual = [tuple(p) if isinstance(p, (list, tuple)) else p for p in prox]
        atual = [(prox[i][0], prox[i][1]) for i in range(len(prox))]
        niveis.append(atual)
    return (atual[0] if atual else (0, 0), niveis)