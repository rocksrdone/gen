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
    applyUserActions: async (acts)=>{ const ids=[]; for(const a of acts){ if(a[0]==='AddRecord'){ const t=__FX[a[1]]; const id=Math.max(0,...t.id)+1; for(const k of Object.keys(t)){ t[k].push(k==='id'?id:(a[3][k]===undefined?null:a[3][k])); } ids.push(id);} } return {retValues: ids}; }
  }
};
""" % json.dumps(fx, ensure_ascii=False)
shots = [
  ('person', 1, (1100, 1300), 'light'), ('person', 12, (1100, 1100), 'dark'), ('person', 1, (420, 1600), 'light'),
  ('tree', 2, (1300, 800), 'light'), ('tree', 1, (1300, 800), 'dark'),
  ('dna', 1, (1100, 1000), 'light'),
  ('sources', 1, (1200, 1000), 'light'), ('sources', 1, (1200, 1000), 'dark'),
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
