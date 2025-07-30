
# 실시간 Grayscale 히스토그램과 중심점 추적을 활용한 라인 트레이서 코드

## 라인 트레이서
- 검은 색 라인을 인식해서 라인을 따라가는 장치로 따라서 굳이 카메라 RGB를 쓸 필요는 없음(쫌 과함)
- 따라서 그레이히스토그램으로 BINARY 즉, 이진화 시켜서 흑과 백으로 나누고 인식하여 효율을 최적화함

---

## 📦 사용 라이브러리

- `opencv-python` (cv2)
- `numpy`
- `matplotlib`

---

## 🧠 코드 기능 요약

### 1. `plt.ion()`  
- Matplotlib의 **인터랙티브 모드**를 활성화하여 실시간 업데이트 가능

### 2. `cv2.VideoCapture(0)`  
- 기본 웹캠(0번 장치) 연결

---

## 🎯 주요 처리 흐름

### 📌 [1] ROI(관심영역) 설정

```python
h, w = frame.shape[:2]
roi_x1, roi_x2 = w // 2 - 300, w // 2 + 300
roi = frame[50:, roi_x1:roi_x2]
```

- 영상의 가로 중심 기준 좌우 `300px`씩 → 총 `600px` 가로폭  
- 상단 `50px`은 제외하여 잡음 제거 (세로 슬라이싱: `50:`)  
- ROI는 관심 객체가 위치할 것으로 예상되는 **세로 막대 영역**을 지정함

---

### 📌 [2] Grayscale 변환 및 Threshold 처리

```python
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)
```

- `cv2.cvtColor`: BGR → Grayscale 변환
- `cv2.threshold`: 밝기 `80 이하`를 흰색(255), 나머지는 검정(0)으로 반전  
  → 검은 물체 인식에 유리한 방식 (`THRESH_BINARY_INV`)

---

### 📌 [3] 외곽선 검출 및 중심점 표시

```python
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
```

- 외곽선 목록 추출  
- 반복문에서 각 contour의 면적(`cv2.contourArea`)이 **1000 이상일 때만 처리**

```python
M = cv2.moments(cnt)
cx = int(M['m10'] / M['m00']) + roi_x1
cy = int(M['m01'] / M['m00'])
```

- 영상의 **모멘트(moment)**를 통해 중심점(centroid) 계산
- `+ roi_x1`은 ROI에서 전체 영상 좌표로 **보정**하는 것

---

### 📌 [4] 외곽선 시각화

```python
cv2.circle(contour_img, (cx, cy), 4, (0, 0, 255), -1)
cv2.drawContours(contour_img, [cnt_offset], -1, (0, 255, 0), 2)
```

- 빨간 점: 중심점 표시
- 초록선: 외곽선 윤곽 그리기  
  ※ `cnt_offset`은 좌표 보정된 외곽선

---

### 📌 [5] 히스토그램 시각화

```python
hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()
line.set_ydata(hist)
fig.canvas.draw()
fig.canvas.flush_events()
```

- `cv2.calcHist`: 픽셀 밝기값의 분포 계산 (0~255)
- `matplotlib` 실시간 갱신

---

### 📌 [6] 종료 조건

```python
key = cv2.waitKey(1) & 0xFF
if key == ord('q'):
    break
```

- 키보드에서 `'q'` 키를 누르면 루프 탈출

---

## 📌 변수 및 파라미터 요약

| 변수/함수 | 역할 |
|-----------|------|
| `roi_x1, roi_x2` | ROI의 가로 시작/끝 좌표 |
| `gray` | Grayscale 이미지 |
| `binary` | Threshold 결과 (이진화 영상) |
| `contours` | 추출된 외곽선 목록 |
| `cv2.contourArea()` | contour의 면적 계산 |
| `cv2.moments()` | 중심점 계산용 수학적 모멘트 |
| `cx, cy` | 중심점 좌표 |
| `cv2.circle()` | 중심점에 빨간 점 그리기 |
| `cv2.drawContours()` | 초록 외곽선 그리기 |
| `cv2.calcHist()` | 히스토그램 계산 |
| `plt.ion()` | matplotlib 실시간 시각화 |
| `cv2.waitKey(1)` | 1ms 동안 키 입력 대기 |

---

## 📸 결과

- `Gray ROI` 창: 이진화된 ROI 영상
- `Contours (ROI)` 창: 원본 영상 + contour + 중심점
- `matplotlib`: 실시간 밝기 분포 그래프
