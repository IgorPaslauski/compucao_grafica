# Visualizador interativo OBJ + MTL (WebGL)

## Objetivo

Projeto acadêmico de **Computação Gráfica**: visualizar modelos **Wavefront OBJ** com materiais **MTL** (`Kd`), aplicar **iluminação difusa simples**, **projeção perspectiva ou isométrica (ortográfica)** e **transformações 3D** com matrizes 4×4, com código legível em **HTML/CSS/JavaScript** puro (sem Three.js nem carregadores prontos).

Este trabalho está alinhado ao conteúdo de introdução a modelagem e visualização em 3D, em especial ao capítulo que descreve pipelines de vértices, modelos e interação com cena, conforme **Shreiner et al., *OpenGL Programming Guide*, 7ª edição, Cap. 2, p. 115** (referência da disciplina).

## Como executar

1. **Recomendado:** subir um servidor HTTP simples na pasta do projeto (alguns navegadores bloqueiam `fetch` em `file://`).

   Com Python 3:

   ```bash
   cd "Aula 08"
   python -m http.server 8080
   ```

   Abra no navegador: `http://localhost:8080/`

2. **Alternativa:** abrir `index.html` diretamente. Se o modelo ou o MTL não aparecerem, use o servidor acima.

## Como carregar modelos

- Use **Carregar modelo (.obj)** para escolher um arquivo OBJ.
- Use **Carregar materiais (.mtl)** para escolher um MTL (por exemplo `models/objetos.mtl`). Ao recarregar o MTL, o último OBJ carregado é **remontado** com as novas cores.
- O projeto inicia, quando servido por HTTP, carregando `models/objetos.mtl` e `models/cubo.obj`.

Na pasta `models/` há quatro exemplos prontos:

| Arquivo          | Observação                                       |
|------------------|--------------------------------------------------|
| `cubo.obj`       | Normais + vários `usemtl`                        |
| `piramide.obj`   | Misto de triângulos/quad + índices negativos     |
| `tetraedro.obj`  | Sem `vn` (normais por face via produto vetorial) |
| `prisma_hex.obj` | Polígonos com mais de 4 vértices (leque)         |

## Controles

| Entrada | Ação |
|---------|------|
| **W** | Modo malha (wireframe) |
| **S** | Modo sólido |
| **P** | Alterna perspectiva e isométrica (ortográfica) |
| **R** depois **X** / **Y** / **Z** | Eixo ativo para rotação |
| **←** **→** | Rotaciona no eixo escolhido *ou* move em X (no modo translação) |
| **↑** **↓** | Move em Y no modo translação |
| **T** | Modo translação no plano da tela (eixos X/Y do objeto) |
| **+** / **-** | Aumenta / diminui escala uniforme |
| **Esc** | Reseta transformações (escala, rotações, translação, orbita do mouse) |
| **Mouse** (arrastar) | Orbita simples (bônus) |

## Estrutura de pastas

```
Aula 08/
  index.html
  style.css
  README.md
  js/
    main.js        — interface, teclado, mouse, laço
    math3d.js      — matrizes 4×4, vetores, proj e look-at
    mtlParser.js   — `newmtl`, `Kd`
    objParser.js   — `v`, `vn`, `vt`, `f`, `mtllib`, `usemtl`, leque
    renderer.js    — WebGL, shaders, sólido / wireframe
  models/
    objetos.mtl
    cubo.obj
    piramide.obj
    tetraedro.obj
    prisma_hex.obj
```

## Suporte a OBJ / MTL (implementação própria)

**OBJ**

- `v`, `vn`, `vt`
- faces `f v`, `f v//vn`, `f v/vt/vn`
- índices negativos
- comentários `#`, grupos `g` / `o` ignorados sem erro
- `mtllib` e `usemtl` para escolher material por face

**MTL**

- `newmtl nome`
- `Kd r g b` (cor difusa aplicada na iluminação por face no fragment shader)

**Geometria**

- polígonos com 4+ vértices: triangulação em **leque**
- centroide → centralizar na origem → escalar para caber na view
- se faltar normal: **n = (v₁ − v₀) × (v₂ − v₀)**

**Renderização**

- sólido com luz direcional fixa e `Kd`
- wireframe por índices de arestas
- **culling** de faces traseiras no fragment shader usando **n.z** no espaço da vista
- matriz normal inversa-transposta (submatriz 3×3) para normais

## Observação

Nomes de funções e variáveis estão em **português** quando faz sentido pedagógico; comentários focam nos passos da pipeline e nos requisitos da atividade.
