from ultralytics import YOLO
import cv2
import os

model = YOLO('yolo11n.pt')

video_path = os.path.normpath('../img/drive.avi')
cap = cv2.VideoCapture(video_path)

while True:
    # 4) 프레임 읽기
    ret, frame = cap.read()

    # 5) 읽기 실패/영상 끝 처리 + 빈 프레임 방어
    if not ret or frame is None or frame.size == 0:
        print('End of video or invalid frame.')
        break

    # 6) YOLO 추론 (유효한 프레임일 때만)
    results = model(frame, verbose=False)

    # 7) 시각화용 프레임 생성
    annotated = results[0].plot(line_width=2)  # numpy array(BGR)

    # 8) 화면 출력
    cv2.imshow('YOLO', annotated)

    # 9) 종료키(q) 처리
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 10) 자원 해제
cap.release()
cv2.destroyAllWindows()
