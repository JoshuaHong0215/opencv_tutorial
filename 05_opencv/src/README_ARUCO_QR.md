# ArUco 마커 및 QR 코드 기반 실시간 거리 측정 및 포즈 추정

이 프로젝트는 OpenCV 기반으로 ArUco 마커를 인식하고, 거리 및 회전 정보를 추정하며, 마커와의 거리에 따라 상태(GO/STOP)를 판단하는 기능을 포함합니다. QR코드를 통한 실시간 웹 이동 기능도 포함됩니다.

로봇비전, 증강현실, 자동화 공정등 다양한 분야에서 마커의 위치와 방향을 추정하는데 활용할 수 있음
**따라서 추후 반드시 코드의 흐름과 작용방식을 이해해야함**

## 단계별 설명
---
step_01(photo.py)
- 캘리브레이션 base 사진촬영
- step_01와 02는 카메라와 렌즈의 왜곡 Parameter를 얻기 위함
- 너무 과한 perspective는 지양하고 적정수준의 perspective 유지

step_02(calibration.py)
- 캘리브레이션 진행

step_03 (scanArucoMarker2.py)
- 아루코마커 진행

step_04 (distanceDetection2.py)
- 거리에 따라 경고문구, 혹은 경고음을 출력한다
---

---

## 파일 구성 및 역할

| 파일명 | 기능 설명 |
|--------|-----------|
| `photo.py` | 사진 촬영 후 저장 (단일 이미지) |
| `calibration3.py` | 카메라 캘리브레이션 수행 및 결과 저장 (`camera_calibration.pkl`) |
| `scanArucoMarker2.py` | ArUco 마커 인식 및 포즈 추정 (회전, 위치) 표시 |
| `distanceDetection2.py` | 마커 거리 측정 후 일정 거리 이하일 경우 STOP 텍스트 출력 |

---

## photo.py (이미지 캡처)

1. `cv2.VideoCapture(0)`를 통해 웹캠에서 프레임을 받아 저장
2. 사용자 키보드 입력 `s`를 누르면 이미지를 저장하고 종료

---

## calibration3.py (카메라 캘리브레이션)

1. OpenCV의 `cv2.findChessboardCorners`와 `cv2.calibrateCamera`로 카메라 보정
2. 보정 결과로 내부 파라미터(`camera_matrix`)와 왜곡 계수(`dist_coeffs`)를 pickle로 저장

### 주요 변수/함수
- `objpoints`: 체스보드 3D 좌표
- `imgpoints`: 각 이미지에서 검출된 2D 좌표
- `cv2.calibrateCamera`: 내부 파라미터 추정

---

## scanArucoMarker2.py (마커 인식 및 포즈 추정)

1. 카메라에서 실시간 프레임 읽기
2. 카메라 왜곡 보정 수행
3. ArUco 마커 인식 및 회전벡터, 이동벡터 추정
4. ID, 좌표, 회전값을 이미지에 출력

### 함수 설명
#### `estimate_pose_single_marker()`
- 마커의 코너(2D)와 실제 크기(3D)를 바탕으로 `solvePnP`로 포즈 계산

#### `live_aruco_detection()`
- 마커 인식 → 포즈 추정 → 이미지에 정보 출력까지 실시간 수행

```python
cv2.putText(img, f"Pos: ({x},{y},{z})", ...)  # 위치 정보 출력
cv2.drawFrameAxes(...)  # 좌표축 그리기
```

---

## distanceDetection2.py (거리 기반 상태 판단)

- `scanArucoMarker2.py` 기반에 조건문 추가:
  - 마커와의 거리 `z < 0.3m` → 빨간 STOP 메시지 출력
  - 거리 초과 시 → 초록 GO 메시지 출력

```python
if pos_z < 0.30:
    cv2.putText(..., "STOP", ...)
else:
    cv2.putText(..., "GO", ...)
```

---

## 주요 개념 요약

| 함수/개념 | 설명 |
|------------|------|
| `cv2.solvePnP` | 3D-2D 점 대응을 바탕으로 위치 및 회전 추정 |
| `cv2.drawFrameAxes` | 마커 위치에 X,Y,Z 축 그리기 |
| `cv2.undistort` | 렌즈 왜곡 보정 |
| `cv2.aruco.ArucoDetector` | 마커 탐지 객체 생성 (OpenCV 4.7 이상) |
| `cv2.putText` | 이미지에 텍스트 추가 (위치, 폰트, 크기 등 지정 가능) |
| `cv2.getTextSize` | 텍스트 크기 측정 (배경 사각형 그릴 때 활용) |

---

## 프로그램 실행 순서
1. **카메라 보정:** `calibration3.py` 실행하여 `camera_calibration.pkl` 생성
2. **테스트 이미지 캡처:** `photo.py` 사용
3. **마커 포즈 확인:** `scanArucoMarker2.py` 실행 (실시간 마커 ID, 위치, 회전)
4. **거리 판단 기능:** `distanceDetection2.py` 실행 (STOP/GO 판단)