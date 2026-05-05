# Aula 08 — Visualizador 3D OBJ + MTL (WebGL)

Projeto da disciplina de **Computação Gráfica**: aplicativo web que interpreta **Wavefront OBJ** e **MTL** manualmente (sem Three.js nem loaders prontos), renderiza com **WebGL 1**, aplica **iluminação difusa**, **projeção perspectiva ou ortográfica** e **transformações 3D** via matrizes $4 \times 4$.

Referência pedagógica: **Shreiner et al., *OpenGL Programming Guide*, 7ª edição, Cap. 2, p. 115** (pipeline, modelos e interação com a cena).

---

## Interface (layout atual)

- **Cabeçalho:** título, botões **Importar OBJ** / **Importar MTL** (atalhos para os mesmos campos da barra lateral), navegação **Anterior** / **Próximo** no catálogo e indicador **posição / total**.
- **Área principal:** canvas 3D em moldura; foco visual da tela.
- **Barra lateral:** upload OBJ/MTL, abertura da **galeria**, estatísticas ($V$, $E$, $F$, Euler), atalhos de teclado.
- **Galeria (rodapé):** painel que **expande para cima**; grade de cartões com ícone de malha; agrupamento por pasta (`models/` e `models/online/`). Lista definida em `js/exemplosCatalogo.js`.

Tema visual: layout claro, tipografia **Inter**, acento azul discreto.

---

## Como executar

1. **Recomendado:** servidor HTTP local (o `fetch` dos exemplos e do `objetos.mtl` costuma falhar em `file://`).

   ```bash
   cd "Aula 08"
   python -m http.server 8080
   ```

   Abra: `http://localhost:8080/`

2. **Alternativa:** abrir `index.html` direto no navegador. Use **Importar OBJ/MTL** manualmente se a carga automática não rodar.

**Requisitos:** navegador com **WebGL**; malhas muito grandes podem precisar da extensão `OES_element_index_uint` (índices 32 bits).

---

## Carregar modelos

| Forma | Descrição |
|--------|-----------|
| **Importar OBJ / MTL** (topo ou lateral) | Escolhe arquivos locais. Recarregar o MTL **remonta** o último OBJ com as novas cores. |
| **Galeria** | Clique no cartão; tenta carregar `.mtl` com o mesmo prefixo do `.obj`. |
| **Anterior / Próximo** | Percorre a lista ordenada do catálogo (com *wrap-around*). |
| **Inicialização** | Com HTTP, carrega `models/objetos.mtl` e `models/cubo.obj`. |

Modelos de exemplo:

- **Raiz `models/`:** `cubo.obj`, `piramide.obj`, `tetraedro.obj`, `prisma_hex.obj`, `objetos.mtl`
- **`models/online/`:** conjunto adicional de OBJ de teste (incluídos no catálogo em `exemplosCatalogo.js`)

---

## Controles

| Entrada | Ação |
|---------|------|
| **W** | Malha (wireframe) |
| **S** | Sólido |
| **P** | Perspectiva ↔ ortográfica (“isométrica” didática) |
| **R** depois **X** / **Y** / **Z** | Eixo de rotação |
| **←** **→** | Rotação (modo padrão) ou translação em X (**T**) |
| **↑** **↓** | Translação em Y (com **T**) |
| **T** | Modo translação |
| **+** **−** | Escala uniforme |
| **[** **]** | Modelo anterior / próximo no catálogo |
| **Esc** | Fecha a galeria, se aberta; senão **reseta** transformações |
| **Mouse** (arrastar) | Órbita simples |

---

## Estrutura do projeto

```
Aula 08/
  index.html
  style.css
  README.md
  js/
    main.js              — UI, teclado, mouse, câmera, galeria, navegação catálogo
    math3d.js            — matrizes 4×4, vetores, perspectiva, ortográfica, look-at
    mtlParser.js         — newmtl, Kd
    objParser.js         — v, vn, vt, f, mtllib, usemtl, leque, Euler
    renderer.js          — WebGL, shaders, sólido / wireframe
    exemplosCatalogo.js  — caminhos dos OBJ da galeria (por grupo)
  models/
    objetos.mtl
    cubo.obj, piramide.obj, tetraedro.obj, prisma_hex.obj
    online/              — OBJ (e alguns MTL) extras no catálogo
  latex/
    relatorio.tex        — relatório técnico LaTeX (Overleaf / pdfLaTeX)
```

---

## Suporte OBJ / MTL (implementação própria)

**OBJ:** `v`, `vn`, `vt`; faces `f v`, `f v//vn`, `f v/vt/vn`; índices negativos; `#`; `g`/`o` ignorados sem quebrar; `mtllib`, `usemtl`.

**MTL:** `newmtl`, `Kd r g b` (cor difusa no shader).

**Geometria:** triangulação em **leque** para polígonos com 4+ vértices; centralização pelo centroide; normalização de escala; normal de face `(v₁ − v₀) × (v₂ − v₀)` quando faltar `vn`.

**Renderização:** luz direcional + ambiente; **culling** simplificado pela componente $z$ da normal no espaço da vista (fragment shader); matriz normal $3 \times 3$ consistente com o modelo-vista; wireframe por arestas únicas.

---

## Relatório técnico (LaTeX)

Em **`latex/relatorio.tex`** há um artigo em português descrevendo arquitetura, parsers, pipeline e limitações — pronto para **Overleaf** (pdfLaTeX). Ajuste `\author{...}` com nome e dados da turma, se necessário.

---

## Observação

Nomes de funções e variáveis aparecem em **português** onde ajuda a leitura didática; a lógica de renderização e de carga permanece explícita, sem camadas desnecessárias.
