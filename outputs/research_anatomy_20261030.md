# 사진 기반 발·하퇴 해부학 시각화: 모델·아틀라스·렌더러 조사

조사일: 2026-10-30. 공식 저장소·프로젝트 문서·라이선스 중심의 문헌 조사이며 설치, 모델 다운로드, 추론, 성능 실험은 수행하지 않았다. “뼈 이상”은 뼈 이외 근육·지방·혈관 등 더 많은 구조로 해석한다.

## 판단

족욕기/스파 통의 고정 RGB 카메라 사진에 맞춰 **표준 해부학 모델을 정렬하고 피부·뼈·근육·힘줄·혈관을 단계별로 드러내는 3D 연출**은 MVP로 현실적이다. 개인 외형에 맞는 표면과 내부 아틀라스를 결합하는 방식이다. 사진에서 실제 개인의 근육 경계, 피하지방 두께, 뼈 피질/골수, 혈관 주행을 측정했다는 뜻은 아니다.

상업 수요 검증의 첫 후보는 **BodyParts3D 최신 공식 배포 + Blender + Three.js**다. 최신 원본은 공식 이용허락이 CC BY 4.0으로 갱신되어 있다. 외형용 MakeHuman/MPFB의 core asset은 CC0여서 대체 외피에 유용하다. SKEL은 피부에서 골격 메시로 연결하는 연구 후보지만 비상업 연구 라이선스이며 근육·장기를 자동 제공하지 않는다. SMPL 계열 전체를 무료 상업 사용 가능한 오픈소스로 묶어 소개하면 안 된다.

## 무엇이 서로 다른가

- **Pose skeleton:** 관절 좌표와 이를 연결한 선 또는 애니메이션 rig. 관절 추정이 잘 돼도 각 발가락뼈의 실제 형태를 복원한 것은 아니다.
- **Parametric body:** 체형/자세 변수로 피부 표면 메시를 생성한다. SMPL, SMPL-X, STAR 등이 해당하며 내부 근육·지방 분할까지 의미하지 않는다.
- **Anatomical skeleton:** 뼈처럼 생긴 메시와 생체역학적 관절 모델. SKEL은 이쪽으로 진전하지만 외부 영상만으로 개인의 모든 골형태를 직접 관찰한 결과는 아니다.
- **Anatomical atlas:** 특정 기준 인체에서 제작한 뼈·근육·장기 등 분리 자산. 사진 외형에 맞춰 변형해도 내부는 참조 해부학이다.
- **Renderer:** 이미 존재하는 모델을 아름답게 보여준다. Blender/Three.js 자체에는 RGB→내부 해부학 추론 기능이 없다.

이 구분은 각 공식 모델의 출력 정의와 아틀라스 제작 방식을 바탕으로 한 기술적 해석이다. [SMPL](https://smpl.is.tue.mpg.de/), [SKEL](https://github.com/MarilynKeller/SKEL), [SPL Knee Atlas](https://www.openanatomy.org/atlas-pages/atlas-spl-knee.html).

## 핵심 후보 12개

GPU/Windows 항목은 공식 실행 문서와 구현 구조에 따른 도입 판단이다. 실측 FPS, 최소 VRAM, 정확도를 뜻하지 않는다. “메시 출력”과 최종 GLB 변환은 다른 단계다.

| 후보 | 입력 → 출력·표현 범위 | 라이선스 분리 및 상업 판단 | 실행·포맷·MVP 적합성 |
|---|---|---|---|
| **1. SMPL** | 체형 beta/관절 pose → 전신 피부 메시·rig. 사진 피팅은 별도 최적화/추정기가 필요. 근육/실제 뼈 메시 없음. | 전체 Model·software/data는 비상업 연구 조건. 상업용 생성·서비스는 별도 라이선스 경로. 공개 코드와 shape model 권리는 별도 검토. | Python/Unity/Maya, FBX 예시. CPU에서 단순 forward를 사용할 수 있는 구조지만 사진 피팅 속도는 별개. 전신을 못 보는 통 내부 발 사진에는 체형 미관측 부분이 많아 우선순위 낮음. [공식](https://smpl.is.tue.mpg.de/), [모델 라이선스](https://smpl.is.tue.mpg.de/modellicense.html) |
| **2. SMPL-X / SMPLify-X** | 전신+손+얼굴의 체형/자세 → 피부 메시. SMPLify-X는 이미지 특징을 사용한 피팅. 발 특징을 쓰더라도 발 내부 아틀라스는 아님. | 공식 loader/Model & Software는 비상업 연구. 별도의 **SMPL-X Body CC BY 4.0**은 shape blendshape 및 그것으로 몸을 만드는 도구를 제외한 body subset. Body 허용을 전체 생성 모델 허용으로 확대 해석 금지. | PyTorch, Blender/Unity/Unreal 통합 경로. OBJ/FBX body 전달 가능. 얼굴·손이 필요 없는 하퇴 MVP에는 과함. 사진 피팅/학습은 GPU 이점이 크며 Windows 전용 설치 보장은 확인하지 않음. [코드](https://github.com/vchoutas/smplx), [Model](https://smpl-x.is.tue.mpg.de/modellicense.html), [Body](https://smpl-x.is.tue.mpg.de/bodylicense.html) |
| **3. STAR** | 체형/자세 → 피부 메시. sparse local pose corrective를 사용하는 SMPL 대안. 골격 내부 구조 생성기는 아님. | 코드·모델 비상업 과학 연구. 가중치는 별도 등록/다운로드. | PyTorch/TensorFlow/Chumpy loader. 공식 테스트 환경은 오래된 Ubuntu/Python/CUDA 버전. 최신 Windows 재현 작업 위험. 외형 연구 비교용, 상업 MVP 기본 채택 비추천. [공식 코드·환경·조건](https://github.com/ahmedosman/STAR) |
| **4. SKEL** | beta/46개 pose 변수 또는 SMPL 정렬 → 관절 위치·피부 메시·뼈 메시. 10개 체형 변수. 근육/장기 출력 없음. | **코드와 모델 모두 비상업 과학 연구**. 상업 별도 문의. SMPL 정렬 사용 시 해당 모델 조건도 추가. | PyTorch. 2025년 Python 3.12 환경 갱신. Bash 설치, 피팅 시각화용 MPI mesh는 Linux만 지원한다고 명시. Windows는 WSL/Linux 경로가 합리적 추정이며 native 검증 안 됨. “피부와 뼈가 함께 움직이는 연출” 연구 1순위. [공식](https://github.com/MarilynKeller/SKEL) |
| **5. SUPR / SUPR-Foot** | 체형/pose 및 접촉 관련 표현 → 전신 또는 분리된 발 표면. 발가락 관절과 접촉 변형이 전신 모델보다 목적에 가깝다. 내부 근육/뼈는 아님. | 코드·모델 비상업 연구, 모델 등록 필요. 상업 문의 경로 명시. | PyTorch/TensorFlow. 공식 README 의존성이 오래돼 Windows 최신환경 보장 안 됨. 단순 forward와 영상→파라미터 추정기를 구분해야 함. 전신 대신 발 전용 외형 연구 후보로 반드시 비교. [공식 코드·라이선스](https://github.com/ahmedosman/SUPR) |
| **6. MakeHuman / MPFB** | 수동 체형 설정/target → 외형 메시·rig. RGB 자동 역추정 없음. core asset으로 외피 제작. | MakeHuman code AGPL, MPFB code GPL, **core assets CC0**. 출력 상업 사용 가능. 커뮤니티 의상/피부/타겟은 개별 조건으로 core와 다를 수 있음. | Windows 배포와 Blender 연계. OBJ/FBX/DAE/MHX2 등. CUDA 필수 아님. 전신이 필요한 화면용 아바타/표준 외피에 적합, 발 실측 특화는 아님. [라이선스](https://www.makehumancommunity.org/about/license.html), [출력 FAQ](https://www.makehumancommunity.org/makehuman/faq/can_i_sell_models_created_with_makehuman.html), [Windows](https://www.makehumancommunity.org/makehuman/releases/releases_130.html) |
| **7. OpenSim** | 근골격 모델·스케일/관절 동작 → 뼈의 운동과 근육 경로·생체역학 시뮬레이션. 사진→개인 해부학 모델 기능은 별도. | **core Apache 2.0**, 상업 사용 가능. GUI, 플러그인, 외부 모델·기하 자산·데이터는 각 라이선스. “OpenSim 모델”이라는 이유만으로 전 자산 Apache라 가정 금지. | C++/Python/Java, Windows/macOS/Linux build 경로. .osim 모델과 연결 geometry, 시뮬레이션 데이터. 기본 활용은 CPU 중심. 근육은 선/경로/작용 모델일 수 있어, 도톰한 근육 표면 연출은 atlas mesh와 결합해야 함. 정적 MVP보다 움직임 단계에 유용. [공식 core](https://github.com/opensim-org/opensim-core) |
| **8. BodyParts3D** | 기준 인체 부위별 polygon mesh·이름/관계표 → 뼈·근육·장기 등 참조 해부학. 사진 입력 없음. | **공식 일본어 이용허락은 2025-02-27 갱신 CC BY 4.0**. 과거 BY-SA 2.1 Japan 자료/미러와 혼동 주의. 최신 공식 취득본·이용허락을 함께 보관해야 함. 학습 가중치가 아니라 3D 데이터. | OBJ zip, 부위 ID/명칭/포함관계 텍스트. Blender에서 하퇴/발만 추출해 GLB 전환. 학습 GPU 불필요. 부위별 재질·투명도·레이어 연출의 MVP **최우선 원천**. [공식 최신 허락](https://dbarchive.biosciencedbc.jp/jp/bodyparts3d/lic.html), [다운로드](https://dbarchive.biosciencedbc.jp/jp/bodyparts3d/download.html) |
| **9. Z-Anatomy** | Blender에서 탐색 가능한 전신 해부학 template. 뼈·근육·내장·신경 등 풍부한 레이어. | 자체 코드/content CC BY-SA 4.0. 그러나 **공식 README가 내이 CC BY-NC-SA, 신장 CC BY-NC 자산도 포함·참조했다고 명시**. 전체 압축파일을 상업 사용 가능 자산으로 일괄 판정 불가. 최신 BodyParts3D 허락이 Z-Anatomy 추가 창작을 재허락하지도 않음. | Blender template ZIP, 별도 Unity판에는 FBX 시스템별 자산. Windows 사용 안내 존재. 하퇴/발만 선별하고 출처 명세를 만드는 경우 빠름. 상업 우선이면 원본 BodyParts3D 경로가 단순. [모델·포함 자산·조건](https://github.com/Z-Anatomy/Models-of-human-anatomy), [Unity 모델 허락](https://github.com/LluisV/Z-Anatomy/blob/PC-Version/Resources/Models/License.txt) |
| **10. AnatomyTOOL / Open3DModel + LUMC viewer** | 교육용 해부학 모델을 브라우저에서 선택·회전·숨김. 인체 내부 자산 공급 및 UI 참고. RGB 역추정 없음. | 공식 모델 웹페이지는 이번 조사 도구에서 timeout/502. **모델 geometry/texture의 정확한 현재 조건은 원문 재확인 전 보류**. 공식 LUMC viewer code는 GPL 3.0으로 확인했으며 모델 자산과 별개. 타 사이트의 CC BY-SA geometry/NC texture 요약만으로 최종 상업 승인하지 않음. | 공식 viewer는 .glb와 Chrome/Edge/Firefox 지원, 구조별 숨김. 하퇴 모델의 실제 제공범위·라이선스 확인 후 유력 atlas 후보. Three.js 자작 UI 대신 viewer 재사용 시 GPL 검토 필요. [공식 모델 입구](https://anatomytool.org/open3dmodel), [공식 create](https://anatomytool.org/open3dmodel-create), [LUMC 코드](https://github.com/djansma/open3dviewer) |
| **11. Blender** | OBJ/FBX/GLB 등 3D 자산 → 리깅·재질·투명화·단면/클리핑·정렬·이미지/영상 및 GLB. 해부학 데이터 제공 모델은 아님. | 도구 GPL. 자기 창작 이미지/영상/모델 출력은 GPL로 강제되지 않음. 단, 가져온 BP3D/Z-Anatomy/텍스처 권리는 유지. bpy add-on 재배포와 출력물은 구분. | Windows native, GPU 렌더링 또는 CPU Cycles 경로. 모델 준비·광고용 정지/영상의 **최우선**. 하드웨어 요구는 장면/렌더러 의존으로 수치 단정 불가. [공식 FAQ](https://www.blender.org/support/faq/), [공식 조건](https://www.blender.org/about/license/) |
| **12. Three.js** | glTF/GLB 등 → Windows 브라우저의 회전/확대·레이어·투명 피부·부위 선택 UI. 인체 추론 없음. | code MIT. 모델·텍스처가 MIT가 되는 것은 아님. 각 atlas credit과 변경 고지 별도 유지. | GLTFLoader, Draco/meshopt/KTX2 관련 확장 지원. 브라우저 GPU 렌더링이며 CUDA 서버 필수 아님. 설치 부담이 적은 사용자 테스트·키오스크 UI **최우선**. [MIT](https://github.com/mrdoob/three.js/blob/dev/LICENSE), [GLTFLoader](https://threejs.org/docs/pages/GLTFLoader) |

## 발·하퇴만 촬영할 때의 실제 한계

1. **미관측 전신:** 골반·무릎·상체가 보이지 않으면 전신 SMPL의 shape/pose는 동일한 발 사진에 맞는 해가 여러 개다. 모델 prior가 빈 부분을 채우며 이것을 측정값으로 표시하면 안 된다. 발 전용 SUPR-Foot 또는 하퇴 부분 메시와 atlas 정렬이 더 맞는 문제 설정이다. 이는 입력 가시성 및 모델 정의에 따른 추론이다.
2. **카메라가 많아도 내부는 관찰하지 않는다:** 여러 시점은 외피 기하에 도움을 주지만 광학 RGB가 내부 단층 정보를 추가하는 것은 아니다. 피부 아래 근육·지방·장기는 표준 모델 기반 설명이다.
3. **물·벽면·가림:** 물속 굴절, 수면 반사, 곡면 통 벽, 거품, 젖은 피부 하이라이트, 발바닥이 바닥에 닿는 가림이 외형 재구성에 영향을 준다. dry 촬영과 underwater 촬영을 같은 보정으로 취급하지 않는 설계가 필요하다. 이번에는 보정이나 정확도 실험을 하지 않았으므로 성능 보장 없음.
4. **정적 atlas의 자세:** 표준 전신 atlas가 straight-leg 자세면 앉은 자세의 발목/하퇴와 다르다. 뼈·근육을 한꺼번에 단순 확대하거나 비선형 변형하면 근육 부착/관절관계가 깨질 수 있다. 첫 MVP는 촬영 자세를 일정하게 하고 “모델 정렬” 품질을 먼저 확인하는 편이 단순하다.
5. **지방·장기:** BodyParts3D/Z-Anatomy에 있다고 모든 피하지방층이 개인화돼 제공되는 것은 아니다. 피하지방을 원한다면 구체적인 자산 항목·분할 범위를 확인해야 한다. 발/하퇴 화면에서 복부 장기를 개인화해 드러내는 기능은 촬영 정보와 맞지 않는다. 근육·힘줄·혈관·신경만으로도 뼈 이상의 풍부한 연출이 가능하다.

## 권장 MVP 연결 방식

`고정 다중 RGB → 외피/사진 정렬(별도 파이프라인) → 발·하퇴 참조 atlas 정렬 → Blender 재질/연출 → GLB → Three.js 레이어 UI`

- 초기 수요 검증은 고정된 발 위치에서 사진/외피와 atlas를 수동 정렬한 결과로도 가능하다. 자동화가 가치를 만드는지 먼저 분리해서 검증할 수 있다.
- **개인화할 수 있는 것:** 관측 외형, 피부 텍스처, 촬영 자세에 맞는 화면 위치·크기.
- **참조로 보여줄 것:** 각 뼈/근육/힘줄/혈관·신경의 표준 형상 및 설명. 피부 fade, 근육 reveal, 뼈 reveal, 부분 선택, 회전·줌이 주요 연출이다.
- 사용자 화면에는 “사진에 맞춘 표준 해부학 시각화”를 일관되게 표시한다. 초음파를 구현하지 않은 현재 단계에 초음파 실측/개인 내부 스캔이라는 표시를 붙이지 않는다.
- 골격 동작이 필요해지면 SKEL 상업 라이선스 또는 OpenSim의 라이선스 확인된 모델을 후속 검토한다. 처음부터 전신 모델·생체역학·의료영상 체계를 모두 연결할 필요는 없다.

## BodyParts3D 라이선스 표기 충돌과 적용 범위

확인 시점에 두 공식 사이트의 문구가 다르다. [기존 lifesciencedb 라이선스 페이지](https://lifesciencedb.jp/bp3d/info/license/index.html)는 그 사이트와 Anatomography 이미지의 표준 조건을 여전히 CC BY-SA 2.1 Japan으로 표기하면서, 세부 사항은 LSDB Archive 이용허락에 따른다고 안내한다. 반면 [LSDB Archive 일본어 이용허락](https://dbarchive.biosciencedbc.jp/jp/bodyparts3d/lic.html)은 2025/02/27 갱신일과 CC BY 4.0을 명시한다. 따라서 본 보고서의 BY 4.0 판단은 **현재 LSDB Archive에서 직접 취득하는 BodyParts3D 데이터**에 한정한다. 기존 사이트의 모든 이미지·과거 취득본·타인 파생물이 일괄 BY 4.0으로 전환됐다고 주장하지 않는다.

아카이브 [공식 다운로드 페이지](https://dbarchive.biosciencedbc.jp/jp/bodyparts3d/download.html)는 최초 이용허락 열람을 요구하고, 이곳의 데이터와 원래 데이터베이스 내용이 다를 수 있다고도 명시한다. 직접 연결되는 파일은 [IS-A OBJ 4.0](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/isa_BP3D_4.0_obj_99.zip), [PART-OF OBJ 4.0](https://dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/partof_BP3D_4.0_obj_99.zip)이다. 이번 도구는 ZIP 내부를 열지 않았으므로 내부 고지와 mesh별 권리의 추가 확인은 남는다. 실제 MVP 자산 취득 시 이 다운로드 경로·취득일·라이선스 페이지 사본을 함께 고정하고, ZIP 내부에 다른 고지가 있다면 배포처에 확인한다. Z-Anatomy 등 추가 가공물은 그 추가 창작과 혼합 자산의 기존 조건을 별도로 유지한다.

## 추가 참고 및 미확인 사항

**지방까지 보이는 atlas의 실물 예시:** SPL Knee Atlas는 MRI 기반으로 근육·뼈·힘줄·인대·지방·혈관·연골·반월판·신경과 원 MRI/label map/3D 모델을 제공한다. 다만 무릎 atlas이고 사용자 본인 데이터가 아니다. 현재 발 중심 MVP의 주 자산보다 후속 영역 확장의 참조다. 배포 조건은 3D Slicer License section B라고 명시되어 있으며 그 전문은 이번 조회에서 열리지 않아 상업 조건 판정을 유보한다. [공식 atlas](https://www.openanatomy.org/atlas-pages/atlas-spl-knee.html).

**라이선스 명세에 기록할 단위:** 코드 저장소 commit, 모델/가중치 이름·버전, atlas 원본 URL·취득일, 개별 mesh/texture 출처·조건, 가공 내역, 사용자에게 전달되는 GLB/영상의 attribution. “GitHub 공개”, “교육용 무료”, “renderer MIT/GPL”은 전체 자산의 상업 허락을 대신하지 않는다.

**아직 검증하지 않은 것:** 발/하퇴 부위별 자산 완전성, 실제 zip 내부 파일 목록, 최신 Windows 패키지 호환성, 현재 PC에서의 VRAM/속도, 수중 다중카메라 보정, 사용자별 정렬 정확도. AnatomyTOOL의 모델/texture 현재 라이선스는 공식 원문 접근 실패로 보류했다. 이 문서는 실행 검증 결과가 아닌 후보·권리·구조 조사다.

완료 경로: 사용자 확인 파일과 실제 저장 파일은 모두 `린/outputs/research_anatomy_20261030.md`. 실행 서비스 없음. 이 조사 하위 작업은 지정 파일만 작성했으며 브랜치 변경·merge·push를 수행하지 않았다.
