# 목적

# 3채널 컬러 영상을 하나의 색상을 위해서 24비트(8x3) 16777216가지의 색상 표현이 가능하다
# 모든 색상을 다 사용하지 않고 비슷한 색상끼리 그룹으로 묶어 같은 색상으로 처리하여 "처리용량 간소화 가능"

import numpy as np
import cv2
import matplotlib.pyplot as plt

# 군집화 갯수
K = 4

img = cv2.imread('../img/load_line.jpg')
img = cv2.resize(img, (400,400))

# np.float32는 데이터 평균을 구할때 소숫점 이하값을 가질 수 있음으로 변환
data = img.reshape((-1, 3)).astype(np.float32)

# 반복 중지 조건
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

# 평균 클리스터링 적용
# KMEANS_RANDOM_CENTERS: 중심점 랜덤
ret, label, center = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# 중심값을 정수형으로 전환
center = np.uint8(center)
print(center)

# 각 레이블에 해당하는 중심값으로 픽셀 값 선택
res = center[label.flatten()]

# 원본 영상의 형태로 변환
res = res.reshape((img.shape))

# 클러스터별 픽셀 수 세기
counts = np.bincount(label.flatten())
ratios = counts / counts.sum()

# BGR -> RGB 변환 (matplotlib은 RGB를 사용한다)
center_rgb = center[:, ::-1]  # BGR -> RGB

# BGR + 비율출력
print("== 대표 색상(BGR) 및 비율 ==")
for i, (bgr, ratio) in enumerate(zip(center, ratios)):
    print(f'클러스터 {i}: 색상 BGR = {bgr}, 비율 = {ratio*100:.2f}%')

# 색상 팔레트
plt.figure(figsize=(8, 2))
for i in range(K):
    plt.bar(i, 1, color=center_rgb[i]/255.0)
plt.xticks(range(K), [f"{int(ratios[i]*100)}%" for i in range(K)])
plt.title("Color Palette (Proportions)")
plt.axis('off')
plt.show()

# 비율 막대 그래프
plt.figure(figsize=(6, 4))
bars = plt.bar(range(K), ratios * 100, color=center_rgb/255.0)
plt.xticks(range(K), [f"Cluster {i}" for i in range(K)])
plt.ylabel("Ratio (%)")
plt.title("Color Proportion by Cluster")
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.show()


# 결과 출력
merged = np.hstack((img, res))
cv2.imshow('Kmeans color', merged)
cv2.waitKey(0)
cv2.destroyWindow()

