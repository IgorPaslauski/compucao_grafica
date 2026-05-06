/**
 * Parser manual de arquivo MTL (subset: newmtl, Kd).
 * Retorna Map: nomeMaterial -> { kd: [r, g, b] }
 */

/**
 * @param {string} texto
 * @returns {Map<string, { kd: number[] }>}
 */
function analisarMtl(texto) {
  const materiais = new Map();
  let atual = null;

  const linhas = texto.split(/\r?\n/);

  for (let raw of linhas) {
    const linha = raw.trim();

    if (!linha || linha.startsWith("#")) {
      continue;
    }

    const partes = linha.split(/\s+/);
    const comando = partes[0].toLowerCase();

    if (comando === "newmtl") {
      const nome = partes.slice(1).join(" ").trim() || "default";

      atual = {
        kd: [0.7, 0.7, 0.7],
      };

      materiais.set(nome, atual);
      continue;
    }

    if (comando === "kd" && atual) {
      const r = parseFloat(partes[1] ?? "0.7");
      const g = parseFloat(partes[2] ?? "0.7");
      const b = parseFloat(partes[3] ?? "0.7");

      atual.kd = [
        clamp01(isNaN(r) ? 0.7 : r),
        clamp01(isNaN(g) ? 0.7 : g),
        clamp01(isNaN(b) ? 0.7 : b),
      ];
    }
  }

  return materiais;
}

function clamp01(x) {
  return Math.min(1, Math.max(0, x));
}

/**
 * Cor difusa para nome de material; cinza se ausente.
 */
function obterKd(materiais, nomeMaterial) {
  const m = materiais.get(nomeMaterial);

  if (m && m.kd) {
    return m.kd;
  }

  return [0.65, 0.65, 0.65];
}
