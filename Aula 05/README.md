# Aula 05 - Braço Robótico Animado

Braço robótico articulado 2D desenvolvido em **PyGame-ce** para a disciplina de Computação Gráfica.

## Estrutura do Braço

- **Base fixa**: Retângulo que pode ser deslocado horizontalmente (esquerda/direita)
- **Braço 1**: Segmento ligado à base, com rotação em uma extremidade
- **Braço 2**: Segmento ligado à extremidade do Braço 1, com rotação na articulação

## Execução

```bash
pip install -r requirements.txt
python braco_robotico.py
```

## Controles

| Tecla | Ação |
|-------|------|
| A ou ← | Mover base para esquerda |
| D ou → | Mover base para direita |
| W | Rotacionar braço 1 (anti-horário) |
| S | Rotacionar braço 1 (horário) |
| ↑ | Rotacionar braço 2 (anti-horário) |
| ↓ | Rotacionar braço 2 (horário) |
| ESC | Sair |

## Principais Funções do Código

| Função | Descrição |
|--------|-----------|
| `desenhar_eixos()` | Desenha os eixos X (vermelho) e Y (verde) na tela |
| `ponto_angulo()` | Calcula (x, y) da extremidade de um segmento dado origem, comprimento e ângulo |
| `desenhar_braco_robotico()` | Desenha base, braço 1 e braço 2 |
| `processar_teclas()` | Processa eventos do teclado e retorna (rodando, base_x, ang1, ang2) |

## Transformações Utilizadas

- **Translação**: A base é deslocada via alteração de `base_x`; os braços são calculados a partir dessa posição.
- **Rotação**: Os ângulos `angulo_braco1` e `angulo_braco2` são usados com `math.cos()` e `math.sin()` para obter as coordenadas dos segmentos, simulando rotação em torno das articulações.

## Cores

- **Base**: Azul acinzentado `(80, 80, 120)`
- **Braço 1**: Azul `(60, 140, 200)`
- **Braço 2**: Laranja/terra `(200, 100, 60)`
- **Eixo X**: Vermelho
- **Eixo Y**: Verde
