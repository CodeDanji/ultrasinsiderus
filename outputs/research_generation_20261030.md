# 고정 RGB 카메라 → 내부 개념 시각화: 생성·의료영상 도구 조사

확인일: 2026-10-30. 공식 저장소·문서·저자 논문·모델카드만 기술 근거로 사용했다. 설치, 모델 다운로드, 추론, 속도·품질 시험은 수행하지 않았다. Windows와 GPU 정보는 문서 수준 확인이다.

## 먼저 내릴 결정

현재 스파·족욕기에서 찍는 여러 RGB 사진으로 만들 수 있는 것은 외형에 맞춘 **합성 해부학 체험**이다. 이를 사용자의 실제 내부·골밀도·근육량·체지방·연골 두께·혈관 상태를 측정한 결과라고 제시할 근거는 이 조사에서 확인하지 못했다. 카메라 수를 늘리면 보이는 표면의 기하 제약은 늘어나지만, 내부 장기를 촬영하는 신호가 추가되는 것은 아니다. 생성 영상의 사실적인 질감과 개인 내부의 정확성은 별개다. X2CT 논문도 광학 표면 복원과 X-ray 내부 복원의 입력 차이를 명시한다. [X2CT 공식 논문](https://openaccess.thecvf.com/content_CVPR_2019/papers/Ying_X2CT-GAN_Reconstructing_CT_From_Biplanar_X-Rays_With_Generative_Adversarial_Networks_CVPR_2019_paper.pdf)

우선순위는 **ComfyUI에서 마스크·외부 깊이·포즈 조건을 사용한 2D 개념 시안 → 사용자 반응 검증 → 검증이 되면 diffusers로 자동화**다. 관절·근육·지방층 등 '뼈보다 더'를 보여주는 요구로 이해하며 병변 생성 요구로 해석하지 않는다. 내부 3D의 회전·층별 보기에는 매 시점 독립 생성보다 일관된 해부학 템플릿을 외형에 맞춰 배치하고 렌더하는 접근이 적절하다. 이 마지막 문장은 본 조사자의 설계 판단이며, RGB에서 개인 내부를 복원했다는 뜻이 아니다.

## 입력에 따른 구분

| 범주 | 실제 입력 | 산출물 | 현재 사진만으로 사용 가능성 |
|---|---|---|---|
| 조건부 2D 생성 | RGB + 텍스트 + 외부 깊이/윤곽/포즈/마스크 | 합성 RGB 그림 | 가능. 개인 내부 측정으로 해석 불가 |
| 외부 전처리 | RGB, 점·박스 등의 프롬프트 | 보이는 영역 마스크, 외부 상대 깊이 | 가능. 뼈·내장 분할 결과가 아님 |
| 의료영상 분할 | 실제 CT/MRI 볼륨 | 장기·근육·뼈 등의 label map | RGB를 대신 넣을 수 없음 |
| X-ray → 합성 CT 연구 | 실제 또는 CT에서 만든 X-ray 투영 | 예측 CT 볼륨 | RGB 사진과 입력 물리가 다름 |
| 무조건/조건부 합성 CT | 잡음, 해부학 조건, 경우에 따라 마스크 | 가상 CT와 마스크 | 개인의 촬영 결과가 아님 |
| 표면 → 합성 X-ray 연구 | 3D 표면 기하 | 통계적으로 예측한 X-ray | 연구 실재. 공개 즉시사용 제품·개인 정확성은 별도 |

## 상세 후보 12개

### 1. ComfyUI — 가장 빠른 시안 도구

- 역할/입력/출력: 노드 그래프로 RGB img2img, 마스크 inpainting, ControlNet 등의 조건을 연결해 2D 합성 이미지를 만든다. 워크플로 재현과 비교에 유리하다.
- 공개성/Windows: 공식 코드 공개. Windows 데스크톱 및 NVIDIA/CPU용 portable이 안내된다. Python 직접 구성보다 시안 접근성이 좋다.
- 라이선스: 엔진 코드는 GPL-3.0. 사용할 체크포인트와 커스텀 노드의 라이선스는 각각 별도이며 GPL만 보고 모델 상업 사용을 판단하면 안 된다.
- GPU: 모델별 요구가 달라 통일 최소 VRAM 미확인. CPU 실행 경로가 있다고 현장 대기시간에 적합하다는 뜻은 아니다.
- 판단: 1순위 시안. 카메라별 생성 결과에 해부학적 다중시점 일관성이 자동 보장되지는 않는다.
- 출처: [공식 저장소·Windows 설치](https://github.com/Comfy-Org/ComfyUI), [코드 라이선스](https://github.com/Comfy-Org/ComfyUI/blob/master/LICENSE)

### 2. Hugging Face diffusers — 자동화용 기반 라이브러리

- 역할/입력/출력: Python/PyTorch 라이브러리. img2img, inpainting, 조건부 diffusion 파이프라인을 앱/API로 묶어 이미지·latent 등을 반환한다. 완성된 '의료영상 변환기'가 아니다.
- 공개성/Windows: 코드 공개. PyTorch 설치가 필요하며 선택 모델·최적화 확장에 따라 Windows 환경 구성이 달라진다. 이 조사에서 해당 조합의 Windows 실행은 미검증.
- 라이선스: 코드 Apache-2.0. 다운로드한 모델·VAE·adapter·전처리기의 가중치 라이선스는 별도다.
- GPU: 공통 최소 VRAM 없음. 모델/해상도/offload별 확인 필요.
- 판단: 2순위. ComfyUI에서 표현과 조건이 정해진 후 여러 카메라·배치·일관된 로그를 처리하는 쪽에 적합하다.
- 출처: [공식 저장소](https://github.com/huggingface/diffusers)

### 3. ControlNet / ControlNet 1.1 — 외형 조건을 붙이는 도구

- 역할/입력/출력: edge, depth, pose, segmentation 등의 조건으로 diffusion 생성을 제어한다. 사진 속 자세·윤곽을 참조한 해부학 일러스트가 가능하다. 'segmentation 조건'은 주어진 label map을 쓰는 기능이지 내부 장기를 사진에서 검출하는 기능이 아니다.
- 공개성/Windows: 공식 코드·사전학습 모델 공개. 원본 Gradio/conda 또는 ComfyUI/diffusers 통합을 사용할 수 있다. 네이티브 Windows 조합은 실행 미검증.
- 라이선스: 코드 Apache-2.0. 예시 depth 가중치 `control_v11f1p_sd15_depth` 모델카드는 OpenRAIL이다. 기반 SD 및 pose/depth annotator의 조건도 별도 확인한다.
- GPU: 원본 README는 8GB GPU용 low-VRAM 모드를 안내한다. 이는 모든 SDXL·고해상도·다중 ControlNet의 8GB 보장이 아니다.
- 판단: 외형 유지에 유용하나 내부 참값을 제공하지 않는다.
- 출처: [공식 코드](https://github.com/lllyasviel/ControlNet), [공식 depth 모델카드](https://huggingface.co/lllyasviel/control_v11f1p_sd15_depth)

### 4. Stable Diffusion XL 1.0 — 합성 이미지의 기반 모델

- 역할/입력/출력: text-to-image 기반 체크포인트. 대응 파이프라인에서 사진/마스크 조건 편집을 구성하며 결과는 2D 이미지다. 해부학 전용 모델로 검증된 것은 아니다.
- 공개성/Windows: 공식 base/refiner 가중치 공개. ComfyUI 또는 diffusers로 실행할 수 있다. Windows 엔진 지원과 실제 모델 속도는 구분해야 한다.
- 라이선스: 가중치는 CreativeML Open RAIL++-M 계열이며 단순 MIT가 아니다. 상업 사용 시 사용 제한을 준수해야 한다. 추가 LoRA의 별도 권리도 확인한다.
- GPU: 모델카드에서 이 용도의 통일 최소 VRAM은 미확인.
- 판단: 일반 시안 기반 후보. 근육·뼈 구조의 오류를 사용자가 실제 내부라고 받아들이지 않게 템플릿/검수가 필요하다.
- 출처: [공식 모델카드](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)

### 5. SAM 2 — 피부·발·다리 외부 마스킹

- 역할/입력/출력: 사진/영상과 점·박스 등의 프롬프트를 받아 보이는 물체 마스크와 영상 추적을 만든다. 다리 외곽, 물/족욕기와 사람 분리, 합성 영역 제한에 적합하다.
- 공개성/Windows: 공식 코드·체크포인트 공개. 공식 문서는 Windows에서 Ubuntu WSL 사용을 강하게 권장한다.
- 라이선스: 모델 체크포인트, 학습·데모 코드 Apache-2.0. 데모 폰트/이모지 및 일부 외부 코드에는 별도 조건이 있다.
- GPU: CUDA 환경 안내는 있으나 이 현장 구성의 최소 VRAM은 미확인. 체크포인트별 속도 비교를 현장 지연으로 환산하지 않았다.
- 판단: 전처리 보조. 피부 아래 근육·장기·뼈를 사진에서 분할하는 모델로 소개하면 부정확하다.
- 출처: [Meta 공식 저장소·설치·라이선스](https://github.com/facebookresearch/sam2)

### 6. Depth Anything V2 — 외부 깊이 조건

- 역할/입력/출력: 단안 RGB → 보이는 표면의 상대 깊이 map. 전경 분리나 ControlNet 조건용이다. 별도 metric 모델도 있으나 실제 크기·거리 정확도 검증은 다른 문제다.
- 공개성/Windows: 코드 및 Small/Base/Large/Giant 가중치 공개. Python/PyTorch 경로가 있으며 이 조사에서 네이티브 Windows 추론은 미검증.
- 라이선스: 코드 Apache-2.0. **Small 가중치 Apache-2.0, Base/Large/Giant 가중치 CC-BY-NC-4.0**. 상업 시안 경로에는 Small부터 검토한다.
- GPU: 정확한 현장 최소 VRAM 미확인. Small이 작다고 반사 수면·증기·피부에서 metric 정확성이 보장되는 것은 아니다.
- 판단: 내부 깊이나 조직 층 두께를 얻는 도구가 아니다.
- 출처: [공식 저장소·모델별 라이선스](https://github.com/DepthAnything/Depth-Anything-V2)

### 7. FLUX.1 Depth [dev] — 고품질 대안, 상업 실행 권리 주의

- 역할/입력/출력: 텍스트와 외부 depth 구조를 따라 2D 이미지를 만든다. 12B rectified-flow 모델이며 FLUX Depth 자체는 일반 ControlNetModel과 동일한 모델이 아니다.
- 공개성/Windows: 가중치 접근에 약관 동의가 필요하다. 공식 diffusers 예제가 있다. 이 환경의 Windows·최적화 조합은 미검증.
- 라이선스: dev 가중치는 FLUX.1 dev Non-Commercial License. 모델카드의 '생성 출력 상업 사용 가능'과 '상업 서비스에서 dev 가중치를 실행 가능'은 다른 권리다. 유료 현장 서비스는 별도 상업 권리/적절한 API를 확인해야 한다.
- GPU: 이 용도 최소 VRAM 미확인. 12B 파라미터 수만으로 특정 GPU 가능 여부를 확정하지 않았다.
- 판단: 권리 확인 후 비교 시안 후보. 사실 정보를 제공할 수 있는 모델이 아니라는 모델카드의 한계도 유념한다.
- 출처: [공식 모델카드](https://huggingface.co/black-forest-labs/FLUX.1-Depth-dev), [diffusers 공식 FLUX 설명](https://github.com/huggingface/diffusers/blob/main/docs/source/en/api/pipelines/flux.md)

### 8. TotalSegmentator — CT/MRI가 있을 때 내부 분할

- 역할/입력/출력: CT 또는 해당 task에 맞는 MRI → 장기·근육·뼈 등의 NIfTI label map. 일부 DICOM segmentation 출력도 지원한다.
- 공개성/Windows: 공식 코드·기본 모델 공개. Windows, Ubuntu, Mac 및 CPU/GPU 지원이 명시돼 있다.
- 라이선스: 코드 Apache-2.0. open task와 별도 허가 task가 나뉜다. 기본 공개 모델 조건을 특수 task에 일반화하면 안 된다. 일부는 비상업 무료 라이선스/상업 별도 계약이며, TOF MRI brain_aneurysm은 CC BY-NC4 및 상업 라이선스 불가로 명시된다.
- GPU: RTX3090 기준 자원 표와 `--fast`, ROI subset, split 메모리 절약 옵션이 있다. 옵션·볼륨과 무관한 단일 최소 VRAM은 여기서 단정하지 않는다.
- 판단: 현재 RGB 시제품의 내부 생성 엔진으로 제외. 동의·권리가 확보된 샘플 CT를 해부학 템플릿으로 가공하는 용도는 가능하나 참여자 본인의 내부가 아니다.
- 출처: [공식 저장소](https://github.com/wasserth/TotalSegmentator)

### 9. MONAI / Auto3DSeg — 의료영상 학습·분할 개발 기반

- 역할/입력/출력: 의료영상 전처리·학습·추론 프레임워크. Auto3DSeg는 데이터 분석→알고리즘 구성→학습→앙상블 과정을 제공한다. 실제 CT/MRI 등의 task 데이터와 맞는 모델이 필요하다.
- 공개성/Windows: 코드 공개. MONAI 설치 문서에 Windows 명령 차이가 안내되지만 각 bundle·확장·학습 구성을 별도 확인해야 한다.
- 라이선스: MONAI 코드 Apache-2.0. bundle 가중치는 해당 bundle 라이선스를 확인한다. MAISI처럼 코드와 weights가 다른 사례가 있다.
- GPU: 모델/학습량에 따라 달라 공통 최소 VRAM 없음.
- 판단: RGB→내부를 즉시 제공하는 모델로 선택할 대상이 아니다. 실제 초음파 도입 후 데이터·라벨·검증을 다룰 개발 기반으로 장기 검토한다.
- 출처: [공식 코드](https://github.com/Project-MONAI/MONAI), [Auto3DSeg 공식 문서](https://monai.readthedocs.io/en/stable/modules.html), [Windows 설치 안내](https://github.com/Project-MONAI/MONAI/blob/dev/docs/source/installation.md)

### 10. 3D Slicer — 의료영상과 해부학 3D를 확인하는 GUI

- 역할/입력/출력: DICOM/볼륨/분할/mesh의 표시·편집·등록·3D 렌더링. CT/MRI의 label을 표면 모델로 만드는 등 의료영상 콘텐츠 제작에 적합하다. 단순히 사진을 넣어서 개인 내부를 알아내는 앱은 아니다.
- 공개성/Windows: Windows 배포판이 공식 제공된다. 사람 손으로 label을 검토하고 데모용 렌더를 만드는 데 접근성이 좋다.
- 라이선스: BSD 스타일 Slicer 라이선스는 상업 사용을 허용한다. 확장·모델·입력 데이터의 권리는 별도로 확인한다.
- GPU: GPU volume rendering이 있으나 분할/렌더 설정별 최소 VRAM 미확인.
- 판단: 샘플 해부학 콘텐츠 검토와 3D 시연 제작에 추천. Slicer가 생성 모델의 환각이나 개인 식별 정확성을 보증하지는 않는다.
- 출처: [공식 상업 사용 설명](https://www.slicer.org/commercial-use.html), [공식 Windows 다운로드](https://download.slicer.org/), [DICOM 문서](https://slicer.readthedocs.io/en/latest/user_guide/modules/dicom.html)

### 11. NVIDIA MAISI — 가상 3D CT 생성, 개인 복원 아님

- 역할/입력/출력: 잡음·해부학/크기 조건 등으로 synthetic 3D CT와 짝지은 segmentation mask를 생성한다. 사진으로 특정인의 내부를 측정하는 모델이 아니다.
- 공개성/Windows: MONAI 공식 튜토리얼·구성이 공개돼 있다. CUDA/서버 실행 예제가 중심이며 이 조사에서 Windows 전체 워크플로 지원·추론을 검증하지 않았다.
- 라이선스: 현재 공식 튜토리얼 **코드 Apache-2.0 / 가중치 NSCLv1**. weights 파일의 3.3항은 비상업적 연구·평가 용도로 제한한다. MONAI가 Apache라는 이유로 이 가중치의 상업 서비스 사용을 허용된다고 판단하면 안 된다.
- GPU: 공식 현재 튜토리얼은 설정별 메모리 표를 제공한다. 예: 512×512×128에서 약 15.7GB, 512³에서 약 22.8GB 설정이 있으며 A100 80GB에서 측정했다. 오래된 bundle의 512³ 58GB 안내와 혼합하지 않는다.
- 판단: 학술적 synthetic CT 연구 후보. 현장 MVP 1순위가 아니다.
- 출처: [공식 튜토리얼·자원표](https://github.com/Project-MONAI/tutorials/tree/main/generation/maisi), [가중치 사용 제한 원문](https://github.com/Project-MONAI/tutorials/blob/main/generation/maisi/LICENSE.weights), [별도 bundle 문서](https://huggingface.co/MONAI/maisi_ct_generative/blob/main/docs/README.md)

### 12. X2CT-GAN — X-ray 두 장 → 예측 CT 연구

- 역할/입력/출력: 직교하는 두 X-ray projection → 3D CT 예측. 공식 저자 코드는 실험 모델·데이터 및 CT→synthetic X-ray 학습 경로를 제공한다. 정면/측면 RGB 사진을 같은 입력으로 취급할 수 없다.
- 공개성/Windows: 공식 코드·학습 모델 제공은 확인. 오래된 PyTorch/CUDA 의존성이 있으며 현재 Windows에서 즉시 실행 가능성은 미검증. GPU 최소 VRAM도 미확인.
- 라이선스: README는 GPLv3라고 설명하지만 저장소 표시는 LGPL-3.0이고 LICENSE는 GPL 본문과 LGPL 추가 허가를 포함한다. 이 불일치를 숨기지 않으며 정확한 배포 artifact·가중치·데이터 권리를 확인할 때까지 무제한 상업 가능으로 분류하지 않는다.
- 판단: '2장으로 CT 생성' 표현의 입력 오해를 교정하는 연구 사례다. RGB-only MVP 후보에서 제외한다.
- 출처: [저자 공식 저장소](https://github.com/kylekma/X2CT), [LICENSE](https://github.com/kylekma/X2CT/blob/master/LICENSE), [논문](https://arxiv.org/abs/1905.06902)

## RGB·표면 → 내부 연구는 정말 있는가?

**있다. 다만 합성/예측 연구의 존재와 개인 내부의 측정 가능성을 구분해야 한다.** Teixeira 등의 CVPR 2018 연구는 사람의 3D surface geometry에서 synthetic X-ray를 예측하고, body marker를 바꿔 여러 영상을 생성한다. [저자 논문](https://arxiv.org/abs/1805.00553)

이 연구의 입력은 일반 스마트폰 RGB 한 장이라는 설명이 아니라 표면 기하다. 따라서 여러 카메라로 얻은 외형 3D와 개념적으로 접점은 있다. 그러나 공개 논문만으로 발·족욕기 데이터의 검증 정확도, 즉시 쓸 공식 weights, 상업 허가, Windows 지원, 최소 GPU를 확인하지 못했다. **논문 존재 = 공개 실행 제품 = RGB 기반 진단 정확성**으로 이어지지 않는다. 해당 연구를 사업 설명에 쓰려면 '표면에서 통계적 내부 추정 연구가 있다'까지만 말하는 것이 정확하다.

'RGB→X-ray'라는 이름의 일반 이미지 변환이나 X-ray 스타일 필터도 가능한 이미지 생성 범주다. 내부를 관측한 신호가 없는 상태에서 개인별 내부 특징의 정답을 검증하지 못했다면 이는 체험 영상이다. 동일한 외형에 여러 내부 해부학이 대응할 수 있다는 점 때문에 생성 모델은 학습한 사전분포로 빈 정보를 채운다. [X2CT 논문의 복원 모호성 논의](https://openaccess.thecvf.com/content_CVPR_2019/papers/Ying_X2CT-GAN_Reconstructing_CT_From_Biplanar_X-Rays_With_Generative_Adversarial_Networks_CVPR_2019_paper.pdf)

## 기타 관련 후보와 제외 이유

- **DiffuX2CT**: diffusion 기반 X-ray→CT 연구. 입력이 biplanar X-ray인 점은 동일해 RGB-only 경로에서 제외한다. 코드·weights·상업 조건 및 Windows/GPU는 본 조사에서 개별 확인하지 않았다. [저자 논문](https://arxiv.org/abs/2407.13545)
- **Xray2CT / neural implicit CT reconstruction**: 소수 각도의 planar X-ray를 이용한다. 논문이 코드 링크를 제공하지만 RGB-only 생성기가 아니다. [저자 논문·코드 링크](https://arxiv.org/abs/2308.02100)
- **MONAI Label / Slicer MONAI Auto3DSeg extension**: 분할 작업을 돕는 통합 UI다. CT/MRI task 모델을 쓴다고 입력이 RGB로 바뀌지 않는다. [공식 MONAI Label 설치](https://monai.readthedocs.io/projects/label/en/latest/installation.html), [Slicer 확장 저장소](https://github.com/lassoan/SlicerMONAIAuto3DSeg)
- **3D 복원·avatar 모델**은 다른 담당 범위다. 이 보고서의 depth와 segmentation은 그 전처리로 연결할 수 있으나 외부 mesh 안을 채운 해부학은 별도 합성 콘텐츠임을 유지해야 한다.

## 권장 MVP의 표현과 평가

1. 사진에서 발/다리 마스크와 외부 depth/윤곽을 얻는다.
2. 피부 바깥 외형은 사진을 따르고, 내부는 검수한 일반 해부학 템플릿 또는 명시적 합성 일러스트로 보여준다.
3. 2D 확산 생성은 색감·표현·전환 시안에 사용한다. 각 시점에 독립 생성한 뼈/혈관을 합쳐 의료적인 3D 정답이라고 부르지 않는다.
4. 첫 화면과 내부 화면에 **'사진의 외형을 바탕으로 만든 합성 해부학 체험입니다. 실제 내부를 촬영·측정한 결과가 아닙니다.'**를 표시한다.
5. 설문은 '내 몸을 이해하는 데 도움', '재미/몰입', '다시 쓸 의향', '실제 초음파 촬영 체험에 대한 관심'을 따로 묻는다. 사진만으로 내부를 봤다고 오인했는지도 확인한다.

합성 체험에 대한 호감은 초음파의 촬영 품질·조직 정량화·임상적 유용성 검증이 아니다. 미래 초음파 수요를 조사한다면 영상의 인상과 실제 장비 촬영 서비스에 대한 지불/체험 의향을 나눠 해석한다. 근육량·체지방률 등 숫자를 표시하려면 별도 측정 장비나 해당 추정모델의 표적·참값·오차 검증이 필요하며, 이 생성 스택에서 나온 수치를 신체 측정값으로 사용하지 않는다.

## 조사 한계와 경로 정렬

- 확인한 것: 12개 상세 후보의 공식 존재, 입력·출력, 코드/모델 권리 차이, 공개 문서의 플랫폼·자원 안내.
- 미확인: 현장 카메라 샘플의 품질, 수면/증기/반사 영향, 설치 성공, 실시간 속도, 생성 해부학의 일관성, 임상·정량 정확도.
- 사용자 결과 경로와 실제 작성 경로: 모두 `린/outputs/research_generation_20261030.md`.
- 런타임 배포/스케줄러: 없음. 실행 테스트 미수행.
- 푸시 브랜치/커밋: 없음. 현재 작업 디렉터리는 git 저장소가 아니므로 병합·푸시 대상이 없다.

