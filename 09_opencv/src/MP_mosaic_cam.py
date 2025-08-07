import cv2

rate = 15               # 모자이크에 사용할 축소 비율 (1/rate)
win_title = 'mosaic'    # 창 제목
face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
# img = cv2.imread('../img/like_lenna.png')    # 이미지 읽기


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 그레이스케일 변환 (얼굴 검출은 흑백에서 더 잘 됨)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 검출
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # 얼굴 영역마다 모자이크 처리
    for (x, y, w, h) in faces:
        roi = frame[y:y+h, x:x+w]
        roi = cv2.resize(roi, (w//rate, h//rate))
        roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_AREA)
        frame[y:y+h, x:x+w] = roi

    # 결과 출력
    cv2.imshow(win_title, frame)

    # 종료 키: q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()