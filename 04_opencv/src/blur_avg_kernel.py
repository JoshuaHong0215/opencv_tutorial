import cv2
import numpy as np

img = cv2.imread('../img/vessel.jpg')


# 1. 5x5 평균 필터 커널 생성

'''
kernel = np.array([[0.04, 0.04, 0.04, 0.04, 0.04],
                   [0.04, 0.04, 0.04, 0.04, 0.04],
                   [0.04, 0.04, 0.04, .0.4, 0.04],
                   [0.04, 0.04, 0.04, .0.4, 0.04]])
'''
# 2. 5x5 평균 필터 커널 생성
# - (5,5)는 필터의 크기로서 값이 커지면 선명도는 더 떨어짐
kernel = np.ones((5,5))/5**2

 
# 3. 필터 적용
blured = cv2.filter2D(img, -1, kernel)

# 4. 결과 출력
cv2.imshow('origin', img)
cv2.imshow('avrg blur', blured)
cv2.waitKey(0)
cv2.destroyAllWindows()