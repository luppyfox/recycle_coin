import cv2



def Cap_Img(img_counter):
    try:
        cam = cv2.VideoCapture(0)
#         cv2.namedWindow("test")
        ret, frame = cam.read()                         #บันทึกภาพ
        cutframe = cv2.resize(frame, (320,320))         #ปรับขนาดของภาพให้เป็น 320x320 pixle
#         cv2.imshow("test", cutframe)
        img_name = "/home/pi/Desktop/Smart-bin/img/" + "{}.jpg".format(img_counter)
        cv2.imwrite(img_name, cutframe)
        print("{} written!".format(img_name))
        return(True)
    
    except:
        print("failed to grab frame")
        return(False)
    
if __name__ == '__main__':
    img = Cap_Img(1)
    print(img)
#     cam.release()
#     cv2.destroyAllWindows()
    

