import cv2
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

win_name = "scanning"
img = cv2.imread('../img/car_05.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

rows, cols = img.shape[:2]
draw = img.copy()
pts_cnt = 0
pts = np.zeros((4, 2), dtype=np.float32)

def onMouse(event, x, y, flags, param):  # 마우스 이벤트 콜백 함수 구현 --- 1
    global pts_cnt                     # 마우스로 찍은 좌표의 갯수 저장
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(draw, (x, y), 10, (0, 255, 0), -1)  # 좌표에 초록색 동그라미 표시
        cv2.imshow(win_name, draw)

        pts[pts_cnt] = [x, y]          # 마우스 좌표 저장
        pts_cnt += 1

        if pts_cnt == 4:  # 좌표가 4개 수집됨
            sm = pts.sum(axis=1)                 # 4쌍의 좌표 각각 x+y 계산
            diff = np.diff(pts, axis=1)          # 4쌍의 좌표 각각 x-y 계산

            topLeft = pts[np.argmin(sm)]         # x+y가 가장 작은 값이 좌상단 좌표
            bottomRight = pts[np.argmax(sm)]     # x+y가 가장 큰 값이 우하단 좌표
            topRight = pts[np.argmin(diff)]      # x-y가 가장 작은 것이 우상단 좌표
            bottomLeft = pts[np.argmax(diff)]    # x-y가 가장 큰 값이 좌하단 좌표

            pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

            w1 = abs(bottomRight[0] - bottomLeft[0])
            w2 = abs(topRight[0] - topLeft[0])
            h1 = abs(topRight[1] - bottomRight[1])
            h2 = abs(topLeft[1] - bottomLeft[1])
            width = int(max(w1, w2))
            height = int(max(h1, h2))

            pts2 = np.float32([[0, 0], [width-1, 0],
                               [width-1, height-1], [0, height-1]])

            mtrx = cv2.getPerspectiveTransform(pts1, pts2)
            result = cv2.warpPerspective(img, mtrx, (width, height))

            # 그레이스케일 변환
            gray_result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

            # CLAHE 적용
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray_result)

            # 적응형 임계 처리
            thresh = cv2.adaptiveThreshold(
                enhanced,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2
            )

            # matplotlib으로 이미지 한 번에 출력
            fig, axes = plt.subplots(1, 5, figsize=(18, 5))
            titles = ['Original', 'Warped', 'Grayscale', 'CLAHE', 'Thresholded']
            images = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB),
                      cv2.cvtColor(result, cv2.COLOR_BGR2RGB),
                      gray_result,
                      enhanced,
                      thresh]

            for i in range(5):
                axes[i].imshow(images[i], cmap='gray' if i >= 2 else None)
                axes[i].set_title(titles[i], fontsize=12)
                axes[i].axis('off')

            plt.tight_layout()
            plt.show()

            # # 저장 경로 처리
            # save_dir = "../extracted_plates"              # 절대경로 지정 함
            # if not os.path.exists(save_dir):
            #     os.makedirs(save_dir)

            # # 저장 설정 
            # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            # filename =  f"../extracted_plates/plate_{timestamp}.png"  # 여기서도 save_dir과 똑같은 경로로 설정할것 
            #                                                           # .png, .jpg등 확장자명도 변경
            # success = cv2.imwrite(filename, result)

            # if success:
            #     print(f'번호판 저장완료: {filename}')
            #     cv2.imshow('Extracted Plate', result)
            # else:
            #     print("저장실패")


cv2.imshow(win_name, img)
cv2.setMouseCallback(win_name, onMouse)
cv2.waitKey(0)
cv2.destroyAllWindows()