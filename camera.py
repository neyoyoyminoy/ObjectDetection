# import cv2
# from pyzbar.pyzbar import decode
# import numpy as np
# import time

# cap = cv2.VideoCapture(0)
# cap.set(3, 640) #3 - Width
# cap.set(4, 480) #4 - Height
# used_codes = []

# camera = True

# while camera == True:
#         success, frame = cap.read()

#         for code in decode(frame):
#                  if code.data.decode('utf-8') not in used_codes:
#                         print('Approved. This code exists!')
#                         print(code.data.decode('utf-8'))
#                         used_codes.append(code.data.decode('utf-8'))
#                         #time.sleep(5)

#                     elif code.data.decode('utf-8') in used_codes:
#                         print('Sorry, this code has expired')
#                        # print(code.data.decode('utf-8'))
#                        #time.sleep(5)
#                     else:
#                        pass
                
#         cv2.imshow('Testing-code-scan', frame)
#         cv2.waitKey(3)


#/                          /                           /                                   /                               /#


import cv2
import numpy as np
from pyzbar.pyzbar import decode

def enhance(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8)).apply(gray)
    blur = cv2.GaussianBlur(clahe, (0,0), 1.0)
    sharp = cv2.addWeighted(clahe, 1.5, blur, -0.5, 0) 


cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

camera = True

while camera == True:

    success, frame = cap.read()

    for code in decode(frame):
        myData = code.data.decode('utf-8')
        print(myData)
        pts = np.array([code.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame,[pts],True,(255,0,255),5)
        pts2 = code.rect
        cv2.putText(frame,myData,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX, 0.9,(255,0,255),2)

    cv2.imshow('Result',frame)
    cv2.waitKey(1)



    #/                          /                           /                                   /                               /#
# import cv2
# import numpy as np
# from pyzbar.pyzbar import decode

# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)   # DSHOW often reduces lag on Windows
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)    # bump up resolution for multi-code
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# print("Press 'q' to quit")
# while True:
#     ok, frame = cap.read()
#     if not ok:
#         continue

#     # Convert to grayscale for more stable decode
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     codes = decode(gray)
#     for code in codes:
#         data = code.data.decode('utf-8') if code.data else ''
#         if not data:
#             continue

#         # 👉 Print each decoded barcode/QR to the terminal
#         print("Scanned:", data)

#         # Draw polygon if available
#         if code.polygon:
#             pts = np.array([(p.x, p.y) for p in code.polygon], dtype=np.int32).reshape(-1,1,2)
#             cv2.polylines(frame, [pts], True, (255, 0, 255), 2)

#         # Draw label near bounding rect
#         x, y, w, h = code.rect
#         cv2.putText(frame, data, (x, max(0, y - 10)),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2)

#     # Display the live feed with drawings
#     cv2.imshow("Multi-code Scanner", frame)

#     # Exit with 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

