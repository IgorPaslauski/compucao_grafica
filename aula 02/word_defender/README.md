# Word Defender - Jogo 2D

**Aula 02 - Atividade 03** - Computação Gráfica

Jogo em que palavras em PT-BR e EN descem em direção ao solo. O jogador digita as letras para disparar lasers que eliminam a primeira letra de cada palavra.

---

## Instalação

### Pré-requisito
- Python 3.8 ou superior

### Passos

1. **Criar ambiente virtual (recomendado):**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

2. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Como Executar

Na pasta do projeto:

```bash
python main.py
```

Ou com um CSV customizado:

```bash
python main.py caminho/para/seu_arquivo.csv
```

---

## Controles

| Tecla        | Ação                         |
|--------------|------------------------------|
| Letras A–Z   | Digitar a letra-alvo         |
| F1           | Modo PT-BR (palavras em português) |
| F2           | Modo EN (palavras em inglês) |
| R            | Reiniciar (após Game Over)   |
| ESC          | Sair                         |

---

## Formato do CSV

O arquivo `words.csv` deve ter o formato:

```
pt-br,len-pt-br,en,len-en
gato,4,cat,3
computador,10,computer,8
```

- `len-pt-br` = número exato de caracteres de `pt-br`
- `len-en` = número exato de caracteres de `en`
- Ordenado por `len-pt-br` (crescente), depois por `pt-br` (alfabético)
- Encoding UTF-8 (suporta acentuação)

---

## Estrutura do Projeto

```
word_defender/
├── main.py         # Ponto de entrada
├── game.py         # Loop principal, lógica, renderização
├── word.py         # Classe Word (palavra descendo)
├── projectile.py   # Classe Projectile (laser)
├── loader_csv.py   # Leitura e validação do CSV
├── utils.py        # Funções auxiliares
├── words.csv       # Base de palavras PT-BR/EN
├── requirements.txt
└── README.md
```

---

## Mecânicas

- **Digitação:** Ao digitar a letra correta (primeira letra restante), um laser é disparado automaticamente e elimina essa letra.
- **Erro:** Letra errada acelera todas as palavras por alguns segundos.
- **Vidas:** Se uma palavra tocar a plataforma, você perde uma vida. 3 vidas, depois Game Over.
- **Níveis:** A dificuldade aumenta com a pontuação (mais palavras simultâneas, velocidades maiores, palavras mais longas).

---

## Ferramentas Utilizadas

- **Python 3**
- **Pygame** (gráficos 2D e input)
- **CSV** (módulo padrão para leitura de arquivos)
