/**
 * Utilitários de álgebra linear 3D — matrizes 4x4 (coluna-major para WebGL).
 * Nomes em português para apresentação acadêmica.
 */

/** Cria matriz identidade 4x4 (array 16 elementos, coluna a coluna). */
function matrizIdentidade() {
  return new Float32Array([
    1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1,
  ]);
}

/** Multiplica A * B (ambas 4x4 col-major). */
function multiplicarMatrizes4(a, b) {
  const out = new Float32Array(16);
  for (let c = 0; c < 4; c++) {
    for (let r = 0; r < 4; r++) {
      out[c * 4 + r] =
        a[0 * 4 + r] * b[c * 4 + 0] +
        a[1 * 4 + r] * b[c * 4 + 1] +
        a[2 * 4 + r] * b[c * 4 + 2] +
        a[3 * 4 + r] * b[c * 4 + 3];
    }
  }
  return out;
}

function matrizTranslacao(tx, ty, tz) {
  const m = matrizIdentidade();
  m[12] = tx;
  m[13] = ty;
  m[14] = tz;
  return m;
}

/** Escala uniforme em torno da origem. */
function matrizEscalaUniforme(s) {
  const m = matrizIdentidade();
  m[0] = m[5] = m[10] = s;
  return m;
}

function matrizRotacaoEixoX(rad) {
  const c = Math.cos(rad);
  const s = Math.sin(rad);
  return new Float32Array([
    1, 0, 0, 0,
    0, c, s, 0,
    0, -s, c, 0,
    0, 0, 0, 1,
  ]);
}

function matrizRotacaoEixoY(rad) {
  const c = Math.cos(rad);
  const s = Math.sin(rad);
  return new Float32Array([
    c, 0, -s, 0,
    0, 1, 0, 0,
    s, 0, c, 0,
    0, 0, 0, 1,
  ]);
}

function matrizRotacaoEixoZ(rad) {
  const c = Math.cos(rad);
  const s = Math.sin(rad);
  return new Float32Array([
    c, s, 0, 0,
    -s, c, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1,
  ]);
}

/**
 * Extrai submatriz 3x3 superior-esquerda de uma 4x4 (para normais).
 * Saída em coluna-major 9 elementos.
 */
function submatriz3x3De4x4(m) {
  return new Float32Array([
    m[0], m[1], m[2],
    m[4], m[5], m[6],
    m[8], m[9], m[10],
  ]);
}

/** Inversa 3x3 (para transformar normais quando só há rotação+escala uniforme). */
function inverterMatriz3x3(m) {
  const a = m[0], b = m[1], c = m[2];
  const d = m[3], e = m[4], f = m[5];
  const g = m[6], h = m[7], i = m[8];
  const A = e * i - f * h;
  const B = -(d * i - f * g);
  const C = d * h - e * g;
  const D = -(b * i - c * h);
  const E = a * i - c * g;
  const F = -(a * h - b * g);
  const G = b * f - c * e;
  const H = -(a * f - c * d);
  const I = a * e - b * d;
  let det = a * A + b * B + c * C;
  if (Math.abs(det) < 1e-12) return null;
  det = 1 / det;
  return new Float32Array([
    A * det, D * det, G * det,
    B * det, E * det, H * det,
    C * det, F * det, I * det,
  ]);
}

/** Transposta 3x3 (col-major in/out). */
function transporMatriz3x3(m) {
  return new Float32Array([
    m[0], m[3], m[6],
    m[1], m[4], m[7],
    m[2], m[5], m[8],
  ]);
}

/**
 * Normal = (R^-1)^T para normais com matriz de modelo não ortogonal.
 * Com rotação + escala uniforme, inversa transposta = R * (1/s).
 */
function matrizNormal3x3(matrizModelo) {
  const r3 = submatriz3x3De4x4(matrizModelo);
  const inv = inverterMatriz3x3(r3);
  if (!inv) return new Float32Array([1, 0, 0, 0, 1, 0, 0, 0, 1]);
  return transporMatriz3x3(inv);
}

function vetor3(x, y, z) {
  return new Float32Array([x, y, z]);
}

function copiarVetor3(v) {
  return new Float32Array([v[0], v[1], v[2]]);
}

function normalizarVetor3(v) {
  const len = Math.hypot(v[0], v[1], v[2]);
  if (len < 1e-12) return vetor3(0, 0, 1);
  return vetor3(v[0] / len, v[1] / len, v[2] / len);
}

function produtoEscalar3(a, b) {
  return a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
}

/** a x b */
function produtoVetorial3(a, b) {
  return vetor3(
    a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2],
    a[0] * b[1] - a[1] * b[0],
  );
}

function somarVetor3(a, b) {
  return vetor3(a[0] + b[0], a[1] + b[1], a[2] + b[2]);
}

function escalarVetor3(k, v) {
  return vetor3(k * v[0], k * v[1], k * v[2]);
}

/** Perspectiva simples (campo em radianos, aspecto w/h, near, far), coluna-major WebGL. */
function matrizPerspectiva(fovyRad, aspecto, perto, longe) {
  const f = 1 / Math.tan(fovyRad / 2);
  const inv = 1 / (perto - longe);
  return new Float32Array([
    f / aspecto, 0, 0, 0,
    0, f, 0, 0,
    0, 0, (longe + perto) * inv, -1,
    0, 0, 2 * longe * perto * inv, 0,
  ]);
}

/** Ortográfica simétrica (útil para vista isométrica sem distorção). */
function matrizOrtografica(esquerda, direita, baixo, cima, perto, longe) {
  const rl = direita - esquerda;
  const tb = cima - baixo;
  const fn = longe - perto;
  return new Float32Array([
    2 / rl, 0, 0, 0,
    0, 2 / tb, 0, 0,
    0, 0, -2 / fn, 0,
    -(direita + esquerda) / rl,
    -(cima + baixo) / tb,
    -(longe + perto) / fn,
    1,
  ]);
}

/** Olhar de câmera: eye, alvo, up — gera view matrix 4x4. */
function matrizLookAt(olho, alvo, cima) {
  const zx = olho[0] - alvo[0];
  const zy = olho[1] - alvo[1];
  const zz = olho[2] - alvo[2];
  let len = Math.hypot(zx, zy, zz);
  const z0 = zx / len, z1 = zy / len, z2 = zz / len;

  let x0 = cima[1] * z2 - cima[2] * z1;
  let x1 = cima[2] * z0 - cima[0] * z2;
  let x2 = cima[0] * z1 - cima[1] * z0;
  len = Math.hypot(x0, x1, x2);
  x0 /= len;
  x1 /= len;
  x2 /= len;

  const y0 = z1 * x2 - z2 * x1;
  const y1 = z2 * x0 - z0 * x2;
  const y2 = z0 * x1 - z1 * x0;

  return new Float32Array([
    x0, y0, z0, 0,
    x1, y1, z1, 0,
    x2, y2, z2, 0,
    -produtoEscalar3([x0, x1, x2], olho),
    -produtoEscalar3([y0, y1, y2], olho),
    -produtoEscalar3([z0, z1, z2], olho),
    1,
  ]);
}

/** Multiplica matriz 4x4 por ponto homogêneo (x,y,z,1). Saída (x,y,z). */
function transformarPonto(matriz, p) {
  const x = p[0], y = p[1], z = p[2];
  const w =
    matriz[3] * x + matriz[7] * y + matriz[11] * z + matriz[15];
  const owx = (matriz[0] * x + matriz[4] * y + matriz[8] * z + matriz[12]) / w;
  const owy = (matriz[1] * x + matriz[5] * y + matriz[9] * z + matriz[13]) / w;
  const owz = (matriz[2] * x + matriz[6] * y + matriz[10] * z + matriz[14]) / w;
  return vetor3(owx, owy, owz);
}

/** Multiplica matriz 3x3 (col-major 9) por vetor 3. */
function transformarDirecao(mat3, v) {
  return vetor3(
    mat3[0] * v[0] + mat3[3] * v[1] + mat3[6] * v[2],
    mat3[1] * v[0] + mat3[4] * v[1] + mat3[7] * v[2],
    mat3[2] * v[0] + mat3[5] * v[1] + mat3[8] * v[2],
  );
}
