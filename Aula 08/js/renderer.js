const VERT_SHADER = `
attribute vec3 aPosicao;
attribute vec3 aNormal;
attribute vec3 aCor;

uniform mat4 uMVP;
uniform mat3 uMatNormal;

varying vec3 vNormalVista;
varying vec3 vCor;

void main(void) {
  vNormalVista = normalize(uMatNormal * aNormal);
  vCor = aCor;
  gl_Position = uMVP * vec4(aPosicao, 1.0);
}
`;

const FRAG_SHADER = `
precision mediump float;

varying vec3 vNormalVista;
varying vec3 vCor;

uniform vec3 uDirecaoLuzVista;
uniform float uModoMalha;
uniform float uCullTraseiras;

void main(void) {
  if (uModoMalha > 0.5) {
    gl_FragColor = vec4(0.2, 0.95, 0.45, 1.0);
    return;
  }

  vec3 n = normalize(vNormalVista);
  if (uCullTraseiras > 0.5 && n.z <= 0.0) {
    discard;
  }

  float ambiente = 0.28;
  vec3 L = normalize(uDirecaoLuzVista);
  float difuso = max(dot(n, L), 0.0);
  vec3 rgb = vCor * (ambiente + 0.72 * difuso);
  gl_FragColor = vec4(rgb, 1.0);
}
`;

function criarShader(gl, tipo, codigo) {
  const s = gl.createShader(tipo);
  gl.shaderSource(s, codigo);
  gl.compileShader(s);
  if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
    const msg = gl.getShaderInfoLog(s) || 'erro de shader';
    gl.deleteShader(s);
    throw new Error(msg);
  }
  return s;
}

function criarPrograma(gl, vsSrc, fsSrc) {
  const vs = criarShader(gl, gl.VERTEX_SHADER, vsSrc);
  const fs = criarShader(gl, gl.FRAGMENT_SHADER, fsSrc);
  const prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.linkProgram(prog);
  gl.deleteShader(vs);
  gl.deleteShader(fs);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
    const msg = gl.getProgramInfoLog(prog) || 'erro de link';
    gl.deleteProgram(prog);
    throw new Error(msg);
  }
  return prog;
}

function criarRenderizador(canvas) {
  const gl = canvas.getContext('webgl', { alpha: true, antialias: true });
  if (!gl) return { ok: false, erro: 'WebGL não disponível neste navegador.' };

  const programa = criarPrograma(gl, VERT_SHADER, FRAG_SHADER);

  const loc = {
    aPosicao: gl.getAttribLocation(programa, 'aPosicao'),
    aNormal: gl.getAttribLocation(programa, 'aNormal'),
    aCor: gl.getAttribLocation(programa, 'aCor'),
    uMVP: gl.getUniformLocation(programa, 'uMVP'),
    uMatNormal: gl.getUniformLocation(programa, 'uMatNormal'),
    uDirecaoLuzVista: gl.getUniformLocation(programa, 'uDirecaoLuzVista'),
    uModoMalha: gl.getUniformLocation(programa, 'uModoMalha'),
    uCullTraseiras: gl.getUniformLocation(programa, 'uCullTraseiras'),
  };

  const buffers = {
    posicao: gl.createBuffer(),
    normal: gl.createBuffer(),
    cor: gl.createBuffer(),
    elementosTri: gl.createBuffer(),
    elementosLinha: gl.createBuffer(),
  };

  const extUint = gl.getExtension('OES_element_index_uint');
  let tipoElemento = gl.UNSIGNED_SHORT;

  let contagemTriIndices = 0;
  let contagemLinhaIndices = 0;

  gl.enable(gl.DEPTH_TEST);
  gl.clearColor(0.06, 0.07, 0.09, 1.0);

  function definirMalha(malha) {
    contagemTriIndices = malha.indicesTriangulos.length;
    contagemLinhaIndices = malha.indicesLinhas.length;

    if (malha.usouIndices32bits) {
      if (!extUint) {
        throw new Error('Malha grande: extensão OES_element_index_uint indisponível.');
      }
      tipoElemento = gl.UNSIGNED_INT;
    } else {
      tipoElemento = gl.UNSIGNED_SHORT;
    }

    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.posicao);
    gl.bufferData(gl.ARRAY_BUFFER, malha.posicoes, gl.STATIC_DRAW);

    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.normal);
    gl.bufferData(gl.ARRAY_BUFFER, malha.normais, gl.STATIC_DRAW);

    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.cor);
    gl.bufferData(gl.ARRAY_BUFFER, malha.cores, gl.STATIC_DRAW);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.elementosTri);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, malha.indicesTriangulos, gl.STATIC_DRAW);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.elementosLinha);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, malha.indicesLinhas, gl.STATIC_DRAW);

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, null);
    gl.bindBuffer(gl.ARRAY_BUFFER, null);
  }

  function ligarAtributos() {
    const stride = 0;
    const offset = 0;

    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.posicao);
    gl.enableVertexAttribArray(loc.aPosicao);
    gl.vertexAttribPointer(loc.aPosicao, 3, gl.FLOAT, false, stride, offset);

    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.normal);
    gl.enableVertexAttribArray(loc.aNormal);
    gl.vertexAttribPointer(loc.aNormal, 3, gl.FLOAT, false, stride, offset);

    gl.bindBuffer(gl.ARRAY_BUFFER, buffers.cor);
    gl.enableVertexAttribArray(loc.aCor);
    gl.vertexAttribPointer(loc.aCor, 3, gl.FLOAT, false, stride, offset);
  }

  function desenharCena(mvp, matNormal3, luzDirVista, modoDesenho) {
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    gl.useProgram(programa);
    ligarAtributos();

    gl.uniformMatrix4fv(loc.uMVP, false, mvp);
    gl.uniformMatrix3fv(loc.uMatNormal, false, matNormal3);
    gl.uniform3fv(loc.uDirecaoLuzVista, luzDirVista);

    if (modoDesenho === 'malha') {
      gl.uniform1f(loc.uModoMalha, 1.0);
      gl.uniform1f(loc.uCullTraseiras, 0.0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.elementosLinha);
      gl.drawElements(gl.LINES, contagemLinhaIndices, tipoElemento, 0);
    } else {
      gl.uniform1f(loc.uModoMalha, 0.0);
      gl.uniform1f(loc.uCullTraseiras, 1.0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.elementosTri);
      gl.drawElements(gl.TRIANGLES, contagemTriIndices, tipoElemento, 0);
    }

    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, null);
  }

  function redimensionar(larguraCss, alturaCss) {
    const dpr = window.devicePixelRatio || 1;
    const w = Math.max(1, Math.floor(larguraCss * dpr));
    const h = Math.max(1, Math.floor(alturaCss * dpr));
    if (canvas.width !== w || canvas.height !== h) {
      canvas.width = w;
      canvas.height = h;
    }
  }

  return {
    ok: true,
    gl,
    definirMalha,
    desenharCena,
    redimensionar,
  };
}

function direcaoLuzNoEspacoDaVista(matrizVista) {
  const luzMundo = normalizarVetor3(vetor3(0.35, 0.85, 0.42));
  const r3 = submatriz3x3De4x4(matrizVista);
  const lv = normalizarVetor3(transformarDirecao(r3, luzMundo));
  return new Float32Array([lv[0], lv[1], lv[2]]);
}
