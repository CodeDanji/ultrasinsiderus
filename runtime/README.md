# 실행 가능한 사진 → 표준 모형 → 렌더링 시제품

이전 저장소 추출에서 빠진 로컬 구현을 이 폴더에 포함했다. 실행 코드, 사전학습 가중치, 3D 원본 자산, 웹 화면을 Git으로 함께 받는다. 결과 이미지 모음만 있는 폴더가 아니다.

## 포함 파일

| 위치 | 역할 |
|---|---|
| `app.py`, `web/` | 로컬 사진 업로드, 외형 확인, 결과·의견·삭제 화면 |
| `run.py`, `generate_anatomy.py` | 검사·샘플·사진 처리 진입점과 단계 실행 |
| `silhouette.py` | rembg U²-Netp 분할, 선택적 작업자 확인 마스크 |
| `build_anatomy.py` | 표준 해부학 메시 추출·근사 정렬, 선택적 수동 기준점 |
| `render_photo_layers.py`, `photo_composite.py` | 같은 GLB의 Blender 렌더 레이어와 원본 사진 합성 |
| `assets/weights/u2netp.onnx` | 실제 사전학습 분할 가중치 (~4.4MB) |
| `assets/ecorche.glb`, `assets/vessels.glb` | 실제 사용하는 뼈·근육 및 혈관 참조 자산 (~16MB) |
| `assets/manifest.json`, 출처·라이선스 문서 | 원출처, 고정 버전, 체크섬, 이용조건 |
| `requirements.txt`, `constraints-linux-py312.txt`, `environment.json` | 의존성과 검증 환경 |
| `references/synthetic-footbath.png` | 실행 검증용 합성 사진. 실제 이용자 사진이 아님 |

개인 입력·출력, 기존 가상환경과 OS별 Blender 실행 바이너리는 포함하지 않았다. Python과 Blender를 먼저 설치한다. 모델/자산이 Git LFS 포인터가 아니라 실제 바이너리로 포함되므로 `git clone`으로 받는다.

## Linux 설치와 실행

Python 3.12와 Blender **4.3.2**를 설치하고 `blender`가 PATH에서 실행되는지 확인한다. Blender 다운로드: https://download.blender.org/release/Blender4.3/ . 시스템 그래픽·공유 라이브러리가 필요할 수 있으며, 테스트 환경은 `environment.json`을 따른다.

```sh
cd runtime
bash setup.sh
.venv/bin/python run.py check
.venv/bin/python run.py sample --output results/first-sample
.venv/bin/python app.py
```

실행한 컴퓨터의 브라우저에서 `http://127.0.0.1:8765`를 연다. 클라우드에서 실행하면 이 주소는 클라우드 컴퓨터의 로컬 주소다. 공개 호스팅은 구성하지 않았다. 결과 폴더는 덮어쓰지 않으므로 다시 시험할 때 새 `--output`을 지정한다.

## Windows 설치와 실행

Python 3.12와 Blender 4.3.2를 설치한다. PowerShell에서:

```powershell
cd runtime
.\setup.ps1
$blender = 'C:\Program Files\Blender Foundation\Blender 4.3\blender.exe'
.\.venv\Scripts\python.exe run.py check --blender $blender
.\.venv\Scripts\python.exe run.py sample --blender $blender --output results\first-sample
```

`app.py`는 `blender` 명령을 사용하므로 웹 화면 실행 전 Blender 폴더를 해당 PowerShell의 PATH에 추가한다.

```powershell
$env:Path = 'C:\Program Files\Blender Foundation\Blender 4.3;' + $env:Path
.\.venv\Scripts\python.exe app.py
```

PowerShell 절차는 제공하지만 Windows에서 실행 검증한 것은 아니다. Linux에서 의존성을 고정한 목록은 `constraints-linux-py312.txt`이며 Windows에서는 `requirements.txt`를 사용한다.

## 직접 사진 처리

발끝이 오른쪽인 측면 사진을 기본 경로로 사용한다. 실제 실행 코드의 지원 범위이며, 다른 자세를 자동 인식해 정렬하는 구현은 아니다.

```sh
.venv/bin/python run.py process --image /path/to/photo.jpg --output results/my-photo
```

기존 실사진 실증은 **분할 마스크 선택과 외부 기준점 4곳을 수동 확인**했다. 사선·왼쪽 방향 사진을 완전 자동 처리했다고 주장하지 않는다. 같은 절차를 재현하려면 원본과 처리 크기(최대 1024px)에 맞춘 마스크, 기준점 JSON을 지정한다.

```sh
.venv/bin/python run.py process --image /path/to/photo.jpg --mask /path/to/mask.png --anchors /path/to/anchors.json --output results/assisted-photo
```

기준점 형식:

```json
{"anchors":[
 {"mesh":"Distal phalanx of left big toe","pixel_xy":[277,286]},
 {"mesh":"Distal phalanx of left little toe","pixel_xy":[278,415]},
 {"mesh":"Left calcaneus","pixel_xy":[719,477]},
 {"mesh":"Left tibia","point":"upper_end","pixel_xy":[869,105]}
]}
```

위 값은 형식 예시다. 자기 사진에 그대로 적용하면 맞지 않는다. 기준점은 개인 내부를 측정한 것이 아니라 표준 모형을 대략 배치하는 작업자 가정이다.

`result.json`에는 원본 SHA-256, 단계, 출력, 실패 이유가 남는다. `anatomy/illustrative-foot.glb`가 실제 렌더링 모형이다. `views/front.png`와 조직별 PNG는 이 모형의 RGBA 렌더를 입력 사진과 합성한 결과다. `segmentation/diagnostic.png`로 분리를 확인한다. 가중치와 자산은 포함되어 있으므로 정상 설치 후 추론 때 모델 다운로드는 필요하지 않다.

## 검사·한계·보관

```sh
.venv/bin/python -m unittest discover -s tests -v
```

`run.py check`는 번들 자산 SHA-256과 필수 모듈·Blender 버전을 확인한다. 설치에는 Python 패키지 다운로드용 인터넷이 필요하다. 모든 OS 의존성이나 Python/Blender 자체를 넣은 완전 오프라인 설치본은 아니다.

실제 수중 굴절 보정, 4카메라 융합, 개인 내부 복원, 임상 성능, 시민 만족도는 검증하지 않았다. 사진 외형에 맞춘 **표준 참조 시뮬레이션**이다. 혈관 정렬은 근사이고 지방패드는 도식적이다. 결과를 실제 측정·검사로 설명하면 안 된다.

사진은 로컬 `local-sessions/`에 보관되며 자동 만료하지 않는다. 사용자 동의와 보관·삭제 방침을 정한다. 화면의 삭제는 해당 사진·결과·의견을 함께 지운다. 이 폴더와 `results/`, `.venv/`는 Git에서 제외한다. 개인 사진을 새로 커밋하지 않는다.

## 동일 GLB의 HTML 뷰어 만들기

```sh
.venv/bin/python build_viewer.py --model results/first-sample/anatomy/illustrative-foot.glb --output results/first-sample/viewer.html
```

모형을 바꾸지 않고 GLB 바이트와 뷰어 코드를 HTML 안에 넣는다. 뷰어에는 외부 서버로 사진·모델을 전송하는 코드가 없다. 파일 열기가 브라우저 정책으로 막히면 해당 결과 폴더에서 `python -m http.server 8871 --bind 127.0.0.1`로 열 수 있다.

`viewer/viewer.js`, 정확한 npm 버전·lock, 사전 빌드된 `bundle.js`도 포함했다. 뷰어를 변경해 재빌드할 때만 Node.js 20+에서 `cd viewer && npm ci && npm run build`를 실행한다. 일반 파이프라인과 HTML 생성에는 Node.js가 필요 없다.

실제 수행한 새 환경 검증과 한계는 [VALIDATION.md](./VALIDATION.md)에 있다. 특히 기존 PNG와의 일치는 확인했지만 GLB 구 메시의 삼각분할 인덱스는 실행 사이에 달라질 수 있어 파일 전체 해시의 재현을 보장하지 않는다.
