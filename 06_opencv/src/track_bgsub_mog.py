# BackgroundSubtractorMOG로 배경 제거 (track_bgsub_mog.py)

import numpy as np, cv2

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS) # 프레임 수 구하기
delay = int(1000/fps)
# 배경 제거 객체 생성 --- ①
# History : 과거 프레임의 갯수, 배경을 학습하는데 얼마나 많은 프레임을 기억할지  (50)
# History : 값이 클 수록 배경이 안정되지만 반응속도 느림, 값이 작을수록 민감하게 반응하지만 노이즈에 약함
# varThreshold : 전경/배경을 구분하는 민감도 (45)
# 기본값이 16정도인데 값이 높으면 불필요한 검출이 줄고 더 정제된 결과가 나올 수 있음
fgbg = cv2.createBackgroundSubtractorMOG2(50, 45, detectShadows=False)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # 배경 제거 마스크 계산 --- ②
    fgmask = fgbg.apply(frame)
    cv2.imshow('frame',frame)
    cv2.imshow('bgsub',fgmask)
    if cv2.waitKey(1) & 0xff == 27:
        break
cap.release()
cv2.destroyAllWindows()