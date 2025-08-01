import cv2
import pyzbar.pyzbar as pyzbar
import webbrowser

# 웹캠 열기
cap = cv2.VideoCapture(0)

# 해상도 향상 (선택 사항)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# 이미 열어본 URL 저장 (중복 방지)
opened_urls = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # 흑백 변환 후 디코딩
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    decoded = pyzbar.decode(gray)

    for d in decoded:
        data = d.data.decode('utf-8')
        barcode_type = d.type
        x, y, w, h = d.rect

        # QR 코드 영역 시각화
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, data, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

        # URL이면 브라우저로 열기 (한 번만)
        if data.startswith("http") and data not in opened_urls:
            print(f"열기: {data}")
            webbrowser.open(data)
            opened_urls.add(data)

    # 프레임 출력
    cv2.imshow("QR Scanner", frame)

    # q 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 종료
cap.release()
cv2.destroyAllWindows()
