import cv2
import numpy as np
import os 
import emailer
import time
import gpio


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Rahul: id=1,  etc
names = ['None', 'Rahul', 'Tejasvi'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img =cam.read()
    img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    if len(faces) == 0:
        gpio.led_off()

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            cv2.imwrite("capture.jpg", img)
            gpio.led_on()
            id = names[id]
            emailer.sendMail(["mmspiproject@gmail.com"], "Visitor Alert",
                             str(id) + " is at your door",
                             ["capture.jpg"])
            confidence = "  {0}%".format(round(100 - confidence))
            time.sleep(8)
        else:
            id = "unknown"
            gpio.led_off()
            cv2.imwrite("capture.jpg", img)
            emailer.sendMail(["mmspiproject@gmail.com"],
                             "Visitor alert",
                             "There is someone unknown at the door",
                             ["capture.jpg"])
            confidence = "  {0}%".format(round(100 - confidence))
            time.sleep(8)
            
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
gpio.exit_led()
cv2.destroyAllWindows()