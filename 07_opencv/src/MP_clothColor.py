
import cv2
import numpy as np
from collections import defaultdict

label_names = {
    1: "Red", 2: "Blue", 3: "Green", 4: "Yellow",
    5: "Black", 6: "White", 7: "Gray"
}

label_colors = {
    1: (0, 0, 255), 2: (255, 0, 0), 3: (0, 255, 0),
    4: (0, 255, 255), 5: (0, 0, 0), 6: (255, 255, 255), 7: (128, 128, 128)
}

def load_npz_data(path="color_dataset.npz"):
    try:
        with np.load(path) as data:
            x_train = data["x_train"].astype(np.float32) / 255.0
            y_train = data["y_train"].astype(np.int32)
        print(f"✅ 데이터 로드 완료: {path}")
        return list(x_train * 255), list(y_train)
    except:
        print("❌ 기존 데이터 없음. 새로 수집 시작")
        return [], []

def save_npz(x_train, y_train, path="color_dataset.npz"):
    x_arr = np.array(x_train, dtype=np.float32)
    y_arr = np.array(y_train, dtype=np.int32)
    np.savez(path, x_train=x_arr, y_train=y_arr)
    print(f"💾 저장 완료: {path} (총 {len(x_train)}개)")

def train_knn(x, y, k=3):
    model = cv2.ml.KNearest_create()
    x_arr = np.array(x, dtype=np.float32) / 255.0
    y_arr = np.array(y, dtype=np.int32)
    model.train(x_arr, cv2.ml.ROW_SAMPLE, y_arr)
    return model

def main():
    mode = "predict"  # 'learn' or 'predict'
    x_train, y_train = load_npz_data()
    label_counter = defaultdict(int)
    for y in y_train:
        label_counter[y] += 1

    model = train_knn(x_train, y_train) if y_train else None

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    roi_size = 100

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]
        cx, cy = w // 2, h // 2
        x1, y1 = cx - roi_size // 2, cy - roi_size // 2
        x2, y2 = cx + roi_size // 2, cy + roi_size // 2
        roi = frame[y1:y2, x1:x2]
        avg_bgr = cv2.mean(roi)[:3]
        avg_rgb = [avg_bgr[2], avg_bgr[1], avg_bgr[0]]

        if mode == "predict" and model:
            norm_rgb = np.array([avg_rgb], dtype=np.float32) / 255.0
            ret, result, _, _ = model.findNearest(norm_rgb, k=3)
            label = int(result[0][0])
            color_name = label_names.get(label, "Unknown")
            color = label_colors.get(label, (200, 200, 200))
            cv2.putText(frame, f"Predicted: {color_name}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        else:
            cv2.putText(frame, "학습 모드 (1~7키로 저장)", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # 공통 UI
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(frame, f"Mode: {mode.upper()}", (10, 460),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (150, 150, 150), 1)
        for i in range(1, 8):
            name = label_names[i]
            count = label_counter[i]
            cv2.putText(frame, f"{i}:{name}({count})", (10, 60 + i * 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow("Color Trainer & Predictor", frame)
        key = cv2.waitKey(1)

        if key == 27:  # ESC
            save_npz(x_train, y_train)
            break
        elif key == ord('l'):  # 학습 모드 전환
            mode = "learn"
        elif key == ord('p'):  # 예측 모드 전환
            if y_train:
                model = train_knn(x_train, y_train)
            mode = "predict"
        elif mode == "learn" and key in [49,50,51,52,53,54,55]:  # '1'~'7'
            label = key - 48
            x_train.append(avg_rgb)
            y_train.append(label)
            label_counter[label] += 1
            print(f"🟢 {label_names[label]} 샘플 추가 → 총 {label_counter[label]}개")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
