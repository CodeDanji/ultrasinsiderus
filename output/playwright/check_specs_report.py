from pathlib import Path
from html.parser import HTMLParser
from playwright.sync_api import sync_playwright
import json

base=Path(__file__).resolve().parents[2]
report=next(p for p in (base/'outputs').glob('B2B2C_*.html'))
out=Path(__file__).resolve().parent
class Audit(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[];self.anchors=[];self.external=[];self.local=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':
            href=a.get('href','')
            if href.startswith('#'):self.anchors.append(href[1:])
            elif href.startswith('https://'):self.external.append(href)
            elif href:self.local.append(href)

text=report.read_text(encoding='utf-8'); audit=Audit();audit.feed(text)
assert len(audit.ids)==len(set(audit.ids))
assert all(anchor in audit.ids for anchor in audit.anchors)
assert all((report.parent/p).exists() for p in audit.local)
assert '\ufffd' not in text
assert '0.25~0.5인월' in text and '0.5~0.8인월' in text
assert sum(x.startswith('s') and x[1:].isdigit() for x in audit.ids)==21
assert all(x in audit.ids for x in ['kit','station','hospital','feedback','service','outputs','budget'])
budget=json.loads((out/'specs-budget.json').read_text(encoding='utf-8'))
for x in budget['scenarios'].values():
    assert all(abs(x['with_reserve'][i]-x['direct'][i]*1.2)<0.001 for i in (0,1))
    assert all(abs(x['direct'][i]-budget['common_direct'][i]-x['incremental'][i])<0.001 for i in (0,1))
assert abs((210-180)/210*100-14.285714)<0.00001
result=dict(candidates=5,sources=21,internal_links=len(audit.anchors),local_research_link='passed',budget_arithmetic='passed')
print('Static and cost checks passed',flush=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,timeout=20000)
    page=browser.new_page(viewport=dict(width=1440,height=1100),device_scale_factor=1)
    page.set_default_timeout(10000)
    errors=[];requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
    page.goto(report.as_uri(),wait_until='load')
    assert page.locator('h1').count()==1
    assert page.locator('.source').count()==21
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.screenshot(path=str(out/'specs-desktop.png'))
    page.locator('#station').scroll_into_view_if_needed()
    page.screenshot(path=str(out/'specs-station.png'))
    page.locator('#common a.cite[href="#s14"]').click()
    assert page.locator('#source-list').get_attribute('open') is not None
    assert page.locator('#s14').is_visible()
    page.locator('#source-list').evaluate('(node)=>node.open=false')
    page.evaluate('window.print=()=>{window.__printCalled=true}')
    page.get_by_role('button').click()
    assert page.evaluate('window.__printCalled===true')
    page.set_viewport_size(dict(width=390,height=844))
    page.evaluate('scrollTo(0,0)')
    page.screenshot(path=str(out/'specs-mobile.png'))
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('.mobile-nav summary').click()
    page.locator('.mobile-nav a[href="#outputs"]').click()
    assert page.url.endswith('#outputs')
    page.locator('.sample-report').first.screenshot(path=str(out/'specs-mobile-result.png'))
    page.evaluate('dispatchEvent(new Event("beforeprint"))')
    assert page.locator('details:not([open])').count()==0
    page.emulate_media(media='print')
    assert not page.locator('.sidebar').is_visible()
    assert not page.get_by_role('button').is_visible()
    page.evaluate('dispatchEvent(new Event("afterprint"))')
    assert page.locator('#source-list').get_attribute('open') is None
    assert not errors,errors
    assert not [r for r in requests if r.startswith('http')]
    browser.close()
    result.update(desktop='passed',mobile_overflow=False,mobile_navigation='passed',citation_expansion='passed',print_button='passed',print_expansion='passed',print_restore='passed',offline_requests=0,page_errors=[])
(out/'specs-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True),flush=True)
