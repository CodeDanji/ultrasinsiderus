from pathlib import Path
import re
import shutil

base = Path(__file__).resolve().parents[2]
report = base / 'outputs' / '\uadfc\uace8\uaca9\uacc4_\ubd88\ud3b8\ud568_\uae30\ub2a5\ud3c9\uac00_\ubb38\uc81c\ud0d0\uc0c9_\ubcf4\uace0\uc11c.html'
original = report.read_text(encoding='utf-8')
backup = Path(__file__).with_name('report-before-readability.html')
if not backup.exists():
    shutil.copy2(report, backup)
sources = re.findall(r'<article class="source".*?</article>', original, flags=re.S)
assert len(sources) == 23

template = r'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="근골격계 불편함의 원인 이해와 기능평가, 기존 진료와 제품, 새로운 사업 주제를 정리한 조사 보고서">
<title>근골격계 불편함과 기능평가 | 인사이더스 린 프로젝트</title>
<style>
:root{--ink:#242d35;--muted:#626d77;--line:#e1e5e9;--accent:#245e50;--soft:#f2f7f4;--paper:#fff;--bg:#f7f8f9}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:24px}body{margin:0;color:var(--ink);background:var(--paper);font:17px/1.95 "Malgun Gothic","Apple SD Gothic Neo",system-ui,sans-serif;word-break:keep-all;overflow-wrap:anywhere}a{color:var(--accent);text-underline-offset:4px}a:hover{text-decoration-thickness:2px}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #3e806c;outline-offset:5px}p{margin:0 0 18px}strong{font-weight:750}h1,h2,h3{line-height:1.5;letter-spacing:-.035em}h1{font-size:34px;margin:13px 0 11px}h2{font-size:27px;margin:0 0 25px}h3{font-size:19px;margin:29px 0 10px}ul,ol{padding-left:1.3em;margin:13px 0 23px}li{padding-left:3px;margin:10px 0}.skip{position:fixed;left:15px;top:-80px;background:white;padding:10px;z-index:5}.skip:focus{top:15px}.page{max-width:1120px;padding:0 34px;margin:auto}.header{padding:40px 0 29px;border-bottom:1px solid var(--line)}.project{font-size:13px;font-weight:700;color:var(--accent);letter-spacing:.04em}.subtitle{font-size:17px;color:var(--muted);margin-bottom:22px}.header-bottom{display:flex;justify-content:space-between;align-items:center;gap:16px;font-size:13px;color:var(--muted)}button{font:inherit;background:white;border:1px solid #c6d0ca;padding:7px 13px;border-radius:5px;color:var(--accent);cursor:pointer;white-space:nowrap}.layout{display:grid;grid-template-columns:180px minmax(0,760px);gap:55px;padding-top:35px}.sidebar{position:sticky;top:28px;align-self:start;font-size:13px;line-height:1.8}.nav-title{font-weight:800;margin-bottom:12px}.sidebar a{display:block;text-decoration:none;color:var(--muted);padding:6px 0}.sidebar a:hover{color:var(--accent)}.sidebar .nav-note{font-size:12px;color:#737f87;margin-top:25px;line-height:1.8}.mobile-nav{display:none}main{min-width:0}section{margin-bottom:58px;padding-bottom:38px;border-bottom:1px solid var(--line);scroll-margin-top:26px}.number{font-size:12px;color:var(--accent);font-weight:800;margin-bottom:9px}.intro{font-size:19px;line-height:1.9}.summary{background:var(--soft);padding:24px 28px;border-radius:7px;margin:0 0 25px}.summary h2{font-size:21px;margin-bottom:15px}.summary ul{margin:0;padding-left:1.2em}.summary li{margin:10px 0}.summary li:last-child{margin-bottom:0}.small{font-size:14px;line-height:1.85;color:var(--muted)}.cite{font-size:12px;text-decoration:none;white-space:nowrap;margin-left:4px;font-weight:700}.key{border-left:3px solid #47846c;padding:3px 0 3px 18px;margin:24px 0;font-size:18px}.key p{margin:0}.case{padding:19px 0;border-top:1px solid var(--line)}.case h3{margin:0 0 8px}.case p{margin-bottom:0}.case .voice{color:var(--muted);font-size:15px;margin-bottom:7px}.steps{list-style:none;padding:0;counter-reset:step}.steps li{counter-increment:step;position:relative;padding:0 0 15px 38px;margin:0 0 12px;border-bottom:1px solid #edf0f2}.steps li::before{content:counter(step);position:absolute;left:0;top:3px;width:24px;height:24px;border-radius:50%;background:#eaf2ed;color:var(--accent);text-align:center;font-size:12px;line-height:24px;font-weight:800}.steps strong{display:block;margin-bottom:4px}.steps p{margin:0;font-size:16px}.caption{font-size:13px;line-height:1.8;color:var(--muted)}.notice{background:#f8f6f0;padding:17px 20px;border-radius:5px;margin:23px 0;font-size:15px;line-height:1.85}.notice p:last-child{margin:0}.block{margin:24px 0;padding:0 0 22px;border-bottom:1px solid var(--line)}.block:last-child{border:0}.block h3{margin:0 0 9px}.block p:last-child{margin-bottom:0}.label{font-size:12px;color:var(--accent);font-weight:800;display:block;margin-bottom:6px}.product-list{margin:20px 0}.product-list dt{font-size:17px;font-weight:750;margin-top:21px}.product-list dd{margin:4px 0 0;font-size:16px}.topic{border:1px solid var(--line);padding:23px 25px;margin:16px 0;border-radius:6px}.topic h3{margin:0 0 12px;font-size:20px}.topic p{font-size:16px;margin-bottom:13px}.topic p:last-child{margin:0}.topic .question{font-size:17px;color:var(--accent)}details{border:1px solid var(--line);border-radius:6px;margin:22px 0;background:#fff}summary{padding:14px 18px;cursor:pointer;font-size:15px;font-weight:700;line-height:1.7}details[open]>summary{border-bottom:1px solid var(--line)}.detail-body{padding:20px 23px;font-size:15px;line-height:1.9}.detail-body p:last-child{margin-bottom:0}.detail-body h3{font-size:17px;margin-top:23px}.detail-body h3:first-child{margin-top:0}.source{padding:20px 0;border-bottom:1px solid var(--line);scroll-margin-top:26px}.source:last-child{border:0}.source h3{font-size:15px;letter-spacing:0;line-height:1.8;margin:7px 0 10px}.source p{font-size:14px;line-height:1.85;margin:0 0 7px}.source .source-meta{font-size:12px;color:var(--accent);font-weight:700}.source .limit{font-size:13px;color:var(--muted)}.footer{font-size:13px;color:var(--muted);padding:0 0 45px}.footer p{margin-bottom:12px}.references .detail-body{padding-top:0;padding-bottom:0}
@media(max-width:1050px){.layout{grid-template-columns:155px minmax(0,1fr);gap:32px}.page{padding:0 27px}}
@media(max-width:760px){body{font-size:16px;line-height:1.95}.page{padding:0 21px}.header{padding:27px 0 23px}h1{font-size:27px;margin-top:10px}.subtitle{font-size:15px;margin-bottom:17px}.header-bottom{font-size:12px;flex-wrap:wrap;gap:10px}.layout{display:block;padding-top:22px}.sidebar{display:none}.mobile-nav{display:block;margin:0 0 30px}.mobile-nav a{display:block;color:var(--muted);font-size:14px;padding:5px 0}.mobile-nav .detail-body{padding:10px 18px}h2{font-size:24px;margin-bottom:20px}h3{font-size:18px}.intro{font-size:17px}.summary{padding:20px}.summary h2{font-size:19px}.key{font-size:17px;padding-left:15px}.case{padding:20px 0}.case .voice{font-size:14px}.topic{padding:20px}.topic h3{font-size:19px}.topic p{font-size:15px}.topic .question{font-size:16px}.small{font-size:13px}.steps p{font-size:15px}.detail-body{padding:18px;font-size:14px}.notice{font-size:14px;padding:16px 18px}section{margin-bottom:40px;padding-bottom:28px}.product-list dd{font-size:15px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
@media print{@page{size:A4;margin:17mm}body{font-size:10.5pt;line-height:1.75;background:white}.page{max-width:none;padding:0}.header{padding:0 0 15px}h1{font-size:24pt}h2{font-size:18pt}.subtitle{font-size:11pt}.header-bottom{font-size:8.5pt}.layout{display:block;padding-top:22px}.sidebar,.mobile-nav,.skip,button{display:none!important}section{margin-bottom:25px;padding-bottom:20px}.summary{padding:18px}.intro,.key{font-size:12pt}.topic,.notice,.case,.source,.block{break-inside:avoid}.topic{padding:15px}h2,h3,summary{break-after:avoid}.detail-body{padding:15px;font-size:9.5pt}.source p{font-size:9pt}.source h3{font-size:9.5pt}.source .limit{font-size:8.5pt}.small,.caption{font-size:9pt}a{color:#234a3e}.footer{font-size:8.5pt}}
</style>
</head>
<body>
<a href="#main" class="skip">본문으로 바로 가기</a>
<div class="page">
<header class="header" id="top"><div class="project">인사이더스 · 린 프로젝트 조사 보고서</div><h1>근골격계 불편함과 기능평가</h1><p class="subtitle">웰니스·의료기기 아이디어를 찾기 위한 문제 조사</p><div class="header-bottom"><span>조사 기준 2026.10.26 · 출처 23개</span><button type="button" onclick="window.print()">인쇄 / PDF 저장</button></div></header>
<div class="layout">
<aside class="sidebar"><nav aria-label="보고서 목차"><div class="nav-title">목차</div><a href="#summary">핵심 결론</a><a href="#problem">1. 해결하고 싶은 문제</a><a href="#clinical">2. 평가로 알 수 있는 것</a><a href="#pathway">3. 기존 진료와 제품</a><a href="#needs">4. 아직 남는 문제</a><a href="#opportunities">5. 검토할 사업 주제</a><a href="#validation">6. 다음 조사</a><a href="#sources">출처와 조사 범위</a></nav><p class="nav-note">본문은 결론과 해석 중심입니다.<br>자세한 연구 내용과 출처는<br>각 항목을 펼쳐볼 수 있습니다.</p></aside>
<main id="main">
<details class="mobile-nav"><summary>목차</summary><nav class="detail-body" aria-label="모바일 목차"><a href="#summary">핵심 결론</a><a href="#problem">1. 해결하고 싶은 문제</a><a href="#clinical">2. 평가로 알 수 있는 것</a><a href="#pathway">3. 기존 진료와 제품</a><a href="#needs">4. 아직 남는 문제</a><a href="#opportunities">5. 검토할 사업 주제</a><a href="#validation">6. 다음 조사</a><a href="#sources">출처와 조사 범위</a></nav></details>

<section id="summary">
<div class="summary"><h2>핵심 결론</h2><ul><li><strong>기능을 평가하는 방법과 기기는 이미 있다.</strong> 국내 병원에서도 근력·가동범위를 측정하고 운동 계획과 전후 비교에 활용한다.<a class="cite" href="#s14">[14]</a></li><li><strong>기능의 문제를 찾는 것과 통증의 원인을 밝히는 것은 다르다.</strong> 힘이나 움직임의 차이만으로 특정 근육을 원인으로 지목할 수는 없다.<a class="cite" href="#s05">[5]</a><a class="cite" href="#s07">[7]</a></li><li><strong>새로운 기회가 어디에 있는지는 현장에서 확인해야 한다.</strong> 문헌에는 설명·관리·추적의 어려움이 나타나지만, 국내 수요와 지불의향은 아직 확인되지 않았다.<a class="cite" href="#s11">[11]</a><a class="cite" href="#s13">[13]</a></li></ul></div>
<p>다음 단계에서는 <strong>원인 확인에 부족한 정보가 무엇인지</strong>, 그리고 <strong>기존 평가가 관리로 이어지지 않는 이유가 무엇인지</strong>를 함께 조사한다. 아직 기기나 서비스를 하나로 정할 단계는 아니다.</p>
<p class="small">초음파 아이디어는 제외했다. 이 보고서는 사업 주제를 찾기 위한 조사이며, 개인의 증상을 진단하거나 운동을 처방하는 자료가 아니다.</p>
</section>

<section id="problem"><div class="number">01</div><h2>해결하고 싶은 문제</h2>
<p class="intro">몸이 불편한 사람은 자신의 추정이 맞는지 확인하고, 그 결과에 따라 무엇을 해야 할지 알고 싶다.</p>
<div class="key"><p>“어떤 부위가 제대로 기능하지 않아 다른 곳에 부담이 가는 것 같다. 내 생각이 맞는지, 얼마나 문제인지, 전문가가 필요한지, 어떤 운동을 해야 하는지 알고 싶다.”</p></div>
<p>대화에서 나온 사례를 보면, 필요한 답은 네 가지로 나뉜다.</p>
<div class="case"><h3>고관절: 불편한 이유를 알고 싶다</h3><p class="voice">“오른쪽 고관절이 계속 불편한데 이유를 모르겠다.”</p><p>어떤 상황에서 문제가 나타나는지 파악하고, 무엇을 더 확인해야 하는지 알고 싶은 경우다.</p></div>
<div class="case"><h3>어깨: 알고 있는 설명을 관리로 연결하고 싶다</h3><p class="voice">“견갑골 움직임과 관련이 있다고 이해하고 있다. 효과적인 관리 방법이 궁금하다.”</p><p>그 설명이 맞는지, 운동을 제대로 하고 있는지, 실제로 좋아지는지 확인하고 싶은 경우다. 전거근이 원인이라는 설명은 현재 사용자가 가진 이해로 기록하며, 확인된 진단으로 다루지 않는다.</p></div>
<div class="case"><h3>허리: 내 추정을 확인하고 문제의 정도를 알고 싶다</h3><p class="voice">“고관절·하체 후면·복부 등을 잘 활용하지 못하는 것 같다.”</p><p>정말 그런지, 어느 기능이 얼마나 부족한지, 전문가의 도움과 자가 관리 중 무엇이 적절한지 알고 싶은 경우다.</p></div>
<div class="case"><h3>무릎: 검사 후에도 남는 불확실성을 해결하고 싶다</h3><p class="voice">“X-ray에는 문제가 없다는데 계속 불편하다. 다음에 무엇을 해야 할까?”</p><p>추가 검사, 경과 관찰, 관리 중 다음 행동을 정하기 어려운 경우다. 전달받은 경험이며 진료기록을 확인한 사례는 아니다.</p></div>
<p class="small">위 사례는 문제를 찾기 위한 출발점이다. 기능 저하가 실제로 존재하는지, 그것이 통증과 어떤 관계인지는 별도로 확인해야 한다.</p>
</section>

<section id="clinical"><div class="number">02</div><h2>기능평가로 어디까지 알 수 있나?</h2>
<p>평가는 크게 세 단계로 나뉜다. <strong>몸의 상태를 측정하는 것, 측정 결과를 해석하는 것, 그에 맞는 관리를 선택하는 것</strong>이다. 각 단계에는 서로 다른 근거가 필요하다.</p>
<ol class="steps"><li><strong>현재 기능을 측정한다</strong><p>정해진 자세에서 힘과 가동범위를 재거나, 걷기·일어나기 같은 동작을 평가한다. 같은 조건에서 얼마나 일관되게 측정되는지가 중요하다.<a class="cite" href="#s05">[5]</a><a class="cite" href="#s06">[6]</a></p></li><li><strong>증상과 함께 해석한다</strong><p>관찰된 차이가 어떤 의미인지 병력, 증상, 다른 검사와 함께 판단한다. 좌우 차이가 있다는 사실만으로 통증의 원인이 확인되는 것은 아니다.<a class="cite" href="#s07">[7]</a></p></li><li><strong>관리 방법을 선택한다</strong><p>평가 결과와 환자의 목표에 맞춰 다음 행동을 정한다. 임상 지침에는 기능 특성을 고려한 운동 접근이 있지만, 수치 하나로 정답 운동을 고르는 규칙은 아니다.<a class="cite" href="#s04">[4]</a></p></li></ol>
<h3>“어느 정도면 괜찮은가?”도 나눠서 봐야 한다</h3>
<ul><li><strong>다른 사람과 비교:</strong> 비슷한 조건의 사람보다 어느 수준인가?</li><li><strong>목표와 비교:</strong> 내가 원하는 활동을 수행하기에 충분한가?</li><li><strong>이전의 나와 비교:</strong> 변화가 측정오차보다 큰가?</li><li><strong>생활과 비교:</strong> 수치뿐 아니라 불편한 활동도 나아졌는가?</li></ul>
<p>따라서 모든 질문에 답하는 하나의 ‘정상 점수’를 먼저 만들기보다, <strong>어떤 활동과 결정을 위해 측정하는지</strong>부터 정해야 한다.</p>
<div class="notice"><p><strong>전문가에게 갈지 여부를 근력 점수만으로 정할 수는 없다.</strong> 기능 수준과 위험 판단은 다른 문제다. 병력과 증상, 추가 평가 필요성을 함께 검토해야 한다.<a class="cite" href="#s02">[2]</a><a class="cite" href="#s09">[9]</a></p></div>
<details><summary>연구에서 확인한 내용과 한계</summary><div class="detail-body">
<h3>일부 기능검사는 반복 측정에 쓸 수 있다</h3><p>Denteneer 등의 고찰은 20개 연구에서 38개 검사를 검토했다. 걷기·앉았다 일어나기·일부 몸통 지구력 검사에서 양호한 반복 신뢰도가 나타났다. 다만 같은 수치를 반복해서 얻는다는 사실이 통증 원인 진단이나 치료 효과를 입증하지는 않는다.<a class="cite" href="#s05">[5]</a></p>
<h3>작은 수치 변화는 오차일 수 있다</h3><p>McNabb 등의 연구는 건강한 성인 30명을 대상으로 고관절 힘을 측정했다. 높은 반복 신뢰도와 상당한 절대 측정오차가 함께 나타났고, 일부 최대 토크 지표의 최소검출변화는 22~35%였다. 이는 특정 장비·자세·당일 반복 조건의 결과다.<a class="cite" href="#s06">[6]</a></p><p>최소검출변화는 오차와 구분할 수 있는 변화의 크기다. 환자가 중요하게 느끼는 개선과는 다르며, 위 수치를 다른 장비나 환자의 기준으로 쓸 수 없다.</p>
<h3>센서를 추가해도 결과가 더 좋아지지는 않을 수 있다</h3><p>RESTORE 시험은 호주 20개 클리닉에서 만성·활동 제한 요통 성인 492명을 비교했다. 3년 추적 참여자는 312명이었다. 개별화된 인지기능치료(CFT)의 효과는 유지됐지만, 센서를 추가한 군과 추가하지 않은 군 사이의 활동 제한 차이는 유의하지 않았다.<a class="cite" href="#s10">[10]</a></p><p>모든 센서가 불필요하다는 뜻은 아니다. 전문가 관리의 가치와 장비의 추가 가치를 따로 검증해야 한다는 사례다. 추적 탈락과 특정 환자·치료 방식이라는 한계도 있다.</p>
<h3>어깨 움직임과 통증의 관계는 별도 확인이 필요하다</h3><p>2013년 견갑골 관련 합의문은 움직임 평가의 가치를 다루면서도, 어깨 문제에서 정확한 원인적 역할은 명확하지 않다고 설명한다. 오래된 합의문이며, 전거근 한 곳을 원인으로 확정하는 근거가 아니다.<a class="cite" href="#s07">[7]</a></p>
<h3>위험 신호도 완전한 판별 규칙은 아니다</h3><p>2023년 Cochrane 고찰은 척추골절 위험 신호에 관한 14개 연구를 검토했다. 유용한 신호가 제한적이고 연구 간 차이가 컸다. 모든 응급·신경학적 위험을 자동 선별하는 규칙으로 확대할 수 없다.<a class="cite" href="#s09">[9]</a></p>
</div></details>
</section>

<section id="pathway"><div class="number">03</div><h2>기존 진료와 제품은 무엇을 하고 있나?</h2>
<p><strong>기능평가가 의료 현장에 없는 것은 아니다.</strong> 분당서울대병원은 고관절·무릎·어깨·요추 등의 근력과 가동범위를 측정하고, 이를 바탕으로 개별 운동 계획을 세우고 향상 정도를 비교한다고 안내한다.<a class="cite" href="#s14">[14]</a></p>
<p>임상 지침도 영상검사만 다루지 않는다. 요통의 평가와 관리에는 증상·병력 파악, 필요한 검사 선택, 교육과 운동 등이 포함된다.<a class="cite" href="#s02">[2]</a><a class="cite" href="#s03">[3]</a><a class="cite" href="#s04">[4]</a></p>
<ol class="steps"><li><strong>증상과 생활의 어려움을 파악한다</strong><p>언제부터 불편했는지, 어떤 활동이 어려운지, 무엇을 회복하고 싶은지 확인한다.</p></li><li><strong>필요한 평가와 검사를 선택한다</strong><p>의학적 평가와 필요한 기능검사로 현재 상태와 추가 확인 사항을 파악한다.</p></li><li><strong>관리 계획을 세우고 다시 평가한다</strong><p>결과를 설명하고 실행할 행동을 정한 뒤, 증상과 기능의 변화에 따라 조정한다.</p></li></ol>
<p class="caption">국내 기관 안내와 해외 지침을 종합한 과정이다. 모든 국내 기관이 같은 절차를 제공한다는 조사 결과는 아니다.</p>
<h3>관련 제품도 이미 있다</h3>
<dl class="product-list"><dt>VALD DynaMo — 기능 측정</dt><dd>전문가가 힘과 관절가동범위를 측정하고 결과를 기록·보고하는 도구다.<a class="cite" href="#s16">[16]</a></dd><dt>Physitrack / PhysiApp — 운동 안내와 추적</dt><dd>전문가가 운동을 배정하고 수행 여부, 불편감, 설문 결과를 확인한다.<a class="cite" href="#s17">[17]</a></dd><dt>Hinge Health — 디지털 근골격 관리</dt><dd>문진, 운동 피드백과 케어팀을 연결한다. 미국의 참여 고용주·보험을 통한 이용 모델이다.<a class="cite" href="#s15">[15]</a></dd><dt>EverEx MORA 제품군 — 동작평가와 재활</dt><dd>국내 동작평가·재활·웰니스 제품을 구분해 소개한다. MORA Vu의 개발자 설명은 전문가 사용과 진단 대체 불가를 명시한다.<a class="cite" href="#s18">[18]</a><a class="cite" href="#s19">[19]</a></dd></dl>
<p class="small">제품 기능은 회사·개발자의 공개 설명을 확인한 것이다. 독립적인 정확도·효과·한국 허가 범위를 일괄 검증한 비교는 아니다.</p>
<div class="key"><p>새 기회를 찾으려면 “기능을 측정한다”에서 한 걸음 더 나아가야 한다. <strong>기존 방식으로 해결되지 않는 고객의 결정이 무엇인지</strong>가 중요하다.</p></div>
<details><summary>영상검사와 기능평가의 관계</summary><div class="detail-body"><p>NICE는 요통의 비전문 진료에서 영상검사를 일상적으로 시행하지 않도록 권고한다. 전문 진료에서도 검사 결과가 관리 방향을 바꿀 가능성을 고려한다. 검사를 하지 않는 것 자체를 진료의 공백으로 볼 수는 없다.<a class="cite" href="#s02">[2]</a></p><p>반대로, 정상 X-ray가 기능 문제를 확정하는 것도 아니다. ACR 2026 만성 무릎 통증 지침은 임상 상황별 추가 영상 선택을 다룬다. 정상 X-ray 후에도 의심 소견에 따라 MRI가 적절할 수 있다.<a class="cite" href="#s08">[8]</a></p><p>무릎 사례의 출발 질문은 “MRI를 대체할 기기가 필요한가?”로 한정하지 않는다. 어떤 불확실성이 남았고 다음 결정을 위해 무엇이 필요한지부터 확인한다.</p></div></details>
</section>

<section id="needs"><div class="number">04</div><h2>아직 남는 문제는 무엇인가?</h2>
<div class="block"><h3>설명을 들어도 내 상태를 이해하기 어렵다</h3><p>요통 경험자 15명을 인터뷰한 Costa 등의 연구에서는 앞으로의 경과, 의료진의 도움, 설명 이해에 관한 불확실성이 나타났다. 경청과 관리계획, 지속적인 대화의 필요도 제기됐다.<a class="cite" href="#s11">[11]</a></p></div>
<div class="block"><h3>운동 방법을 알아도 혼자 관리하기 어렵다</h3><p>영국 만성 요통 환자 9명을 인터뷰한 Bourke 등의 연구에서는 설명, 일상 경험, 자기 의심과 활동 자신감이 자기관리 경험과 연결됐다. 운동 정보를 받는 것과 실제로 관리하는 것은 다를 수 있다.<a class="cite" href="#s12">[12]</a></p></div>
<div class="block"><h3>전문가도 평가·설명·추적에 어려움을 겪는다</h3><p>네팔 물리치료사 연구는 시간, 언어 도구, 환자의 이해와 추적을 결과측정의 장벽으로 보고했다. 의료인 10명의 별도 질적연구에서도 비특이적 요통을 설명하고 함께 결정하는 어려움을 다뤘다.<a class="cite" href="#s13">[13]</a><a class="cite" href="#s23">[23]</a></p></div>
<p><strong>이 연구들은 확인할 문제를 알려주지만, 한국에서 얼마나 흔한지는 말해주지 않는다.</strong> 새로운 기기를 구매하거나 추가 서비스에 돈을 낼 것이라는 근거도 아니다.</p>
<div class="notice"><p>고객에게는 두 가지를 따로 물어야 한다. <strong>정확한 원인 이름이 반드시 필요한가?</strong> 아니면 원인을 확정하지 못하더라도, 확인한 상태와 다음 행동을 알면 도움이 되는가? 후자가 전자를 대신한다고 미리 가정하지 않는다.</p></div>
</section>

<section id="opportunities"><div class="number">05</div><h2>어떤 사업 주제를 검토할 수 있나?</h2>
<p>지금은 네 가지 주제를 열어둘 수 있다. 아래는 <strong>검증할 사업 가설</strong>이며, 시장성이나 구매 의향이 확인된 순위가 아니다.</p>
<article class="topic"><span class="label">주제 A · 병원 방문 전</span><h3>일상 불편함을 이해하고 다음 확인으로 연결하기</h3><p class="question">“무엇을 기록하고, 누구에게 무엇을 확인해야 할까?”</p><p>증상이 나타나는 상황과 생활의 어려움을 정리하고 적절한 평가로 연결하는 데 가치가 있을 수 있다.</p><p class="small"><strong>확인할 점:</strong> 원인 확정 없이도 가치가 있는가? 기존 상담이나 정보만으로 충분하지 않은가?</p></article>
<article class="topic"><span class="label">주제 B · 진료 이후</span><h3>평가 결과를 구체적인 관리로 연결하기</h3><p class="question">“진료는 받았는데, 이제 무엇을 해야 할까?”</p><p>전문가가 증상·기능·목표를 검토하고 환자가 실행할 계획으로 설명하는 과정에 공백이 있을 수 있다.</p><p class="small"><strong>확인할 점:</strong> 실제로 무엇이 해결되지 않았는가? 추가 평가가 필요한가, 설명과 실행 지원이 필요한가?</p></article>
<article class="topic"><span class="label">주제 C · 전문가 업무</span><h3>기능평가의 기록·설명·재측정을 돕기</h3><p class="question">“어떤 변화를 근거로 관리 계획을 조정할까?”</p><p>같은 방식으로 측정하고, 기록을 비교하고, 환자에게 설명하는 부담을 줄이는 도구가 필요할 수 있다.</p><p class="small"><strong>확인할 점:</strong> 기존 도구로 충분하지 않은가? 새 정보가 판단을 바꾸거나 업무 시간을 줄이는가? 구매자는 누구인가?</p></article>
<article class="topic"><span class="label">주제 D · 전문 임상 평가</span><h3>내 원인 가설이 맞는지 확인하기</h3><p class="question">“이 기능 이상이 정말 내 증상에 영향을 주는가?”</p><p>사용자의 요구에 가장 직접적으로 답하려는 주제다. 부위·환자·임상 질문을 좁히고, 어떤 평가가 기존 판단에 무엇을 더할 수 있는지 확인해야 한다.</p><p class="small"><strong>확인할 점:</strong> 기능 이상이 원인·기여요인인지, 통증의 결과인지 어떻게 구분하는가? 비교 기준과 검증 방법을 정할 수 있는가?</p></article>
<p>다음에는 B·C의 실제 사례를 살펴보면서 A의 수요와 D의 임상적 가능성을 함께 확인한다. <strong>새 측정기, 전문가용 도구, 연결 서비스 중 무엇이 필요한지는 그 후에 정한다.</strong></p>
<details><summary>웰니스와 의료기기의 경계에서 확인할 것</summary><div class="detail-body"><p>고객 요구에는 일반 운동 기록뿐 아니라 통증 원인 해석, 전문가 도움의 필요성, 개인별 관리 선택이 들어 있다. 제품명보다 <strong>무슨 목적으로, 누구에게, 어떤 판단을 제공하는지</strong>를 먼저 정의해야 한다.</p><p>식약처는 2026년 의료기기와 개인용 건강관리(웰니스) 제품 판단기준을 개정했다. 다만 이번 조사에서는 첨부 지침의 세부 사례까지 검토하지 못했다.<a class="cite" href="#s20">[20]</a></p><p>의료법 제27조는 무면허 의료행위 등을 제한하며, 의료기사의 업무는 관련 법령에서 정한다. 해외 제품의 전문가 구성을 한국에 그대로 적용할 수는 없다.<a class="cite" href="#s21">[21]</a><a class="cite" href="#s22">[22]</a></p><p>기능 측정이나 운동 안내가 모두 의료행위라는 뜻도, ‘웰니스’라는 이름이면 비의료기기라는 뜻도 아니다. 서비스와 운영 방식을 구체화한 뒤 별도 검토가 필요하다.</p></div></details>
</section>

<section id="validation"><div class="number">06</div><h2>다음 조사에서 확인할 것</h2>
<p>이제 실제 경험자와 전문가를 만나야 한다. “이런 기기가 있으면 쓰겠는가?”보다 <strong>최근에 무엇 때문에 막혔고, 어떻게 해결하려 했는지</strong>를 먼저 묻는다.</p>
<h3>경험자에게 묻기</h3><ol><li>최근 불편함 때문에 진료·운동을 받거나 정보를 찾은 과정을 설명해 달라.</li><li>어떤 답을 원했고, 무엇을 받았으며, 어떤 결정이 남았는가?</li><li>해결하려고 어디에 시간과 돈을 썼고, 계속하거나 중단한 이유는 무엇인가?</li></ol>
<h3>전문가에게 묻기</h3><ol><li>최근 사례에서 무엇을 평가했고, 결과가 관리 선택을 어떻게 바꿨는가?</li><li>기능 이상이 증상의 원인·기여요인인지, 통증의 결과인지 어떻게 구분하는가?</li><li>기존 평가로 답하기 어려운 질문은 무엇인가? 기록·설명·재평가 중 가장 어려운 업무는 무엇인가?</li></ol>
<h3>조사 후 판단하기</h3><ul><li><strong>문제가 반복되는가?</strong> 서로 다른 사람에게 같은 어려움과 해결 행동이 나타나는지 본다.</li><li><strong>무엇이 부족한가?</strong> 새로운 측정 정보인지, 접근성인지, 설명이나 실행 지원인지 구분한다.</li><li><strong>누가 도입하는가?</strong> 이용자와 구매자를 확인하고 실제 파일럿 논의로 이어지는지 본다.</li><li><strong>검증할 수 있는가?</strong> 임상적 주장을 한다면 좁은 질문과 비교 기준을 정할 수 있어야 한다.</li></ul>
<div class="key"><p>다음 산출물은 기기 아이디어 목록이 아니다. <strong>누가 어떤 결정을 내리지 못하고 있으며, 기존 대안으로 왜 해결되지 않는지</strong>를 설명하는 문제 정의다.</p></div>
<details><summary>인터뷰 인원과 후속 검증 계획</summary><div class="detail-body"><p><strong>경험자 9명:</strong> 병원 방문 전 3명, 진료 후 질문이 남은 사람 3명, 운동·재활 중 변화 확인이 필요한 사람 3명으로 시작한다. 최근 3개월의 실제 사건을 중심으로 확인한다.</p><p><strong>전문가 6명:</strong> 정형외과·재활의학과 의사 2명, 물리치료사 2명, 일반 운동·관리 현장 전문가 2명으로 시작한다. 직역별 역할을 구분하며, 가능하면 승인과 동의를 받아 익명화된 사례와 업무 흐름을 살펴본다.</p><p>이는 탐색을 위한 작업안이다. 통계적 대표성이나 임상 성능을 입증하는 표본 설계가 아니다. 건강 자료는 필요한 범위에서 동의를 받아 다룬다.</p><p>후속 단계에서는 가상의 사례로 두 가지 결과 설명을 비교할 수 있다. 하나는 가능한 원인과 추가 확인에, 다른 하나는 측정된 기능과 관리 계획에 초점을 둔다. 이해도, 원인 확정으로 오해하는지, 자신의 추정과 다른 결과를 받아들이는지 확인한다. 이는 임상 유효성 검증이 아니다.</p><p>긍정적인 말만 있고 실제 손실·행동·구매자가 없다면 가설을 수정한다. 기존 평가로 충분하다면 측정기보다 다른 해결 방식을 검토한다. 범용 원인 진단을 약속해야만 가치가 성립한다면 임상 검증 경로부터 다시 확인한다.</p></div></details>
</section>

<section id="sources"><h2>출처와 조사 범위</h2>
<p class="small">임상 평가, 기존 진료·재활, 미충족 요구와 제품을 세 분야로 나눠 조사했다. 가이드라인·학술 자료·국내 기관 안내·공식 제품 설명과 법령을 우선했다. 모든 출처의 확인일은 2026년 10월 26일이다.</p>
<details><summary>조사에서 확인하지 못한 것</summary><div class="detail-body"><p>신속한 범위 탐색이며 체계적 문헌고찰은 아니다. 요통 근거가 상대적으로 많아 고관절·어깨·무릎에 일괄 적용할 수 없다. 국내 가격·급여·대기시간·기관별 평가 빈도·수요·지불의향은 확인하지 못했다.</p><p>한국 환자·전문가 인터뷰, 임상시험, 기기 성능시험을 수행하지 않았다. 질적 인터뷰는 경험을, 회사 문서는 제품 기능을 설명한다. 이를 수요 규모나 독립적인 효과 근거로 취급하지 않았다.</p><p>NICE 권고는 검색 색인으로 확인했으며 직접 열기는 제한됐다. 2026년 업데이트 정황이 있어 2020년을 최신판으로 표시하지 않았고, 영상·자가 관리·운동 관련 절만 사용했다. ACR 2026은 서지·초록·공개 검색 본문을 확인했지만 전문 전체 접근에는 제한이 있었다.</p><p>WHO는 2022년 자료에서 인구 증가·고령화에 따른 근골격 질환과 기능 제한 인구 증가를 설명한다. 약 17.1억 명이라는 수치는 2019년 추정에 근거한다. 이는 질병 부담의 배경이며, 디스크 발생률 증가나 한국의 유료시장 규모를 입증하지 않는다.<a class="cite" href="#s01">[1]</a></p></div></details>
<details class="references" id="source-list"><summary>출처 23개와 자료별 한계 보기</summary><div class="detail-body">__SOURCES__</div></details>
</section>
<footer class="footer"><p>인사이더스 린 프로젝트 · 문제 탐색 단계<br>조사 내용과 사업 가설을 구분했다. 제품·고객·기술·수익모델은 아직 확정하지 않았다.</p><a href="#top">처음으로 ↑</a></footer>
</main>
</div>
</div>
<script>
function revealTarget(hash){
  const target=document.getElementById(hash.slice(1));
  if(!target)return;
  for(let node=target.parentElement;node;node=node.parentElement){
    if(node.tagName==='DETAILS')node.open=true;
  }
  requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));
}
document.addEventListener('click',event=>{
  const link=event.target.closest('a[href^="#"]');
  if(link)revealTarget(link.hash);
});
window.addEventListener('hashchange',()=>revealTarget(location.hash));
if(location.hash)revealTarget(location.hash);
let printState=[];
window.addEventListener('beforeprint',()=>{
  if(printState.length)return;
  printState=Array.from(document.querySelectorAll('details')).map(node=>[node,node.open]);
  printState.forEach(([node])=>node.open=true);
});
window.addEventListener('afterprint',()=>{
  printState.forEach(([node,open])=>node.open=open);
  printState=[];
});
</script>
</body>
</html>
'''
result = template.replace('__SOURCES__', '\n'.join(sources))
report.write_text(result, encoding='utf-8')
print('Updated report; original backed up. Sources retained:', len(sources))
