"""
Word Defender - Configurações do jogo
Todas as constantes em um único lugar para facilitar ajustes.
"""

# Dimensões da tela
LARGURA_TELA = 900
ALTURA_TELA = 600

# Plataforma (onde o canhão está)
ALTURA_PLATAFORMA = 90
POSICAO_Y_PLATAFORMA = ALTURA_TELA - ALTURA_PLATAFORMA

# Canhão
POSICAO_X_CANHAO = LARGURA_TELA // 2
POSICAO_Y_CANHAO = POSICAO_Y_PLATAFORMA - 35

# Jogo
VIDAS_INICIAIS = 3
PONTOS_POR_LETRA = 10
PONTOS_POR_PALAVRA = 50
INTERVALO_NASCIMENTO_PALAVRA = 100  # frames entre cada nova palavra
MAX_PALAVRAS_TELA = 3
MIN_LETRAS_PALAVRA = 3
MAX_LETRAS_PALAVRA = 8
VELOCIDADE_BASE = 1.4
ACELERACAO_POR_PONTO = 0.0008
MULTIPLICADOR_PUNICAO_ERRO = 1.15  # palavras aceleram 15% ao errar
TENTATIVAS_POSICAO_LIVRE = 25
MARGEM_TELA = 60  # margem para posicionar palavras longe das bordas
FPS = 60

# Paleta de cores
class Cores:
    """Cores usadas no jogo."""
    FUNDO_TOPO = (15, 23, 42)
    FUNDO_BASE = (30, 41, 59)
    GRADE = (25, 35, 52)
    PLATAFORMA = (51, 65, 85)
    PLATAFORMA_BORDA = (71, 85, 105)
    PALAVRA_VERDE = (34, 197, 94)
    PALAVRA_VERDE_BORDA = (22, 163, 74)
    PALAVRA_AMARELA = (251, 191, 36)
    PALAVRA_AMARELA_BORDA = (245, 158, 11)
    PROJETIL = (248, 113, 113)
    PROJETIL_BRILHO = (254, 202, 202)
    CANHAO = (148, 163, 184)
    CANHAO_BOCA = (100, 116, 139)
    HUD = (226, 232, 240)
    HUD_VIDA = (248, 113, 113)
    TEXTO_PALAVRA = (15, 23, 42)
    # Cores do HUD (valores usados no painel e textos)
    HUD_LABEL = (148, 163, 184)
    PAINEL_FUNDO = (30, 41, 59)
    PAINEL_BORDA = (51, 65, 85)
