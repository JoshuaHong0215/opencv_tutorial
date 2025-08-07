# based by step1_basic_landmark.py

import cv2
import dlib
import os
import time


# 눈 지정
LEFT_EYE = [36, 37, 38, 39, 40, 41]
RIGHT_EYE = [42, 43, 44, 45, 46, 47]


# FPS 측정
start_time = time.time()
frame_count = 0


# 얼굴 검출기와 랜드마크 검출기 생성 --- ①
detector = dlib.get_frontal_face_detector()

# MODEL_PATH를 지정한 이유는 나중에 프로젝트를 구조화할 때 config/settings.py에서 모델 경로를 관리하기 위함
MODEL_PATH = os.path.join('models', 'shape_predictor_68_face_landmarks.dat')
predictor = dlib.shape_predictor(MODEL_PATH)

cap = cv2.VideoCapture(0)
cap.set(cv2.cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        print('no frame.');break
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
   
    # 눈 영역 검출 
    for rect in faces:
        shape = predictor(gray, rect)

        for i in  LEFT_EYE:
            part = shape.part(i)
            cv2.circle(img, (part.x, part.y), 2, (255, 0, 0), -1)

        for i in  RIGHT_EYE:
            part = shape.part(i)
            cv2.circle(img, (part.x, part.y), 2, (255, 0, 0), -1)


    # FPS 측정 및 표시
    frame_count += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1.0:
         fps = frame_count / elapsed_time
         cv2.putText(img, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
         frame_count = 0
         start_time = time.time()


    cv2.imshow("face landmark", img)
    if cv2.waitKey(1)== 27:
        break
cap.release()