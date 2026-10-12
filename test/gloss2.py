import pathlib
from playwright.sync_api import sync_playwright
root=pathlib.Path('/home/claude/genealogy-widgets')
exec(open(root/'test/run.py').read().split('shots = [')[0])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page()
    pg.route('**/grist-plugin-api.js', lambda r: r.fulfill(body=MOCK, content_type='application/javascript'))
    pg.goto((root/'glossary/index.html').as_uri()); pg.click('.tabs button[data-p="decode"]')
    pg.fill('#txt','1º de Julio, la Sra. Genoveva, Chih., 8bre, padrinos, viuda de García, hija natural, abuelos maternos'); pg.wait_for_timeout(100)
    print(pg.inner_text('#found')); b.close()
