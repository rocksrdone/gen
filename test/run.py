import json, sys, pathlib
from playwright.sync_api import sync_playwright
root = pathlib.Path(__file__).resolve().parent.parent
fx = json.load(open(root/'test/fixture.json'))
MOCK = """
window.__FX = %s; window.__errors = [];
window.grist = {
  ready(){}, onThemeChange(){},
  onRecord(cb){ setTimeout(()=>cb({id: window.__SEL || 1}), 30); },
  onRecords(cb){},
  setCursorPos: async (p)=>{ window.__cursor = p; },
  getAccessToken: async ()=>({token:'t', baseUrl:'data:'}),
  docApi: {
    fetchTable: async (t)=>{ if(!__FX[t]) throw new Error('no table '+t); return JSON.parse(JSON.stringify(__FX[t])); },
    applyUserActions: async (acts)=>{ window.__acts=(window.__acts||[]).concat(acts); const rv=[]; const add=(tn,rec)=>{ const t=__FX[tn]||(__FX[tn]={id:[]}); const id=Math.max(0,...t.id)+1; const n=t.id.length; Object.keys(rec).forEach(k=>{ if(!t[k]) t[k]=Array(n).fill(null); }); for(const k of Object.keys(t)){ t[k].push(k==='id'?id:(rec[k]===undefined?null:rec[k])); } return id; };
      for(const a of acts){ if(a[0]==='AddRecord'){ rv.push(add(a[1],a[3])); } else if(a[0]==='BulkAddRecord'){ const ks=Object.keys(a[3]); rv.push(a[2].map((_,i)=>{const r={};ks.forEach(k=>r[k]=a[3][k][i]);return add(a[1],r);})); } else if(a[0]==='UpdateRecord'){ const t=__FX[a[1]]; const i=t.id.indexOf(a[2]); Object.keys(a[3]).forEach(k=>{ if(!t[k]) t[k]=Array(t.id.length).fill(null); t[k][i]=a[3][k]; }); rv.push(null);} else if(a[0]==='BulkUpdateRecord'){ const t=__FX[a[1]]; a[2].forEach((id,j)=>{const i=t.id.indexOf(id); Object.keys(a[3]).forEach(k=>{ if(!t[k]) t[k]=Array(t.id.length).fill(null); t[k][i]=a[3][k][j];});}); rv.push(null);} } return {retValues: rv}; }
  }
};
""" % json.dumps(fx, ensure_ascii=False)
shots = [
  ('person', 1, (1100, 1300), 'light'), ('person', 12, (1100, 1100), 'dark'), ('person', 1, (420, 1600), 'light'),
  ('tree', 2, (1300, 800), 'light'), ('tree', 1, (1300, 800), 'dark'),
  ('dna', 1, (1100, 1000), 'light'),
  ('sources', 1, (1200, 1000), 'light'), ('sources', 1, (1200, 1000), 'dark'), ('entry', 1, (1200, 1400), 'light'),
]
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, sel, (W, H), scheme in shots:
        ctx = b.new_context(viewport={'width': W, 'height': H}, color_scheme=scheme)
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
        pg.route('**/grist-plugin-api.js', lambda r: r.fulfill(body=MOCK.replace('window.__SEL || 1', str(sel)), content_type='application/javascript'))
        pg.goto((root/w/'index.html').as_uri())
        pg.wait_for_timeout(700)
        out = root/'test'/f'{w}-{sel}-{W}-{scheme}.png'
        pg.screenshot(path=str(out), full_page=True)
        print(out.name, 'errors:', errs)
        ctx.close()
    b.close()
