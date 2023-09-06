
import threading , cv2  , serial , sqlite3 , torch , torch.hub , ultralytics , time
import numpy as np
from findSerial import *



#327.5 327.5 349.5 319.5
class mainX:
    #global

    def __init__(self) :

        #OBJECT
        self.numclass = 0

        #COM => Find => COM5
        serialInst = FindOutPort()
        try:
            for numport in serialInst:
                new_value = str(numport[0])
            
            print(new_value)
        
        
            if new_value != '':
                self.Ser = serial.Serial(new_value,9600,timeout=0)

            threading.Thread(target=self.main).start()
            

            

        except:
            print("ไม่เจอ port")

        threading.Thread(target=self.capstart()).start()

    #main1 
    def main(self):
        while True:
            
            #รับค่ามาจาก arduino
            pyau = self.Ser.readline().decode('utf-8').strip()
            
            if self.numclass != 0:
                print(self.numclass)
                self.Ser.write(bytes(str(self.numclass),'utf-8'))
                time.sleep(15)
                print("Sucess")
                self.numclass = 0
                self.Ser.write(bytes(str(self.numclass),'utf-8'))

#
            #if pyau == '1':
            #    self.numclass = 0
            #elif pyau == '2':
            #    self.numclass = 0
            #elif pyau == '3':
            #    self.numclass = 0
           # elif pyau == '4':
    
    #main2
    def capstart(self):
        model = torch.hub.load('ultralytics/yolov5', 'custom','C:\\Users\\wilas\\OneDrive\\เดสก์ท็อป\\Bigproject\\best.pt')
        print("START")
        cap = cv2.VideoCapture(0)
        
        while(True):
            ret, frame = cap.read()
            if not ret:
                break
            

            # Detect objects in the captured frame

            results = model(frame)

            # Process the detected objects (e.g., draw bounding boxes)
            detection = results.pandas().xyxy[0]

            # Display the processed frame

            for index, row in detection.iterrows():
                numberclass = row['class']
                nameclass = row['name']
                conf = row['confidence']
                conf = float(conf)
                conf = '{:.2f}'.format(conf)
                x1 = int(row['xmin'])
                y1 = int(row['ymin'])
                x2 = int(row['xmax'])
                y2 = int(row['ymax'])
                
                if float(conf) > 0.35:
                    if numberclass == 0:
                        self.numclass = 2
                    if numberclass == 1:
                        self.numclass = 3
                    if numberclass == 2:
                        self.numclass = 4

                cv2.rectangle(frame, (int(x1),int(y1)), (int(x2),int(y2)),(0,255,0), 2)
                cv2.putText(frame,(f'{str(conf)} {str(nameclass)} {str(numberclass)}'), (int(x1), int(y1)+20), 1, 1, (179, 55, 0),2)

            cv2.imshow('Detection', frame)

            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        

if __name__ == '__main__':
    mainX()


        