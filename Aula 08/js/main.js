const PASSO_ROTACAO = 0.045;
const PASSO_TRANSLACAO = 0.04;
const FATOR_ESCALA = 1.08;

const estado = {
  materiais: new Map(),
  malha: null,
  nomeObj: '—',
  textoObjGuardado: '',
  modoVisual: 'solido',
  projecao: 'perspectiva',
  translacao: { x: 0, y: 0 },
  escala: 1,
  anguloX: 0,
  anguloY: 0,
  anguloZ: 0,
  eixoRotacao: 'Y',
  modoInteracao: 'rotacao',
  aguardandoEixoPosR: false,
  orbitaMouseX: 0,
  orbitaMouseY: 0,
  caminhoCatalogoAtual: null,
};

let renderizador = null;
let canvas = null;
let animacaoAtiva = false;

function mesclarMateriais(mapa) {
  for (const [k, v] of mapa) {
    estado.materiais.set(k, v);
  }
}

function matrizModeloDoUsuario() {
  const { translacao, escala, anguloX, anguloY, anguloZ, orbitaMouseX, orbitaMouseY } = estado;
  const mS = matrizEscalaUniforme(escala);
  const mRxM = matrizRotacaoEixoX(orbitaMouseY);
  const mRyM = matrizRotacaoEixoY(orbitaMouseX);
  const mRx = matrizRotacaoEixoX(anguloX);
  const mRy = matrizRotacaoEixoY(anguloY);
  const mRz = matrizRotacaoEixoZ(anguloZ);
  const mT = matrizTranslacao(translacao.x, translacao.y, 0);

  let M = mS;
  M = multiplicarMatrizes4(mRyM, M);
  M = multiplicarMatrizes4(mRxM, M);
  M = multiplicarMatrizes4(mRx, M);
  M = multiplicarMatrizes4(mRy, M);
  M = multiplicarMatrizes4(mRz, M);
  M = multiplicarMatrizes4(mT, M);
  return M;
}

function montarMatrizesCamera(largura, altura) {
  const aspecto = largura / Math.max(altura, 1);
  const olho = vetor3(0, 0.35, 4);
  const alvo = vetor3(0, 0, 0);
  const cima = vetor3(0, 1, 0);
  const V = matrizLookAt(olho, alvo, cima);

  let P;
  if (estado.projecao === 'isometrica') {
    const h = 1.35;
    P = matrizOrtografica(-h * aspecto, h * aspecto, -h, h, 0.1, 80);
  } else {
    P = matrizPerspectiva((50 * Math.PI) / 180, aspecto, 0.1, 80);
  }

  const M = matrizModeloDoUsuario();
  const VM = multiplicarMatrizes4(V, M);
  const mvp = multiplicarMatrizes4(P, VM);
  const matNorm = matrizNormal3x3(VM);
  const luzDir = direcaoLuzNoEspacoDaVista(V);
  return { mvp, matNorm, luzDir };
}

function atualizarPainel() {
  const m = estado.malha;
  document.getElementById('valorNome').textContent = estado.nomeObj;
  document.getElementById('valorV').textContent = m ? String(m.numVerticesArquivo) : '—';
  document.getElementById('valorE').textContent = m ? String(m.numArestasUnicas) : '—';
  document.getElementById('valorF').textContent = m ? String(m.numFacesTriangulos) : '—';
  document.getElementById('valorEuler').textContent = m ? String(m.euler) : '—';
  document.getElementById('valorModo').textContent =
    estado.modoVisual === 'malha' ? 'malha (wireframe)' : 'sólido';
  document.getElementById('valorProjecao').textContent =
    estado.projecao === 'isometrica' ? 'isométrica (ortográfica)' : 'perspectiva';
  document.getElementById('valorTransformacao').textContent =
    estado.modoInteracao === 'translacao' ? 'translação (setas movem)' : 'rotação (setas giram)';
  document.getElementById('valorEixo').textContent = estado.eixoRotacao;
}

function cicloDesenho() {
  if (!renderizador || !renderizador.ok || !estado.malha) return;

  const rect = canvas.getBoundingClientRect();
  renderizador.redimensionar(rect.width, rect.height);
  const { mvp, matNorm, luzDir } = montarMatrizesCamera(canvas.width, canvas.height);

  renderizador.desenharCena(mvp, matNorm, luzDir, estado.modoVisual);
}

function iniciarAnimacao() {
  if (animacaoAtiva) return;
  animacaoAtiva = true;
  function quadro() {
    cicloDesenho();
    requestAnimationFrame(quadro);
  }
  requestAnimationFrame(quadro);
}

function aplicarMalhaDoTexto(nomeArquivo, texto) {
  try {
    estado.textoObjGuardado = texto;
    const malha = montarMalhaDeObj(texto, estado.materiais);
    estado.malha = malha;
    estado.nomeObj = nomeArquivo;
    renderizador.definirMalha(malha);
    atualizarPainel();
    return true;
  } catch (e) {
    console.error(e);
    alert('Falha ao interpretar OBJ: ' + (e.message || e));
    return false;
  }
}

function carregarMtlDoTexto(texto) {
  const mapa = analisarMtl(texto);
  mesclarMateriais(mapa);
  atualizarPainel();
}

function nomeArquivoDeCaminho(caminho) {
  const partes = caminho.replace(/\\/g, '/').split('/');
  return partes[partes.length - 1] || caminho;
}

function listaCaminhosCatalogoOrdenada() {
  if (typeof CATALOGO_EXEMPLOS_OBJ === 'undefined') return [];
  const out = [];
  for (const titulo of Object.keys(CATALOGO_EXEMPLOS_OBJ)) {
    const caminhos = [...CATALOGO_EXEMPLOS_OBJ[titulo]].sort((a, b) =>
      nomeArquivoDeCaminho(a).localeCompare(nomeArquivoDeCaminho(b), 'pt', {
        sensitivity: 'base',
      }),
    );
    out.push(...caminhos);
  }
  return out;
}

function indiceAtualNoCatalogo() {
  const lista = listaCaminhosCatalogoOrdenada();
  if (!lista.length) return -1;
  const c = estado.caminhoCatalogoAtual;
  if (c == null) return -1;
  const i = lista.indexOf(c);
  return i >= 0 ? i : -1;
}

function atualizarBarraNavegacaoModelos() {
  const ant = document.getElementById('btnModeloAnterior');
  const prox = document.getElementById('btnModeloProximo');
  const hint = document.getElementById('hintNavegacaoModelos');
  const lista = listaCaminhosCatalogoOrdenada();
  const n = lista.length;
  const idx = indiceAtualNoCatalogo();

  if (ant) ant.disabled = n === 0;
  if (prox) prox.disabled = n === 0;

  if (hint) {
    if (n === 0) {
      hint.textContent = '';
    } else if (idx < 0) {
      hint.textContent = 'Catálogo: — / ' + n + ' (arquivo próprio)';
    } else {
      hint.textContent = 'Catálogo: ' + (idx + 1) + ' / ' + n;
    }
  }
}

async function carregarModeloCatalogoDelta(delta) {
  const lista = listaCaminhosCatalogoOrdenada();
  if (!lista.length) return;
  let i = indiceAtualNoCatalogo();
  if (i < 0) {
    i = delta > 0 ? 0 : lista.length - 1;
  } else {
    i = (i + delta + lista.length) % lista.length;
  }
  await carregarExemploRemoto(lista[i]);
}

function configurarBotoesNavegacaoTopo() {
  const ant = document.getElementById('btnModeloAnterior');
  const prox = document.getElementById('btnModeloProximo');
  if (ant) ant.addEventListener('click', () => carregarModeloCatalogoDelta(-1));
  if (prox) prox.addEventListener('click', () => carregarModeloCatalogoDelta(1));
  atualizarBarraNavegacaoModelos();
}

function marcarExemploAtivo(caminho) {
  document.querySelectorAll('.cartao-modelo').forEach((el) => {
    const ativo = caminho != null && el.dataset.caminho === caminho;
    el.classList.toggle('ativo', ativo);
  });
}

function corFundoMiniaturaCartao(caminho) {
  let h = 5381;
  for (let i = 0; i < caminho.length; i++) {
    h = (h * 33) ^ caminho.charCodeAt(i);
  }
  const tons = ['#3d4452', '#353b48', '#424a58', '#323844', '#404956'];
  return tons[(h >>> 0) % tons.length];
}

function rotuloMetaPasta(caminho) {
  const norm = caminho.replace(/\\/g, '/');
  if (norm.includes('/online/')) return 'models › online';
  const partes = norm.split('/').filter(Boolean);
  if (partes.length >= 2) return partes.slice(0, -1).join(' › ');
  return 'models';
}

function seletorModelosRaiz() {
  return document.getElementById('seletorModelos');
}

function fecharSeletorModelos() {
  const root = seletorModelosRaiz();
  if (!root) return;
  root.classList.remove('seletor-modelos--aberto');
  root.setAttribute('aria-expanded', 'false');
  const alca = document.getElementById('alcaSeletorModelos');
  if (alca) alca.setAttribute('aria-expanded', 'false');
}

function abrirSeletorModelos() {
  const root = seletorModelosRaiz();
  if (!root) return;
  root.classList.add('seletor-modelos--aberto');
  root.setAttribute('aria-expanded', 'true');
  const alca = document.getElementById('alcaSeletorModelos');
  if (alca) alca.setAttribute('aria-expanded', 'true');
}

function alternarSeletorModelos() {
  const root = seletorModelosRaiz();
  if (!root) return;
  if (root.classList.contains('seletor-modelos--aberto')) fecharSeletorModelos();
  else abrirSeletorModelos();
}

function configurarSeletorModelosUi() {
  const alca = document.getElementById('alcaSeletorModelos');
  const overlay = document.getElementById('seletorModelosOverlay');
  const btnLateral = document.getElementById('btnAbrirGaleriaLateral');
  if (alca) alca.addEventListener('click', alternarSeletorModelos);
  if (overlay) overlay.addEventListener('click', fecharSeletorModelos);
  if (btnLateral) btnLateral.addEventListener('click', abrirSeletorModelos);
}

const SVG_MALHA_CARTAO = `<svg class="cartao-modelo__svg" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round" stroke-linecap="round" d="M32 8 L52 22 L52 42 L32 56 L12 42 L12 22 Z M32 8 L32 28 M12 22 L32 28 L52 22 M12 42 L32 28 L52 42"/><circle cx="32" cy="28" r="2.5" fill="currentColor"/></svg>`;

function montarGaleriaModelos() {
  const host = document.getElementById('gradeModelosPorGrupo');
  const badge = document.getElementById('badgeContagemModelos');
  if (!host || typeof CATALOGO_EXEMPLOS_OBJ === 'undefined') return;

  host.innerHTML = '';
  let total = 0;
  const titulosGrupo = Object.keys(CATALOGO_EXEMPLOS_OBJ);

  for (const tituloGrupo of titulosGrupo) {
    const caminhos = [...CATALOGO_EXEMPLOS_OBJ[tituloGrupo]].sort((a, b) =>
      nomeArquivoDeCaminho(a).localeCompare(nomeArquivoDeCaminho(b), 'pt', {
        sensitivity: 'base',
      }),
    );
    total += caminhos.length;

    const sec = document.createElement('section');
    sec.className = 'grupo-grade-modelos';

    const h3 = document.createElement('h3');
    h3.className = 'titulo-grupo-grade';
    h3.textContent = tituloGrupo;

    const grade = document.createElement('div');
    grade.className = 'grade-modelos';

    for (const caminho of caminhos) {
      const nomeArq = nomeArquivoDeCaminho(caminho);
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'cartao-modelo';
      btn.dataset.caminho = caminho;
      btn.title = caminho;

      const arte = document.createElement('div');
      arte.className = 'cartao-modelo__arte';
      arte.style.background = corFundoMiniaturaCartao(caminho);
      const wrapSvg = document.createElement('div');
      wrapSvg.innerHTML = SVG_MALHA_CARTAO;
      arte.appendChild(wrapSvg.firstElementChild);

      const corpo = document.createElement('div');
      corpo.className = 'cartao-modelo__corpo';
      const nomeEl = document.createElement('div');
      nomeEl.className = 'cartao-modelo__nome';
      nomeEl.textContent = nomeArq;
      const meta = document.createElement('div');
      meta.className = 'cartao-modelo__meta';
      meta.textContent = rotuloMetaPasta(caminho);
      corpo.appendChild(nomeEl);
      corpo.appendChild(meta);

      btn.appendChild(arte);
      btn.appendChild(corpo);
      btn.addEventListener('click', async () => {
        const ok = await carregarExemploRemoto(caminho);
        if (ok) fecharSeletorModelos();
      });
      grade.appendChild(btn);
    }

    sec.appendChild(h3);
    sec.appendChild(grade);
    host.appendChild(sec);
  }

  if (badge) badge.textContent = String(total);
}

async function carregarExemploRemoto(caminho) {
  const msg = document.getElementById('msgWebgl');
  if (msg) msg.textContent = 'Carregando…';

  const nomeArquivo = nomeArquivoDeCaminho(caminho);
  const prefixo = caminho.replace(/\.obj$/i, '');
  const caminhoMtl = prefixo + '.mtl';

  try {
    const respMtl = await fetch(encodeURI(caminhoMtl));
    if (respMtl.ok) {
      carregarMtlDoTexto(await respMtl.text());
    }
  } catch (_) {}

  try {
    const respObj = await fetch(encodeURI(caminho));
    if (!respObj.ok) throw new Error('HTTP ' + respObj.status);
    const texto = await respObj.text();
    if (!aplicarMalhaDoTexto(nomeArquivo, texto)) {
      marcarExemploAtivo(estado.caminhoCatalogoAtual);
      if (msg) msg.textContent = '';
      return false;
    }
    estado.caminhoCatalogoAtual = caminho;
    marcarExemploAtivo(caminho);
    atualizarBarraNavegacaoModelos();
    if (msg) msg.textContent = '';
    return true;
  } catch (e) {
    console.error(e);
    marcarExemploAtivo(estado.caminhoCatalogoAtual);
    if (msg) {
      msg.textContent =
        'Não foi possível carregar o exemplo. Use servidor HTTP (ex.: python -m http.server).';
    }
    alert('Erro ao carregar: ' + nomeArquivo + ' — ' + (e.message || e));
    return false;
  }
}

function tentarCarregarModelosIniciais() {
  Promise.all([
    fetch('models/objetos.mtl')
      .then((r) => (r.ok ? r.text() : ''))
      .catch(() => ''),
    fetch('models/cubo.obj')
      .then((r) => (r.ok ? r.text() : null))
      .catch(() => null),
  ]).then(([mtlTxt, objTxt]) => {
    if (mtlTxt) carregarMtlDoTexto(mtlTxt);
    if (objTxt && aplicarMalhaDoTexto('cubo.obj', objTxt)) {
      estado.caminhoCatalogoAtual = 'models/cubo.obj';
      marcarExemploAtivo('models/cubo.obj');
    }
    atualizarBarraNavegacaoModelos();
    atualizarPainel();
  });
}

function tratarTecla(ev) {
  const k = ev.key.length === 1 ? ev.key.toLowerCase() : ev.key;

  if (k === 'Escape') {
    const root = document.getElementById('seletorModelos');
    if (root && root.classList.contains('seletor-modelos--aberto')) {
      fecharSeletorModelos();
      ev.preventDefault();
      return;
    }
    estado.translacao.x = 0;
    estado.translacao.y = 0;
    estado.escala = 1;
    estado.anguloX = estado.anguloY = estado.anguloZ = 0;
    estado.orbitaMouseX = estado.orbitaMouseY = 0;
    estado.modoInteracao = 'rotacao';
    estado.aguardandoEixoPosR = false;
    atualizarPainel();
    ev.preventDefault();
    return;
  }

  if (ev.key === '[') {
    carregarModeloCatalogoDelta(-1);
    ev.preventDefault();
    return;
  }
  if (ev.key === ']') {
    carregarModeloCatalogoDelta(1);
    ev.preventDefault();
    return;
  }

  if (k === 'r') {
    estado.aguardandoEixoPosR = true;
    atualizarPainel();
    ev.preventDefault();
    return;
  }

  if (estado.aguardandoEixoPosR && (k === 'x' || k === 'y' || k === 'z')) {
    estado.eixoRotacao = k.toUpperCase();
    estado.aguardandoEixoPosR = false;
    estado.modoInteracao = 'rotacao';
    atualizarPainel();
    ev.preventDefault();
    return;
  }

  if (k === 'w') {
    estado.modoVisual = 'malha';
    atualizarPainel();
    ev.preventDefault();
    return;
  }
  if (k === 's' && ev.key !== 'ArrowDown') {
    estado.modoVisual = 'solido';
    atualizarPainel();
    ev.preventDefault();
    return;
  }
  if (k === 'p') {
    estado.projecao = estado.projecao === 'perspectiva' ? 'isometrica' : 'perspectiva';
    atualizarPainel();
    ev.preventDefault();
    return;
  }
  if (k === 't') {
    estado.modoInteracao = 'translacao';
    estado.aguardandoEixoPosR = false;
    atualizarPainel();
    ev.preventDefault();
    return;
  }

  if (k === '+' || k === '=') {
    estado.escala *= FATOR_ESCALA;
    ev.preventDefault();
    return;
  }
  if (k === '-' || k === '_') {
    estado.escala /= FATOR_ESCALA;
    ev.preventDefault();
    return;
  }

  if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') {
    const sinal = ev.key === 'ArrowRight' ? 1 : -1;
    if (estado.modoInteracao === 'translacao') {
      estado.translacao.x += sinal * PASSO_TRANSLACAO;
    } else {
      const da = sinal * PASSO_ROTACAO;
      if (estado.eixoRotacao === 'X') estado.anguloX += da;
      if (estado.eixoRotacao === 'Y') estado.anguloY += da;
      if (estado.eixoRotacao === 'Z') estado.anguloZ += da;
    }
    ev.preventDefault();
    return;
  }

  if (ev.key === 'ArrowUp' || ev.key === 'ArrowDown') {
    const sinal = ev.key === 'ArrowUp' ? 1 : -1;
    if (estado.modoInteracao === 'translacao') {
      estado.translacao.y += sinal * PASSO_TRANSLACAO;
      ev.preventDefault();
    }
  }
}

function configurarMouse(canvasEl) {
  let arrastando = false;
  let ultimoX = 0;
  let ultimoY = 0;

  canvasEl.addEventListener('mousedown', (e) => {
    arrastando = true;
    ultimoX = e.clientX;
    ultimoY = e.clientY;
  });
  window.addEventListener('mouseup', () => {
    arrastando = false;
  });
  canvasEl.addEventListener('mouseleave', () => {
    arrastando = false;
  });
  window.addEventListener('mousemove', (e) => {
    if (!arrastando) return;
    const dx = e.clientX - ultimoX;
    const dy = e.clientY - ultimoY;
    ultimoX = e.clientX;
    ultimoY = e.clientY;
    estado.orbitaMouseX += dx * 0.007;
    estado.orbitaMouseY += dy * 0.007;
  });
}

function aoCarregar() {
  canvas = document.getElementById('canvas3d');
  const msg = document.getElementById('msgWebgl');

  renderizador = criarRenderizador(canvas);
  if (!renderizador.ok) {
    msg.textContent = renderizador.erro;
    return;
  }
  msg.textContent = '';

  document.getElementById('entradaObj').addEventListener('change', (e) => {
    const arq = e.target.files && e.target.files[0];
    if (!arq) return;
    const leitor = new FileReader();
    leitor.onload = () => {
      marcarExemploAtivo(null);
      estado.caminhoCatalogoAtual = null;
      if (aplicarMalhaDoTexto(arq.name, String(leitor.result))) {
        atualizarBarraNavegacaoModelos();
      }
    };
    leitor.readAsText(arq);
  });

  document.getElementById('entradaMtl').addEventListener('change', (e) => {
    const arq = e.target.files && e.target.files[0];
    if (!arq) return;
    const leitor = new FileReader();
    leitor.onload = () => {
      carregarMtlDoTexto(String(leitor.result));
      if (estado.textoObjGuardado) {
        aplicarMalhaDoTexto(estado.nomeObj, estado.textoObjGuardado);
      }
      marcarExemploAtivo(estado.caminhoCatalogoAtual);
      atualizarBarraNavegacaoModelos();
    };
    leitor.readAsText(arq);
  });

  window.addEventListener('keydown', tratarTecla);
  window.addEventListener('resize', cicloDesenho);
  configurarMouse(canvas);

  montarGaleriaModelos();
  configurarSeletorModelosUi();
  configurarBotoesNavegacaoTopo();
  tentarCarregarModelosIniciais();

  atualizarPainel();
  iniciarAnimacao();
}

window.addEventListener('DOMContentLoaded', aoCarregar);
