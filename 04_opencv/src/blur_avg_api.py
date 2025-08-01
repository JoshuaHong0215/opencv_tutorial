# 블러 전용 함수로 블러링 적용

import cv2
import numpy as np

file_name = '../img/vessel.jpg'
img = cv2.imread(file_name)

# 1. blur() 함수로 블러링
blur1 = cv2.blur(img, (10, 10))

# 2. boxFilter() 함수로 블러링 적용
blur2 = cv2.boxFilter(img, -1, (10, 10))

# 3. 결과 출력
merged = np.hstack((img, blur1, blur2))
cv2.imshow('blur', merged)
cv2.waitKey(0)
cv2.destroyAllWindows()