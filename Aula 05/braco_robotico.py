import math
import pygame

LARGURA, ALTURA = 800, 600
CY = ALTURA // 2
L1, L2 = 120, 100  # comprimentos dos braços


def desenhar_eixos(tela):
    """Desenha eixos X (vermelho) e Y (verde)."""
    cx = LARGURA // 2
    pygame.draw.line(tela, (220, 60, 60), (0, CY), (LARGURA, CY), 2)  # X
    pygame.draw.line(tela, (60, 180, 60), (cx, 0), (cx, ALTURA), 2)   # Y


def ponto_angulo(origem_x, origem_y, comprimento, angulo_graus):
    """Retorna (x, y) do ponto na extremidade do segmento."""
    r = math.radians(angulo_graus)
    return (origem_x + comprimento * math.cos(r), origem_y + comprimento * math.sin(r))


def desenhar_braco_robotico(tela, base_x, ang1, ang2):
    """Desenha base, braço 1 e braço 2."""
    fim1 = ponto_angulo(base_x, CY, L1, ang1)
    fim2 = ponto_angulo(fim1[0], fim1[1], L2, ang1 + ang2)

    # Base (cantos arredondados + borda)
    rect = (int(base_x - 25), int(CY - 15), 50, 30)
    pygame.draw.rect(tela, (80, 80, 120), rect, border_radius=5)
    pygame.draw.rect(tela, (120, 120, 160), rect, 2, border_radius=5)

    # Braços
    pygame.draw.line(tela, (60, 140, 200), (base_x, CY), fim1, 12)
    pygame.draw.line(tela, (200, 100, 60), fim1, fim2, 12)

    # Articulações (círculos metálicos)
    for x, y in [(base_x, CY), fim1, fim2]:
        pygame.draw.circle(tela, (200, 200, 220), (int(x), int(y)), 8)
        pygame.draw.circle(tela, (100, 100, 120), (int(x), int(y)), 8, 2)


def processar_teclas(base_x, ang1, ang2):
    """Processa eventos e retorna (rodando, base_x, ang1, ang2)."""
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            return False, base_x, ang1, ang2
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_a, pygame.K_LEFT):   base_x = max(50, base_x - 8)
            elif e.key in (pygame.K_d, pygame.K_RIGHT): base_x = min(LARGURA - 50, base_x + 8)
            elif e.key == pygame.K_w: ang1 = (ang1 + 4) % 360
            elif e.key == pygame.K_s: ang1 = (ang1 - 4) % 360
            elif e.key == pygame.K_UP:   ang2 = (ang2 + 4) % 360
            elif e.key == pygame.K_DOWN: ang2 = (ang2 - 4) % 360
    return True, base_x, ang1, ang2


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Braço Robótico")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(80, 50)

    base_x = LARGURA // 2
    ang1, ang2 = 30, -45

    rodando = True
    while rodando:
        rodando, base_x, ang1, ang2 = processar_teclas(base_x, ang1, ang2)

        tela.fill((25, 28, 35))
        desenhar_eixos(tela)
        desenhar_braco_robotico(tela, base_x, ang1, ang2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
