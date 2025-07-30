import cv2
import numpy as np
import matplotlib.pylab as plt

image1 = cv2.imread('../img/source_01.jpg')
image2 = cv2.imread('../img/source_02.png')

image1 = cv2.resize(image1, (500,500))
image2 = cv2.resize(image2, (500,500))

blended = cv2.addWeighted(image1, 0.5, image2, 0.5, 0)

cv2.putText(blended, 'TARGET', (220, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)


cv2.imshow('test', blended)
cv2.waitKey(0)
cv2.destroyAllWindows()

# dlrjtdmads