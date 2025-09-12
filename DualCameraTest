import cv2
import numpy as np
from pyzbar.pyzbar import decode

def enhance(img):
    """Apply contrast and sharpening to improve barcode detection."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
    blur = cv2.GaussianBlur(clahe, (0, 0), 1.0)
    return cv2.addWeighted(clahe, 1.5, blur, -0.5, 0)

# Open both cameras
caps = [cv2.VideoCapture(0), cv2.VideoCapture(1)]

# Configure resolution for both
for cap in caps:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Press 'q' in any window to quit.")

while True:
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if not ret:
            continue

        # Enhance frame for better barcode recognition
        processed = enhance(frame)
        barcodes = decode(processed)

        for barcode in barcodes:
            data = barcode.data.decode('utf-8')
            pts = np.array([barcode.polygon], np.int32).reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (255, 0, 255), 3)
            x, y, w, h = barcode.rect
            cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 0, 255), 2)
            print(f"Camera {i}: {data}")

        cv2.imshow(f"Camera {i}", frame)

    # Allow exit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
for cap in caps:
    cap.release()
cv2.destroyAllWindows()
