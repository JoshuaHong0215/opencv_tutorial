# 목적

# 3채널 컬러 영상을 하나의 색상을 위해서 24비트(8x3) 16777216가지의 색상 표현이 가능하다
# 모든 색상을 다 사용하지 않고 비슷한 색상끼리 그룹으로 묶어 같은 색상으로 처리하여 "처리용량 간소화 가능"

import numpy as np
import cv2
import matplotlib.pyplot as plt

# 군집화 갯수
K = 6

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



# matplotlib으로 모든 결과를 시각화함
# fig : 전체 도화지(figure)
# axs : subplot(세부그래프)의 배열
# axs[0] : 첫 번째 그래프
# axs[1] : 두 번째 그래프(색상 팔레트)
# axs[0] : 세 번째 그래프(비율 바 차트)

# plt.subplot() : 단순하고 빠르지만 동시에 여러 그래프를 다루기 어려움
# fig, axs = plt.subplot() : 그래프를 객체화해서 각각 개별 제어 가능


# 3 : 행(row) 갯수 -> 세로로 3개의 그래프 영역 생성
# 1 : 열(column) 갯수 -> 한 줄에 하나씩만 표시하겠다라는 뜻
# (8, 10) : 전체 그림의 크기로서 가로 8인치, 세로 10인치 영역을 주겠다는 뜻
fig, axs = plt.subplots(3, 1, figsize=(8, 10))

# 1. 원본 vs KMeans 이미지 출력
merged = cv2.cvtColor(np.hstack((img, res)), cv2.COLOR_BGR2RGB)
axs[0].imshow(merged)
axs[0].axis('off')
axs[0].set_title("Original Image vs KMeans Result")

# 2. 색상 팔레트
axs[1].bar(range(K), [1]*K, color=center_rgb/255.0, edgecolor='black')
axs[1].set_xticks(range(K))
axs[1].set_xticklabels([f"{int(r*100)}%" for r in ratios])

# 퍼센트 텍스트를 각 색상 박스 중앙에 표시
for i, ratio in enumerate(ratios):
    axs[1].text(i, 0.5, f"{ratio*100:.1f}%", ha='center', va='center', fontsize=12, color='black', weight='bold')

axs[1].set_title("Color Palette (Proportions)")
axs[1].axis('off')

# 3. 색상 비율 차트
bars = axs[2].bar(range(K), ratios * 100, color=center_rgb/255.0)
axs[2].set_xticks(range(K))
axs[2].set_xticklabels([f"Cluster {i}" for i in range(K)])
axs[2].set_ylabel("Ratio (%)")
axs[2].set_title("Color Proportion by Cluster")
axs[2].grid(axis='y', linestyle='--', alpha=0.5)

# 전체 표시
plt.tight_layout()
plt.show()