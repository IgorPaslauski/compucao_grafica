"""
Word Defender - Funções utilitárias
Funções reutilizáveis para texto e desenho.
"""

import unicodedata
import pygame


def normalizar_letra(letra):
    """Remove acentos e converte para minúscula (ex: 'É' -> 'e')."""
    if len(letra) != 1:
        return letra
    forma_normalizada = unicodedata.normalize('NFD', letra)
    sem_acentos = ''.join(c for c in forma_normalizada if unicodedata.category(c) != 'Mn')
    return sem_acentos.lower() if sem_acentos else letra


def letras_sao_iguais(letra_a, letra_b):
    """Compara duas letras ignorando acentos e maiúsculas/minúsculas."""
    return normalizar_letra(letra_a) == normalizar_letra(letra_b)


def desenhar_gradiente_vertical(superficie, retangulo, cor_topo, cor_base):
    """Preenche um retângulo com gradiente de cima para baixo."""
    x, y, largura, altura = retangulo
    for i in range(altura):
        progresso = i / max(altura - 1, 1)
        r = int(cor_topo[0] * (1 - progresso) + cor_base[0] * progresso)
        g = int(cor_topo[1] * (1 - progresso) + cor_base[1] * progresso)
        b = int(cor_topo[2] * (1 - progresso) + cor_base[2] * progresso)
        pygame.draw.line(superficie, (r, g, b), (x, y + i), (x + largura, y + i))


def desenhar_retangulo_arredondado(superficie, retangulo, cor, raio=10, cor_borda=None, espessura_borda=2):
    """Desenha um retângulo com cantos arredondados."""
    x, y, largura, altura = retangulo
    raio = min(raio, largura // 2, altura // 2)
    pygame.draw.rect(superficie, cor, (x, y, largura, altura), border_radius=raio)
    if cor_borda:
        pygame.draw.rect(superficie, cor_borda, (x, y, largura, altura), espessura_borda, border_radius=raio)
