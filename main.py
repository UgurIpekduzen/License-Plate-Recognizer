import cv2
import os
import time
from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt

count = 0
vidcap = cv2.VideoCapture(0)
capDuration = 5
startTime = time.time()
while int(time.time() - startTime) != capDuration:
    success, frame = vidcap.read()
    cv2.imwrite("./frames/frame%d.jpg" % count, frame)
    print('Screenshot alındı!')
    count = count + 1
    time.sleep(1)

vidcap.release()
cv2.destroyAllWindows()
#
#   Tüm kodlar buraya...
#

image = imread("./frames/frame%d.jpg" % (count - 1), as_gray="True")

imageGray = image * 255
fig, (ax1, ax2) = plt.subplots(1,2)
ax1.imshow(imageGray, cmap="gray")
thresholdValue = threshold_otsu(imageGray)
binaryImage = imageGray > thresholdValue
ax2.imshow(binaryImage, cmap="gray")
plt.show()

#işlemler bitince sil
while count != 0:
    count = count - 1
    os.unlink("./frames/frame%d.jpg" % count)
    print(count)
