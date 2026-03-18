"""
EI 2 - Transformações Geométricas 2D
Algoritmos: ESCALA, ROTAÇÃO e TRANLAÇÃO em objetos 2D.

Use: S=escala, R=rotação, T=translação, Backspace=voltar
"""

import math
import pygame

# Tela
LARGURA, ALTURA = 800, 600

# Objeto inicial: triângulo no centro da tela (fácil de visualizar)
def triangulo_inicial():
    cx, cy = LARGURA // 2, ALTURA // 2
    return [(cx, cy - 80), (cx - 60, cy + 60), (cx + 60, cy + 60)]


# ============== ALGORITMOS DE TRANSFORMAÇÃO ==============
# Todos usam coordenadas homogêneas: ponto (x,y) vira [x, y, 1]

def translacao(pontos, tx, ty):
    """Translação: move o objeto. Matriz T = [[1,0,tx],[0,1,ty],[0,0,1]]
       Resultado: x'=x+tx, y'=y+ty"""
    return [(x + tx, y + ty) for x, y in pontos]


def escala(pontos, sx, sy, centro_x, centro_y):
    """Escala: aumenta/diminui. Matriz S = [[sx,0,0],[0,sy,0],[0,0,1]]
       Em torno do centro: 1) vai pra origem 2) escala 3) volta"""
    resultado = []
    for x, y in pontos:
        x1 = x - centro_x  # passo 1
        y1 = y - centro_y
        x2 = x1 * sx       # passo 2
        y2 = y1 * sy
        resultado.append((x2 + centro_x, y2 + centro_y))  # passo 3
    return resultado


def rotacao(pontos, angulo_graus, centro_x, centro_y):
    """Rotação: gira o objeto. Matriz R = [[cos,-sin,0],[sin,cos,0],[0,0,1]]
       Em torno do centro: aplica cos/sin nas distâncias dx, dy"""
    rad = math.radians(angulo_graus)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)
    resultado = []
    for x, y in pontos:
        dx = x - centro_x
        dy = y - centro_y
        x_novo = centro_x + dx * cos_a - dy * sin_a
        y_novo = centro_y + dx * sin_a + dy * cos_a
        resultado.append((x_novo, y_novo))
    return resultado


def centro(pontos):
    """Centro do objeto: média de x e média de y"""
    n = len(pontos)
    return sum(p[0] for p in pontos) / n, sum(p[1] for p in pontos) / n


# ============== INTERFACE ==============

def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("EI 2 - Transformações 2D")
    fonte = pygame.font.Font(None, 28)

    # Histórico: cada elemento é a lista de pontos naquele momento
    historico = [triangulo_inicial()]
    rodando = True

    while rodando:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                rodando = False
            elif e.type == pygame.KEYDOWN and len(historico) > 0:
                if e.key == pygame.K_BACKSPACE:
                    historico = [triangulo_inicial()]
                else:
                    pts = historico[-1]
                    cx, cy = centro(pts)
                    if e.key == pygame.K_s:
                        historico.append(escala(pts, 1.2, 1.2, cx, cy))
                    elif e.key == pygame.K_r:
                        historico.append(rotacao(pts, 15, cx, cy))
                    elif e.key == pygame.K_t:
                        historico.append(translacao(pts, 30, 20))

        # Desenho
        tela.fill((240, 242, 245))
        for x in range(0, LARGURA, 50):
            pygame.draw.line(tela, (220, 220, 220), (x, 0), (x, ALTURA))
        for y in range(0, ALTURA, 50):
            pygame.draw.line(tela, (220, 220, 220), (0, y), (LARGURA, y))

        # Desenha o objeto atual
        pts = historico[-1]
        if len(pts) >= 3:
            pts_int = [(int(x), int(y)) for x, y in pts]
            pygame.draw.polygon(tela, (100, 180, 220), pts_int)
            pygame.draw.polygon(tela, (30, 100, 180), pts_int, 2)
        for x, y in pts:
            pygame.draw.circle(tela, (50, 50, 50), (int(x), int(y)), 5)

        # Instruções
        tela.blit(fonte.render("S: escala | R: rotacao | T: translacao | Backspace: reset", True, (0, 0, 0)), (10, 10))
        tela.blit(fonte.render("ESC: sair", True, (100, 100, 100)), (10, 40))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
