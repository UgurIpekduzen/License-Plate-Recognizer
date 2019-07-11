import cv2
import os
import time
from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt

vidcap = cv2.VideoCapture(0)
filePath = "./frames/frame.jpg"
capDuration = 5
startTime = time.time()
while True:
    success, frame = vidcap.read()

    if(int(time.time() - startTime) == capDuration):
        cv2.imwrite(filePath, frame)
        print('Screenshot alındı!')
        break

vidcap.release()
cv2.destroyAllWindows()
#
#   Tüm kodlar buraya...
#

image = imread(filePath, as_gray="True")

imageGray = image * 255
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.imshow(imageGray, cmap="gray")
thresholdValue = threshold_otsu(imageGray)
binaryImage = imageGray > thresholdValue
ax2.imshow(binaryImage, cmap="gray")
plt.show()

#işlemler bitince sil
os.unlink(filePath)