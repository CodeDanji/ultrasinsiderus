from pathlib import Path
from html.parser import HTMLParser
import json
import re
from playwright.sync_api import sync_playwright

base = Path(__file__).resolve().parents[2]
report = base / 'outputs' / '\uadfc\uace8\uaca9\uacc4_\ubd88\ud3b8\ud568_\uae30\ub2a5\ud3c9\uac00_\ubb38\uc81c\ud0d0\uc0c9_\ubcf4\uace0\uc11c.html'
out = Path(__file__).resolve().parent
print('Checking report:', report.name.encode('unicode_escape').decode(), flush=True)

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.anchors, self.links = [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if tag == 'a':
            href = a.get('href', '')
            self.links.append(href)
            if href.startswith('#'):
                self.anchors.append(href[1:])

audit = Audit()
content = report.read_text(encoding='utf-8')
audit.feed(content)
assert len(audit.ids) == len(set(audit.ids)), 'duplicate ids'
assert all(x in audit.ids for x in audit.anchors), 'broken internal anchors'
assert '\ufffd' not in content, 'replacement character'
research_path = out / 'expanded-research-data.json'
research = json.loads(research_path.read_text(encoding='utf-8')) if research_path.exists() else None
source_count = research['total_sources'] if research else 23
assert sum(x.startswith('s') and x[1:].isdigit() for x in audit.ids) == source_count
results = dict(source_count=source_count, internal_links=len(audit.anchors), external_links=sum(x.startswith('https://') for x in audit.links))
backup = out / 'report-before-readability.html'
if backup.exists():
    previous = backup.read_text(encoding='utf-8')
    source_pattern = r'<article class="source".*?</article>'
    previous_sources = re.findall(source_pattern, previous, re.S)
    current_sources = re.findall(source_pattern, content, re.S)
    assert previous_sources == current_sources[:len(previous_sources)], 'original source content changed'
    results['source_content_preserved'] = True
print('Static checks passed', flush=True)

with sync_playwright() as p:
    print('Launching browser', flush=True)
    browser = p.chromium.launch(headless=True, timeout=20000)
    page = browser.new_page(viewport=dict(width=1440, height=1100), device_scale_factor=1)
    page.set_default_timeout(10000)
    errors, requests = [], []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('request', lambda r: requests.append(r.url))
    page.goto(report.as_uri(), wait_until='load')
    page.screenshot(path=str(out / 'report-desktop.png'))
    assert page.locator('h1').count() == 1
    assert page.locator('.source').count() == source_count
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'desktop overflow'
    citation_target = 's04' if research else 's14'
    page.locator(f'a.cite[href="#{citation_target}"]').first.click()
    assert page.locator('#source-list').get_attribute('open') is not None, 'citation did not expand sources'
    assert page.locator(f'#{citation_target}').is_visible(), 'citation target hidden'
    page.locator('#source-list').evaluate('(node) => node.open = false')
    if research:
        assert page.locator('.method-card').count() == 13
        assert page.locator('.product-card').count() == 17
        for selector, count in [('.method-card',13),('.product-card',17)]:
            assert page.locator(selector+' .catalog-no').all_text_contents() == [f'{i:02}' for i in range(1,count+1)]
        page.locator('#method-10 summary').click()
        assert page.locator('#method-10 .spec').is_visible()
        page.locator('#method-10').evaluate('(node) => node.open = false')
        page.locator('#product-14 summary').click()
        assert page.locator('#product-14 .spec').is_visible()
        page.locator('#product-14').screenshot(path=str(out / 'report-product-detail.png'))
        page.locator('#product-14').evaluate('(node) => node.open = false')
        page.locator('#needs').scroll_into_view_if_needed()
        page.screenshot(path=str(out / 'report-product-catalog.png'))
        results.update(method_count=13,product_group_count=17,catalog_numbering='passed',catalog_expansion='passed')
    page.locator('#opportunities').scroll_into_view_if_needed()
    page.screenshot(path=str(out / 'report-opportunities.png'))
    page.evaluate('window.print = () => { window.__printCalled = true; }')
    page.get_by_role('button').click()
    assert page.evaluate('window.__printCalled === true')
    print('Desktop checks passed', flush=True)
    page.set_viewport_size(dict(width=390, height=844))
    page.evaluate('scrollTo(0,0)')
    page.screenshot(path=str(out / 'report-mobile.png'))
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'mobile overflow'
    page.locator('.mobile-nav summary').click()
    assert page.locator('.mobile-nav').get_attribute('open') is not None
    page.locator('.mobile-nav a[href="#clinical"]').click()
    assert page.url.endswith('#clinical'), 'mobile toc target'
    page.locator('#clinical').screenshot(path=str(out / 'report-mobile-reading.png'))
    if research:
        page.locator('#method-10 summary').click()
        page.locator('#method-10').screenshot(path=str(out / 'report-mobile-method.png'))
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'expanded mobile overflow'
        page.locator('#method-10').evaluate('(node) => node.open = false')
        page.locator('#product-14 summary').click()
        page.locator('#product-14').screenshot(path=str(out / 'report-mobile-product.png'))
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), 'expanded product mobile overflow'
        page.locator('#product-14').evaluate('(node) => node.open = false')
    page.evaluate('dispatchEvent(new Event("beforeprint"))')
    assert page.locator('details:not([open])').count() == 0, 'print omitted details'
    page.emulate_media(media='print')
    assert not page.locator('.sidebar').is_visible()
    assert not page.get_by_role('button').is_visible()
    page.evaluate('dispatchEvent(new Event("afterprint"))')
    assert page.locator('#source-list').get_attribute('open') is None, 'print state not restored'
    assert not errors, errors
    assert not [r for r in requests if r.startswith('http')], 'external dependency'
    results.update(page_errors=errors, offline_external_requests=0, desktop_overflow=False, mobile_overflow=False, mobile_navigation='passed', citation_expansion='passed', print_button='passed', print_styles='passed', print_detail_expansion='passed', print_state_restore='passed')
    browser.close()

(out / 'report-validation.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(results, ensure_ascii=True), flush=True)
