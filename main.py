import cv2
import os
import pytesseract as tess
import time
from PIL import Image
from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt

tess.pytesseract.tesseract_cmd = 'D:/Tesseract-OCR/tesseract.exe'
count = 0
cam = cv2.VideoCapture(0)
capDuration = 5
startTime = time.time()
frames = []

while True:
    success, frame = cam.read()
    frames.append(frame)
    cv2.imwrite("./frames/frame%d.jpg" % count, frame)
    print('Screenshot alındı!')
    count = count + 1
    time.sleep(1)
    if int(time.time() - startTime) == capDuration:
        break

cam.release()
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

listExtacts = []
for fr in frames:
    new_im = Image.fromarray(fr)
    test = tess.image_to_string(new_im)
    listExtacts.append(test)
    print(test)


#işlemler bitince sil
while count != 0:
    count = count - 1
    os.unlink("./frames/frame%d.jpg" % count)
    print(count)

print(time.time() - startTime)