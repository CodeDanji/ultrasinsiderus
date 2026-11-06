from pathlib import Path
from html import escape
import re

base = Path(__file__).resolve().parents[2]
report = base / 'outputs' / '린_기능평가_아이템_동료공유.html'
backup = Path(__file__).with_name('brief-before-evidence.html')
if not backup.exists():
    backup.write_text(report.read_text(encoding='utf-8'), encoding='utf-8')
html = backup.read_text(encoding='utf-8')

def link(url, label):
    return f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener">{label} ↗</a>'

shoulder = link('https://doi.org/10.2519/jospt.2025.13182', '2025 회전근개 건병증 진료지침')
hip = link('https://pmc.ncbi.nlm.nih.gov/articles/PMC11329127/', '고관절 힘 측정 연구 · 2024')
cosmin = link('https://doi.org/10.1016/j.jclinepi.2010.02.006', 'COSMIN 측정 속성 합의 · 2010')
oarsi = link('https://oarsi.org/research/physical-performance-measures', 'OARSI 공식 권고·측정 매뉴얼')
cdc = link('https://www.cdc.gov/steadi/hcp/clinical-resources/', 'CDC STEADI 공식 평가 도구')

gaps = '''<section id="gaps"><span class="section-no">03 · 시장의 현재와 사업기회</span>
<h2>제품은 등장했다.<br>널리 쓰이는 서비스는 자리 잡았을까?</h2>
<p>관련 제품이 있다는 사실과 사람들이 쉽게 접하고 이용한다는 것은 별개다. 이번 조사의 출발점도 <strong>몸의 불편함은 느끼지만, 이런 평가를 어디서 어떻게 받을 수 있는지 일상에서 접하기 어려웠다는 경험</strong>이다.</p>
<p>공식 자료에서는 아래 사례가 확인된다. 이는 이미 시도가 이뤄지고 있다는 근거다. 보급 정도와 시장이 얼마나 형성됐는지는 별도로 살펴봐야 한다.</p>
<div class="finding"><span class="evidence-label">공식 안내에서 확인</span><h3>국내 제품·운동센터가 이미 연결을 제공한다</h3>
<p>에버엑스는 평가·리포트, 의료진의 운동처방과 모니터링을 제품군으로 안내한다. 리뉴미필라테스는 분석·움직임평가를 프로그램에 반영하고 정기 분석·운동기록으로 방향을 조정한다고 설명한다.</p>
<p class="source-line">__EVEREX__ · __RENEW__</p><p class="small">제공사의 설명이다. 에버엑스는 공식 제품 페이지의 검색 추출문을 확인했다. 실제 사용률·업무 절감·성과를 독립 검증한 자료는 아니다. 센터 한 곳의 사례를 전체 시장으로 일반화할 수도 없다.</p></div>
<div class="finding"><span class="evidence-label">공공·해외 서비스에서 확인</span><h3>측정 이후의 운동 안내·추적도 기존 서비스 영역이다</h3>
<p>국민체력100은 평가 이후 운동처방·체력관리 절차를 안내하며 별도 검사비가 없다. 해외 VALD MoveHealth도 운동 프로그램·교육·환자보고 결과·객관적 검사 결과를 연결한다. 신규 서비스는 이들에 비해 고객이 얻을 추가 가치를 설명해야 한다.</p>
<p class="source-line">__NFA__ · __MOVE__</p><p class="small">국민체력100은 체력관리 서비스로, 통증의 의학적 진단과 목적이 다르다. 해외 제품의 기능 존재가 국내 도입·사용률을 뜻하지는 않는다.</p></div>
<details class="research-detail"><summary>의료의 후속 관리도 이미 제도·운영 사례가 있다</summary><div class="detail-inner"><p>국립재활원은 처방·동의 후 교육·상담과 재택 상태 모니터링을 운영한다. 근골격계 대상은 하지 주요 관절치환술·하지골절 수술 등으로 구체화돼 있다. 이는 후속 관리의 존재와 적용 범위를 보여주며, 일반 요통환자 모두의 서비스 접근성을 설명하는 자료는 아니다.</p><p class="source-line">__NRC__</p></div></details>
<h3>우리가 보는 기회: 기능평가를 일상적인 서비스로 만드는 것</h3>
<p><strong>기술과 제품은 등장했지만, 고객이 필요성을 알고 쉽게 이용하는 시장은 아직 형성 중일 수 있다.</strong> 그렇다면 기존 장비의 운영을 개선하는 것에 더해, 처음 이용할 고객을 찾고 익숙한 이용 방식을 만드는 데도 사업의 의미가 있다.</p>
<div class="hypotheses"><article><span class="evidence-label">고객</span><b>불편함을 느끼지만 평가를 받아본 적 없는 사람에게</b><p>어떤 기능을 확인할 수 있는지, 결과가 관리에 어떻게 도움이 되는지 알기 쉽게 제시한다. 처음 이용할 이유와 비용을 낼 의사가 있는지 확인한다.</p></article>
<article><span class="evidence-label">접점</span><b>헬스장·필라테스·병원·기업을 통해 쉽게 접하게</b><p>이미 방문하거나 소속된 기관에서 평가를 받아볼 수 있게 한다. 어느 고객군에서 필요와 구매 이유가 가장 뚜렷한지 찾는다.</p></article>
<article><span class="evidence-label">서비스</span><b>측정에서 끝나지 않고, 이해·관리·변화 확인까지</b><p>결과를 설명하고 다음 행동과 재평가를 연결한다. 기존 서비스와 비교하면서 접근성·신뢰·이용 경험 중 우리가 더 잘 제공할 가치를 정한다.</p></article></div>
<div class="takeaway"><p><strong>핵심 사업가설은 ‘아직 널리 이용되지 않는 기능평가를, 기관을 통해 반복해서 찾는 서비스로 만들 수 있다’는 것이다.</strong> 낮은 인지도가 실제 수요와 만나는지부터 검증한다.</p></div>
<p class="small">현재 ‘시장 형성 초기일 수 있다’는 관점으로 검토한다. 국내 보급률·업체별 점유율 자료는 확보하지 못했으므로 미개발 시장이나 선도업체 부재를 확정한 것은 아니다.</p>
</section>'''
for token, value in {
    '__EVEREX__': link('https://everex.kr/ko/products', '에버엑스 제품 안내'),
    '__RENEW__': link('https://renewmepilates.com/body-analysis/', '리뉴미필라테스 운영 안내'),
    '__NFA__': link('https://nfa.kspo.or.kr/reserve/selectMeasureUseGuide.kspo', '국민체력100 이용 안내'),
    '__MOVE__': link('https://valdhealth.com/products/movehealth', 'VALD MoveHealth'),
    '__NRC__': link('https://nrc.go.kr/hospital/html/content.do?depth=rb&menu_cd=03_07_01', '국립재활원 질환별 재택관리'),
}.items():
    gaps = gaps.replace(token, value)

methods = [
    dict(id='prom', title='통증과 생활의 제한이 얼마나 달라졌나?', name='환자보고 설문 · PROM', category='기본 후보',
         short='본인이 느끼는 통증·일상 기능을 검증된 문항으로 기록한다.',
         how='대상과 증상에 맞는 검증된 설문을 같은 판본으로 반복한다. 예를 들어 어깨의 SPADI, 일반 신체기능의 PROMIS Physical Function 등이 있다.',
         value='힘이 늘었는지와 별개로, 당사자가 중요하게 여기는 활동과 불편함이 달라졌는지 평가한다. 센서 값과 서로 보완한다.',
         evidence='어깨 진료지침은 타당도·신뢰도·변화 반응성이 확인된 환자보고 도구의 사용을 권고한다. HealthMeasures는 목적에 맞는 신체기능 척도 선택을 안내한다.',
         sources=shoulder+' · '+link('https://healthmeasures.net/select-measures/recommended-measures/', 'HealthMeasures 공식 도구 선택 안내'),
         limit='최대 근력이나 원인 조직을 측정하지는 않는다. 실제 적용 전 검증된 한국어판·해당 환자군·채점법·사용권을 확인한다.'),
    dict(id='force', title='이 방향으로 얼마나 힘을 낼 수 있나?', name='힘 센서 · HHD / 고정식', category='기본 후보',
         short='표준 자세에서 특정 움직임을 담당하는 근육군의 출력을 본다.',
         how='자세와 패드 위치를 맞추고, 고정된 센서를 향해 힘을 내게 한다. 유효 시도의 힘(N)을 정한 규칙으로 요약한다. 수직 모멘트암을 기록한 경우 토크(N·m)도 계산할 수 있다.',
         value='고관절 외전·어깨 외회전처럼 동작을 담당하는 근육군의 수행능력과 경과를 정량화한다. 초기의 관리 목표와 재평가 자료가 될 수 있다.',
         evidence='회전근개 건병증 지침은 등척성 힘의 객관적 측정에 HHD 사용을 권고한다. 고관절 연구는 특정 절차의 타당도·당일 동일 검사자 반복성을 검토했다. 단, 건강인 30명의 결과를 모든 통증환자와 새 장비에 적용할 수는 없다.',
         sources=shoulder+' · '+hip,
         limit='낮은 힘은 통증·노력·고정·신경 문제의 영향도 받는다. 개별 근육의 힘이나 통증 원인을 직접 분리하지 못한다. 좌우 차이 14.3%만으로 비정상 등급을 만들지 않는다.'),
    dict(id='rom', title='관절을 어느 범위까지 움직일 수 있나?', name='각도계·경사계 · ROM', category='기본 후보',
         short='능동·수동 가동범위와 움직일 때의 증상을 기록한다.',
         how='정한 기준 자세에서 본인이 움직이는 각도와 검사자가 움직여 보는 각도를 구분한다. 관절·방향·보상 동작·증상 반응을 함께 기록한다.',
         value='어깨를 올리거나 고관절을 회전할 때의 제한을 수치화한다. 동작 범위에 맞춰 과제와 진행 목표를 정하는 자료가 된다.',
         evidence='어깨 지침은 눈대중 대신 각도계·경사계 또는 관련 스마트폰 앱을 사용해 능동·수동 ROM을 측정하도록 권고한다.',
         sources=shoulder,
         limit='각도만으로 근육·관절낭·통증 중 무엇이 제한 원인인지 정하지 못한다. 이 지침은 동적 견갑골 ROM 측정의 신뢰도·타당도 한계도 명시한다. 일반 팔 각도 측정을 날개뼈 정밀 진단으로 바꾸면 안 된다.'),
    dict(id='function', title='일어나고 걷고 계단을 오를 수 있나?', name='표준 기능과제', category='기본 후보',
         short='생활 동작의 시간·횟수·지구력 등 복합 수행능력을 본다.',
         how='30초 의자 일어나기, 정해진 거리 걷기, 계단 오르기, 일어서서 걷고 돌아오는 TUG 등에서 표준 절차로 시간·횟수를 기록한다. 균형은 대상에 따라 별도 표준 과제로 확인한다.',
         value='단일 관절의 힘보다 실제 활동에 가까운 정보를 준다. 운동 후 힘이 늘어도 생활 과제가 개선되지 않는 경우를 구분할 수 있다.',
         evidence='OARSI는 고관절·무릎 골관절염과 관절치환 후 집단을 위한 수행검사 세트를 권고한다. CDC STEADI는 고령자 낙상 평가에서 일어나기·TUG·균형 과제를 제공한다.',
         sources=oarsi+' · '+cdc,
         limit='다리 힘뿐 아니라 통증·균형·심폐능력·전략이 영향을 준다. 둔근 약화로 환원하지 않는다. 고령자 또는 골관절염의 기준을 젊은 요통환자의 정상 기준으로 쓰지 않는다. 일반 스쿼트·step-down의 점수화도 별도 검증이 필요하다.'),
    dict(id='imu', title='움직임의 각도와 속도를 자동으로 기록할 수 있나?', name='착용형 움직임 센서 · IMU', category='목적별 추가',
         short='몸에 붙인 센서로 분절의 방향과 움직임 변화를 계산한다.',
         how='상완·몸통 등 정한 위치에 센서를 붙이고 기준 자세를 보정한다. 신호를 정해진 좌표계·알고리즘으로 처리해 각도·속도 등을 산출한다.',
         value='특정 동작을 반복 기록하거나 수행 중 피드백을 주는 데 쓸 수 있다. 수작업 측정을 줄일 수 있는지는 별도로 실측한다.',
         evidence='2023년 어깨 IMU 연구는 건강한 젊은 성인 15명에서 반복성과 동시타당도를 평가했다. 양호한 신뢰도와 별개로, 측정 방식 간 일치 범위의 한계가 있었다.',
         sources=link('https://pmc.ncbi.nlm.nih.gov/articles/PMC10490745/', '어깨 IMU 측정 원논문 · 2023'),
         limit='부착·보정·장비·알고리즘별 검증이 필요하다. 근육 힘을 직접 읽지 않으며 작은 각도 차이를 곧바로 임상적 개선으로 볼 수 없다.'),
    dict(id='camera', title='어떤 방식으로 몸을 움직이는가?', name='카메라 기반 동작 분석', category='목적별 추가',
         short='영상으로 관절 위치·각도·몸통 기울임 등 움직임을 추정한다.',
         how='정해진 카메라 배치에서 과제를 촬영하고 관절점·각도·움직임 전략을 계산한다. 역학 모델을 더해 힘·모멘트를 추정할 수도 있지만 직접 측정값과 구분한다.',
         value='동작을 기록·설명하고 과제 수행의 변화를 비교하는 데 활용할 수 있다. 실제 제품의 자동 측정 범위는 검증한 부위와 과제로 한정한다.',
         evidence='OpenCap 2023 연구는 건강인 10명, 스마트폰 2대의 특정 과제에서 평균 관절각 오차 4.5°를 보고했다. 2026년 독립 연구는 과제·운동면에 따라 정확도 한계가 다름을 확인했다.',
         sources=link('https://pmc.ncbi.nlm.nih.gov/articles/PMC10586693/', 'OpenCap 원논문 · 2023')+' · '+link('https://pubmed.ncbi.nlm.nih.gov/42318929/', '독립 검증 연구 · 2026'),
         limit='이 연구가 단일 카메라·모든 환자·상용 제품의 정확도를 보증하지 않는다. 영상에서 특정 근육의 힘이나 통증 원인을 직접 읽는 것은 아니다.'),
    dict(id='semg', title='운동 중 표층 근육의 전기활동은 어떻게 변하나?', name='표면근전도 · sEMG', category='제한된 보조 용도',
         short='정한 부위의 신호 시점·상대 진폭을 관찰하거나 피드백한다.',
         how='피부 전극을 표준 위치에 고정하고 잡음을 확인한다. 질문에 맞는 참조 과제로 정규화한 뒤 운동 중 신호를 처리한다.',
         value='특정 운동에서 전기활동을 관찰하고 학습 피드백을 주는 보조 도구가 될 수 있다. 피드백을 끈 뒤에도 수행이 좋아지는지 확인해야 한다.',
         evidence='CEDE 방법론 합의는 목적에 맞는 진폭 정규화를, SENIAM은 전극 배치·고정의 표준화를 다룬다. 신호 측정 방법의 근거이며, 그 자체로 특정 운동의 치료효과를 입증하는 자료는 아니다.',
         sources=link('https://pubmed.ncbi.nlm.nih.gov/32569878/', 'CEDE 합의 · 2020')+' · '+link('https://seniam.org/fixation.htm', 'SENIAM 전극 고정 안내'),
         limit='진폭은 근력과 같지 않다. 인접 신호·전극 위치·피부 등의 영향을 받고 심부근을 분리하기 어렵다. 표면 신호로 신경근병증을 확진하거나 원인 근육을 자동 지목하지 않는다.'),
    dict(id='neuro', title='힘 저하에 신경 문제가 관련돼 있나?', name='신경학적 진찰·침근전도/NCS', category='의료진 평가',
         short='근력·감각·반사와 적응증에 따른 전기진단으로 병변을 평가한다.',
         how='의료진이 증상·진찰로 신경학적 이상을 평가한다. 필요한 경우 침근전도와 신경전도검사 등으로 신경계 병변의 전기생리학적 소견을 확인한다.',
         value='단순한 과제 힘 저하와 별도로 신경근·말초신경 병변을 평가하는 경로다. 일반 운동기관의 자동 측정과 역할을 구분한다.',
         evidence='AAPM&R 전문 자료와 AANEM 학회 모노그래프는 신경근병증에서 전기진단의 역할과 한계를 설명한다. 침근전도는 민감도가 제한돼 정상이어도 일부 신경근병증을 배제하지 못한다.',
         sources=link('https://now.aapmr.org/electrodiagnosis-of-radiculopathies-cervical-thoracic-and-lumbar/', 'AAPM&R 전기진단 전문 자료')+' · '+link('https://education.aanem.org/AssetListing/Monograph-Evaluation-of-persons-with-suspected-lumbosacral-and-cervical-radiculopathy-Electrodiagnostic-assessment-and-implications-for-treatment-and-outcomes-Part-II-2401/MUS27008-7972', 'AANEM 학회 모노그래프'),
         limit='휴대 힘 센서나 피부에 붙이는 sEMG로 대체하는 검사가 아니다. 초기 서비스에는 검사 자체보다 의료진 의뢰·결과 연계 경로를 설계한다.'),
]

method_cards = []
for i, m in enumerate(methods, 1):
    method_cards.append(f'''<details class="method" id="method-{m['id']}"><summary>
    <span class="method-top"><span>{i:02} · {m['name']}</span><span class="method-tag">{m['category']}</span></span>
    <strong>{m['title']}</strong><span class="method-short">{m['short']}</span></summary>
    <div class="detail-inner"><dl><dt>측정 과정</dt><dd>{m['how']}</dd>
    <dt>쓸모 있는 판단</dt><dd>{m['value']}</dd><dt>근거와 적용 범위</dt><dd>{m['evidence']}</dd>
    <dt>해석의 한계</dt><dd>{m['limit']}</dd></dl><p class="source-line">{m['sources']}</p></div></details>''')

assessment = f'''<section id="assessment"><span class="section-no">06 · 평가 방식과 의료적 근거</span>
<h2>기능평가는 의미가 있다.<br>무엇을 평가하는지 구분해서 써야 한다</h2>
<p>힘·가동범위·기능과제·환자보고 결과는 임상 평가와 경과 확인에 쓰이는 방법이다. 예를 들어 2025년 회전근개 건병증 진료지침은 해당 질환이 의심되는 성인의 어깨 통증 평가에서 HHD 힘 측정, 각도 측정, 검증된 환자보고 도구 사용을 권고한다. <span class="source-inline">{shoulder}</span></p>
<div class="evidence-scale"><b>‘근거가 있다’는 말을 세 단계로 읽는다</b><p><strong>잘 측정하는가?</strong> 반복성·타당도·측정오차·변화 반응성을 확인한다.<br><strong>판단에 도움이 되는가?</strong> 대상과 목적에 맞게 쓰여 관리 결정을 바꾸는지 본다.<br><strong>치료 결과도 개선하는가?</strong> 기존 진료와 비교한 별도 연구가 필요하다.</p><p class="source-line">측정 속성의 구분: {cosmin}</p></div>
<p class="small">아래 분류는 초기 서비스에서의 활용 제안이며 공식 근거 등급은 아니다. 각 항목을 열면 측정 원리·의미·근거·한계를 볼 수 있다.</p>
{''.join(method_cards)}
<div class="takeaway"><p><strong>첫 평가 묶음은 ‘환자보고 + 표준 힘 + ROM + 목적에 맞는 기능과제’부터 검토한다.</strong> 몸 전체를 한 점수로 판정하기보다 서로 다른 측면을 함께 본다. 이는 위 근거를 종합한 설계 제안이며 이 조합 자체의 효과가 입증됐다는 뜻은 아니다.</p></div>
<h3>측정이 좋아도, 새 서비스의 효과는 따로 확인해야 한다</h3>
<p>만성 요통의 RESTORE 무작위시험 3년 추적에서는 인지기능치료의 효과가 유지됐지만, 움직임 센서 피드백을 추가한 군의 추가 이득은 확인되지 않았다. 이 결과를 모든 센서에 일반화할 수는 없지만, <strong>센서를 더했다고 치료 결과가 좋아진다고 가정해서는 안 된다.</strong></p>
<p class="source-line">{link('https://pubmed.ncbi.nlm.nih.gov/40780241/', 'RESTORE 3년 추적 원논문 · 2025')}</p>
<details class="research-detail"><summary>어떤 기능을 관리할지 정하는 실제 원리</summary><div class="detail-inner"><p>예를 들어 고관절 외전 힘 저하, 관련 생활 과제의 제한, 증상 반응이 함께 확인되면 전문가가 외전 기능을 관리 목표로 검토할 수 있다. 통증으로 힘을 못 낸 결과라면 먼저 부하·검사 조건·추가 평가를 다시 본다.</p><p>근육군의 기능을 관리 대상으로 삼는 판단은 가능하다. 다만 ‘어느 근육이 통증을 일으켰다’는 원인 판정과 구별하고, 선택한 운동이 실제 증상·기능에 도움이 되는지는 재평가로 확인한다.</p></div></details>
</section>'''

# Keep the original brief and official embedded photographs; add two focused sections.
html = html.replace('<div class="conclusion"><span class="eyebrow">현재 결론</span><p><strong>기능을 측정하는 장비는 이미 있다.</strong> 먼저 기존 장비로 기관의 평가 과정을 운영해보고, 결과가 실제 운동·관리 결정에 쓰이는지 확인하려 한다. 독자 기기 개발은 그 과정에서 반복되는 문제가 드러난 뒤 판단한다.</p></div>',
'''<div class="conclusion"><span class="eyebrow">현재 보는 사업기회</span><p><strong>기능평가에는 임상 근거가 있고 관련 제품도 등장했다. 이제 고객이 쉽게 접하고 반복해서 이용할 서비스로 만들 수 있는지 보려 한다.</strong> 기관을 통해 평가·설명·관리·재평가를 제공하고, 처음 이용할 고객과 구매 이유를 확인한다. 시장이 아직 형성 중일 수 있다는 가설에서 출발한다.</p></div>''')
html = html.replace('<div class="takeaway"><p><strong>측정·기록·리포트만으로는 차별화하기 어렵다.</strong> 국내 기관이 이 과정을 운영하고 결과를 운동·관리와 연결할 때 남는 불편이 있는지 확인해야 한다.</p></div>',
'''<div class="takeaway"><p><strong>평가와 운동을 연결하는 제품까지 등장했다.</strong> 이제 살펴볼 것은 이 서비스가 얼마나 알려지고 이용되는지, 어떤 고객에게 더 쉽게 제공할 수 있는지다. <a href="#gaps">시장과 사업기회 보기 ↓</a></p></div>''')
html = html.replace('<section id="customers">', gaps+'<section id="customers">')
html = html.replace('<section id="plan">', assessment+'<section id="plan">')
html = html.replace('03 · 예상 고객과 제공 가치', '04 · 예상 고객과 제공 가치').replace('04 · 솔루션', '05 · 솔루션').replace('05 · 린 스타트업 진행 방향', '07 · 린 스타트업 진행 방향')
html = html.replace('<a href="#customers">고객과 가치</a>', '<a href="#gaps">시장과 사업기회</a><a href="#customers">고객과 가치</a>').replace('<a href="#plan">진행 방향</a>', '<a href="#assessment">평가 근거·8가지 방식</a><a href="#plan">진행 방향</a>')
html = html.replace('후보 고객군별 기관 몇 곳을 만나 기존 평가, 결과 설명, 재평가 방식과 비용을 누가 부담하는지 확인한다. 가장 반복되고 해결할 가치가 큰 문제 하나를 고른다.', '기존 서비스를 쓰는 기관과 쓰지 않는 기관, 평가를 받아보지 않은 이용자를 함께 만난다. 몰라서 이용하지 않는지, 필요를 못 느끼는지, 비용·접근성이 문제인지 확인하고 첫 고객군을 고른다.')
html = html.replace('실제 항목은 담당 전문가와 정한다.', '실제 항목은 대상과 목적에 맞춰 담당 전문가와 정한다. <a href="#assessment">방식별 근거 보기 ↓</a>')
html = html.replace('오른쪽 180N / 왼쪽 210N → 좌우 차이 14.3%', '오른쪽 180N / 왼쪽 210N → 오른쪽이 14.3% 낮음')
html = html.replace('이 수치만으로 특정 근육을 통증의 원인으로 지목하지 않는다.', '차이는 왼쪽 대비 (210−180)/210×100으로 계산했다. 이 수치만으로 특정 근육을 통증의 원인으로 지목하지 않는다.')
html = html.replace('이후 같은 조건으로 다시 측정하고 불편감·생활 동작의 변화도 함께 확인한다.', '이후 같은 조건으로 다시 측정하고 불편감·생활 동작의 변화도 함께 확인한다. 전후 차이가 해당 검사의 측정오차를 넘는지는 별도로 판단한다.')
html = re.sub(r'<details class="sources">.*?</details>', '''<details class="sources"><summary>조사 범위와 남은 확인</summary><p>2026.10.26 기준 공식 운영 안내·제품 자료, 진료지침·원논문·방법론 합의를 검토했다. 공개자료는 서비스의 존재와 평가 방법의 근거를 보여주지만, 국내 전체 보급률·기관별 업무 부담·구매 의향은 설명하지 못한다.</p><p>현장 관찰과 인터뷰를 아직 수행하지 않았다. 국내 사례는 기관·제공사의 설명이며 독립적인 효과 검증과 구분했다. 실제 도입 전 대상·절차·한국어 도구·사용권·사용 목적에 따른 요건을 확인해야 한다.</p></details>''', html, flags=re.S)
css = '''
.finding{padding:20px 0;border-bottom:1px solid var(--line)}.finding h3{margin:8px 0 12px}.finding p:last-child{margin-bottom:0}.evidence-label{display:block;font-size:12px;color:var(--green);font-weight:700;margin-bottom:8px}.source-line{font-size:12px;line-height:1.9;margin:12px 0;color:var(--muted)}.source-line a{display:inline-block;margin-right:6px}.source-inline{font-size:12px}.hypotheses{margin:22px 0}.hypotheses article{padding:17px 0;border-bottom:1px solid var(--line)}.hypotheses p{font-size:15px;margin:7px 0 0}.evidence-scale{padding:21px 23px;background:var(--soft);border-radius:6px;margin:23px 0}.evidence-scale p{font-size:15px;margin:10px 0 0}.method,.research-detail{border:1px solid var(--line);border-radius:6px;margin:13px 0}.method summary,.research-detail summary{padding:17px 20px;list-style:none}.method summary::-webkit-details-marker{display:none}.method summary{position:relative;padding-right:38px}.method summary:after{content:'+';position:absolute;right:17px;top:44px;font-size:21px;font-weight:400}.method[open] summary:after{content:'−'}.method-top{display:flex;justify-content:space-between;gap:12px;font-size:12px;color:var(--muted);font-weight:400;margin-bottom:6px}.method-tag{color:var(--green);flex-shrink:0;font-size:11px}.method summary strong{display:block;font-size:17px}.method-short{display:block;font-size:14px;line-height:1.8;color:var(--muted);font-weight:400;margin-top:5px}.detail-inner{padding:20px 23px;border-top:1px solid var(--line);font-size:15px}.detail-inner dl{margin:0}.detail-inner dt{color:var(--green);font-size:12px;font-weight:700;margin:18px 0 5px}.detail-inner dt:first-child{margin-top:0}.detail-inner dd{margin:0 0 12px}.detail-inner p:last-child{margin-bottom:0}@media(max-width:720px){.method summary,.research-detail summary{padding:16px}.method summary{padding-right:33px}.method-top{flex-direction:column;gap:1px}.method summary strong{font-size:16px}.method-short{font-size:13px}.detail-inner{padding:18px;font-size:14px}.evidence-scale{padding:18px}.evidence-scale p,.hypotheses p{font-size:14px}}@media print{.method summary strong{font-size:10.5pt}.method-short,.detail-inner,.evidence-scale p,.hypotheses p{font-size:9pt}.method,.research-detail{break-inside:auto}.method-top,.source-line,.source-inline{font-size:8pt}.method-tag{font-size:7pt}.finding,.hypotheses article{break-inside:avoid}}
'''
html = html.replace('</style>', css+'</style>')
report.write_text(html, encoding='utf-8')
print(f'Updated: {report.name}; methods={len(methods)}; bytes={report.stat().st_size}')
