import cv2
import matplotlib.pyplot as plt
import pyzbar.pyzbar as pyzbar  


img = cv2.imread('../img/frame.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# plt.imshow(img)
# plt.imshow(gray, cmap = 'gray')  # cmap = colormap, 흑백, 또는 특정 색상으로 이미지를 표현하고 싶을떄 cmap = 'colorname' 을 지정한다
# plt.show()

# 디코딩
decoded = pyzbar.decode(gray)  # QR이나 바코드,얼굴,객채 등 이미지속 데이터를 읽어내는 작업이 디코딩이라 함
print(decoded)

for d in decoded:
    print(d.data.decode('utf-8'))
    print(d.type)

    barcode_data = d.data.decode('utf-8')
    print(d.type)
    barcode_type = d.type

    text = '%s (%s)' % (barcode_data, barcode_type)

    cv2.rectangle(img ,(d.rect[0], d.rect[1]), (d.rect[0] + d.rect[2], d.rect[1] + d.rect[3]), (0, 255, 0), 20)
    cv2.putText(img, text, (d.rect[0], d.rect[3]), cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 255, 255), 3, cv2.LINE_AA)

plt.imshow(img)
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()