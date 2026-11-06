from pathlib import Path
from html import escape
import re
import shutil
import json

base = Path(__file__).resolve().parents[2]
report = base / 'outputs' / '\uadfc\uace8\uaca9\uacc4_\ubd88\ud3b8\ud568_\uae30\ub2a5\ud3c9\uac00_\ubb38\uc81c\ud0d0\uc0c9_\ubcf4\uace0\uc11c.html'
original = report.read_text(encoding='utf-8')
backup = Path(__file__).with_name('report-before-expanded-research.html')
if not backup.exists():
    shutil.copy2(report, backup)
original = backup.read_text(encoding='utf-8')
old_sources = re.findall(r'<article class="source" id="s(?:0[1-9]|1[0-9]|2[0-3])">.*?</article>', original, re.S)
assert len(old_sources) == 23
sources = {}

def source(key, title, url, meta, claim, limit, extra=None):
    sources[key] = dict(id=f's{24+len(sources):02}', title=title, url=url, meta=meta, claim=claim, limit=limit, extra=extra)

source('hira','심평원 — 나661 도수근력검사 급여기준','https://www.hira.or.kr/rc/insu/insuadtcrtr/InsuAdtCrtrPopup.do?brdScnBltNo=4&isPopupYn=Y&mtgHmeDd=20231130&mtgMtrRegSno=1&sno=1','공식 기준 · 2023.11.30 게시 / 12.01 시행','부분 근력검사는 기본진료료 포함. 별도 산정 대상과 기록 요건을 구분한다.','2025년 공식 편집본 수록 확인. 2026년까지의 개정 이력 전체는 미검증. 실제 시행 빈도·환자 비용을 뜻하지 않음.',('2025년 10월 심사지침','https://www.hira.or.kr/ebooksc/2025/10/BZ202510212390104.pdf'))
source('nowon','노원삼성정형외과의원 — 스포츠메디컬센터','https://nowonsamsungos.com/sports','국내 의원 공식 안내 · 게시일 미표기','서울 노원구 의원의 ROM·근력·균형 확인, 목표 설정과 단계별 재활 안내.','직접 본문·기관명 확인. 규모 있는 스포츠 진료 기관이며 일반 의원 대표성·실제 시행률·성과는 미확인.')
source('sejong','세종스포츠정형외과의원 — 시설소개','https://www.sjsclinic.com/facilities/','국내 의원 공식 안내 · 게시일 미표기','서울 광진구 의원의 바이오덱스 장비와 스포츠재활 시설 보유 사례.','직접 본문·기관명 확인. 장비 보유가 모든 초진의 검사 시행이나 효과를 증명하지 않음.')
source('nrc','국립재활원 — 물리치료','https://www.nrc.go.kr/hospital/html/content.do?depth=mi&menu_cd=01_05_04_02','국내 공공기관 안내 · 게시일 미표기','근력·관절범위·감각·이동·보행 기능평가와 치료 계획의 연결.','일반 경증 통증 외래를 대표하는 시행률 자료는 아님.')
source('lumbar','AAPM&R — Lumbar Radiculopathy','https://now.aapmr.org/lumbar-radiculopathy/','학회 임상 참조 · 2026.07.30 개정','근력·감각·반사·보행·신경역학과 필요 시 전기진단의 역할.','직접 본문 확인. 개별 진료의 적정성이나 사용자의 검사 결과를 판단하지 않음.')
source('edx','AAPM&R — Electrodiagnosis of Radiculopathies','https://now.aapmr.org/electrodiagnosis-of-radiculopathies-cervical-thoracic-and-lumbar/','학회 임상 참조 · 2023.06.22 개정','침근전도·신경전도·H반사·유발전위의 임상 질문과 한계.','신경근병증의 전문 검사 맥락. 정상 검사로 모든 신경 이상을 배제할 수 없음.')
source('neppain','EAN–EFIC–NeuPSIG — Neuropathic pain assessment','https://pubmed.ncbi.nlm.nih.gov/37253688/','공동 가이드라인 · 2023.05 온라인 / 08 인쇄','신경병증통 진단 경로의 선별도구, QST·신경생리·피부생검의 역할.','공식 초록 확인. 적응증이 다른 검사들을 일반 결림의 일괄 검사로 확대하지 않음.')
source('peripheral','AAPM&R — Peripheral Polyneuropathy Evaluation','https://now.aapmr.org/approach-to-peripheral-polyneuropathy-evaluation-and-differential-diagnosis/','학회 임상 참조 · 2026.05.14 개정','신경병증 유형에 맞춘 검사와 선택된 소섬유·자율신경 평가.','일상적인 근골격 불편함 고객에게 전부 시행하는 근거는 아님.')
source('shoulder','회전근개 건병증 진단·재활 임상지침','https://doi.org/10.2519/jospt.2025.13182','APTA/JOSPT · 2025.01.30 온라인 / 04 인쇄','HHD·ROM·환자보고 평가와 운동 관리. 동적 견갑골 ROM 측정의 제한.','공식 본문/검색 본문 확인. 회전근개 건병증 대상이며 모든 어깨 질환·전거근 원인 판정으로 확대 불가.')
source('pfp','Neal 등 — 슬개대퇴통증 Best-practice guide','https://doi.org/10.1136/bjsports-2024-108110','근거·환자·전문가 종합 · 2024.10.14 온라인','교육을 바탕으로 무릎 ± 고관절 표적 운동, 평가와 개인 필요에 따른 관리 선택.','65개 고품질 RCT·3,796명과 질적 자료를 종합. 모든 무릎 통증을 대상으로 한 지침 아님.')
source('mash','Hicks 등 — MASH 무작위시험','https://pubmed.ncbi.nlm.nih.gov/38258673/','다기관 RCT · 2024.01','60~85세 184명, 요통+고관절 통증·약화 집단에서 고관절 중심 치료 비교.','8주 장애점수 우세, 같은 시점 보행속도 우세 없음. 원인 확정 시험 아님. 공식 초록 확인.')
source('hipreview','고관절 개입과 요통 — 체계적 고찰·메타분석','https://pubmed.ncbi.nlm.nih.gov/37037144/','8개 시험·508명 · 2023.04.05 온라인','고관절 강화·스트레칭의 단기 효과를 검토.','근거 확실성이 매우 낮음. 모든 요통에서 고관절이 원인이라는 주장이나 장기 효과 근거로 사용 불가.')
source('neuroreview','Clinical neurological examination accuracy review','https://pmc.ncbi.nlm.nih.gov/articles/PMC5324296/','12개 연구 고찰 · 2017.02.23','운동·감각·반사·신경역학 검사의 진단 성능과 한계.','오래된 고찰이며 개별 검사 하나로 신경근 병변을 확진·배제하는 근거가 아님.')
source('semgreview','만성 요통의 표면근전도 — 체계적 고찰','https://pubmed.ncbi.nlm.nih.gov/39427457/','11개 연구 · 2024 온라인 / 11 인쇄','굴곡–폄–이완 과제에서 표면근전도의 신뢰도·정확도를 검토.','정확도 편차와 선택·기준검사 편향. 범용 원인 근육 진단기라는 근거는 아님.')
source('cdc','CDC STEADI — 기능평가 자료','https://www.cdc.gov/steadi/hcp/clinical-resources/','공공 임상 자료 · 페이지 날짜 미표기','TUG·30초 의자 일어나기·단계별 균형 검사 안내.','주로 고령자의 낙상 위험 평가 맥락. 기준치를 젊은 요통 환자의 정상치로 사용하지 않음.')
source('kinvent','KINVENT — K-Push / K-Move','https://physio.kinvent.com/page-produit/k-push/','공식 제품 소개 · 발행일 미표기','압박 기반 힘 측정과 IMU 기반 관절각 측정의 별도 제품.','회사 기능 설명과 특정 검사 프로토콜의 실제 성능은 구분.',('K-Move 공식 안내','https://kinvent.com/kinvent-product/goniometer-k-move/'))
source('forceframe','VALD — ForceFrame','https://valdhealth.com/products/forceframe','공식 제품 소개 · 발행일 미표기','프레임 고정 힘 센서를 이용한 등척성 측정·훈련.','모든 검사 방향이 동일하게 타당하거나 장비 간 값이 같다는 근거는 아님.')
source('biodex','Biodex System 4 — 공식 사용설명서','https://biodexrehab.com/wp-content/uploads/2024/08/20-001-CLR-System-4-IFU-Rev-D.pdf','System 4 IFU Rev D · 정확한 발행일 미확인','고정·축 정렬·속도와 모드 설정에 따른 관절 평가·훈련.','2024-08은 업로드 경로. 문서 발행일로 단정하지 않음. 한국 허가·가격은 미확인.')
source('humac','CSMi — HUMAC NORM','https://csmisolutions.com/wp-content/uploads/2024/01/200003E-HUMAC-NORM-Product-Brochure.pdf','공식 제품 브로슈어 · 발행일 미표기','등속성·등척성 등 관절 평가와 재활 모드.','2024-01은 파일 경로이며 발행일을 확정하지 않음. 독립적인 모든 적응증의 효과 자료가 아님.')
source('forcedecks','VALD — ForceDecks','https://valdhealth.com/products/forcedecks','공식 제품 소개 · 발행일 미표기','힘판을 이용한 힘·균형·움직임 과제와 보고서.','측정 지표·장비 모델별 성능 차이와 해당 검증 범위를 확인해야 함.')
source('humantrak','VALD — HumanTrak','https://valdhealth.com/products/humantrak','공식 제품 소개 · 발행일 미표기','카메라 기반 3D 움직임·관절각과 평가 보고서.','현재 제품 설명과 특정 연구 버전의 센서·알고리즘을 동일시하지 않음.')
source('vimove','dorsaVi — ViMove+','https://dorsavi.com/vimove-plus/','현재 제품 공식 소개 · 발행일 미표기','모듈별 착용 센서와 움직임 분석·영상 AI 평가.','구형 ViMove의 IMU+EMG 사양을 현재 ViMove+ 전 모듈에 적용하지 않음.',('현재 교육 자료','https://dorsavi.com/knowledge-center-training-for-vimove/'))
source('delsys','Delsys — Trigno','https://delsys.com/trigno/','공식 제품·사용 문서 · 발행일 미표기','무선 표면 근전기 신호와 구성별 움직임 신호.','부속품별 용도를 구분해야 함. 표면 신호와 침근전도 진단은 다른 검사.',('공식 시스템 사용자 안내','https://www.delsys.com/downloads/USERSGUIDE/trigno/wireless-biofeedback-system.pdf'))
source('noraxon','Noraxon — Ultium EMG','https://www.noraxon.com/our-products/ultium-emg/','공식 제품·매뉴얼 목록 · 2026.05 매뉴얼 색인 확인','표면근전도·IMU 및 구성별 신호 동기화.','표면 EMG 구성과 별도 fine-wire 부속품을 구분. 신호 크기가 곧 근력·원인은 아님.',('공식 매뉴얼 목록','https://www.noraxon.com/support-categories/current-user-manuals/'))
source('natus','Natus — UltraPro S100','https://natus.com/neuro/ultrapro-s100-emg/','공식 전기진단 제품 소개 · 발행일 미표기','NCS·EMG 등 전문 전기진단 프로토콜 지원.','국가별 제공 차이. 특정 질환의 자동 진단 정확도·한국 허가는 별도 확인 필요.')
source('nihon','Nihon Kohden — Neuropack X1','https://eu.nihonkohden.com/products/neurology/neuropack-x1','공식 전기진단 제품 소개 · 발행일 미표기','증폭·자극·기록과 EMG/NCS/유발전위 검사.','신호 수집·보고 기능이 모든 질환의 진단 성능을 뜻하지 않음.')
source('cadwell','Cadwell — Sierra Summit','https://www.cadwell.com/products/electrodiagnostic-products/sierra-summit/','공식 전기진단 제품 소개 · 발행일 미표기','EMG/NCS·유발전위와 프로토콜·기록 지원.','전문 검사 선택과 의학적 해석이 필요. 회사 효율 주장은 임상 효과와 구분.')
source('zebris','zebris — FDM-T 트레드밀 보행 분석','https://www.zebris.de/medizin/dynamische-ganganalyse-auf-dem-laufband','공식 제품 소개 / 확인한 IFU는 2019.12.04','트레드밀 아래 정전용량 압력센서로 보행과 압력 분포 기록.','IFU는 구버전 폴더 문서. 최신 전체 사양·적응증 검증으로 표현하지 않음.',('확인한 2019 IFU','https://www.zebris.de/fileadmin/Editoren/zebris-PDF-Manuals/Medizin/Hardware/Alte_Versionen/FDM-T_Hardware-Manual_Med_191204_en.pdf'))
source('tekscan','Tekscan — Strideway / F-Scan GO','https://www.tekscan.com/gait-analysis-systems','공식 보행 제품 비교 · 발행일 미표기','압력 보행로와 인솔 기반 측정의 서로 다른 구성.','보행로·인솔 결과를 같은 조건으로 취급하지 않음. 통증 원인 진단 성능은 별개.',('Strideway 공식 안내','https://www.tekscan.com/products-solutions/systems/strideway-system'))
source('medoc','Medoc — TSA2 Air','https://www.medoc-web.com/tsa-2air','공식 제품 소개 · 발행일 미표기','온도 자극과 감각·통각 역치 기록을 위한 QST 장비.','환자의 응답이 필요한 감각 평가. 단독으로 신경병증·통증 원인을 모두 확정하지 않음.')
source('kpushtrial','Trybulski 등 — K-Push 반복성 연구','https://pubmed.ncbi.nlm.nih.gov/40630389/','측정 원연구 · 2025.06.24','남성 44명, 선수·비훈련 건강인의 대퇴사두근 힘·힘발달률 반복성.','여성·환자·다른 부위·원인 진단으로 일반화 불가. 이해상충 전체 감사는 미실시.')
source('fftrial','Arp 등 — ForceFrame 타당도·일치도·신뢰도','https://pmc.ncbi.nlm.nih.gov/articles/PMC11368445/','측정 원연구 · 2024.09.01','ACL 손상·재건 후 27명의 무릎 등척성 힘을 다른 장비와 비교.','특정 굽힘 자세에서 낮은 비교 성능과 절대값 차이. 연구위원회가 장비·교통비 지원, 저자 관련 이해상충 없음 보고.')
source('fdtrial','Collings 등 — ForceDecks 타당도·반복성','https://doi.org/10.1016/j.jsams.2024.04.014','측정 원연구 · 2024 온라인 / 08 인쇄','건강인 16명·12개 과제·2회 세션의 힘판 비교.','VALD가 수집·분석·보고 비용을 지원. 저자는 분석 독립 수행을 명시. 모든 지표·환자·임상 효과로 확대 불가.',('연구자 공개 결과·지원 내역','https://tylercollings.github.io/ForceDecks-validity-reliability/'))
source('httrial','HumanTrak 하체 관절각 검증 연구','https://pubmed.ncbi.nlm.nih.gov/40493557/','측정 원연구 · 2025 / 정확한 월일 미확인','17명, V2.9.3의 고관절 ROM·스쿼트·런지와 Vicon 비교.','두 시스템 비동시 측정. 특정 버전·과제·집단의 결과. 상업적 독립성 전체는 미감사.')

def refs(*keys):
    values=[]
    for key in keys:
        ident = key if key.startswith('s') and key[1:].isdigit() else sources[key]['id']
        values.append(f'<a class="cite" href="#{ident}" aria-label="출처 {int(ident[1:])}">[{int(ident[1:])}]</a>')
    return ''.join(values)

methods=[]
def method(name, group, question, how, output, benefit, limit, keys):
    methods.append(dict(name=name,group=group,question=question,how=how,output=output,benefit=benefit,limit=limit,keys=keys))

method('문진·환자보고 설문','기본 평가','무엇이 불편하고 어떤 활동이 중요한가?','병력·악화 상황·목표를 묻고 ODI/RMDQ 등 대상에 맞는 설문을 사용한다.','통증·생활 제한·환자 목표와 경과.','검사 우선순위와 관리 목표를 정하고 환자가 느끼는 변화를 확인한다.','자기보고와 실제 힘·신경 기능은 다른 정보다. 도구의 대상·언어·사용 조건을 확인한다.',['s02','shoulder'])
method('도수근력검사(MMT)','기본 평가','뚜렷한 힘 저하가 있으며 어떤 움직임에 나타나는가?','검사자가 자세를 정하고 저항을 주어 힘을 등급으로 기록한다. 신경 진찰에서는 다른 소견과 분포를 함께 본다.','부위·움직임별 근력 등급.','신경학적 약화 가능성과 재활 시작 수준을 파악한다.','검사자·통증·노력의 영향이 있고 미세한 차이·천장효과에 한계가 있다. 근력 등급과 정밀 힘 측정은 다르다.',['lumbar','hira','shoulder'])
method('각도계·경사계·ROM 평가','기본 평가','어느 방향으로 얼마나 움직이고 어디에서 불편한가?','능동·수동 움직임을 표준 자세에서 각도계·경사계 또는 검증된 앱으로 측정한다.','관절가동범위와 동작 중 증상 반응.','목표 범위와 운동 구성을 정하고 같은 방식으로 변화를 비교한다.','관절·동작별 타당도와 오차가 다르다. 어깨 ROM과 동적 견갑골 ROM을 같은 신뢰도로 취급하지 않는다.',['shoulder','s14'])
method('휴대형·고정형 힘 측정','기본 평가','고관절 외전·신전 등 특정 방향의 힘은 어느 정도인가?','센서를 손·벨트·프레임으로 고정하고 정한 자세에서 힘을 발휘하게 한다.','힘·시간 곡선, 최대 힘, 조건에 따른 토크·좌우·전후 비교.','근육군의 기능 수준과 저항운동 진행을 수치로 검토한다.','자세·고정·레버암·노력에 좌우된다. 반복성이 좋아도 장비 간 절대값이 같거나 원인 진단이 된다는 뜻은 아니다.',['s06','fftrial'])
method('등속성 동력계','기본 평가','일정 속도로 관절을 움직일 때 힘·일·지구력은 어떠한가?','몸과 관절축을 장비에 맞춰 고정하고 속도·운동범위·검사 모드를 설정한다.','토크 곡선·최대 토크·일·파워·반복 중 변화.','관절별 동적 능력과 재활 전후 차이를 자세히 비교한다.','공간·정렬·고정·훈련된 인력이 필요하다. 고립 관절 과제가 실제 생활 동작을 모두 대변하지는 않는다.',['biodex','humac','s14'])
method('동작·지구력·균형 과제','움직임·부하 평가','걷기·일어나기·버티기 등 실제 과제를 얼마나 수행하는가?','걷기·앉았다 일어나기·계단·체간 지구력 등을 표준화한다. 고령자에서는 TUG·의자 일어나기·균형 과제를 선택할 수 있다.','시간·횟수·거리·유지시간·증상 반응.','생활 목표와 훈련량을 정하고 수행 변화를 확인한다.','하나의 과제에는 여러 기능이 관여한다. 고령자 낙상 기준을 젊은 요통 환자 정상치로 사용하지 않는다.',['s05','cdc'])
method('동작관찰·카메라·IMU','움직임·부하 평가','어떤 움직임 전략을 쓰고 안내를 바꾸면 어떻게 달라지는가?','팔 올리기·힌지·스쿼트·보행 등을 관찰하거나 카메라·착용 센서로 기록한다.','각도·시점·속도·분절 관계 및 계산된 움직임 지표.','연습할 동작과 피드백을 구체화하고 반복 과제를 비교한다.','카메라 가림·센서 부착·버전·과제에 영향. 근력·심부근육 활성·조직 부하를 직접 측정한 값과 구분한다.',['s04','humantrak','vimove'])
method('힘판·족저압·보행 분석','움직임·부하 평가','양쪽 발에 어떻게 힘을 싣고 걷기·착지에서 어떻게 분배하는가?','힘판 또는 압력센서 보행로·트레드밀·인솔 위에서 정한 과제를 수행한다.','지면반력·압력중심·발바닥 압력·접촉시간·보행 지표.','균형·하중 전략과 신발·보조기·재활 전후를 비교한다.','힘판과 압력매트·인솔은 측정 신호가 다르다. 특정 근육이나 통증 원인을 직접 알려주는 검사는 아니다.',['forcedecks','zebris','tekscan'])
method('표면근전도(sEMG)','움직임·부하 평가','과제 중 표면 근육의 전기활동과 타이밍은 어떠한가?','피부 전극을 배치하고 정한 과제에서 신호를 수집·정규화한다.','전기활동 진폭·활성 시점·이완 및 근육 간 타이밍.','근육 사용 연습의 피드백과 움직임 분석 정보를 보탠다.','근력 자체가 아니다. 피부·전극 위치·인접 신호에 영향받으며 진단용 침근전도/NCS와도 다르다.',['delsys','noraxon','semgreview'])
method('신경학적 진찰·신경역학 검사','신경 평가','신경근·말초신경과 맞는 약화·감각·반사·증상 분포가 있는가?','움직임별 힘·감각·반사·보행과 필요 시 SLR·slump 등을 함께 확인한다.','소견의 분포와 일치 여부, 증상 재현 양상.','신경 관련 문제를 감별하고 추가 검사·진료의 우선순위를 정한다.','발가락 힘 확인은 이 과정의 일부일 수 있다. 단일 음성 소견으로 모든 신경 문제를 배제하지 않는다.',['lumbar','neuroreview'])
method('신경전도검사(NCS)','신경 평가','말초신경의 전기신호 전달에 이상이 있는가?','신경을 자극하고 정해진 위치의 운동·감각 반응을 기록한다.','잠복기·진폭·전도속도 등 선택 신경별 결과.','말초신경 병변의 위치·특성과 다른 신경 문제의 감별을 돕는다.','검사 신경·온도·기술·병변 유형에 영향. 일부 신경근병증에서 감각 신경전도는 정상일 수 있다.',['edx'])
method('침근전도(needle EMG)','신경 평가','근육의 전기활동에 신경근·말초신경·근육 질환을 시사하는 소견이 있는가?','전문 의료진이 선택한 근육에 침 전극을 넣어 안정·수축 중 활동을 기록한다.','자발활동·운동단위 등 여러 근육의 분포 패턴.','NCS·진찰·영상과 함께 병변의 생리학적 근거와 감별 정보를 보탠다.','시점·검사 근육·운동축삭 침범 여부에 영향. 단독으로 모든 통증 또는 감각성 문제를 설명하지는 않는다.',['edx'])
method('선택적 감각·유발전위·소섬유 검사','신경 평가','일반 신경 검사만으로 설명되지 않는 특정 경로·감각 문제가 있는가?','임상 질문에 따라 QST·유발전위·H반사·피부생검·자율신경검사 등을 각각 선택한다.','감각 역치·유발 반응·소섬유나 자율신경 관련 정보.','선택한 신경병증 가설의 확인과 추가 원인평가를 지원한다.','서로 다른 검사들의 묶음이다. QST는 응답에 의존하며, 일반 결림 고객에게 전부 시행할 평가가 아니다.',['neppain','peripheral','edx'])

products=[]
def product(name,group,short,problem,how,benefit,setting,evidence,keys):
    products.append(dict(name=name,group=group,short=short,problem=problem,how=how,benefit=benefit,setting=setting,evidence=evidence,keys=keys))

product('VALD DynaMo','힘·관절 평가','힘과 가동범위를 휴대 장비로 기록','손으로만 평가하면 힘 차이와 전후 변화를 수치로 남기기 어렵다.','밀기·당기기 힘 센서와 관성 기반 각도 측정. 검사별 힘·시간 곡선·ROM·좌우 결과를 기록한다.','특정 방향의 힘과 범위를 수치로 설명하고 반복 측정 기록을 남긴다.','전문가가 자세·고정·과제를 정해 시행.','공식 기능 확인. 검사자·고정·노력 영향. 개별 근육 원인을 자동 확정하지 않는다.',['s16'])
product('KINVENT K-Push / K-Move','힘·관절 평가','휴대 힘 측정과 착용형 관절각 측정','근육군의 힘과 관절 범위를 쉽게 기록·비교하고 싶다.','K-Push는 압박 힘, K-Move는 IMU 기반 각도를 기록한다. 힘·힘발달률·ROM 등 제품별 출력이 다르다.','휴대 측정과 앱 피드백으로 평가·운동 진행을 확인한다.','의료·운동 전문가의 표준 과제.','K-Push의 남성 44명 대퇴사두근 반복성 연구 확인. 다른 부위·환자·K-Move의 성능까지 검증된 것은 아니다.',['kinvent','kpushtrial'])
product('VALD ForceFrame','힘·관절 평가','프레임에 센서를 고정한 등척성 검사','검사자가 손으로 저항을 유지하는 조건을 줄이고 싶다.','조절 프레임에 힘 센서를 고정하고 정한 자세에서 힘을 잰다. 최대 힘·힘–시간·좌우 결과를 기록한다.','고정된 조건에서 반복 검사와 실시간 힘 목표 피드백을 제공한다.','기관의 공간·자세 설정 필요.','ACL 환자 27명 연구에서 반복성은 좋았지만 특정 굽힘 검사와 비교 장비 일치도에 한계가 있었다.',['forceframe','fftrial'])
product('Biodex System 4 / HUMAC NORM','힘·관절 평가','관절 속도를 제어하며 토크를 측정','관절이 움직이는 동안의 동적 힘·일·지구력을 자세히 알고 싶다.','몸과 축을 맞춰 고정하고 일정 속도 또는 정한 모드로 검사한다. 토크 곡선·일·파워 등을 얻는다.','관절별 능력과 재활 전후 변화를 비교하고 설정한 조건에서 훈련한다.','설치 공간·고정·정렬·숙련 인력 필요.','공식 IFU·브로슈어 확인. 국내 의원 보유 사례도 있음. 생활 기능·통증 원인의 전부를 대변하지 않는다.',['biodex','humac','sejong'])
product('VALD ForceDecks','움직임·부하 평가','서기·점프·착지에서 지면에 가하는 힘','움직일 때 좌우 힘 분배와 힘의 시간 변화를 알고 싶다.','두 힘판 위에서 과제를 수행한다. 지면반력·압력중심과 계산된 충격량·수행 지표를 얻는다.','균형·착지·일어나기 등 부하 전략과 수행 변화를 비교한다.','전문가가 과제·안전·분석 지표를 선택.','건강인 16명·12개 과제 측정 검증. 모든 지표가 동일 성능은 아니며 VALD 지원 연구다. 치료 효과 시험은 아니다.',['forcedecks','fdtrial'])
product('VALD HumanTrak','움직임·부하 평가','카메라로 관절각과 동작을 기록','몸을 움직일 때 여러 분절이 어떻게 움직이는지 정량적으로 보고 싶다.','마커 없는 3D 움직임 추정으로 관절각·ROM·패턴과 보고서를 산출한다.','표준 동작의 반복 비교와 환자 설명을 돕는다.','전문가가 촬영 공간·위치·과제를 설정.','17명 하체 관절각 연구 확인. 특정 버전·과제·집단의 결과이며 힘·심부근육 활성의 직접 측정은 아니다.',['humantrak','httrial'])
product('EverEx MORA Vu / Flexum','움직임·부하 평가','국내 사진·영상 기반 자세·동작평가','진료에서 관절 움직임을 기록하고 이전 결과와 비교하고 싶다.','영상 AI로 자세·관절각·ROM·리포트를 산출한다. 앱과 키오스크 등 제품별 구성을 구분한다.','촬영 평가와 결과 기록·설명을 지원한다.','제품별 의도된 사용자·용도를 확인.','공식 제품·개발자 안내 확인. 의료·웰니스 버전을 합쳐 표현하지 않으며 MORA Vu는 전문가 사용·진단 대체 불가를 표시한다.',['s18','s19'])
product('dorsaVi ViMove+','움직임·부하 평가','착용 센서로 움직임과 비대칭을 기록','카메라만으로 기록하기 어려운 과제의 움직임을 반복 평가하고 싶다.','모듈별 2~4개 착용 센서, 일부 영상 AI 평가. 동작·균형·케이던스 등 모듈별 지표를 산출한다.','센서 기반 반복 평가와 움직임 코칭에 정보를 보탠다.','전문가가 센서 위치·모듈·과제를 선택.','공식 현재 제품 확인. 구형 ViMove의 IMU+EMG 사양과 혼용하지 않음. IMU는 힘판처럼 지면반력을 직접 재지 않는다.',['vimove'])
product('Delsys Trigno','근육 전기활동','과제 중 표면 근육 전기활동을 기록','힘·각도만으로 알 수 없는 근육 사용 타이밍을 보고 싶다.','피부 전극으로 전기신호를 수집하고 활성 시점·진폭·정규화 패턴을 분석한다.','바이오피드백과 과제별 근육 사용 연습·연구를 지원한다.','전극 배치·신호 처리에 숙련된 인력.','공식 제품·매뉴얼 확인. 피부·인접근 신호·정규화 영향을 받으며 신호 크기가 곧 힘이나 원인은 아니다.',['delsys','semgreview'])
product('Noraxon Ultium EMG','근육 전기활동','표면근전도와 움직임 신호를 동기화','근육 전기활동이 어떤 움직임·부하 시점에 나타나는지 함께 보고 싶다.','무선 sEMG·내장 IMU와 구성별 다른 센서 신호를 동기화한다.','임상·스포츠·인체공학의 과제 분석과 피드백 정보를 보탠다.','센서·부속품·분석 프로토콜 설정 필요.','공식 제품·매뉴얼 목록 확인. 일반 표면 EMG와 별도 fine-wire 부속품을 구분한다. 진단용 NCS를 대신하지 않는다.',['noraxon'])
product('Natus UltraPro S100','전문 신경 평가','EMG/NCS 전문 전기진단 시스템','신경·근육 질환의 특정 임상 질문에 생리학적 정보가 필요하다.','자극·증폭·기록 장비로 NCS와 침근전도 등의 파형·잠복기·진폭·운동단위 정보를 얻는다.','진찰·영상과 함께 신경·근육 병변의 감별과 위치 판단을 지원한다.','전문 의료진의 검사 선택·해석.','공식 기능 확인. 국가별 제공 차이. 특정 질환의 자동 진단 정확도·한국 허가는 별도 확인이 필요하다.',['natus','edx'])
product('Nihon Kohden Neuropack X1','전문 신경 평가','다채널 EMG/NCS·유발전위 시스템','선택한 신경 경로·근육의 전기반응을 측정하고 해석해야 한다.','자극기·증폭기·검사 소프트웨어로 신경전도·근전도·유발반응과 보고서를 기록한다.','전문 신경생리 검사의 표준 절차와 기록을 지원한다.','병원 신경생리·재활의학 검사 환경.','공식 기능 확인. 수집·보고 기능 자체가 질환별 자동 진단 정확도를 뜻하지 않는다.',['nihon','edx'])
product('Cadwell Sierra Summit','전문 신경 평가','전기진단 검사와 기록·보고 지원','여러 전기진단 프로토콜을 수행하고 결과를 정리해야 한다.','EMG/NCS·유발전위 검사와 프로토콜·기록·보고 기능을 제공한다.','전문가의 검사 수행과 의학적 해석에 필요한 파형·정보를 제공한다.','신경생리 전문 인력·전극·검사 설정 필요.','공식 기능 확인. 회사의 신호품질·효율 설명은 독립적 질환별 진단 성능과 구분한다.',['cadwell','edx'])
product('zebris FDM-T','보행·발바닥 압력','트레드밀에서 여러 걸음의 압력 분포 측정','보행 중 어느 발·부위에 언제 부하가 실리는지 알고 싶다.','벨트 아래 정전용량 압력센서로 접촉·압력·보행주기와 좌우 결과를 기록한다.','같은 속도 조건에서 보행·신발·재활 전후를 비교한다.','전문시설·훈련 인력·속도 설정·안전 확보.','공식 안내와 2019 IFU 확인. 최신 전체 사양 검증은 아니며 트레드밀과 지상 보행은 다를 수 있다.',['zebris'])
product('Tekscan Strideway / F-Scan GO','보행·발바닥 압력','보행로 또는 신발 안의 압력 측정','걷거나 신발·보조기를 사용할 때 발의 접촉 압력을 알고 싶다.','Strideway 보행로 또는 F-Scan GO 인솔 센서로 압력·접촉·보행 지표를 기록한다.','신발·보조기 조건과 보행·재활 변화를 비교한다.','측정 환경·센서 보정·반복 걸음 수 설정.','공식 제품 비교 확인. 보행로와 인솔은 같은 조건이 아니며 압력만으로 허리·고관절의 원인을 특정하지 않는다.',['tekscan'])
product('Medoc TSA2 Air','전문 신경 평가','온도 감각·통각 역치를 기록','선택한 환자의 냉·온 감각과 통증 반응을 정량화하고 싶다.','온도 자극을 제어하고 사용자의 감지·통각 응답으로 역치를 기록한다.','특정 신경병증 평가와 감각 특성 연구에 보조 정보를 제공한다.','임상·연구 전문가의 표준 자극 절차.','공식 기능과 신경병증통 지침 확인. 응답·주의의 영향을 받으며 QST 단독으로 병변 위치·원인을 확정하지 않는다.',['medoc','neppain'])
product('Hinge Health / Physitrack','일상 관리·연결','평가 이후 운동·피드백·추적 연결','평가나 운동 안내를 받은 뒤 생활에서 실행·추적이 끊긴다.','설문·운동 과제·수행 및 불편감 보고·피드백·전문가 관리를 서비스별로 연결한다.','관리 수행과 경과 공유를 이어가도록 돕는다.','Hinge는 미국 기업·보험 모델, Physitrack은 전문가의 운동 배정·환자 앱 사용.','공식 기능 확인. 새 신경 진단 신호를 제공하는 장비와 다르며 한국 결제 수요·치료 효과는 별도 검증이다.',['s15','s17'])

group_order = list(dict.fromkeys(item['group'] for item in products))
products.sort(key=lambda item: group_order.index(item['group']))

def field(label, value):
    return f'<dt>{label}</dt><dd>{escape(value)}</dd>'

def method_cards():
    result=[]
    for group in dict.fromkeys(x['group'] for x in methods):
        result.append(f'<h3 class="catalog-group">{group}</h3>')
        for i,x in enumerate(methods,1):
            if x['group'] != group: continue
            fields=''.join(field(k,x[v]) for k,v in [('방식','how'),('얻는 정보','output'),('기대효과','benefit'),('해석의 한계','limit')])
            result.append(f'<details class="catalog method-card" id="method-{i:02}"><summary><span class="catalog-no">{i:02}</span><span><strong>{escape(x["name"])}</strong><span class="catalog-question">{escape(x["question"])}</span></span></summary><div class="detail-body"><dl class="spec">{fields}</dl><p class="small">관련 근거 {refs(*x["keys"])}</p></div></details>')
    return ''.join(result)

def product_cards():
    result=[]
    for group in dict.fromkeys(x['group'] for x in products):
        result.append(f'<h3 class="catalog-group">{group}</h3>')
        for i,x in enumerate(products,1):
            if x['group'] != group: continue
            fields=''.join(field(k,x[v]) for k,v in [('해결하려는 문제','problem'),('방식·얻는 값','how'),('기대효과','benefit'),('사용 환경','setting'),('확인한 근거·한계','evidence')])
            result.append(f'<details class="catalog product-card" id="product-{i:02}"><summary><span class="catalog-no">{i:02}</span><span><strong>{escape(x["name"])}</strong><span class="catalog-question">{escape(x["short"])}</span></span></summary><div class="detail-body"><dl class="spec">{fields}</dl><p class="small">공식 자료·관련 근거 {refs(*x["keys"])}</p></div></details>')
    return ''.join(result)

def new_source_cards():
    result=[]
    for x in sources.values():
        extra=''
        if x['extra']:
            label,url=x['extra']; extra=f'<p><a href="{escape(url,quote=True)}" target="_blank" rel="noopener noreferrer">{escape(label)}</a></p>'
        result.append(f'<article class="source" id="{x["id"]}"><div class="source-meta">{int(x["id"][1:])} · {escape(x["meta"])}</div><h3><a href="{escape(x["url"],quote=True)}" target="_blank" rel="noopener noreferrer">{escape(x["title"])}</a></h3><p>{escape(x["claim"])}</p>{extra}<p class="limit">{escape(x["limit"])}</p></article>')
    return ''.join(result)

summary=f'''<section id="summary"><div class="summary"><h2>추가 조사에서 확인한 세 가지</h2><ul><li><strong>평가가 있어도, 필요한 사람이 원하는 답을 얻는 것은 별개다.</strong> 사용자의 경험은 접근·평가 내용·결과 설명의 공백을 조사할 이유가 된다. 다만 기존 평가의 효과가 없다는 증거는 아니다.</li><li><strong>근육군·기능계를 평가해 관리 표적으로 삼을 수 있다.</strong> 실제 임상 지침과 하위집단 비교시험이 있다. 기능 저하의 확인, 증상 기여 가능성, 원인 확정은 구분한다.{refs('s04','pfp','mash')}</li><li><strong>기능·신경 평가는 서로 다른 질문에 답한다.</strong> 이번에는 평가 13종과 대표 제품·서비스 17묶음을 문제·방식·기대효과별로 정리했다.</li></ul></div><p>핵심은 “기기가 있느냐”보다 <strong>내가 알고 싶은 것을 평가해 주고, 그 결과로 다음 행동을 정할 수 있느냐</strong>다. 기존 기술을 더 쉽게 전달하는 서비스도, 특정 판단을 개선하는 새 기기도 사업 가설이 될 수 있다.</p><p class="small">2026.10.26 기준 추가 조사. 초음파 아이디어는 제외했다. 특정 검사를 개인에게 권하거나 증상을 진단하는 보고서는 아니다.</p></section>'''

access=f'''<section id="problem"><div class="number">01</div><h2>있는데 왜 나는 받아보지 못했을까?</h2><p class="intro">사용자의 문제 인식은 여전히 의미가 있다. 다만 <strong>평가의 의학적 효과</strong>와 <strong>실제 진료에서 제공·이해·활용되는 정도</strong>를 나눠 봐야 한다.</p><h3>발가락 힘 확인과 상세 기능평가는 목적이 다를 수 있다</h3><p>발가락의 힘을 확인하는 진찰은 신경 기능 저하를 살피는 과정의 일부일 수 있다. 반면 사용자가 원하는 것은 고관절·체간·하체의 힘, 지구력과 움직임을 평가해 관리 방향을 정하는 것이다.{refs('lumbar')}</p><p><strong>“신경에 뚜렷한 이상이 있는가?”와 “어떤 기능을 어떻게 관리해야 하는가?”는 같은 질문이 아니다.</strong> 진료기록을 보지 않은 상태에서 받은 진찰이 충분했는지 또는 어떤 검사였는지는 판단할 수 없다.</p><h3>대학병원 밖에서도 제공하는 사례가 있다</h3><div class="case"><h3>노원삼성정형외과의원 · 서울 노원</h3><p>공식 진료 안내에 관절가동범위·근력·균형 확인, 목표 설정, 단계별 재활을 명시한다. 의원급 기능평가의 사례다.{refs('nowon')}</p></div><div class="case"><h3>세종스포츠정형외과의원 · 서울 광진</h3><p>공식 시설 안내에서 바이오덱스 장비와 스포츠재활 시설을 확인했다. 의원급에서도 장비를 보유할 수 있다는 사례다.{refs('sejong')}</p></div><p>두 곳 모두 재활·스포츠 진료 시설을 갖춘 규모 있는 의원이다. <strong>일반 동네 의원에서도 쉽게 받을 수 있다는 뜻은 아니다.</strong> 모든 초진의 검사 시행 여부·시간·비용·성과와 전국 보급률은 확인하지 못했다.</p><details><summary>수가 기준에서 확인한 점</summary><div class="detail-body"><p>심평원의 나661 기준은 국소적인 단순 근골격계 질환이나 1~2개 관절의 부분 근력검사를 일반 이학적 진찰로 보아 기본진료료에 포함한다. 전반적 근력평가의 별도 산정에는 대상과 기록 요건이 있다.{refs('hira')}</p><p>따라서 <strong>별도 검사비를 청구하지 않았다고 평가를 하지 않은 것은 아니다.</strong> 반대로, 이 구조 때문에 상세 평가가 생략된다고 단정할 수도 없다. 실제 시간·인력·보상·필요성은 현장에서 확인해야 한다.</p><p class="small">2023 공고 기준과 2025년 공식 편집본 수록을 확인했다. 2026년까지 개정 이력 전체는 검증하지 않았으며 현재 환자 부담액을 산정한 자료가 아니다.</p></div></details><div class="key"><p>사업 기회는 남아 있다. <strong>평가가 없어서인지, 접근이 어려워서인지, 질문이 달라서인지, 결과가 관리로 이어지지 않아서인지</strong>를 확인하면 해결 방식도 달라진다.</p></div><details><summary>접근성 문제를 구분할 네 가지 질문</summary><div class="detail-body"><ol><li>어떤 기능이 궁금한 환자가 어디로 가야 하는지 아는가?</li><li>그 기관에서 필요한 평가를 받을 수 있고 시간·비용을 감당할 수 있는가?</li><li>평가가 단순 신경 확인인지, 상세 기능 측정인지, 관리계획까지 포함하는지 알 수 있는가?</li><li>평가 결과를 이해하고 운동·재평가로 이어갈 수 있는가?</li></ol><p>사용자의 경험은 이 질문들을 조사할 출발점이다. 반복되는 문제와 실제 행동을 확인해야 새 솔루션의 필요성을 판단할 수 있다.</p></div></details></section>'''

clinical=f'''<section id="clinical"><div class="number">02</div><h2>근육군을 문제로 지목할 수는 있지 않을까?</h2><p class="intro"><strong>근육군이나 기능계를 평가하고 관리 표적으로 삼는 것은 가능하다.</strong> 고관절 외전·신전의 힘, 체간 지구력·운동조절, 무릎 부하 내성처럼 구체적인 단위로 접근한다.</p><p>다만 “기능이 부족하다”는 판단과 “그것이 통증을 일으켰다”는 주장은 다르다. 근육 하나 대신 집단을 지목하더라도, 원인이라는 주장이 자동으로 증명되지는 않는다.</p><ol class="steps"><li><strong>확인된 기능 저하</strong><p>정한 자세에서 고관절 외전 힘이 낮다. 어떤 조건에서 얼마나 낮고, 오차와 구분되는지 기록한다.</p></li><li><strong>증상에 기여할 가능성</strong><p>증상·과제·다른 소견을 함께 보고 기능 변화나 동작 조절이 어떤 반응과 연결되는지 검토한다. 임상 가설로 삼고 다시 확인할 수 있다.</p></li><li><strong>관리 표적으로서의 가치</strong><p>그 기능을 겨냥한 개입이 적합한 환자에게 도움이 되는지 본다. 원인을 완전히 확정하기 전에도 유용한 관리 선택은 가능하다.</p></li></ol><h3>실제 관리에 연결된 사례</h3><div class="block"><h3>허리 통증과 고관절 기능</h3><p>MASH 시험은 요통과 고관절 통증·약화가 함께 있는 60~85세 184명을 비교했다. 고관절 중심 치료가 8주 장애점수에서는 유리했고, 같은 시점 보행속도에서는 우세하지 않았다. <strong>특정 기능 소견으로 환자군을 나누고 관리를 비교한 사례</strong>다.{refs('mash')}</p><p class="small">고관절이 모든 요통의 원인이었다는 시험은 아니다. 젊은 사용자·일반 요통으로 그대로 확대할 수 없으며, 저자들도 실제 적용 전 추가 조사를 요구한다.</p></div><div class="block"><h3>슬개대퇴 통증과 무릎·고관절 기능</h3><p>2024 지침은 교육을 바탕으로 무릎 표적 운동을 제공하고, 필요에 따라 고관절 표적 운동 등을 선택하도록 안내한다. <strong>평가한 기능·부하 내성·목표가 관리 구성을 바꿀 수 있다.</strong>{refs('pfp')}</p><p class="small">슬개대퇴 통증으로 확인된 상황의 근거이며, X-ray가 정상인 모든 무릎 통증에 같은 설명을 적용하지 않는다.</p></div><div class="block"><h3>어깨 힘·가동범위와 견갑대 조절</h3><p>2025 회전근개 건병증 지침은 HHD를 이용한 힘 측정과 관절가동범위·환자보고 평가를 권고한다. 동시에 <strong>동적 견갑골 ROM 수치의 신뢰도·타당도에는 한계</strong>가 있다고 설명한다.{refs('shoulder')}</p><p class="small">어깨의 힘과 활동 제한을 평가할 수 있다는 것과 카메라의 견갑골 각도로 전거근을 원인 판정한다는 것은 다르다.</p></div><div class="notice"><p><strong>신경 검사는 또 다른 임상 정보를 줄 수 있다.</strong> 근력·감각·반사 분포와 침근전도/NCS가 일치하면 특정 신경근·말초신경 병변의 판단에 도움을 준다. 모든 기능평가를 ‘원인을 알 수 없는 점수’로 묶는 것도 부정확하다.{refs('lumbar','edx')}</p></div><details><summary>연관·예측·치료 반응·원인 주장을 구분하기</summary><div class="detail-body"><ul><li><strong>연관:</strong> 통증과 기능 저하가 함께 나타난다.</li><li><strong>예측:</strong> 특정 소견이 이후 경과와 관련된다.</li><li><strong>치료 반응:</strong> 그 기능을 겨냥한 관리가 비교군보다 도움이 된다.</li><li><strong>인과:</strong> 시간적 선후·다른 요인·역인과 등을 고려해 기능 변화가 증상을 바꾸는 경로를 설명한다.</li></ul><p>치료 효과가 있었다고 처음 지목한 원인이 전부 입증되는 것은 아니다. 반대로 인과가 완전히 확정되지 않았다고 관리 선택의 가치가 없어지는 것도 아니다.</p><p>2023년 고관절 개입 고찰은 8개 시험·508명을 검토했지만 근거 확실성이 매우 낮았다. MASH의 특정 집단 결과와 일반 요통 전체의 근거를 구분해야 한다.{refs('hipreview')}</p><p>MASH의 8주 QBPDS 군간 차이는 4.0점(95% CI 0.5~7.5)이었다. 보행속도 차이는 0.004m/s(95% CI -0.044~0.052)였고, 6개월에는 두 군 모두 개선됐다. 기능별 결과가 같은 방향이라고 가정하지 않는다.{refs('mash')}</p></div></details></section>'''

catalog=f'''<section id="pathway"><div class="number">03</div><h2>기능·신경 평가 13종</h2><p>검사 이름보다 <strong>어떤 질문에 답하고, 결과가 무엇을 바꾸는지</strong>를 기준으로 정리했다. 원하는 항목을 펼치면 방식·결과·기대효과·한계를 볼 수 있다.</p><p class="small">모든 사람에게 전부 시행할 목록은 아니다. 신경 진찰, 정밀 힘 측정, 전기진단은 대상과 목적이 다르다. 아래 ‘기대효과’는 평가가 보탤 수 있는 의사결정 가치이며 검사 자체가 통증을 개선한다는 뜻은 아니다.</p>{method_cards()}<div class="key"><p>엄지발가락 검사는 이 지도에서 <strong>신경학적 진찰</strong>에 가까울 수 있다. 사용자가 궁금한 고관절·몸통·하체의 상세 능력은 다른 평가 조합이 답할 수 있는 질문이다.</p></div></section>'''

devices=f'''<section id="needs"><div class="number">04</div><h2>관련 제품·서비스 17묶음</h2><p><strong>힘, 각도, 지면반력, 근육 전기활동, 신경전도는 서로 다른 신호다.</strong> 무엇을 직접 측정하고 무엇을 계산·해석하는지 구분해야 제품 역할이 보인다.</p><p class="small">구매 추천이나 성능 순위가 아니다. 가격·국내 유통·한국 허가는 확인하지 않았다. ‘기대효과’는 사용 목적과 실무상 기대 가치다. 회사 설명, 측정 검증, 실제 임상 효과를 아래에서 구분한다.</p>{product_cards()}<details><summary>제품 검증 논문이 있어도 확인 범위는 다르다</summary><div class="detail-body"><h3>K-Push · 힘 검사의 반복성</h3><p>2025 연구는 남성 44명의 대퇴사두근 힘·힘발달률을 검사했다. 해당 프로토콜의 반복성을 지지하지만 환자·다른 근육·다른 제품 또는 통증 원인 진단까지 검증한 것은 아니다.{refs('kpushtrial')}</p><h3>ForceFrame · 반복성과 장비 간 일치도의 차이</h3><p>ACL 손상·재건 후 27명 연구에서 반복성은 양호했지만 비교 장비와의 일치도에는 차이가 있었다. 특히 연구의 무릎 굽힘 자세는 적절하지 않을 수 있다고 보고했다. 장비가 고정돼 있다고 모든 과제가 같은 성능을 갖는 것은 아니다.{refs('fftrial')}</p><h3>ForceDecks · 지표별 성능과 제조사 지원</h3><p>건강인 16명·12개 과제 연구는 모든 지표에서 같은 성능을 보인 것은 아니다. VALD가 수집·분석·보고 비용을 지원했고, 저자는 분석을 독립 수행했다고 밝혔다. ‘독립 검증 완료’라는 표현만으로 요약하지 않는다.{refs('fdtrial')}</p><h3>HumanTrak · 버전·관절·과제의 범위</h3><p>17명 연구는 V2.9.3의 고관절 ROM·스쿼트·런지를 Vicon과 비교했다. 두 시스템의 측정은 동시가 아니었다. 해당 결과를 모든 관절·환자·현재 버전의 성능으로 확대할 수 없다.{refs('httrial')}</p><p><strong>측정이 정확한가 → 판단이 달라지는가 → 환자의 결과가 좋아지는가</strong>는 각각 다른 검증 질문이다. 기존 RESTORE 시험에서도 관리의 가치와 센서 추가 가치는 구분됐다.{refs('s10')}</p></div></details></section>'''

opportunities=f'''<section id="opportunities"><div class="number">05</div><h2>그렇다면 어떤 솔루션이 의미가 있나?</h2><p>사용자의 문제 인식은 <strong>“기능평가를 새로 발명해야 한다”보다 “내 질문에 답하는 평가와 관리를 받을 수 있어야 한다”</strong>로 구체화할 수 있다. 새 하드웨어가 필요한지, 기존 평가를 더 잘 전달해야 하는지는 아직 열려 있다.</p><article class="topic"><span class="label">접근의 문제</span><h3>가까운 곳에서 필요한 평가를 받기 어렵다</h3><p>기본 진찰과 상세 기능평가의 차이를 설명하고, 목적에 맞는 평가·기관으로 연결한다.</p><p class="small"><strong>검증:</strong> 실제로 어디에서 막히는가? 제공 기관을 모르는가, 시간·비용 부담인가, 필요한 평가를 받지 못하는가?</p></article><article class="topic"><span class="label">검사 선택·해석의 문제</span><h3>어떤 기능을 재야 내 추정을 확인할 수 있는지 모른다</h3><p>특정 고객과 활동에 맞는 평가 조합을 정하고, 기능 저하·기여 가능성·신경학적 이상을 구분해 전문가 판단을 돕는다.</p><p class="small"><strong>검증:</strong> 추가 정보가 실제 어떤 결정을 바꾸는가? 기존 도구로 얻을 수 없는 정보인가, 선택·표준화·해석이 어려운가?</p></article><article class="topic"><span class="label">관리 연결의 문제</span><h3>결과는 받았지만 무엇을 어떻게 해야 할지 모른다</h3><p>확인한 기능과 목표를 운동·생활 계획에 연결하고, 수행 피드백과 재평가를 이어간다.</p><p class="small"><strong>검증:</strong> 새로운 진단명이 필요한가, 실행 가능한 계획과 피드백이 필요한가? 기록·설명·재평가 중 무엇이 끊기는가?</p></article><div class="notice"><p><strong>‘기존에 있다’는 이유만으로 기회가 없어지지 않는다.</strong> 다만 ‘나는 못 받았다’에서 곧바로 ‘기존 검사는 효과가 없다’ 또는 ‘내 솔루션이 효과적이다’로 넘어갈 수는 없다. 문제의 반복성과 새 해결책의 가치를 각각 확인해야 한다.</p></div><details><summary>웰니스·의료기기와 운영 역할</summary><div class="detail-body"><p>일반 운동 수행 기록, 신경 병변의 진단 정보, 통증 원인 해석과 개인 치료 선택은 제공하는 판단이 다르다. 사용자·사용목적·결과·책임과 운영 환경을 구체화한 뒤 제품 분류와 직역을 검토해야 한다.{refs('s20','s21','s22')}</p><p>기능 측정이나 운동 안내가 모두 의료행위라는 뜻도, ‘웰니스’라는 이름이면 비의료기기라는 뜻도 아니다. 해외 제품의 케어팀 모델을 국내에 그대로 적용하지 않는다.</p></div></details></section>'''

validation=f'''<section id="validation"><div class="number">06</div><h2>다음 검증은 ‘왜 안 받았는가’부터</h2><h3>환자에게: 실제 진료와 남은 질문을 재구성한다</h3><ol><li>어떤 이유로 어느 기관을 방문했고, 기억나는 진찰·검사는 무엇이었는가?</li><li>검사가 확인한 것과 자신이 알고 싶었던 것이 어떻게 달랐는가?</li><li>근력·ROM·움직임의 상세 평가가 있다는 것을 알았는가? 받아보려 한 적이 있는가?</li><li>추가 평가나 운동 관리에 실제로 시간·돈을 썼는가? 어떤 답을 얻지 못했는가?</li></ol><h3>전문가에게: 실제 선택과 운영을 확인한다</h3><ol><li>최근 요통·고관절·어깨 환자에게 어떤 신경·기능평가를 선택했고, 하지 않은 평가는 왜 제외했는가?</li><li>기능 저하가 증상의 원인·기여요인인지, 통증의 결과인지 어떻게 구분하는가?</li><li>근육군 단위의 어떤 수치·증상 반응이 운동 선택이나 추가 검사·의뢰를 바꾸는가?</li><li>일상 외래에 넣기 어려운 이유는 필요성·시간·인력·장비·수가·해석·추적 중 무엇인가?</li></ol><h3>실제 평가 과정을 관찰한다</h3><p>의료기관의 승인과 당사자 동의 아래 <strong>평가 선택 → 검사 → 설명 → 관리계획 → 재평가</strong>를 살펴본다. 의원급과 재활·스포츠 진료 기관을 구분하고, 장비 보유와 실제 사용을 나눠 기록한다.</p><p>기존 평가를 이용해 먼저 확인할 수 있는 질문이라면 작은 파일럿으로 관리 연결의 가치를 확인한다. 새 측정이 필요하다면 어떤 판단을 개선하는지와 비교 기준을 먼저 정한다.</p><details><summary>시작 표본과 판단 기준</summary><div class="detail-body"><p>경험자 9명과 전문가 6명으로 시작할 수 있다. 병원 방문 전·진료 후 질문이 남은 경우·운동 중 변화 확인이 필요한 경우를 나누고, 전문가도 의원·전문 재활 환경과 역할을 구분한다. 이는 탐색용 표본이며 대표성 있는 보급률 조사가 아니다.</p><p>반복되는 미해결 결정, 이미 지출한 시간·비용, 기존 대안의 한계, 도입 주체와 실제 파일럿 참여를 근거로 가설을 유지·수정한다. 긍정적 반응만으로 수요가 확인됐다고 하지 않는다.</p><p>평가 추가 전후에 전문가의 판단·설명 시간·환자 이해·실행·기능 변화가 어떻게 달라지는지 분리해서 확인한다. 원인 판정이나 의뢰·운동 선택의 임상적 주장을 하려면 적합한 비교·검증 설계가 별도로 필요하다.</p></div></details></section>'''

source_section=f'''<section id="sources"><h2>출처와 조사 범위</h2><p class="small">모든 자료 확인일은 2026.10.26이다. 임상 근거, 국내 제공 사례·급여 기준, 제품 공식 문서와 측정 검증 연구를 나눠 확인했다. 기존 출처 23개에 추가 자료 {len(sources)}개를 연결했다.</p><details><summary>어디까지 확인했고 무엇은 남았나?</summary><div class="detail-body"><p>신속한 범위 탐색이며 체계적 문헌고찰은 아니다. 제품의 공식 기능 소개, 특정 조건의 측정 검증, 임상 효과 연구를 같은 수준으로 취급하지 않았다. 평가와 제품 목록은 전체 시장을 빠짐없이 조사한 목록이 아니다.</p><p>국내 기관 운영 안내는 직접 확인했지만, 실제 사용량·대기시간·가격·일반 동네 의원 보급률은 확인하지 못했다. 전화·현장 조사, 전문가 인터뷰와 개인 진료기록 검토를 수행하지 않았다.</p><p>심평원은 2023 공고와 2025 편집본을 확인했으며 2026 개정 이력 전체는 검증하지 못했다. 제품의 한국 허가·국내 유통·현재 가격은 확인하지 않았다. 구버전 매뉴얼·연구는 해당 조건에 한정했다.</p><p>기존 NICE 권고의 직접 접근 제한, ACR 전문 접근 제한 등은 기존 출처 설명에 남겼다. 새 임상 자료의 일부는 공식 초록·검색 본문으로 확인했으며 원문 전체를 일괄 검토한 것은 아니다.</p><p>사용자의 문제 인식은 보존하되 진단된 원인으로 다루지 않았다. 새 자료는 의원급 접근 가능성과 기능계별 관리 선택의 가치를 보완하며, 전국 보급이나 개인의 원인·치료를 확정하지 않는다.</p></div></details><details class="references" id="source-list"><summary>출처 {23+len(sources)}개와 자료별 한계 보기</summary><div class="detail-body">{''.join(old_sources)}{new_source_cards()}</div></details></section>'''

sections = [summary,access,clinical,catalog,devices,opportunities,validation,source_section]
navigation=[('summary','핵심 결론'),('problem','1. 실제로 받기 어려운 이유'),('clinical','2. 근육군과 원인 판단'),('pathway','3. 평가 방법 13종'),('needs','4. 관련 제품 17묶음'),('opportunities','5. 솔루션의 기회'),('validation','6. 다음 검증'),('sources','출처와 조사 범위')]
links=''.join(f'<a href="#{ident}">{label}</a>' for ident,label in navigation)
result=re.sub(r'<aside class="sidebar">.*?</aside>',f'<aside class="sidebar"><nav aria-label="보고서 목차"><div class="nav-title">목차</div>{links}</nav><p class="nav-note">핵심 답변은 1·2장에,<br>평가와 제품은 3·4장에<br>정리했습니다.</p></aside>',original,flags=re.S)
start=result.index('<main id="main">')
end=result.index('</main>',start)
mobile=f'<details class="mobile-nav"><summary>목차</summary><nav class="detail-body" aria-label="모바일 목차">{links}</nav></details>'
footer='<footer class="footer"><p>인사이더스 린 프로젝트 · 기능·신경 평가 확장 조사<br>사업 가설과 임상 근거를 구분했다. 제품·고객·수익모델은 아직 확정하지 않았다.</p><a href="#top">처음으로 ↑</a></footer>'
result=result[:start]+'<main id="main">'+mobile+''.join(sections)+footer+result[end:]
result=result.replace('조사 기준 2026.10.26 · 출처 23개','2026.10.26 추가 조사 · 평가 13종 · 제품 17묶음')
result=result.replace('웰니스·의료기기 아이디어를 찾기 위한 문제 조사','접근성 · 근육군의 역할 · 기능·신경 평가와 관련 제품')
extra_css='''
.catalog-group{font-size:18px;margin:32px 0 12px;color:var(--accent)}
.catalog{margin:11px 0}.catalog>summary{display:flex;align-items:flex-start;gap:13px;padding:16px 18px;list-style:none}.catalog>summary::-webkit-details-marker{display:none}.catalog>summary::after{content:'+';font-size:20px;color:var(--accent);margin-left:auto;flex-shrink:0}.catalog[open]>summary::after{content:'−'}.catalog-no{font-size:12px;color:#697f75;padding-top:2px;min-width:20px}.catalog-question{display:block;font-size:14px;font-weight:400;color:var(--muted);margin-top:4px}.spec{margin:0}.spec dt{font-size:13px;font-weight:800;color:var(--accent);margin:17px 0 4px}.spec dt:first-child{margin-top:0}.spec dd{margin:0;font-size:15px;line-height:1.9}.catalog .small{margin:19px 0 0}.catalog .detail-body{padding:20px 25px}.catalog summary strong{font-size:16px}
@media(max-width:760px){.catalog>summary{padding:15px 13px;gap:9px}.catalog summary strong{font-size:15px}.catalog-question{font-size:13px}.catalog .detail-body{padding:18px}.spec dd{font-size:14px}}
@media print{.catalog>summary{padding:10px 13px}.catalog .detail-body{padding:12px}.catalog{break-inside:auto}.spec dd{font-size:9.5pt}.spec dt{font-size:9pt}.catalog-question{font-size:9pt}.catalog>summary::after{display:none}.spec dt{break-after:avoid}.spec dd{break-inside:avoid}}
'''
result=result.replace('</style>',extra_css+'</style>')
report.write_text(result,encoding='utf-8')
data=dict(methods=methods,products=products,sources=sources,total_sources=23+len(sources))
Path(__file__).with_name('expanded-research-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(methods=len(methods),product_groups=len(products),new_sources=len(sources),total_sources=23+len(sources),report_bytes=report.stat().st_size),ensure_ascii=True))
