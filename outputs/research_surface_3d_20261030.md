# RGB 사진으로 발·하퇴 표면 3D 만들기: 후보 조사

조사 기준: 2026-10-30. 공식 저장소·논문·모델카드를 웹에서 확인했다. 설치, 추론, 속도·정확도 실험은 실행하지 않았다. 아래 적합성 평가는 족욕기 안 고정 RGB 카메라라는 조건에 대한 공학적 추론이며 해당 환경에서 검증된 성능이 아니다.

## 먼저 결정할 것

가장 현실적인 출발점은 **물을 채우기 전, 동기화한 여러 카메라로 보이는 피부 표면을 촬영하고 COLMAP을 기준선으로 삼는 것**이다. 적은 사진에서 실패가 많으면 **VGGT-1B-Commercial**을 비교한다. 즉시 멋진 회전형 모델을 보여주는 수요 검증에는 **TripoSR**이 가장 단순한 생성 후보다. 모델이 빈 영역을 만들어 채웠음을 화면에 밝혀야 한다.

RGB로 얻는 것은 보이는 외부 표면과 학습된 형태 추정이다. **개인별 뼈·혈관·근육·발 내부 구조를 실제로 복원하지 못한다.** 생성형 3D의 그럴듯한 뒷면도 측정값이 아니다. 해부학 모델을 겹치는 경우는 일반 참고용 시각화이며 사용자의 실제 내부를 스캔한 결과라고 표시하면 안 된다.

물·유리 경계 굴절은 일반 카메라 모델과 다르다. 실제 수중 단계에는 [Refractive COLMAP 논문](https://arxiv.org/abs/2403.08640), [공식 프로젝트](https://cau-git.rz.uni-kiel.de/inf-ag-koeser/colmap_underwater), [Calibmar](https://github.com/MDSKiel/calibmar)를 별도 검토한다. 방수 하우징의 flat/dome port 지원이 족욕통 곡면 벽·움직이는 수면까지 자동 해결한다는 뜻은 아니다.

## 12개 핵심 후보

표의 VRAM 수치는 공식 문서에 명시된 해당 설정 값이며 보편적 최소 요구량이나 우리 장비 예상치가 아니다. 미확인은 공개 자료에서 수치를 확인하지 못했다는 뜻이다. 전통 사진측량에는 기본적으로 배포 가중치가 필요 없다.

| 후보 | 입력 → 출력 | 코드 / 가중치, 상업 사용 | GPU·Windows | 고정 여러 카메라 판단 |
|---|---|---|---|---|
| COLMAP | 겹치는 여러 사진 → 카메라, sparse/dense 점군, mesh; COLMAP BIN/TXT, PLY 등 | BSD 계열 / 기본 가중치 없음. 상업 가능, 선택 알고리즘·의존성 별도 확인 | 공식 Windows 바이너리. GPU 가속 경로 제공, 특정 VRAM 미확인 | 기준선 1순위. 캘리브레이션·rig·알려진 자세 활용. 표면 무늬 적으면 취약 |
| OpenMVS | 사진+카메라 자세+sparse 점군 → dense 점군·텍스처 mesh, PLY/OBJ 등 | AGPL / 없음. 상업 금지 라이선스는 아니지만 공개 의무와 포함 제3자 조건 검토 필요 | Windows CI/바이너리 안내. GPU 최소 VRAM 미확인 | COLMAP 뒤 mesh 처리 후보. 카메라 추정을 대신하지 않음 |
| Meshroom/AliceVision | 여러 사진 → 카메라·점군·텍스처 mesh, 보통 OBJ+MTL+이미지 | MPL-2.0 / 표준 사진측량 가중치 없음. 수정·배포와 제3자 의무 준수 | Windows. 문서 v2023.1 MVS는 NVIDIA CUDA CC≥3.0; CPU draft meshing. VRAM 수치 미확인 | GUI로 처음 실패 원인 보기 좋음. 실시간 파이프라인보다는 오프라인 기준선 |
| DUSt3R | 쌍 또는 여러 사진 → pointmap·깊이·자세·신뢰도, demo GLB | 코드 CC BY-NC-SA 4.0 / 가중치도 NC 및 학습데이터·base 조건. 상업 기본 불가 | CUDA 중심 설치. 보장된 Windows/최소 VRAM 미확인 | 적은 뷰의 연구 비교. 비관측부 측정·절대 크기 보장 없음 |
| MASt3R / MASt3R-SfM | 사진 쌍/컬렉션 → dense matching·metric pointmap·SfM, demo GLB/COLMAP 연계 | 코드 CC BY-NC-SA 4.0 / 체크포인트 NC 및 데이터 조건. 상업 기본 불가 | PyTorch CUDA·컴파일 의존. Windows/최소 VRAM 미확인 | DUSt3R보다 matching·global alignment 강화. metric 명칭이 수중 발 정확도를 보장하지 않음 |
| VGGT-1B-Commercial | 1장·수장·수백 뷰 → 자세·내부파라미터·깊이·점군·track; COLMAP export | 현행 코드 VGGT custom license / **Commercial 체크포인트만** 상업 허용. 원본 VGGT-1B는 NC. 군사 제외·AUP 확인 | PyTorch CUDA 예제. Windows 공식 보장/고정 최소 VRAM 미확인 | 상업을 고려한 sparse-view 비교 1순위. 매 촬영 재추정 대신 고정 캘리브레이션과 비교 필요 |
| VGGT-Ω | 여러 이미지/영상 → 카메라·깊이·신뢰도·GLB 점군 scene | FAIR Noncommercial Research License / 모델 포함 연구재료 및 결과의 상업 사용 제한 | A100, 624×416 공식 peak: 1뷰 6.02GB, 10뷰 6.67GB, 25뷰 7.80GB. Windows 보장 미확인 | 2026 공개된 효율 개선 연구 후보. 상업 MVP에는 원본 Commercial과 혼동 금지 |
| TripoSR | **단일 이미지** → 색상 mesh 또는 baked texture; OBJ/GLB | 코드·사전학습모델 MIT, 상업 가능 | 기본 약 6GB VRAM/1장. CPU fallback. Windows 공식 보장 미확인 | 빠른 UX 데모 1순위. 여러 경로를 넣어도 각 사진을 따로 처리하며 multi-view fusion이 아님 |
| Stable Fast 3D | **단일 이미지** → UV·재질·조명 분리 mesh, GLB | Stability AI Community License / 가중치도 해당 조건·HF gate. 상업 등록 필요, 연매출 및 계열사 합산 $1M 초과 시 별도 라이선스 | 약 6GB VRAM/1장. CPU, 실험적 Windows(VS2022)·MPS | TripoSR보다 웹 asset 마감에 유리. 각 입력 별 생성이며 여러 카메라 실제 기하 복원이 아님 |
| TRELLIS | 단일 이미지, 선택 multi-image conditioning, text 계열 → mesh GLB·Gaussian PLY·radiance field | 주 코드·모델 MIT. **diffoctreerast는 비상업 연구/평가 제한**. 설치 전체를 MIT로 보면 안 됨 | NVIDIA ≥16GB, 공식 Linux 검증; Windows 미완전 검증 | 멋진 asset 후보. 다중 이미지 conditioning은 별도 훈련된 전용 multi-view 모델이 아니며 실패 가능 공식 명시 |
| TRELLIS.2 | 단일 이미지 → PBR mesh, GLB; O-Voxel 표현 | 주 코드 MIT / TRELLIS.2-4B 모델 MIT. 사용 의존성·asset별 조건은 별도 | 공식 모델카드 NVIDIA ≥24GB, Linux만 테스트, A100/H100 검증 | 시각 품질 우선 후순위. 기본 single-image라 고정 여러 뷰를 측량 입력으로 활용하지 않음 |
| Hunyuan3D-2 / 2.1 | 2: 단일 이미지, 별도 2mv 다중뷰 모델; 2.1 기본 단일 이미지 → shape+texture/PBR mesh, GLB 등 | Tencent 2.0/2.1 Community License / 모델 조건. **두 LICENSE 모두 South Korea 적용 제외 명시. 한국 기본 도입 보류** | 2 README shape 6GB/shape+texture 16GB. 2.1 전용 README shape 10GB/texture 21GB/전체29GB. 2.1 Windows 지원 명시 | 2mv는 3~4방향 물체 뷰 생성 계열 후보지만 실제 피부 재구성 아님. 지역 제한으로 국내 MVP 추천 제외 |

## 후보별 직접 근거와 선택 이유

### 1. COLMAP

[공식 저장소](https://github.com/colmap/colmap), [문서](https://colmap.github.io/), [FAQ](https://colmap.github.io/faq.html). 표면 측정 성격에 가장 충실하고 자체 모형을 새로 학습할 필요가 없다. static rig 촬영마다 변하지 않는 intrinsics/extrinsics는 사전 캘리브레이션해 재사용하는 설계가 유리하다. 사진 수에는 모든 환경에 통하는 최소값이 없다. 장면에 겹치는 특징점이 충분해야 하며 발 뒤·발바닥·발가락 사이가 카메라에 보이지 않으면 재구성할 관측치가 없다. FAQ는 SIFT에 충분한 texture·overlap·유사 조명이 유리하다고 설명한다. 선택 learned matcher는 기본 BSD만 보고 가중치까지 자유 사용으로 간주하면 안 된다.

### 2. OpenMVS

[공식 README](https://github.com/cdcseacave/openMVS), [COPYRIGHT](https://github.com/cdcseacave/openMVS/blob/master/COPYRIGHT.md). 이미 추정한 카메라를 입력받아 dense→mesh→refine→texture를 처리한다. AGPL의 소스 공개 범위는 배포·네트워크 제공 구조에 따라 확인해야 한다. COPYRIGHT에는 **ibfs의 research-only 표기**도 있으므로 실제 빌드·실행 경로의 포함 여부를 확인하기 전 상업 안전 판정을 내릴 수 없다. 초기 사내 평가와 제품 편입은 구분한다.

### 3. Meshroom

[공식 repo](https://github.com/alicevision/Meshroom), [라이선스](https://github.com/alicevision/Meshroom/blob/develop/COPYING.md), [하드웨어 문서](https://meshroom-manual.readthedocs.io/en/latest/first-steps/install/requirements.html). 노드별 실패와 intermediate 결과를 보는 GUI가 장점이다. 최신 develop은 일반 파이프라인 framework 및 AliceVision plugin 구성이므로 오래된 단일 설치 가이드와 버전을 섞지 않는다. 표의 CUDA 요구는 v2023.1 문서 기준이며 실제 다운로드 release 요구를 다시 확인해야 한다.

### 4. DUSt3R

[공식 repo](https://github.com/naver/dust3r), [논문](https://arxiv.org/abs/2312.14132), [가중치 모델카드](https://huggingface.co/naver/DUSt3R_ViTLarge_BaseDecoder_512_dpt). 이미지 쌍의 pointmap을 얻어 global alignment한다. calibration 없이 빠르게 초기 구조를 볼 수 있으나 학습 prior에 의존한다. 피부가 매끈하거나 반사·가림이 심한 경우 생성된 깊이가 실제 표면과 일치하는지 별도 확인해야 한다. 코드뿐 아니라 weights에도 NC 및 학습데이터 조건이 명시되어 사업용 기본 파이프라인으로 선택하지 않는다.

### 5. MASt3R

[공식 repo](https://github.com/naver/mast3r), [논문](https://arxiv.org/abs/2406.09756), [모델카드](https://huggingface.co/naver/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric). DUSt3R에 local feature head와 metric pointmap, 확장 가능한 alignment를 추가한다. MASt3R-SfM 경로는 사진 집합의 카메라 추정을 통합한다. 연구용으로 COLMAP이 실패한 sparse-view에 비교할 가치가 크다. 신체 특정 부위의 물속 절대 치수 정확도를 보장하는 모델은 아니다.

### 6. VGGT-1B-Commercial

[공식 repo](https://github.com/facebookresearch/vggt), [상업 모델카드](https://huggingface.co/facebook/VGGT-1B-Commercial), [LICENSE](https://github.com/facebookresearch/vggt/blob/main/LICENSE.txt). **README 기본 예제는 여전히 `facebook/VGGT-1B`를 로드한다. 상업 버전을 의도하면 모델 ID를 명시적으로 바꿔야 한다.** 카메라/깊이 예측을 COLMAP 형식으로 export 후 재투영 오차와 실제 치수 표준물을 대조하는 비교가 적절하다. 물·반사 표면을 마스크하는 안내는 있으나 발 자체가 물속에 있는 굴절 문제 해결 근거는 아니다.

### 7. VGGT-Ω

[공식 repo 및 GPU표](https://github.com/facebookresearch/vggt-omega), [프로젝트](https://vggt-omega.github.io/), [LICENSE](https://github.com/facebookresearch/vggt-omega/blob/main/LICENSE). May 2026 공개 모델이 실제 존재함을 확인했다. 공식 repo는 512 checkpoint를 in-the-wild용으로, Sep 2026 reproduction checkpoint를 benchmarking용으로 구분한다. 공개 시점 표기가 프로젝트 페이지와 repo에 9월 18일/8일로 다르게 나타나므로 여기서는 정확한 일자 단정 없이 9월 공개로 취급한다. 2025 VGGT Commercial 라이선스를 승계한다고 추정하면 안 된다. Ω 현행 LICENSE는 상업적 이익 목적이 아닌 연구로 제한하며 outputs/results에도 제한을 둔다.

### 8. TripoSR

[공식 README](https://github.com/VAST-AI-Research/TripoSR), [추론 스크립트](https://github.com/VAST-AI-Research/TripoSR/blob/main/run.py), [논문](https://arxiv.org/abs/2403.02151). 코드·weights MIT가 명시되어 가장 단순한 asset 생성 비교다. A100에서 0.5초 미만이라는 공개치는 웹캠·마스킹·mesh export·브라우저 전송 포함 사용자 체감 시간이 아니다. 고립된 물체 이미지 중심이므로 하퇴가 화면 밖으로 이어지거나 다른 다리·통과 붙으면 배경 제거 및 경계 형상에 실패할 수 있다. 발가락 수·발바닥 모양·발목 비율을 사진 밖에서 만들어낼 수 있다.

### 9. Stable Fast 3D

[공식 repo](https://github.com/Stability-AI/stable-fast-3d), [LICENSE](https://github.com/Stability-AI/stable-fast-3d/blob/main/LICENSE.md), [모델카드](https://huggingface.co/stabilityai/stable-fast-3d). GLB, UV, 조명 분리와 재질 추정이 있어 브라우저 회전/확대 경험에 편하다. Windows는 공식적으로 experimental이다. 라이선스는 코드 공개 여부와 무관하게 매출 조건·상업 등록·고지 의무를 갖는다. 정밀 개인 모델보다 체험용 생성 asset에 맞는다.

### 10. TRELLIS

[공식 repo](https://github.com/microsoft/TRELLIS), [MIT 모델카드](https://huggingface.co/microsoft/TRELLIS-image-large), [diffoctreerast LICENSE](https://github.com/JeffreyXiang/diffoctreerast/blob/master/LICENSE). Gaussian과 mesh를 선택할 수 있지만 반투명·부드러운 Gaussian 화면의 인상적 시각 품질은 표면 기하 정확도와 다르다. 기본 setup script는 여러 submodule을 설치하므로 비상업 렌더러가 포함되는지 확인해야 한다. NC 모듈을 제거·대체하고 선택 경로가 기능적으로 동작하는지 검증하기 전 상업 전체-stack 추천은 보류한다. 생성형 다중 입력은 캘리브레이션된 MVS와 별개다.

### 11. TRELLIS.2

[공식 repo](https://github.com/microsoft/TRELLIS.2), [모델카드](https://huggingface.co/microsoft/TRELLIS.2-4B), [MIT LICENSE](https://github.com/microsoft/TRELLIS.2/blob/main/LICENSE). 2025-12 논문·공개 모델을 실제 확인했으며 미래 출시를 가정한 후보가 아니다. 공식 모델카드는 single-image와 PBR mesh를 명시하고 small holes/topological discontinuities를 한계로 설명한다. H100 공개 속도(512³ 약3초, 1024³ 약17초, 1536³ 약60초)는 특정 장비 수치다. 우리 입력에서 24GB 카드만으로 모든 해상도·후처리가 보장되지는 않는다. 3D asset 품질을 우선하는 두 번째 데모에 적절하다.

### 12. Hunyuan3D-2 / 2.1

[2 공식 repo](https://github.com/Tencent-Hunyuan/Hunyuan3D-2), [2mv 모델](https://huggingface.co/tencent/Hunyuan3D-2mv), [2 LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE), [2.1 공식 repo](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1), [2.1 LICENSE](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE). 두 라이선스는 한국을 적용 지역에서 제외하므로 **상업/비상업 여부 이전에 한국 사용 권한을 별도로 해결해야 한다**. 외국 GPU에서 돌리면 자동 해결된다는 근거도 없다. VRAM은 2 repo의 공통표와 2.1 전용 문서가 다르므로 2.1에는 더 구체적인 10/21/29GB를 사용했다. 주 후보에서 제외하되 비교표에 남긴다.

## 추가 후보·연결 도구

- [MUSt3R](https://github.com/naver/must3r): multi-view 메모리 기반 online pose/structure. 공식 Non-Commercial License, 학습데이터 제약도 명시. 연구용 확장 목록.
- [Pow3R](https://github.com/naver/pow3r): known depth/focal/pose prior 활용 계열. 고정 rig와 개념상 잘 맞지만 현행 전체 코드·가중치·데이터 상업 조건은 이번 조사에서 완전 확인하지 않아 제품 채택 보류.
- [COLMAP Underwater](https://github.com/MDSKiel/colmap_underwater): flat/dome refractive SfM. 원본 COLMAP과 DB 및 exported refractive parameter 호환 차이가 있어 일반 OpenMVS 등에 바로 연결된다고 가정하지 않는다.
- [Calibmar](https://github.com/MDSKiel/calibmar): 카메라·stereo·수중 하우징 캘리브레이션. Windows/Linux binary. 물속 실험 이전 캘리브레이션 도구 후보.
- [gsplat](https://github.com/nerfstudio-project/gsplat): VGGT가 공식적으로 COLMAP export 이후 연계를 안내하는 Gaussian 학습 경로. 그 자체가 사진으로 내부를 복원하는 모델은 아니다. 별도 렌더링 조사 범위.

## 이 촬영 조건에서 공통으로 생기는 실패

다음은 논문의 일반 전제와 광학·기하 원리에서 도출한 적용 판단이다. 각 모델이 이 환경을 통과했다는 실험 증거는 없다.

1. **수중·굴절**: 통 밖 카메라가 통 벽과 물을 통과해 보는 경우, 수면 위에서 내려다보는 경우, 카메라 하우징 자체가 수중인 경우는 서로 다른 모델이다. 카메라 고정만으로 굴절이 보정되지 않는다. 곡면 플라스틱 벽·수면 출렁임은 한 번의 pinhole calibration으로 설명되지 않을 수 있다.
2. **반사·기포·수류**: 젖은 피부 하이라이트와 수면 반사는 시점마다 다른 위치를 보인다. 특징점 대응/일관된 색 가정이 깨진다. 확산조명·가능한 편광·짧은 노출·정수 상태·거품 끄기가 실험 변수다. 편광만으로 굴절·가림이 사라지지는 않는다.
3. **매끈한 피부**: 충분한 texture가 없으면 전통 MVS가 빈 점군을 내거나 잘못 연결하고, 신경 모델은 그럴듯한 깊이를 예측할 수 있다. 모형의 정답 표면·알려진 치수로 구분해야 한다.
4. **가림과 시야**: 통 바닥에 붙은 발바닥, 붙어 있는 발가락, 반대 다리 뒤 표면은 측정할 수 없다. 그 부분을 mesh hole로 남길지 일반 형태로 채울지 결정하고 추정임을 구분한다.
5. **움직임**: 싸구려 웹캠 여러 대는 exposure·프레임 timestamp·rolling shutter가 다를 수 있다. 사진마다 발이 움직이면 같은 정적 물체라는 가정이 깨진다. 먼저 dry 상태에서 가능한 동시 촬영으로 검증한다.
6. **축척**: 단안/uncalibrated 결과는 절대 mm를 보장하지 않는다. 고정 rig baseline, 캘리브레이션 표적, 실제 치수 reference가 필요하다. 측정 기능을 주장하려면 별도 오차 실험이 있어야 한다.

## 다음 비교를 위한 최소 설계안 — 실행하지 않음

- 1차: dry·정적 발 모형, diffuse light, 동일 순간 4/6/8뷰를 비교. 숫자는 실험 설계안이며 공식 필요 최소 카메라 수가 아니다. 카메라 수보다 중첩·시선 분산·보이는 면적을 먼저 확인한다.
- 2차: COLMAP → 점군/mesh 기준선과 VGGT Commercial 결과 비교. 실패 비율, 실제 치수 오차, 관측 표면 coverage, 전체 처리시간, 시각적 만족도를 별도 기록한다.
- 3차: 같은 대표 1장을 TripoSR로 생성해 체험 만족도만 비교. multi-camera 데이터의 실제 활용과 생성형 뒷면을 혼동하지 않는다.
- 4차: water added·수류 off·고정 모형으로 동일 테스트. dry 성공 후에도 수중 성능을 독립 결과로 기록한다. 실제 발 테스트는 그다음이다.
- 사용자 화면에는 `사진으로 추정한 외부 표면`, `보이지 않은 면은 생성으로 보완`, `일반 해부학 참고모델`을 각 데이터 성격에 맞게 표현한다. `내 발 내부 스캔`은 금지한다.

## 파일·실행·동기화 상태

사용자 확인 경로와 실제 저장 경로는 모두 이 파일(`린/outputs/research_surface_3d_20261030.md`)이다. 조사 문서만 작성했으며 runtime·배포 변경, 모델 실행, branch push는 없다. 전체 작업의 merge/push 판단은 상위 통합 작업에서 수행한다.
