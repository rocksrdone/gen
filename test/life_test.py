"""Render the person widget's Life story section with sample Life_Details rows.

Run: python3 test/life_test.py  (screenshots saved as test/life-*.png)
"""
import json, pathlib
from playwright.sync_api import sync_playwright

root = pathlib.Path(__file__).resolve().parent.parent
fx = json.load(open(root / 'test/fixture.json'))
fx['People']['Born'][0] = '4 Aug 1869'

rows = [
    (1, 'Language & citizenship', "His Irish name was Liam Ó Ciarmhacáin; born in Garvey's Lane, Limerick City, and baptized at St. John's Cathedral.", '1869', 1869, 'Limerick City, Ireland', 15, 'From record', ''),
    (2, 'Residence & migration', "Came to America at about 7 (1876): Wilkes-Barre, Pa., where his father mined coal; Golden, Colo.; Leadville from 1879.", '1876-1900', 1876, 'Wilkes-Barre PA; Leadville CO', 15, 'From record', ''),
    (3, 'Military service', "At about 18 he joined Leadville's cavalry militia - 'B' Troop, First Cavalry, Colorado National Guard - and served in the Ute War of 1887.", '1887', 1887, 'Leadville / Rangely, Colorado', 15, 'From record', ''),
    (4, 'Occupation', "Official professional record (BoxRec): 18 bouts, 1895-1900 - 9 wins (7 by knockout), 3 losses, 4 draws.", '1895-1900', 1895, 'Aspen, Colorado', 20, 'From record', ''),
    (5, 'Anecdote', "His big Glenwood Springs fight, Sat. 12 Mar 1898: about 250 fans rode a Colorado Midland excursion train from Aspen to see him take on Aspen's John L. Taylor. In the 20th spectators rushed the ring shouting 'Fight!' - and Billy was declared the winner.", '12 Mar 1898', 1898, 'Glenwood Springs, Colorado', 16, 'From record', ''),
    (6, 'Appearance', "About 5 ft 6 in tall (168 cm); fought at around 124 lb. Ring alias 'Kid'.", '1890s', 1898, '', 19, 'From record', ''),
    (7, 'Anecdote', "Song-and-dance man: 'First Appearance of Billy Irwin and Jimmy Joyce, two Irish Aristocrats.'", '16 Jun 1904', 1904, "Elks' opera house, Leadville", 12, 'From record', 'Confirmed by user.'),
    (8, 'Occupation', "Chief of the Leadville Fire Department in 1907, leading a paid force of eight.", '1907 (reported 1 Jan 1908)', 1907, 'Leadville, Colorado', 5, 'From record', ''),
    (9, 'Occupation', "Career path: fire chief (1907) → Deputy Clerk of Lake County (1910).", '1907–1910', 1907, 'Leadville, Colorado', 5, 'Inferred', 'Combines two records.'),
    (10, 'Anecdote', "Wrote verse: a little poem 'hastily composed by Billy Irwin' - 'Don't stay at home on the Fourth, but take your best girl to the track; / If you go broke on the races, it's not very far to walk back.'", '27 Jun 1908', 1908, 'Leadville, Colorado', 10, 'From record', ''),
    (11, 'Historical event', "Grand marshal of Leadville's Fourth of July parade, 4 Jul 1908.", '4 Jul 1908', 1908, 'Harrison Avenue, Leadville', 11, 'From record', ''),
    (12, 'Community & social', "President of Leadville Aerie No. 91, Fraternal Order of Eagles, in 1908.", '1908', 1908, 'Leadville, Colorado', 10, 'From record', ''),
    (13, 'Health & cause of death', "Fell ill with pneumonia in late October 1910 and fought it for nearly two weeks before dying at home on 5 Nov.", 'late Oct-5 Nov 1910', 1910, '124 West Third St., Leadville', 19, 'From record', ''),
    (14, 'Property & wealth', "Widow probably received fraternal death benefits.", '1910', 1910, 'Leadville', 7, 'Historical context', ''),
    (15, 'Community & social', "Inducted in the first class (2004) of the Leadville-Lake County Sports Hall of Fame.", '2004', 2004, 'Leadville, Colorado', 14, 'From record', ''),
    (16, 'Family life', "Kept a scrapbook of his boxing career.", '1895-1910; book c. 2019', None, '', 14, 'From record', ''),
]
cols = ['id', 'Category', 'Detail', 'When', 'Year', 'Place', 'Source', 'Confidence', 'Notes']
fx['Life_Details'] = {c: [r[i] for r in rows] for i, c in enumerate(cols)}
fx['Life_Details']['Person'] = [1] * len(rows)

MOCK = """
window.__FX = %s;
window.grist = { ready(){}, onThemeChange(){}, onRecord(cb){ setTimeout(()=>cb({id:1}),30); }, onRecords(){},
  setCursorPos: async()=>{}, getAccessToken: async()=>({token:'t', baseUrl:'data:'}),
  docApi: { fetchTable: async t => { if(!__FX[t]) throw new Error('no '+t); return JSON.parse(JSON.stringify(__FX[t])); } } };
""" % json.dumps(fx, ensure_ascii=False)

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, (W, H), scheme, click in [('all', (1100, 1700), 'light', None), ('stories', (1100, 1000), 'dark', '[data-lsf="Anecdote"]'),
                                        ('mobile', (400, 2200), 'light', None)]:
        ctx = b.new_context(viewport={'width': W, 'height': H}, color_scheme=scheme)
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.route('**/grist-plugin-api.js', lambda r: r.fulfill(body=MOCK, content_type='application/javascript'))
        pg.goto((root / 'person/index.html').as_uri())
        pg.wait_for_timeout(600)
        if click:
            pg.click(click)
            pg.wait_for_timeout(200)
        out = root / 'test' / f'life-{name}.png'
        pg.screenshot(path=str(out), full_page=False)
        print(out.name, 'errors:', errs)
        ctx.close()
    b.close()
