import cv2
import matplotlib.pyplot as plt
import pyzbar.pyzbar as pyzbar  


img = cv2.imread('../img/frame.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# plt.imshow(img)
plt.imshow(gray, cmap = 'gray')  # cmap = colormap, 흑백, 또는 특정 색상으로 이미지를 표현하고 싶을떄 cmap = 'colorname' 을 지정한다
plt.show()

# 디코딩
decoded = pyzbar.decode(gray)  # QR이나 바코드,얼굴,객채 등 이미지속 데이터를 읽어내는 작업이 디코딩이라 함
print(decoded)



cv2.waitKey(0)
cv2.destroyAllWindows()

