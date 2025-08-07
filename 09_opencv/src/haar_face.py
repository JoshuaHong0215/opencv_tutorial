import numpy as np
import cv2

# 1. 얼굴 검출을 위한 케스케이드 분류기 생성 
face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_default.xml')
# 2. 눈 검출을 위한 케스케이드 분류기 생성 
eye_cascade = cv2.CascadeClassifier('../data/haarcascade_eye.xml')
# 3. 검출할 이미지 읽고 그레이 스케일로 변환 
img = cv2.imread('../img/like_lenna.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 4. 얼굴 검출 
faces = face_cascade.detectMultiScale(gray)
# 5. 검출된 얼굴 순회 
for (x,y,w,h) in faces:
    # 6. 검출된 얼굴에 사각형 표시 
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    # 7. 얼굴 영역을 ROI로 설정 
    roi = gray[y:y+h, x:x+w]
    # 8. ROI에서 눈 검출 
    eyes = eye_cascade.detectMultiScale(roi)
    # 9. 검출된 눈에 사각형 표 
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(img[y:y+h, x:x+w],(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
# 결과 출력 
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()