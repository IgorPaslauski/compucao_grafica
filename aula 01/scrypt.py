import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Teste Pygame")

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    screen.fill((0, 0, 0))  # Preenche a tela com preto
    pygame.display.flip()

pygame.quit()