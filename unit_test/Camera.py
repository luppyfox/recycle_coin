import cv2

cam = cv2.VideoCapture(0)
cv2.namedWindow("test")
img_counter = 0

while True:
    ret, frame = cam.read()                         #บันทึกภาพ
    if not ret:
        print("failed to grab frame")
        break
    cutframe = cv2.resize(frame, (320,320))         #ปรับขนาดของภาพให้เป็น 320x320 pixle
    cv2.imshow("test", cutframe)
    k = cv2.waitKey(1)
    if k%256 == 27:
        print("Escape hit, closing...")
        break
    elif k%256 == 32:                               #เมื่อกด space bar ให้บันทึกภาพ
        img_name = "D:/VScode Save/Capture/" + "{}.jpg".format(img_counter)
        cv2.imwrite(img_name, cutframe)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()
cv2.destroyAllWindows()