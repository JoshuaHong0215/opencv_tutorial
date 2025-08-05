import numpy as np
import csv

# 1. 라벨 번호 → 색상 이름 매핑
label_names = {
    1: "Red",
    2: "Blue",
    3: "Green",
    4: "Yellow",
    5: "Black",
    6: "White",
    7: "Gray"
}

# 2. .npz 파일 불러오기
data = np.load("color_dataset.npz")
x_train = data["x_train"]        # (N, 3)
y_train = data["y_train"]        # (N,)

# 3. CSV 파일로 저장 (색상 이름 포함)
with open("color_dataset_named.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["R", "G", "B", "label", "label_name"])  # 헤더 작성

    for rgb, label in zip(x_train, y_train):
        r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
        label = int(label)
        label_name = label_names.get(label, "Unknown")
        writer.writerow([r, g, b, label, label_name])

print("color_dataset_named.csv 파일 저장 완료!")
