function resolverIndiceObj(token, contagem) {
  if (!token || token === '') return null;
  const i = parseInt(token, 10);
  if (isNaN(i) || i === 0) return null;
  if (i < 0) return contagem + i;
  return i - 1;
}

function interpretarRefVertice(parte, nv, nvt, nvn) {
  const bits = parte.split('/');
  const vi = resolverIndiceObj(bits[0], nv);
  let vti = null;
  let vni = null;
  if (bits.length >= 2 && bits[1] !== '') {
    vti = resolverIndiceObj(bits[1], nvt);
  }
  if (bits.length >= 3 && bits[2] !== '') {
    vni = resolverIndiceObj(bits[2], nvn);
  }
  if (bits.length >= 3 && bits[1] === '') {
    vti = null;
  }
  return { vi, vti, vni };
}

function triangularLeque(indicesVertices) {
  const tris = [];
  const n = indicesVertices.length;
  if (n < 3) return tris;
  for (let i = 1; i < n - 1; i++) {
    tris.push([indicesVertices[0], indicesVertices[i], indicesVertices[i + 1]]);
  }
  return tris;
}

function montarMalhaDeObj(textoObj, materiais) {
  const vertices = [];
  const normais = [];
  const uvs = [];

  let nomeMtllib = '';
  let materialAtual = '';

  const facesBrutas = [];

  const linhas = textoObj.split(/\r?\n/);
  for (const raw of linhas) {
    const linha = raw.trim();
    if (!linha) continue;
    if (linha.startsWith('#')) continue;

    const partes = linha.split(/\s+/);
    const cmd = partes[0].toLowerCase();

    if (cmd === 'g' || cmd === 'o') {
      continue;
    }

    if (cmd === 'mtllib') {
      nomeMtllib = partes.slice(1).join(' ').trim();
      continue;
    }

    if (cmd === 'usemtl') {
      materialAtual = partes.slice(1).join(' ').trim();
      continue;
    }

    if (cmd === 'v' && partes.length >= 4) {
      vertices.push([
        parseFloat(partes[1]),
        parseFloat(partes[2]),
        parseFloat(partes[3]),
      ]);
      continue;
    }

    if (cmd === 'vn' && partes.length >= 4) {
      normais.push([
        parseFloat(partes[1]),
        parseFloat(partes[2]),
        parseFloat(partes[3]),
      ]);
      continue;
    }

    if (cmd === 'vt') {
      uvs.push([
        parseFloat(partes[1] || '0'),
        parseFloat(partes[2] || '0'),
      ]);
      continue;
    }

    if (cmd === 'f') {
      const refs = partes.slice(1);
      const cantos = [];
      for (const ref of refs) {
        const { vi, vti, vni } = interpretarRefVertice(
          ref,
          vertices.length,
          uvs.length,
          normais.length,
        );
        if (vi === null) continue;
        cantos.push({
          vi,
          vti,
          vni,
          material: materialAtual,
        });
      }
      if (cantos.length >= 3) {
        facesBrutas.push(cantos);
      }
      continue;
    }
  }

  const numVerticesArquivo = vertices.length;

  let cx = 0,
    cy = 0,
    cz = 0;
  if (numVerticesArquivo > 0) {
    for (const v of vertices) {
      cx += v[0];
      cy += v[1];
      cz += v[2];
    }
    cx /= numVerticesArquivo;
    cy /= numVerticesArquivo;
    cz /= numVerticesArquivo;
  }

  const vertsCentralizados = vertices.map((v) => [
    v[0] - cx,
    v[1] - cy,
    v[2] - cz,
  ]);

  let raioMax = 0;
  for (const v of vertsCentralizados) {
    const d = Math.hypot(v[0], v[1], v[2]);
    if (d > raioMax) raioMax = d;
  }
  const escalaNorm = raioMax > 1e-9 ? 1 / raioMax : 1;
  const vertsNorm = vertsCentralizados.map((v) => [
    v[0] * escalaNorm,
    v[1] * escalaNorm,
    v[2] * escalaNorm,
  ]);

  function pontoDeVi(vi) {
    const v = vertsNorm[vi];
    return new Float32Array([v[0], v[1], v[2]]);
  }

  function normalDeVni(vni) {
    if (vni === null) return null;
    const n = normais[vni];
    return normalizarVetor3(new Float32Array([n[0], n[1], n[2]]));
  }

  const triangulos = [];

  for (const face of facesBrutas) {
    const triRefs = triangularLeque(face);
    for (const tri of triRefs) {
      const [a, b, c] = tri;
      const pa = pontoDeVi(a.vi);
      const pb = pontoDeVi(b.vi);
      const pc = pontoDeVi(c.vi);

      let na = normalDeVni(a.vni);
      let nb = normalDeVni(b.vni);
      let nc = normalDeVni(c.vni);

      const faltamNormais = na === null || nb === null || nc === null;
      if (faltamNormais) {
        const e1 = somarVetor3(pb, escalarVetor3(-1, pa));
        const e2 = somarVetor3(pc, escalarVetor3(-1, pa));
        const nf = normalizarVetor3(produtoVetorial3(e1, e2));
        na = copiarVetor3(nf);
        nb = copiarVetor3(nf);
        nc = copiarVetor3(nf);
      }

      const nomeMat = a.material || b.material || c.material || '';
      const kd = obterKd(materiais || new Map(), nomeMat);
      const c0 = new Float32Array(kd);
      const c1 = new Float32Array(kd);
      const c2 = new Float32Array(kd);

      triangulos.push({
        pa,
        pb,
        pc,
        na,
        nb,
        nc,
        c0,
        c1,
        c2,
      });
    }
  }

  const numFacesTriangulos = triangulos.length;
  const numVerticesDesenho = numFacesTriangulos * 3;

  const posicoes = new Float32Array(numVerticesDesenho * 3);
  const normaisOut = new Float32Array(numVerticesDesenho * 3);
  const cores = new Float32Array(numVerticesDesenho * 3);

  let w = 0;
  for (let t = 0; t < triangulos.length; t++) {
    const T = triangulos[t];
    const pts = [T.pa, T.pb, T.pc];
    const ns = [T.na, T.nb, T.nc];
    const cs = [T.c0, T.c1, T.c2];
    for (let i = 0; i < 3; i++) {
      posicoes[w] = pts[i][0];
      posicoes[w + 1] = pts[i][1];
      posicoes[w + 2] = pts[i][2];
      normaisOut[w] = ns[i][0];
      normaisOut[w + 1] = ns[i][1];
      normaisOut[w + 2] = ns[i][2];
      cores[w] = cs[i][0];
      cores[w + 1] = cs[i][1];
      cores[w + 2] = cs[i][2];
      w += 3;
    }
  }

  const usaUint32 = numVerticesDesenho > 65535;
  const CtorIdx = usaUint32 ? Uint32Array : Uint16Array;
  const indicesTriangulos = new CtorIdx(numVerticesDesenho);
  for (let i = 0; i < numVerticesDesenho; i++) indicesTriangulos[i] = i;

  const arestaSet = new Set();
  function chaveAresta(i, j) {
    return i < j ? `${i},${j}` : `${j},${i}`;
  }
  for (let t = 0; t < numFacesTriangulos; t++) {
    const b0 = t * 3;
    const b1 = t * 3 + 1;
    const b2 = t * 3 + 2;
    arestaSet.add(chaveAresta(b0, b1));
    arestaSet.add(chaveAresta(b1, b2));
    arestaSet.add(chaveAresta(b2, b0));
  }
  const numArestasUnicas = arestaSet.size;

  const euler = numVerticesArquivo - numArestasUnicas + numFacesTriangulos;

  const indicesLinhas = new CtorIdx(numArestasUnicas * 2);
  let li = 0;
  for (const key of arestaSet) {
    const [i, j] = key.split(',').map((x) => parseInt(x, 10));
    indicesLinhas[li++] = i;
    indicesLinhas[li++] = j;
  }

  return {
    posicoes,
    normais: normaisOut,
    cores,
    indicesTriangulos,
    indicesLinhas,
    usouIndices32bits: usaUint32,
    numVerticesArquivo,
    numArestasUnicas,
    numFacesTriangulos,
    euler,
    nomeMtllib,
  };
}
