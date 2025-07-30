# 2025. 07. 29 02_openCV_README

---

## 1. 각 프로젝트 개념 정리

| 개념 | 설명 |
|------|------|
| **BGR → GRAY/HSV 변환** | 컬러 이미지를 흑백(Grayscale) 또는 색상(Hue), 채도(Saturation), 명도(Value)로 분해 |
| **ROI (관심 영역)** | 이미지에서 특정 영역만 잘라내거나 선택해서 작업 |
| **마스킹** | 이미지의 특정 영역만 처리하고, 나머지는 무시하는 기법 |
| **Thresholding (이진화)** | 픽셀 값 기준으로 흑/백으로 나누어 단순화 |
| **히스토그램 처리** | 이미지의 픽셀 값 분포를 분석하거나 보정 |
| **정규화 / 이퀄라이즈** | 명암 대비를 개선하여 선명도 향상 |

---

## 2. 예제별 개념 + 기능 + 코드 분석

### 색상 변환 관련

#### `bgr2gray.py`
- **목적**: 컬러 이미지를 흑백 이미지로 바꾸는 두 가지 방식 비교
- **사용 함수**: `cv2.split`, `cv2.cvtColor`
- **코드 분석**:
  - `cv2.split(img)` : B, G, R 채널로 나눈다
  - `(b + g + r)/3` : 단순 평균 방식의 수동 변환
  - `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` : OpenCV 내장 흑백 변환

---

#### `bgr2hsv.py`
- **목적**: HSV 색 공간 이해 (색상, 채도, 명도)
- **사용 함수**: `cv2.cvtColor`
- **코드 분석**:
  - 빨/초/파/노 픽셀을 BGR로 정의 → HSV로 변환
  - HSV 값이 어떤 숫자로 표현되는지 확인

---

### ROI (관심 영역)

#### `roi.py`
- **목적**: 마우스로 이미지에서 원하는 부분을 드래그해 잘라내기
- **사용 함수**: `cv2.setMouseCallback`, `cv2.rectangle`, `cv2.imwrite`
- **코드 분석**:
  - 드래그 시작 좌표(`x0`, `y0`)와 끝 좌표로 `roi = img[y0:y0+h, x0:x0+w]`를 추출
  - 선택된 영역을 저장(`cv2.imwrite`)하고 새 창으로 표시

---

### 마스킹 / 합성

#### `bitwise_masking.py`
- **목적**: 원형 마스크로 특정 영역만 남기고 나머지 제거
- **사용 함수**: `cv2.circle`, `cv2.bitwise_and`
- **코드 분석**:
  - `mask = np.zeros_like(img)` : 검정색 마스크
  - np.zeros_like(array)의 뜻은 입력된 array와 같은 크기,데이터 형식을 가진,모든값이 0인 배열을 뜻함
  - `cv2.circle(...)` : 흰색 원형 마스크 생성
  - `bitwise_and(img, mask)` : 이미지와 마스크를 AND 연산

---

#### `chromakey.py`
- **목적**: 특정 색상(크로마키)을 제거하고 배경 이미지와 합성
- **사용 함수**: `cv2.inRange`, `cv2.bitwise_and`, `cv2.add`
- **코드 분석**:
  - HSV 색상 범위를 기준으로 마스크 생성 (`cv2.inRange`)
  - 전경/배경을 각각 마스킹 → 합성

---

### 이진화 (Thresholding)

#### `threshold.py`
- **목적**: 이미지의 픽셀 값을 기준으로 흑/백으로 나누기
- **사용 함수**: `cv2.threshold`, Numpy 연산
- **코드 분석**:
  - `img > 127` 조건을 사용해 Numpy 방식으로 이진화
  - thresh_np[ img > 127] = 255 라는 코드는 127이상은 255로 변경한다는 뜻
  - 127보다 크면 255(흰색), 작으면 0(검정)
  - `cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)` : OpenCV 방식
  - 127: 픽셀값 기준, 255: 조건을 만족하는 픽셀 값

---

#### `threshold_otsu.py`
- **목적**: Otsu 알고리즘으로 최적 임계값 자동 계산
- **사용 함수**: `cv2.threshold(... | cv2.THRESH_OTSU)`
- **코드 분석**:
  - `cv2.threshold(img, -1, 255, THRESH_BINARY | THRESH_OTSU)` : Otsu 알고리즘 사용
  - 자동으로 임계값(`t`)을 출력

---

### 히스토그램 및 밝기 보정

#### `histo_gray.py`
- **목적**: 히스토그램 시각화
- **사용 함수**: `cv2.calcHist`, `matplotlib.pyplot.plot`
- **코드 분석**:
  - `calcHist([img], [0], None, [256], [0, 256])` : 픽셀 분포 계산
  - `plt.plot()`으로 시각화

---

#### `histo_nomalize.py`
- **목적**: 이미지의 밝기 범위를 0~255로 맞추기
- **사용 함수**: `cv2.normalize`
- **코드 분석**:
  - 수식 연산: `(img - min) / (max - min) * 255`
  - `cv2.normalize(..., NORM_MINMAX)`는 자동 처리

---

#### `histo_equalize.py`
- **목적**: 대비를 향상시키는 히스토그램 이퀄라이즈
- **사용 함수**: `cv2.equalizeHist`
- **코드 분석**:
  - `cumsum()`으로 누적 히스토그램 → 직접 계산
  - `equalizeHist()`로 자동 대비 향상

---

## 실행 방법

```bash
python bgr2gray.py
```

