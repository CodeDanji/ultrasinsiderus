from pathlib import Path
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright
import json

base = Path(__file__).resolve().parents[2]
report = base / 'outputs' / '린_기능평가_아이템_동료공유.html'
out = Path(__file__).resolve().parent

class Audit(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.links=[]; self.images=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        if tag=='a': self.links.append(a.get('href',''))
        if tag=='img': self.images.append(a)

text=report.read_text(encoding='utf-8')
a=Audit(); a.feed(text)
assert len(a.ids)==len(set(a.ids))
assert all(x[1:] in a.ids for x in a.links if x.startswith('#'))
assert len(a.images)==3 and all(x['src'].startswith('data:image/') and x.get('alt') for x in a.images)
assert all(x.startswith(('#','https://')) for x in a.links)
assert '\ufffd' not in text

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1280,'height':1000},device_scale_factor=1)
    errors=[]; requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
    page.goto(report.as_uri(),wait_until='load')
    page.evaluate('document.documentElement.style.scrollBehavior="auto"')
    assert page.evaluate('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)')
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(out/'brief-desktop.png'))
    page.locator('#references').scroll_into_view_if_needed()
    page.screenshot(path=str(out/'brief-references.png'))
    page.locator('#solution').scroll_into_view_if_needed()
    page.screenshot(path=str(out/'brief-solution.png'))
    assert page.locator('section').count()==7
    assert page.locator('.method').count()==8
    page.locator('#gaps').scroll_into_view_if_needed()
    page.screenshot(path=str(out/'brief-gaps.png'))
    page.locator('#assessment').scroll_into_view_if_needed()
    page.screenshot(path=str(out/'brief-evidence.png'))
    page.locator('#method-force summary').click()
    assert page.locator('#method-force .detail-inner').is_visible()
    page.evaluate('window.print=()=>window.__printed=true')
    page.get_by_role('button').click()
    assert page.evaluate('window.__printed===true')
    page.set_viewport_size({'width':390,'height':844})
    page.evaluate('scrollTo(0,0)')
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(out/'brief-mobile.png'))
    page.locator('.product').first.screenshot(path=str(out/'brief-mobile-reference.png'))
    page.locator('a[href="#solution"]').click()
    assert page.url.endswith('#solution')
    page.locator('.example').screenshot(path=str(out/'brief-mobile-example.png'))
    page.locator('#method-force').screenshot(path=str(out/'brief-mobile-method.png'))
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('.sources summary').click()
    assert page.locator('.sources').get_attribute('open') is not None
    page.emulate_media(media='print')
    assert not page.get_by_role('button').is_visible()
    assert not page.locator('nav').is_visible()
    page.pdf(path=str(out/'brief-print-check.pdf'),print_background=True)
    assert not errors
    assert not [r for r in requests if r.startswith(('http://','https://'))]
    chars=page.locator('body').inner_text()
    result=dict(sections=7,assessment_methods=8,embedded_official_images=3,images_loaded=True,
                desktop='passed',mobile_overflow=False,anchor_navigation='passed',
                print='passed',offline_http_requests=0,page_errors=errors,
                visible_text_chars=len(chars),file_bytes=report.stat().st_size)
    browser.close()
(out/'brief-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True))
