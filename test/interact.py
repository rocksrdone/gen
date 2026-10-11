import json, pathlib
from playwright.sync_api import sync_playwright
root = pathlib.Path('/home/claude/genealogy-widgets')
exec(open(root/'test/run.py').read().split('shots = [')[0])  # defines MOCK, fx
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width':1200,'height':1000})
    errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.route('**/grist-plugin-api.js', lambda r: r.fulfill(body=MOCK.replace('window.__SEL || 1','1'), content_type='application/javascript'))
    pg.goto((root/'sources/index.html').as_uri()); pg.wait_for_timeout(600)
    # add evidence
    pg.fill('#evPerson input', 'genoveva'); pg.wait_for_timeout(100); pg.keyboard.press('Enter')
    pg.fill('#evAge', '30'); pg.fill('#evAs', 'Genobeba, 30'); pg.click('#evAdd'); pg.wait_for_timeout(500)
    print('evidence rows:', pg.evaluate('__FX.Evidence.id.length'), 'last person:', pg.evaluate('__FX.Evidence.Person.at(-1)'), 'age', pg.evaluate('__FX.Evidence.Age.at(-1)'))
    # extraction toggle
    pg.click('#exSeg button[data-v="Partly extracted"]'); pg.wait_for_timeout(400)
    print('extraction:', pg.evaluate('__FX.Sources.Extraction[0]'))
    # new source
    pg.click('#newBtn'); pg.wait_for_timeout(200)
    print('next code:', pg.input_value('#sCode'))
    pg.fill('#sTitle','Test death record'); pg.fill('#sRec','https://www.ancestry.com/x?pId=1&_gl=abc'); pg.click('#sSave'); pg.wait_for_timeout(500)
    print('new src:', pg.evaluate('[__FX.Sources.Code.at(-1), __FX.Sources.Record_URL.at(-1), __FX.Sources.Extraction.at(-1)]'))
    # filter
    pg.select_option('#fEx','__img'); pg.wait_for_timeout(100); print('no-image count:', pg.locator('.src').count())
    print('errors', errs); b.close()
