from pathlib import Path
from urllib.request import Request, urlopen
from html import escape
import base64
import json

base = Path(__file__).resolve().parents[2]
out = base / 'outputs' / '린_기능평가_아이템_동료공유.html'
products = [
    dict(name='KINVENT K-Push', tag='휴대형 힘 측정',
         url='https://kinvent.com/kinvent-product/hand-held-dynamometer-k-push/',
         image='https://kinvent.com/wp-content/uploads/2025/04/k-push-usage-arm.webp',
         credit='KINVENT',
         desc='몸에 센서를 대고 밀게 해 힘을 측정한다. 앱에서 결과를 기록하고 피드백한다.',
         implication='휴대 키트·결과 기록과 겹친다.'),
    dict(name='VALD ForceFrame', tag='프레임에 고정한 힘 측정',
         url='https://valdhealth.com/products/forceframe',
         image='https://images.ctfassets.net/98s79sqwuajy/6FQV5bxJ92tzdWEjhPCjrf/d701c3be0f8e7bcac5664ef8ad6e18eb/header-image.png',
         credit='VALD Health',
         desc='패드와 센서를 프레임에 고정해 정해진 자세의 힘을 측정하고 재평가한다.',
         implication='고정 스테이션과 직접 겹친다.'),
    dict(name='VALD HumanTrak', tag='카메라 기반 움직임 평가',
         url='https://valdhealth.com/products/humantrak',
         image='https://images.ctfassets.net/98s79sqwuajy/1GBbUhkSFx0C2L5yXz0oWi/7a7958d71a56a81ef7834f18ae978957/humantrak-hero.png',
         credit='VALD Health',
         desc='카메라로 동작을 기록해 관절 움직임 등을 분석하고 리포트를 제공한다.',
         implication='동작 평가·결과 설명과 겹친다.'),
]
cards = []
manifest = []
for p in products:
    req = Request(p['image'], headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=45) as res:
        data = res.read()
        mime = res.headers.get_content_type()
    assert mime.startswith('image/') and len(data) > 1000
    uri = 'data:' + mime + ';base64,' + base64.b64encode(data).decode()
    cards.append(f'''<article class="product">
      <a class="photo" href="{p['url']}" target="_blank" rel="noopener"><img src="{uri}" alt="{escape(p['name'])} 공식 제품·사용 사진"></a>
      <div class="product-body"><span class="eyebrow">{p['tag']}</span><h3>{p['name']}</h3>
      <p>{p['desc']}</p><p class="implication">{p['implication']}</p>
      <a class="official" href="{p['url']}" target="_blank" rel="noopener">공식 사이트 ↗<span>{p['url']}</span></a>
      <a class="credit" href="{p['image']}" target="_blank" rel="noopener">사진: {p['credit']} 공식 홈페이지</a></div>
    </article>''')
    manifest.append(dict(name=p['name'], url=p['url'], image=p['image'], mime=mime, bytes=len(data)))

html = '''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="린 프로젝트 근골격 기능평가 아이템: 문제, 기존 제품, 고객 가치, 측정·해석 과정과 검증 계획">
<title>린 프로젝트 | 기능평가 아이템 공유</title>
<style>
:root{--ink:#202d2a;--muted:#64726b;--green:#24614b;--line:#dde5df;--soft:#f0f5f1}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:20px}body{margin:0;background:#fff;color:var(--ink);font:16px/1.85 "Malgun Gothic","Apple SD Gothic Neo",sans-serif;word-break:keep-all;overflow-wrap:anywhere}main{max-width:1040px;margin:auto;padding:44px 40px 30px}a{color:var(--green);text-underline-offset:4px}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #79a68d;outline-offset:4px}.meta,.eyebrow{font-size:12px;color:var(--green);font-weight:700}.topline{display:flex;justify-content:space-between;gap:16px;align-items:center}button{font:inherit;font-size:12px;border:1px solid var(--line);border-radius:5px;padding:7px 12px;color:var(--green);background:#fff;cursor:pointer}h1{font-size:35px;line-height:1.5;letter-spacing:-.04em;margin:23px 0 16px}h2{font-size:24px;line-height:1.55;letter-spacing:-.025em;margin:0 0 19px}h3{font-size:18px;line-height:1.6;margin:7px 0 10px}p{margin:0 0 15px}.lead{font-size:19px;max-width:820px}.conclusion{background:var(--soft);border-left:3px solid var(--green);padding:20px 24px;margin:23px 0}.conclusion p{margin:7px 0 0}nav{display:flex;flex-wrap:wrap;gap:8px 22px;border-bottom:1px solid var(--line);padding:4px 0 23px;margin-bottom:32px}nav a{font-size:13px;color:var(--muted);text-decoration:none}section{padding:12px 0 29px;margin:0 0 30px;border-bottom:1px solid var(--line);scroll-margin-top:22px}.section-no{font-size:12px;color:var(--green);display:block;margin-bottom:8px;font-weight:700}.question{font-size:18px;border-left:3px solid #b1c8b8;padding-left:19px;margin:20px 0}.small{font-size:13px;color:var(--muted);line-height:1.8}.products{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:23px 0}.product{border:1px solid var(--line);border-radius:8px;overflow:hidden}.photo{display:flex;align-items:center;justify-content:center;height:190px;background:#f4f6f5;padding:9px}.photo img{display:block;width:100%;height:100%;object-fit:contain}.product-body{padding:17px}.product p{font-size:14px;line-height:1.8}.product h3{font-size:19px}.product .implication{font-weight:700;color:var(--green)}.official{font-size:13px;text-decoration:none}.official span{display:block;font-size:11px;word-break:break-all;line-height:1.6;margin-top:5px}.credit{display:block;font-size:10px;color:var(--muted);margin-top:12px}.takeaway{padding:17px 20px;background:var(--soft);border-radius:5px}.takeaway p{margin:0}.customers{width:100%;border-collapse:collapse;font-size:15px}.customers th,.customers td{text-align:left;vertical-align:top;border-bottom:1px solid var(--line);padding:15px 12px}.customers th{font-size:12px;color:var(--muted);background:#f6f8f6}.customers td:first-child{font-weight:700;width:19%}.customers td:nth-child(2){width:34%}.table-scroll{overflow:auto;margin:22px 0}.flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin:23px 0}.flow article{border-top:3px solid #83a993;background:#f6f8f6;padding:17px 16px}.flow .step{font-size:12px;color:var(--green);font-weight:700}.flow h3{font-size:17px}.flow p{font-size:14px;margin:0}.example{border:1px solid #bcd1c3;border-radius:6px;padding:21px 24px;margin:24px 0}.example .numbers{font-size:21px;letter-spacing:-.02em;margin:9px 0}.example p:last-child{margin:0}.candidates{font-size:14px;color:var(--muted);margin-top:20px}.plan{list-style:none;padding:0;margin:22px 0;counter-reset:plan}.plan li{position:relative;padding:0 0 18px 39px;margin-bottom:15px;border-bottom:1px solid #edf0ed;counter-increment:plan}.plan li:last-child{border-bottom:0;margin-bottom:0}.plan li:before{content:counter(plan);position:absolute;left:0;top:1px;background:var(--soft);color:var(--green);width:25px;height:25px;border-radius:50%;text-align:center;font-size:12px;line-height:25px;font-weight:700}.plan b{display:block;margin-bottom:5px}.plan p{font-size:15px;margin:0}.checks{background:var(--soft);padding:19px 23px;border-radius:5px}.checks p{margin:6px 0 0;font-size:15px}.last{font-size:18px;font-weight:700;margin:23px 0 0}.sources{margin-top:21px;font-size:13px}summary{cursor:pointer;font-weight:700;color:var(--green);padding:8px 0}.sources ul{padding-left:20px}.sources li{margin:10px 0}footer{font-size:12px;color:var(--muted);line-height:1.85}footer p{margin:0}b,strong{font-weight:700}
@media(max-width:720px){main{padding:25px 21px}h1{font-size:28px}h2{font-size:22px}.lead{font-size:17px}.products{grid-template-columns:1fr}.photo{height:220px}.product-body{padding:19px}.product p{font-size:15px}.flow{grid-template-columns:1fr 1fr}.customers{min-width:570px}.conclusion{padding:17px 19px}.example{padding:18px}.example .numbers{font-size:19px}.question{font-size:17px}.topline{align-items:flex-start}.meta{font-size:11px}section{margin-bottom:23px}.official span{font-size:12px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{@page{size:A4;margin:15mm}body{font-size:10pt;line-height:1.7}main{max-width:none;padding:0}button,nav{display:none}h1{font-size:23pt;margin:15px 0}h2{font-size:16pt}h3{font-size:12pt}.lead{font-size:12pt}section{padding:8px 0 17px;margin-bottom:18px}.conclusion{padding:13px 17px}.products{gap:10px}.photo{height:125px}.product-body{padding:12px}.product h3{font-size:12pt}.product p,.flow p,.plan p,.checks p,.customers{font-size:9pt}.product .eyebrow{font-size:8pt}.official{font-size:8pt}.official span,.credit{font-size:7pt}.customers{min-width:0}.customers th,.customers td{padding:10px 8px}.flow{gap:10px}.flow article{padding:12px}.flow h3{font-size:10.5pt}.example .numbers{font-size:14pt}.small,.sources{font-size:8pt}.question,.last{font-size:11pt}.product,.conclusion,.example,.flow article,.checks,.plan li,tr{break-inside:avoid}h2,h3{break-after:avoid}.table-scroll{overflow:visible}footer{font-size:8pt}}
</style></head><body><main>
<header><div class="topline"><span class="meta">인사이더스 · 린 프로젝트 / 아이템 검토 메모 · 2026.10.26</span><button type="button" onclick="window.print()">인쇄 / PDF</button></div>
<h1>몸이 불편한데, 무엇부터 관리해야 할까?</h1>
<p class="lead">근력·가동범위·동작을 측정하고, 결과를 이해한 뒤 관리와 재평가까지 이어주는 서비스를 검토하고 있다. 개인에게 기기를 판매하기보다 <strong>헬스장·필라테스·병원·기업을 통해 제공하는 방식</strong>을 우선 보고 있다.</p>
<div class="conclusion"><span class="eyebrow">현재 결론</span><p><strong>기능을 측정하는 장비는 이미 있다.</strong> 먼저 기존 장비로 기관의 평가 과정을 운영해보고, 결과가 실제 운동·관리 결정에 쓰이는지 확인하려 한다. 독자 기기 개발은 그 과정에서 반복되는 문제가 드러난 뒤 판단한다.</p></div></header>
<nav aria-label="목차"><a href="#problem">문제 인식</a><a href="#references">기존 제품</a><a href="#customers">고객과 가치</a><a href="#solution">솔루션</a><a href="#plan">진행 방향</a></nav>

<section id="problem"><span class="section-no">01 · 문제 인식</span><h2>불편함은 있는데, 관리의 기준이 없다</h2>
<p>고관절이 뻐근하거나 어깨가 계속 결려도 이유를 알기 어렵다. 진료에서 구조적 이상을 확인했거나 영상검사에서 뚜렷한 설명을 얻지 못한 뒤에도, <strong>“지금 어떤 기능이 부족하고 무엇부터 관리해야 하나?”</strong>라는 질문은 남을 수 있다.</p>
<p class="question">“고관절이나 몸통의 기능이 문제라는 내 추측이 맞을까?<br>얼마나 제한돼 있고, 운동한 뒤 실제로 달라졌을까?”</p>
<p>여기서 출발한 아이디어다. 기능평가 자체를 새로 발명하기보다, 필요한 평가를 받고 결과를 이해하며 다음 행동으로 옮기는 과정에 어떤 공백이 있는지 찾으려 한다.</p>
</section>

<section id="references"><span class="section-no">02 · 관련 레퍼런스</span><h2>이미 무엇이 나와 있나?</h2>
<p>휴대형 힘 센서, 고정식 측정 장비, 카메라 기반 동작 평가가 제품화돼 있다. 사진을 누르면 공식 제품 페이지로 이동한다.</p>
<div class="products">__CARDS__</div>
<div class="takeaway"><p><strong>측정·기록·리포트만으로는 차별화하기 어렵다.</strong> 국내 기관이 이 과정을 운영하고 결과를 운동·관리와 연결할 때 남는 불편이 있는지 확인해야 한다.</p></div>
</section>

<section id="customers"><span class="section-no">03 · 예상 고객과 제공 가치</span><h2>누가 비용을 내고, 무엇이 좋아지는가?</h2>
<p>기관이 구매·계약하고 회원·환자·직원이 이용하는 구조다. 아래 가치는 아직 검증할 가설이며, 첫 고객군은 정하지 않았다.</p>
<div class="table-scroll" role="region" aria-label="예상 고객별 제공 가치" tabindex="0"><table class="customers"><thead><tr><th>예상 고객</th><th>기관이 얻을 가치</th><th>이용자가 얻을 가치</th></tr></thead><tbody>
<tr><td>헬스장·필라테스</td><td>평가 기록과 운동 선택 근거를 설명해 서비스 신뢰를 높인다.</td><td>왜 이 운동을 하는지, 전후에 무엇이 달라졌는지 이해한다.</td></tr>
<tr><td>병원</td><td>문진·측정 기록·결과 정리·추적 업무를 보완한다.</td><td>평가 결과와 관리 계획을 이해하고 후속 평가로 이어간다.</td></tr>
<tr><td>기업 복지</td><td>직원이 실제로 활용하는 건강관리 프로그램을 제공한다.</td><td>자신의 기능 상태를 이해하고 관리할 기회를 얻는다.</td></tr>
</tbody></table></div>
<p class="small">장비 보유가 트레이너의 전문성을 보장하지는 않는다. 병원에는 검사 담당자와 의사의 판단이 필요하다. 기업용 서비스는 개인 결과와 기관용 집계를 분리한다.</p>
</section>

<section id="solution"><span class="section-no">04 · 솔루션</span><h2>측정값을 어떻게 쓸모 있는 정보로 바꿀까?</h2>
<p>첫 검증은 <strong>휴대용 평가 키트와 평가·설명·재평가 절차</strong>를 묶어 시작할 수 있다. 태블릿, 힘 센서, 각도 측정 도구와 고정 벨트를 활용한다. 자세를 잡고 측정할 담당자가 함께 운영한다.</p>
<div class="flow">
<article><span class="step">1 · 질문 정하기</span><h3>무엇이 불편한가</h3><p>증상·생활 제한·목표를 확인하고 필요한 검사를 정한다. 진료 필요성이 의심되면 의료진 평가로 연결한다.</p></article>
<article><span class="step">2 · 측정하기</span><h3>힘·각도·동작</h3><p>같은 자세와 고정 조건에서 반복 측정한다. 통증이나 세팅 실패도 함께 기록한다.</p></article>
<article><span class="step">3 · 가공하기</span><h3>유효한 값과 차이</h3><p>실패한 시도를 구분하고, 정한 규칙으로 좌우·전후 차이를 계산해 요약한다.</p></article>
<article><span class="step">4 · 판단·관리</span><h3>다음 행동 정하기</h3><p>전문가가 증상·다른 검사와 함께 검토해 관리 목표·운동·추가 평가를 결정한다.</p></article>
</div>
<div class="example"><span class="eyebrow">가상 예시 · 고관절을 옆으로 벌리는 힘</span>
<p>고정된 패드를 다리로 밀면 센서가 힘을 기록한다. 프로그램은 같은 조건의 유효 시도를 모아 결과를 계산한다.</p>
<p class="numbers"><strong>오른쪽 180N / 왼쪽 210N → 좌우 차이 14.3%</strong></p>
<p>알 수 있는 것은 <strong>“오늘 이 과제에서 오른쪽 출력이 더 낮았다”</strong>는 사실이다. 통증 때문에 멈췄는지, 다른 동작에도 제한이 있는지 함께 봐야 관리 방향을 정할 수 있다. 이 수치만으로 특정 근육을 통증의 원인으로 지목하지 않는다.</p>
</div>
<p>이용자에게는 <strong>측정 결과, 관리할 기능, 운동을 고른 이유, 다음 평가 시점</strong>을 한 장으로 전달한다. 이후 같은 조건으로 다시 측정하고 불편감·생활 동작의 변화도 함께 확인한다.</p>
<p class="candidates">확장 후보: 세팅이 어렵다면 <b>고정 스테이션</b>, 기록·검토가 병목이면 <b>병원 업무 보조</b>, 운동을 배우기 어렵다면 <b>움직임·근전도 피드백</b>. 장비와 인력을 묶은 <b>정기 평가 서비스</b>로 제공할 수도 있다.</p>
</section>

<section id="plan"><span class="section-no">05 · 린 스타트업 진행 방향</span><h2>기기를 만들기 전에, 평가 과정을 팔아본다</h2>
<ol class="plan">
<li><b>기관과 이용자의 현재 방식을 확인한다</b><p>후보 고객군별 기관 몇 곳을 만나 기존 평가, 결과 설명, 재평가 방식과 비용을 누가 부담하는지 확인한다. 가장 반복되고 해결할 가치가 큰 문제 하나를 고른다.</p></li>
<li><b>한 기관·한 대상군·한 평가 묶음으로 운영한다</b><p>기존 장비와 수기 기록으로 소규모 서비스를 제공한다. 예를 들어 설문 + 힘 1종 + 가동범위 1종 + 생활 동작 1종으로 시작할 수 있다. 실제 항목은 담당 전문가와 정한다.</p></li>
<li><b>결과가 결정을 바꾸는지 본다</b><p>평가 전후에 운동 종류·부하·추가 평가 중 무엇이 달라졌는지 기록한다. 직원의 총업무시간, 세팅 실패, 이용자의 결과 이해와 후속 행동도 확인한다.</p></li>
<li><b>유료 재도입을 확인하고 개발 범위를 정한다</b><p>기관이 다시 비용을 낼 이유가 있는지 본다. 반복되는 문제가 세팅인지, 해석인지, 기록인지에 따라 필요한 부분부터 개발한다.</p></li>
</ol>
<div class="checks"><strong>첫 실험에서 답할 세 가지</strong><p>① 기존 방식보다 어떤 결정이나 업무가 나아졌나?<br>② 이용자가 결과를 이해하고 관리에 활용했나?<br>③ 기관이 비용을 내고 다시 도입하려 하나?</p></div>
<p class="last">먼저 평가 결과가 실제 관리 결정에 도움이 되는지,<br>기관이 비용을 내고 다시 이용할지 확인한다.</p>
<details class="sources"><summary>조사 근거와 해석 범위</summary><ul>
<li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC11329127/" target="_blank" rel="noopener">고관절 힘 측정의 타당도·반복성 연구, 2024</a> — 특정 장비·고정·절차의 결과다. 새 제품의 정상 기준으로 그대로 쓰지 않는다.</li>
<li><a href="https://pubmed.ncbi.nlm.nih.gov/32569878/" target="_blank" rel="noopener">표면근전도 진폭 정규화 방법론 합의, 2020</a> — 전기활동의 크기와 근력을 같은 값으로 해석하지 않는다.</li>
</ul><p>제품 설명과 사진은 각 공식 사이트를 참고했다. 제안한 서비스의 수요·임상적 유용성·업무 절감 효과를 입증한 것은 아니다. 사용 목적과 운영 주체가 정해지면 의료기기 해당 여부와 필요한 요건도 확인해야 한다.</p></details>
</section>
<footer><p>아이템 검토 단계의 동료 공유용 요약. 고객군·제품 형태는 미확정이다.<br>제품 사진의 권리는 각 제공사에 있으며, 제품을 설명하기 위해 출처와 함께 수록했다. 사진은 파일에 포함되어 별도 연결 없이 볼 수 있다.</p></footer>
</main></body></html>'''.replace('__CARDS__', ''.join(cards))
out.write_text(html, encoding='utf-8')
Path(__file__).with_name('brief-assets.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(dict(output=str(out), bytes=out.stat().st_size, images=len(products)), ensure_ascii=True))
