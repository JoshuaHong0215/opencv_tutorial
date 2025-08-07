import cv2
import numpy as np

# ===== 1. 모델 불러오기 =====
dictionary = np.load('safeWarning_dict.npy')
svm = cv2.ml.SVM_load('safeWarning_svm.xml')

# ===== 2. BOW 관련 객체 생성 =====
detector = cv2.SIFT_create()
matcher = cv2.BFMatcher(cv2.NORM_L2)
bow_extractor = cv2.BOWImgDescriptorExtractor(detector, matcher)
bow_extractor.setVocabulary(dictionary)

# ===== 3. 클래스 정의 =====
categories = ['SAFE', 'WARNING_PERSON', 'WARNING_CAR']
colors = [(0,255,0), (0,0,255), (0,165,255)]  # GREEN / RED / ORANGE
warnings = ['SAFE', 'WARNING_PERSON!', 'WARNING_CAR']

# ===== 4. 영상 입력 설정 =====
cap = cv2.VideoCapture('../img/drive.avi')  # 0은 웹캠 / 경로 지정시 동영상

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # ===== 5. 그레이 변환 및 특징 추출 =====
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    keypoints = detector.detect(gray)

    if not keypoints:
        cv2.imshow('Detect Warning', frame)
        if cv2.waitKey(1) == 27:
            break
        continue

    feature = bow_extractor.compute(gray, keypoints)
    if feature is None:
        cv2.imshow('Detect Warning', frame)
        if cv2.waitKey(1) == 27:
            break
        continue

    # ===== 6. SVM 분류 =====
    _, result = svm.predict(feature)
    pred = int(result[0][0])  # 0:SAFE, 1:PERSON, 2:CAR

    # ===== 7. 경고 시각화 =====
    color = colors[pred]
    label = warnings[pred]

    # 예시 박스 위치 (전체 프레임 상단에 표시)
    h, w, _ = frame.shape
    cv2.rectangle(frame, (10, 10), (w-10, 60), color, -1)
    cv2.putText(frame, label, (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

    cv2.imshow('Detect Warning', frame)
    if cv2.waitKey(1) == 27:  # ESC 종료
        break

cap.release()
cv2.destroyAllWindows()
