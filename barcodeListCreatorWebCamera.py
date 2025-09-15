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