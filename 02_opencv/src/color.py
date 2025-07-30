import cv2
import numpy as np

# 기본값
image = cv2.imread('../img/like_lenna.png')

# BGR
bgr = cv2.imread('../img/like_lenna.png', cv2.IMREAD_COLOR)

# alpha
bgra = cv2.imread('../img/like_lenna.png', cv2.IMREAD_UNCHANGED)

# shape
print("default", image.shape, "color", bgr.shape, "unchanged", bgra.shape)


cv2.imshow('Image Window', image)
cv2.imshow('bgr image', bgr)
cv2.imshow('alpha', bgra[:, :, 3])

cv2.waitKey(0)
cv2.destroyAllWindows()