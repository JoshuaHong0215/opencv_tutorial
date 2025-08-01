
# QR 코드 인식 프로젝트

이 프로젝트는 Python의 OpenCV와 pyzbar 라이브러리를 사용하여  
QR 코드를 디코딩하고 시각화하거나, 자동으로 웹사이트를 여는 기능을 포함합니다.

---

## 파일 구성

| 파일명 | 설명 |
|--------|------|
| `qr_scan.py` | 이미지 파일에서 QR 코드 인식 및 정보 시각화 |
| `qr_video_scan.py` | 웹캠을 통해 실시간 QR 코드 인식 및 브라우저 자동 연결 |

---

## 1. qr_scan.py

### 목적
- 정적인 이미지(`frame.png`)에서 QR 코드를 인식하고
- 디코딩된 정보를 이미지에 시각적으로 표시
- 최종 결과 이미지를 matplotlib으로 출력

### 실행 흐름 요약

```python
img = cv2.imread('../img/frame.png')            # 1. 이미지 로드
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    # 2. 흑백 변환
decoded = pyzbar.decode(gray)                   # 3. QR 디코딩
for d in decoded:                               # 4. 각 QR 정보에 대해 반복
    ...
plt.imshow(img)                                 # 5. 이미지 시각화
```

---

### QR 디코드 for문

```python
for d in decoded:
    print(d.data.decode('utf-8'))
    print(d.type)

    barcode_data = d.data.decode('utf-8')
    barcode_type = d.type

    text = '%s (%s)' % (barcode_data, barcode_type)

    cv2.rectangle(img, (d.rect[0], d.rect[1]),
                  (d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]),
                  (0, 255, 0), 20)

    cv2.putText(img, text, (d.rect[0], d.rect[0]),
                cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 255), 15, cv2.LINE_AA)
```

#### 흐름 설명:

1. `for d in decoded:`  
   → QR 코드가 여러 개일 수 있으므로 각각 반복 처리  
2. `d.data.decode('utf-8')`  
   → 바이트 데이터를 문자열로 디코딩  
3. `d.type`  
   → QR인지, CODE128인지 등 바코드 타입 확인  
4. `cv2.rectangle(...)`  
   → 인식된 QR 영역에 초록색 사각형 표시  
5. `cv2.putText(...)`  
   → 디코딩된 문자열을 이미지에 표시

#### 주요 함수 및 파라미터 설명

| 함수 | 파라미터 | 설명 |
|------|----------|------|
| `cv2.rectangle(img, pt1, pt2, color, thickness)` | `pt1`, `pt2`: 시작/끝 좌표<br>`color`: BGR 색상<br>`thickness`: 선 두께 | 이미지에 사각형 그리기 |
| `cv2.putText(img, text, org, font, fontScale, color, thickness, lineType)` | `text`: 출력 문자열<br>`org`: 시작 위치<br>`font`: 글꼴<br>`fontScale`: 크기<br>`color`: 색상<br>`thickness`: 굵기<br>`lineType`: 선 유형 | 이미지에 텍스트 쓰기 |

---

## 2. qr_video_scan.py

### 목적
- 웹캠을 통해 실시간으로 QR 코드 인식
- 디코딩된 내용이 URL이면 자동으로 웹 브라우저 실행

### 전체 흐름 요약

```python
cap = cv2.VideoCapture(0)                           # 1. 웹캠 연결
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)             # 2. 해상도 설정
opened_urls = set()                                 # 3. 중복 열기 방지용 set 생성

while cap.isOpened():
    ret, frame = cap.read()                         # 4. 프레임 읽기
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 5. 흑백 변환
    decoded = pyzbar.decode(gray)                   # 6. QR 디코딩
    for d in decoded:
        ...
    cv2.imshow("QR Scanner", frame)                 # 7. 화면 출력
    if cv2.waitKey(1) & 0xFF == ord('q'):           # 8. 종료 조건
        break
```
#### 🔍 while 루프 설명
- `while cap.isOpened():`  
  → 웹캠이 정상적으로 열려 있는 동안 루프를 지속합니다.
- `ret, frame = cap.read()`  
  → 웹캠에서 한 프레임을 읽어옴. `ret`은 성공 여부, `frame`은 이미지 데이터입니다.
- `gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)`  
  → 컬러 이미지를 흑백(Grayscale)으로 변환하여 디코딩을 쉽게 만듭니다.(인식효율 UP)
- `decoded = pyzbar.decode(gray)`  
  → 프레임에서 QR 또는 바코드를 감지하고 디코딩합니다.
- `for d in decoded:`  
  → QR 코드가 여러 개 있을 수 있으므로 각각 처리합니다.
- `cv2.imshow("QR Scanner", frame)`  
  → 인식 결과가 반영된 프레임을 화면에 출력합니다.("QR Scanner는 창의 제목)
- `cv2.waitKey(1) & 0xFF == ord('q')`  
  → 사용자가 'q' 키를 누르면 루프를 종료하고 프로그램을 끝냅니다.

---

### 🔁 QR 디코드 & URL 열기 흐름 설명

```python
for d in decoded:
    data = d.data.decode('utf-8')        # QR 내용 추출
    barcode_type = d.type                # QR 코드 종류
    x, y, w, h = d.rect                  # 사각형 위치 정보

    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 0, 255), 2, cv2.LINE_AA)

    if data.startswith("http") and data not in opened_urls:
        webbrowser.open(data)
        opened_urls.add(data)
```

#### 🔍 흐름 설명:

1. `data = d.data.decode('utf-8')`  
   → QR에 담긴 문자열 추출
2. `d.rect`  
   → (x, y, w, h): QR 코드 영역의 위치
3. `webbrowser.open(data)`  
   → QR 내용이 URL이면 자동 브라우저 실행
4. `opened_urls.add(data)`  
   → 중복 실행 방지
