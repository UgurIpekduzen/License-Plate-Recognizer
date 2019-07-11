import cv2
import os
import time

vidcap = cv2.VideoCapture(0)
filePath = "E:/Repos/License Plate Recognizer/frames/frame.jpg"
capDuration = 5
startTime = time.time()
while True:
    success, image = vidcap.read()
    if(int(time.time() - startTime) == capDuration):
        cv2.imwrite(filePath, image)
        print('Screenshot alındı!')
        break

vidcap.release()
cv2.destroyAllWindows()
#
#   Tüm kodlar buraya...
#

#işlemler bitince sil
os.unlink(filePath)