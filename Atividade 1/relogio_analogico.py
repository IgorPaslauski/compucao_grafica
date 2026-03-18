import pygame
import math
import time

pygame.init()
try:
    import winsound
except ImportError:
    winsound = None

LARGURA, ALTURA = 500, 500
CENTRO = (LARGURA // 2, ALTURA // 2)
RAIO = 200

VERMELHO = (220, 50, 50)
AZUL = (50, 100, 220)
VERDE = (50, 180, 80)
LARANJA = (255, 165, 0)


def angulo_para_posicao(angulo, comprimento):  # 0 = 12h, -90 alinha topo
    rad = math.radians(angulo - 90)
    return (CENTRO[0] + comprimento * math.cos(rad), CENTRO[1] + comprimento * math.sin(rad))


def processar_teclado(rodando, alarme_h, alarme_m):
    """Trata teclas A/D=minuto, W/S=hora; retorna rodando, alarme_h, alarme_m."""
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            rodando = False
        elif e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_a, pygame.K_LEFT):
                alarme_m = (alarme_m - 1) % 60
            elif e.key in (pygame.K_d, pygame.K_RIGHT):
                alarme_m = (alarme_m + 1) % 60
            elif e.key in (pygame.K_w, pygame.K_UP):
                alarme_h = (alarme_h - 1) % 12
            elif e.key in (pygame.K_s, pygame.K_DOWN):
                alarme_h = (alarme_h + 1) % 12
    return rodando, alarme_h, alarme_m


def verificar_alarme(h, m, alarme_h, alarme_m, alarme_soou):
    """Apita quando hora bate no alarme; retorna alarme_soou atualizado."""
    if h == alarme_h and m == alarme_m and alarme_soou != (h, m):
        if winsound:
            winsound.Beep(880, 800)
        return (h, m)
    if alarme_soou and (h != alarme_h or m != alarme_m):
        return None
    return alarme_soou


def desenhar_mostrador(tela):
    """Desenha anel externo, marcas dos minutos e numeros 1 a 12."""
    pygame.draw.circle(tela, (100, 100, 100), CENTRO, RAIO + 8, 4)
    pygame.draw.circle(tela, (255, 255, 255), CENTRO, RAIO)
    for i in range(60):
        a = i * 6
        fim = angulo_para_posicao(a, RAIO)
        inicio = angulo_para_posicao(a, RAIO - 15 if i % 5 == 0 else RAIO - 8)
        pygame.draw.line(tela, (80, 80, 80), inicio, fim, 2 if i % 5 == 0 else 1)
    fonte = pygame.font.Font(None, 42)
    for i in range(1, 13):
        p = angulo_para_posicao(i * 30, RAIO - 35)
        tela.blit(fonte.render(str(i), True, (0, 0, 0)), (p[0] - 10, p[1] - 10))
    pygame.draw.circle(tela, (0, 0, 0), CENTRO, 6)


def desenhar_ponteiros(tela, h, m, s, alarme_h, alarme_m):
    """Desenha ponteiros de hora, minuto, segundo e alarme."""
    ang_s, ang_m = s * 6, m * 6 + s * 0.1
    ang_h = h * 30 + m * 0.5
    pygame.draw.line(tela, VERDE, CENTRO, angulo_para_posicao(ang_h, RAIO * 0.5), 6)
    pygame.draw.line(tela, AZUL, CENTRO, angulo_para_posicao(ang_m, RAIO * 0.7), 4)
    pygame.draw.line(tela, VERMELHO, CENTRO, angulo_para_posicao(ang_s, RAIO * 0.85), 2)
    ang_alarme = alarme_h * 30 + alarme_m * 0.5
    pygame.draw.line(tela, LARANJA, CENTRO, angulo_para_posicao(ang_alarme, RAIO * 0.6), 3)


def desenhar_informacoes(tela, h, m, s, alarme_h, alarme_m):
    """Exibe hora atual e horario do alarme."""
    fonte = pygame.font.Font(None, 28)
    hr = f"{12 if h == 0 else h}:{m:02d}:{s:02d}"
    al = f"Alarme: {12 if alarme_h == 0 else alarme_h}:{alarme_m:02d}"
    tela.blit(fonte.render(f"Hora: {hr}", True, (50, 50, 50)), (20, ALTURA - 50))
    tela.blit(fonte.render(al, True, LARANJA), (20, ALTURA - 28))


tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
pygame.key.set_repeat(200, 80)  # segurar tecla = repete a acao
rodando = True
alarme_h, alarme_m = 0, 0
alarme_soou = None

while rodando:
    rodando, alarme_h, alarme_m = processar_teclado(rodando, alarme_h, alarme_m)
    h, m, s = time.localtime().tm_hour % 12, time.localtime().tm_min, time.localtime().tm_sec
    alarme_soou = verificar_alarme(h, m, alarme_h, alarme_m, alarme_soou)

    tela.fill((240, 240, 245))
    desenhar_mostrador(tela)
    desenhar_ponteiros(tela, h, m, s, alarme_h, alarme_m)
    desenhar_informacoes(tela, h, m, s, alarme_h, alarme_m)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
