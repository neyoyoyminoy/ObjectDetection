import cv2
import numpy as np
from pyzbar.pyzbar import decode

def build_gst_pipeline(device, width=640, height=480, framerate=30):
    """
    Build a GStreamer pipeline string for a V4L2 camera device.
    """
    return (
        f"v4l2src device={device} ! "
        f"video/x-raw, width={width}, height={height}, framerate={framerate}/1 ! "
        f"videoconvert ! appsink"
    )

def enhance(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)
    blur = cv2.GaussianBlur(clahe, (0, 0), 1.0)
    return cv2.addWeighted(clahe, 1.5, blur, -0.5, 0)

# List of camera devices (adjust if needed)
devices = ["/dev/video0", "/dev/video1"]
caps = []

# Try to open each camera with GStreamer
for dev in devices:
    cap = cv2.VideoCapture(build_gst_pipeline(dev), cv2.CAP_GSTREAMER)
    if cap.isOpened():
        print(f"[INFO] Opened {dev}")
        caps.append(cap)
    else:
        print(f"[WARN] Could not open {dev}")

if not caps:
    print("[ERROR] No cameras available.")
    exit(1)

print("Press 'q' to quit.")

while True:
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if not ret:
            print(f"[WARN] Camera {i} failed to return a frame.")
            continue

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

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

for cap in caps:
    cap.release()
cv2.destroyAllWindows()
