import cv2, re, time, sys
import numpy as np
import urllib.request as urlreq
import os, ssl
from xlwt import Workbook

import EditImage
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/detection_functions")
import DetectPlates
import DetectChars

url = "https://10.0.10.52:8080/shot.jpg"

PYTHONHTTPVERIFY = 0
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
  ssl._create_default_https_context = ssl._create_unverified_context

###################################################################################################
def readLPImagePaths(strFolderPath):
    listLP = []
    for file in os.listdir(strFolderPath):
            # Mevcut dizin ve alt dizinlerdeki tüm bilgileri toplar
            strFilePath = os.path.join(strFolderPath, file)
            listLP.append(strFilePath)
            print(strFilePath)
    return listLP
#end function

########################################################ıu###########################################
def fromWebCam():

    cam = cv2.VideoCapture(0)
    strCorrectLPText = ""
    processTimeInSecond = 0
    while processTimeInSecond is not 10:
        ret, imgOriginalScene = cam.read()

        for zoomRate in range(100,400, 50):

            imgOriginalScene = EditImage.adjust(imgOriginalScene, zoomRate)
            listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

            listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

            if len(listOfPossiblePlates) == 0:  # if no plates were found
                print("\nno license plates were detected\n")  # inform user no plates were found
                processTimeInSecond += 1
                time.sleep(1)
                break
            else:  # else
                # if we get in here list of possible plates has at least one plate

                # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
                listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
                licPlate = listOfPossiblePlates[0]

                if len(licPlate.strChars) == 0:  # if no chars were found in the plate
                    print("\nno characters were detected\n\n")  # show message
                    processTimeInSecond += 1
                    time.sleep(1)
                    break
                # end if
                else:
                    matchObj = re.search("^(0[1-9]|[1-7][0-9]|8[01])(([A-Z])(\d{4,5})|([A-Z]{2})(\d{3,4})|([A-Z]{3})(\d{2}))$", licPlate.strChars)
                    if (matchObj):
                        print("\nlicense plate read from image = " + licPlate.strChars + "\n\n")  # write license plate text to std out
                        strCorrectLPText = licPlate.strChars
                        processTimeInSecond += 1
                        time.sleep(1)
                        break
                    else:
                        continue
                   # end if else
                # end if else
            # end if else
        # end for
        print("işlem süresi: " + str(processTimeInSecond))
        if (len(strCorrectLPText) > 0):
            break
        #end if
    #end while
    cam.release()
    cv2.destroyAllWindows()
    return strCorrectLPText
#end function

# HATALI ##########################################################################################
def fromIPCAM():
    while True:
        imgResp = urlreq.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        imgOriginalScene = cv2.imdecode(imgNp, -1)
        for zoomRate in range(100, 400, 50):

            imgOriginalScene = EditImage.adjust(imgOriginalScene, zoomRate)
            listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

            listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

            if len(listOfPossiblePlates) == 0:  # if no plates were found
                print("\nno license plates were detected\n")  # inform user no plates were found
                break
            else:  # else
                # if we get in here list of possible plates has at least one plate

                # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
                listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
                licPlate = listOfPossiblePlates[0]

                if len(licPlate.strChars) == 0:  # if no chars were found in the plate
                    print("\nno characters were detected\n\n")  # show message
                    break
                # end if
                else:
                    matchObj = re.search(
                        "^(0[1-9]|[1-7][0-9]|8[01])(([A-Z])(\d{4,5})|([A-Z]{2})(\d{3,4})|([A-Z]{3})(\d{2}))$",
                        licPlate.strChars)
                    # print("is Match = " + str(matchObj))
                    if (matchObj):
                        print(
                            "\nlicense plate read from image = " + licPlate.strChars + "\n\n")  # write license plate text to std out
                        time.sleep(1)
                        break
                    else:
                        continue
                    # end if else
                # end if else
            # end if else
        # end for
        cv2.waitKey(0)  # hold windows open until user presses a key
    #end while
    return
#end function

#######################################################################################################
def fromLPDatasetAndSaveXLS(path):
    wb = Workbook()
    sheet = wb.add_sheet("License Plates")
    intXLSCounter = 0
    strDetectedLP = ""
    listlicensePlateSamples = readLPImagePaths(path)

    for imgLP in listlicensePlateSamples:
        imgOriginalScene = cv2.imread(imgLP)  # open image

        imgOriginalScene = EditImage.adjust(imgOriginalScene, 100)
        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

        if len(listOfPossiblePlates) == 0:  # if no plates were found
            print("\nno license plates were detected\n")  # inform user no plates were found
            strDetectedLP = "OKUNMADI"
        else:  # else
            # if we get in here list of possible plates has at leat one plate

            # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)

            # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
            licPlate = listOfPossiblePlates[0]

            if len(licPlate.strChars) == 0:  # if no chars were found in the plate
                licPlate.strChars = "OKUNMADI"

            strDetectedLP = licPlate.strChars
        sheet.write(intXLSCounter, 0, imgLP)
        sheet.write(intXLSCounter, 1, strDetectedLP)
        intXLSCounter += 1
    # end for
    wb.save('results.xls')
    return
#end function

#####################################################################################################
def fromLocalPath(path):
    imgOriginalScene = cv2.imread(path)  # Resmi aç

    if imgOriginalScene is None:  # Resim okunmazsa hata mesajını yazdır ve programı bitir.
        print("\nerror: image not read from file \n\n")
        os.system("pause")
        return
    # end if

    imgOriginalScene = EditImage.adjust(imgOriginalScene, 280)
    cv2.imshow("adjust", imgOriginalScene)
    cv2.waitKey(0)

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # Plaka alanını belirler

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # Seçilen plakalardaki plakalardaki karakterleri belirler.

    cv2.imshow("imgOriginalScene", imgOriginalScene)

    if len(listOfPossiblePlates) == 0:                          # Eğer plakalar yoksa ekrana mesaj yazdır.
        print("\nno license plates were detected\n")
    else:
                # if we get in here list of possible plates has at leat one plate

        # Plakalarda tespit edilen karakter sayısına göre büyükten küçüğe doğru plakalar sıralanır.
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

        licPlate = listOfPossiblePlates[0] # En muntazam okunan plakanın en çok karakter sayısına sahip olan plaka olduğunu varsayalım.

        cv2.imshow("imgPlate", licPlate.imgPlate)   #Resimden kesilmiş plaka ve onun eşikleme işleminden geçmiş hali
        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:          # Plakadaki karakterler okunmazsa hata mesajını yazdır ve programı bitir.
            print("\nno characters were detected\n\n")
            return
        # end if

        EditImage.drawRedRectangleAroundPlate(imgOriginalScene, licPlate)            #Plakayı işaretle

        print("\nlicense plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
        print("----------------------------------------")

        EditImage.writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)           # write license plate text on the image

        cv2.imshow("imgOriginalScene", imgOriginalScene)                # re-show scene image

    # end if else

    cv2.waitKey(0)
    return
# Bir tuşa basılana kadar pencereleri açık tut.
#end function

