/* Shared helpers for the Family History Research Grist widgets. */
(function () {
  const G = {};

  // Columnar {id:[...], col:[...]} -> [{id, col, ...}]
  G.rows = function (t) {
    if (!t || !t.id) return [];
    const keys = Object.keys(t);
    return t.id.map((_, i) => {
      const r = {};
      keys.forEach(k => (r[k] = t[k][i]));
      return r;
    });
  };

  // Fetch tables by name; missing tables come back as [].
  G.load = async function (names) {
    const out = {};
    await Promise.all(names.map(async n => {
      try { out[n] = G.rows(await grist.docApi.fetchTable(n)); }
      catch (e) { out[n] = []; }
    }));
    out.byId = {};
    names.forEach(n => {
      const m = new Map();
      out[n].forEach(r => m.set(r.id, r));
      out.byId[n] = m;
    });
    return out;
  };

  // RefList value -> array of ids
  G.list = v => (Array.isArray(v) ? (v[0] === 'L' ? v.slice(1) : v) : (v ? [v] : []));

  G.esc = s => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

  const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  G.toDate = v => {
    if (v == null || v === '') return null;
    if (v instanceof Date) return v;
    if (typeof v === 'number') return new Date(v * 1000);
    const d = new Date(v);
    return isNaN(d) ? null : d;
  };
  G.fmtDate = v => {
    const d = G.toDate(v);
    return d ? `${d.getUTCDate()} ${MON[d.getUTCMonth()]} ${d.getUTCFullYear()}` : '';
  };
  G.year = v => { const d = G.toDate(v); return d ? d.getUTCFullYear() + d.getUTCMonth() / 12 + (d.getUTCDate() - 1) / 365 : null; };

  // Family graph from the Relationships table.
  G.family = function (data, pid) {
    const rel = data.Relationships || [];
    const P = data.byId.People;
    const parents = [], children = [], spouses = [], siblingsDirect = [];
    rel.forEach(r => {
      const a = r.Person, b = r.Related;
      if (r.Relation === 'Parent of') {
        if (b === pid && P.has(a)) parents.push({ id: a, conf: r.Confidence });
        if (a === pid && P.has(b)) children.push({ id: b, conf: r.Confidence });
      } else if (r.Relation === 'Spouse of') {
        if (a === pid && P.has(b)) spouses.push({ id: b, conf: r.Confidence });
        if (b === pid && P.has(a)) spouses.push({ id: a, conf: r.Confidence });
      } else if (r.Relation === 'Sibling of') {
        if (a === pid && P.has(b)) siblingsDirect.push({ id: b, conf: r.Confidence, note: r.Notes });
        if (b === pid && P.has(a)) siblingsDirect.push({ id: a, conf: r.Confidence, note: r.Notes });
      }
    });
    const parentIds = new Set(parents.map(p => p.id));
    const sib = new Map();
    rel.forEach(r => {
      if (r.Relation === 'Parent of' && parentIds.has(r.Person) && r.Related !== pid && P.has(r.Related)) {
        if (!sib.has(r.Related)) sib.set(r.Related, { id: r.Related, conf: r.Confidence });
      }
    });
    const uniq = arr => { const s = new Set(); return arr.filter(x => !s.has(x.id) && s.add(x.id)); };
    return {
      parents: uniq(parents), children: uniq(children), spouses: uniq(spouses),
      siblings: [...sib.values()], related: uniq(siblingsDirect)
    };
  };

  G.lifespan = p => {
    const b = (p.Born || '').replace(/^(about|abt\.?|bapt\.?)\s*/i, '~');
    const d = (p.Died || '');
    if (!b && !d) return '';
    return `${b || '?'} – ${d || ''}`.trim();
  };

  G.statusClass = s => ({
    'Proven': 'st-proven', 'Probable': 'st-probable', 'Hypothesis': 'st-hyp', 'Not this family': 'st-not'
  }[s] || 'st-none');

  // Follow Grist's light/dark theme when it exposes its theme variables.
  G.followTheme = function () {
    const lum = c => {
      const m = c.match(/^#?([0-9a-f]{6})$/i) || [];
      if (m[1]) { const n = parseInt(m[1], 16); return (0.299 * (n >> 16) + 0.587 * ((n >> 8) & 255) + 0.114 * (n & 255)) / 255; }
      const r = c.match(/rgba?\((\d+)[,\s]+(\d+)[,\s]+(\d+)/);
      return r ? (0.299 * r[1] + 0.587 * r[2] + 0.114 * r[3]) / 255 : null;
    };
    const check = () => {
      const v = getComputedStyle(document.documentElement).getPropertyValue('--grist-theme-text').trim();
      const l = v ? lum(v) : null;
      if (l != null) document.documentElement.dataset.theme = l > 0.5 ? 'dark' : 'light';
    };
    [0, 300, 1000, 3000].forEach(t => setTimeout(check, t));
    if (grist.onThemeChange) { try { grist.onThemeChange(() => setTimeout(check, 50)); } catch (e) {} }
  };

  // Searchable person picker. onPick(id)
  G.personSearch = function (el, people, onPick) {
    el.innerHTML = '<input type="search" placeholder="Find a person…" autocomplete="off"><div class="results"></div>';
    const input = el.querySelector('input'), box = el.querySelector('.results');
    let hits = [], active = 0;
    const norm = s => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
    const draw = () => {
      box.innerHTML = hits.map((p, i) => `<button data-id="${p.id}" class="${i === active ? 'active' : ''}">${G.esc(p.Name)} <span class="faint">${G.esc(G.lifespan(p))}</span></button>`).join('');
      box.classList.toggle('open', hits.length > 0);
    };
    input.addEventListener('input', () => {
      const q = norm(input.value).split(/\s+/).filter(Boolean);
      hits = q.length ? people().filter(p => q.every(w => norm(p.Name).includes(w))).slice(0, 12) : [];
      active = 0; draw();
    });
    input.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { active = Math.min(active + 1, hits.length - 1); draw(); e.preventDefault(); }
      else if (e.key === 'ArrowUp') { active = Math.max(active - 1, 0); draw(); e.preventDefault(); }
      else if (e.key === 'Enter' && hits[active]) { pick(hits[active].id); }
      else if (e.key === 'Escape') { hits = []; draw(); }
    });
    box.addEventListener('mousedown', e => { const b = e.target.closest('button'); if (b) { e.preventDefault(); pick(+b.dataset.id); } });
    input.addEventListener('blur', () => setTimeout(() => { hits = []; draw(); }, 150));
    function pick(id) { input.value = ''; hits = []; draw(); onPick(id); }
  };

  window.FH = G;
})();
