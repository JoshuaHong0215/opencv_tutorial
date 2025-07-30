import cv2
import numpy as np
import matplotlib.pyplot as plt

# Matplotlib 실시간 모드 켜기
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(np.zeros(256))
ax.set_xlim([0, 256])
ax.set_ylim([0, 10000])
ax.set_title('Grayscale Histogram')
ax.set_xlabel('Pixel Intensity')
ax.set_ylabel('Frequency')

# 웹캠 연결
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # [1] 중앙 세로 ROI 설정
    h, w = frame.shape[:2]
    roi_x1, roi_x2 = w // 2 - 100, w // 2 + 100
    roi = frame[50:, roi_x1:roi_x2]  # 세로 전체, 가로 100px

    # [2] ROI를 Grayscale로 변환 + Threshold 이진화
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    # [3] 외곽선 검출
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # [4] 원본 프레임 복사 후 외곽선과 중심점 표시
    contour_img = frame.copy()

    for cnt in contours:
        # 작은 노이즈 contour 무시
        if cv2.contourArea(cnt) < 1000:
            continue

        # 중심점 계산
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00']) + roi_x1  # ROI 좌표를 전체 영상 기준으로 보정
            cy = int(M['m01'] / M['m00'])
            cv2.circle(contour_img, (cx, cy), 4, (0, 0, 255), -1)  # 빨간 점

        # 외곽선도 전체 영상 좌표로 보정해서 그림
        cnt_offset = cnt + np.array([[[roi_x1, 0]]])
        cv2.drawContours(contour_img, [cnt_offset], -1, (0, 255, 0), 2)  # 초록 외곽선

    # [5] 히스토그램 계산
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).flatten()

    # [6] 결과 표시
    cv2.imshow('Gray ROI', gray)
    cv2.imshow('Contours (ROI)', contour_img)

    line.set_ydata(hist)
    fig.canvas.draw()
    fig.canvas.flush_events()

    # [7] 종료 조건
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

# [8] 종료 시 정리
cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.close()
