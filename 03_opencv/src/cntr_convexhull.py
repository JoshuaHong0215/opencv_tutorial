import cv2
import numpy as np

img = cv2.imread('../img/hand.jpg')
img2 = img.copy()

# 1. 그레이스케일 및 바이너리 스케일 변환
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# 2. 컨투어 찾기와 그리기
contours, hierarchy = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cntr = contours[0]
cv2.drawContours(img, [cntr], -1, (0, 255, 0), 1)

# 3. 블록 선체 찾기(좌표기준)와 그리기
hull = cv2.convexHull(cntr)
cv2.drawContours(img2, [hull], -1, (0, 255, 0), 1)

# 4. 블록 선체 만족여부 확인
print(cv2.isContourConvex(cntr), cv2.isContourConvex(hull))

# 5. 블록 선체 찾기(인덱스 기준)
hull2 = cv2.convexHull(cntr, returnPoints=False)

# 6. 블록 선체 결함찾기
defects = cv2.convexityDefects(cntr, hull2)

# 블록 선체 결함 순회
for i in range(defects.shape[0]):
    # 7. 시작, 종료, 가장 먼 지점, 거리
    startP, endP, farthestP, distance = defects[i, 0]

    # 8. 가장 먼 지점의 좌표 구하기
    farthest = tuple(cntr[farthestP][0])

    # 9. 거리를 부동 소숫점으로 변환
    dist = distance/256.0

    # 10. 거리가 1보다 큰 경우
    if dist > 1 :
        # 빨간색 점 표시
        cv2.circle(img2, farthest, 3, (0, 0, 255), -1)

# 11. 결과 이미지 표시
cv2.imshow('contour', img)
cv2.imshow('convex hull', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()