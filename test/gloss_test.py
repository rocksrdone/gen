import pathlib
from playwright.sync_api import sync_playwright
root = pathlib.Path('/home/claude/genealogy-widgets')
exec(open(root/'test/run.py').read().split('shots = [')[0])
TXT = ("En San Buenaventura, Dto. Galeana, Chih., siendo las diez horas del día 1º de Julio de mil novecientos treinta, ante mí Porfirio Vega, "
 "Juez del Registro Civil, compareció el C. Primo García, originario de San Lorenzo y vecino de este lugar, de cincuenta y dos años de edad, "
 "casado civil y religiosamente, labrador, presentó una niña viva, hija legítima del mismo exponente y de su esposa la Sra. Genoveva Estrada, "
 "de cuarenta y cuatro años. Es nieta por línea paterna de los finados Juan García y Lozallo. Fueron testigos… Doy fe. Casé y velé in facie Ecclesiae; célibe, edad dieciocho años; diez y ocho; 7bre")
with sync_playwright() as p:
    b = p.chromium.launch()
    for scheme in ['light','dark']:
        pg = b.new_page(viewport={'width':1100,'height':1300}, color_scheme=scheme)
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('**/grist-plugin-api.js', lambda r: r.fulfill(body=MOCK, content_type='application/javascript'))
        pg.goto((root/'glossary/index.html').as_uri()); pg.wait_for_timeout(300)
        pg.fill('#q','finado'); pg.wait_for_timeout(100); print('search finado:', pg.inner_text('#count'))
        pg.fill('#q','widow'); print('search widow:', pg.inner_text('#count'))
        pg.screenshot(path=str(root/f'test/gloss-look-{scheme}.png'))
        pg.click('.tabs button[data-p="decode"]'); pg.fill('#txt', TXT); pg.wait_for_timeout(200)
        print('nums:', [m.inner_text() for m in pg.query_selector_all('mark.num')])
        print('terms:', len(pg.query_selector_all('#found tr')))
        pg.screenshot(path=str(root/f'test/gloss-decode-{scheme}.png'), full_page=True)
        pg.click('.tabs button[data-p="nums"]')
        for w in ['cuarenta y cuatro','mil novecientos treinta','veinte y seis','mil ochocientos setenta y tres','dieciocho']:
            pg.fill('#numIn', w); print(w,'=',pg.inner_text('#numOut'))
        print('errors', errs)
    b.close()
