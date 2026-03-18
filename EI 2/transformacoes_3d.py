"""
EI 2 - Transformações Geométricas 3D
Algoritmos: ESCALA, ROTAÇÃO e TRANLAÇÃO em objetos 3D.

Use: S=escala, R=rotação, T=translação, Backspace=voltar
Objeto: cubo (8 vértices, 12 arestas)
"""

import math
import pygame

LARGURA, ALTURA = 800, 600

# Cubo centrado na origem: 8 vértices (x, y, z)
# Tamanho 60 (de -30 a +30 em cada eixo)
def cubo_inicial():
    s = 30
    return [
        (-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s),  # face traseira
        (-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s)        # face dianteira
    ]

# Arestas do cubo (índices dos vértices)
ARESTAS = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # traseira
    (4, 5), (5, 6), (6, 7), (7, 4),  # dianteira
    (0, 4), (1, 5), (2, 6), (3, 7)   # ligando
]


# ============== ALGORITMOS 3D ==============
# Coordenadas homogêneas: (x,y,z) vira [x,y,z,1]. Matrizes 4x4.

def translacao_3d(pontos, tx, ty, tz):
    """Translação 3D: x'=x+tx, y'=y+ty, z'=z+tz"""
    return [(x + tx, y + ty, z + tz) for x, y, z in pontos]


def escala_3d(pontos, sx, sy, sz, cx, cy, cz):
    """Escala 3D em torno do centro: vai pra origem, escala, volta"""
    return [
        (cx + (x - cx) * sx, cy + (y - cy) * sy, cz + (z - cz) * sz)
        for x, y, z in pontos
    ]


def rotacao_3d_y(pontos, angulo_graus, cx, cy, cz):
    """Rotação em torno do eixo Y (vertical). Mantém y, gira x e z."""
    rad = math.radians(angulo_graus)
    c, s = math.cos(rad), math.sin(rad)
    resultado = []
    for x, y, z in pontos:
        dx, dz = x - cx, z - cz
        x_novo = cx + dx * c - dz * s
        z_novo = cz + dx * s + dz * c
        resultado.append((x_novo, y, z_novo))
    return resultado


def centro_3d(pontos):
    n = len(pontos)
    return (
        sum(p[0] for p in pontos) / n,
        sum(p[1] for p in pontos) / n,
        sum(p[2] for p in pontos) / n
    )


def projetar(pontos):
    """Projeção isométrica: 3D -> 2D para desenhar na tela"""
    cx, cy = LARGURA // 2, ALTURA // 2
    escala = 3
    resultado = []
    for x, y, z in pontos:
        # Isométrico: eixo X vai SE, Z vai SW, Y sobe
        sx = cx + (x - z) * 0.866 * escala
        sy = cy - y * escala + (x + z) * 0.5 * escala
        resultado.append((sx, sy))
    return resultado


# ============== INTERFACE ==============

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("EI 2 - Transformações 3D")
    fonte = pygame.font.Font(None, 28)

    historico = [cubo_inicial()]
    rodando = True

    while rodando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                rodando = False
            elif e.type == pygame.KEYDOWN and historico:
                if e.key == pygame.K_BACKSPACE:
                    historico = [cubo_inicial()]
                else:
                    pts = historico[-1]
                    cx, cy, cz = centro_3d(pts)
                    if e.key == pygame.K_s:
                        historico.append(escala_3d(pts, 1.2, 1.2, 1.2, cx, cy, cz))
                    elif e.key == pygame.K_r:
                        historico.append(rotacao_3d_y(pts, 15, cx, cy, cz))
                    elif e.key == pygame.K_t:
                        historico.append(translacao_3d(pts, 20, 15, 10))

        # Desenho
        tela.fill((240, 242, 245))
        for x in range(0, LARGURA, 50):
            pygame.draw.line(tela, (220, 220, 220), (x, 0), (x, ALTURA))
        for y in range(0, ALTURA, 50):
            pygame.draw.line(tela, (220, 220, 220), (0, y), (LARGURA, y))

        # Projeta e desenha o cubo
        pts_3d = historico[-1]
        pts_2d = projetar(pts_3d)
        for i, j in ARESTAS:
            p1 = (int(pts_2d[i][0]), int(pts_2d[i][1]))
            p2 = (int(pts_2d[j][0]), int(pts_2d[j][1]))
            pygame.draw.line(tela, (30, 100, 180), p1, p2, 2)
        for x, y in pts_2d:
            pygame.draw.circle(tela, (50, 50, 50), (int(x), int(y)), 4)

        tela.blit(fonte.render("S: escala | R: rotacao Y | T: translacao | Backspace: reset", True, (0, 0, 0)), (10, 10))
        tela.blit(fonte.render("ESC: sair | Objeto: cubo 3D (projecao isometrica)", True, (100, 100, 100)), (10, 40))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
