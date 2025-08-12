# ball_only_detector.py
# 목적: YOLO로 '공(스포츠 볼)'만 실시간/동영상/단일 이미지에서 탐지
# 사용법 예시:
#   1) 웹캠:         python ball_only_detector.py
#   2) 비디오 파일:  python ball_only_detector.py --source ../videos/sample.mp4
#   3) 이미지 파일:  python ball_only_detector.py --source ../imgs/ball.jpg
# 옵션:
#   --model yolo11n.pt  --conf 0.35  --line 3

from ultralytics import YOLO
import cv2
import argparse
import time
import os

# ----------------------------
# 공 클래스 ID 자동 탐지 함수
# ----------------------------
def find_ball_id(model):
    # 모델의 클래스 이름 딕셔너리: {id: name}
    names = model.names if hasattr(model, "names") else None
    if not names:
        return None

    # 모두 소문자로 변환한 뒤, 정확 매칭 → 부분 매칭 순으로 탐색
    lower = {i: str(n).lower() for i, n in names.items()}
    # 1) 'sports ball' 정확 매칭
    for i, n in lower.items():
        if n == "sports ball":
            return i
    # 2) 'ball' 정확 매칭
    for i, n in lower.items():
        if n == "ball":
            return i
    # 3) 'ball' 부분 문자열 매칭
    for i, n in lower.items():
        if "ball" in n:
            return i
    return None

# ----------------------------
# 비디오/웹캠 처리 루프
# ----------------------------
def run_on_stream(model, source, ball_id, conf, line_width):
    cap = cv2.VideoCapture('../img/VGJ.mp4')
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open source: {source}")

    win = "Ball Detector (stream) - [ / ] to conf, q to quit"
    prev = time.time()
    while True:
        ret, frame = cap.read()
        if not ret or frame is None or frame.size == 0:
            break

        frame = cv2.resize(frame,None, fx=0.5, fy=0.5)

        # 추론
        results = model(frame, classes=[ball_id], conf=conf, verbose=False)
        annotated = results[0].plot(line_width=2)
        count = 0 if results[0].boxes is None else len(results[0].boxes)

        # FPS 계산
        now = time.time()
        fps = 1.0 / (now - prev) if now > prev else 0.0
        prev = now

        # 정보 오버레이
        cv2.putText(annotated, f"Ball count: {count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(annotated, f"conf={conf:.2f}  FPS={fps:.1f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)

        cv2.imshow(win, annotated)

        # 키 입력 처리: '[' 는 conf -, ']' 는 conf +, 'q' 종료
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('['):
            conf = max(0.05, round(conf - 0.05, 2))
        elif key == ord(']'):
            conf = min(0.95, round(conf + 0.05, 2))

    cap.release()
    cv2.destroyAllWindows()

# ----------------------------
# 메인
# ----------------------------
def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=str, default="0",
                   help="0=웹캠, 또는 비디오/이미지 경로")
    p.add_argument("--model", type=str, default="yolo11n.pt",
                   help="YOLO 가중치 경로")
    p.add_argument("--conf", type=float, default=0.35,
                   help="신뢰도 임계값")
    p.add_argument("--line", type=int, default=3,
                   help="바운딩 박스 선 두께")
    return p.parse_args()

def main():
    args = parse_args()

    # 모델 로드
    model = YOLO(args.model)

    # 공 클래스 ID 자동 탐색
    ball_id = find_ball_id(model)
    if ball_id is None:
        print("Error: cannot find 'sports ball' class in model names.")
        print("model.names =", model.names)
        return
    print(f"[INFO] BALL_ID = {ball_id}  (name='{model.names[ball_id]}')")

    # source 판별: 숫자면 카메라 인덱스, 아니면 경로
    src = args.source
    if src.isdigit():
        # 웹캠/비디오 장치
        run_on_stream(model, int(src), ball_id, args.conf, args.line)
    else:
        # 파일 경로: 이미지/비디오 자동 판별
        ext = os.path.splitext(src)[1].lower()
        if ext in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]:
            run_on_image(model, src, ball_id, args.conf, args.line)
        else:
            run_on_stream(model, src, ball_id, args.conf, args.line)

if __name__ == "__main__":
    main()
