import cv2
import numpy as np
import os
import sys

sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/constants")
import Constant

kNearest = cv2.ml.KNearest_create()

def generateData():

    listOfClassificationsTxtFilePaths = []
    listOfFlattenedImagesTxtFilePaths = []
    intNumberOfTxtFilePairs = 0
    intTotalNumberOfChars = 0

    for file in os.listdir(Constant.strCharacterSetsFilePath):
        if file.endswith('.jpg'):
            strImageName = file
            splittedFileName, _ = os.path.splitext(file)
            isFlattenImagesTxtExists = os.path.exists(Constant.strCharacterSetsFilePath + "/" + splittedFileName + "_flattened_images.txt")
            isClassificationTxtExists = os.path.exists(Constant.strCharacterSetsFilePath + "/" + splittedFileName + "_classifications.txt")

            if (isClassificationTxtExists and isFlattenImagesTxtExists) is False:
                intClassifications = []  # kullanıcı girdilerini tutan sınıflandırma listesi
                npaFlattenedImages = np.empty((0, Constant.RESIZED_IMAGE_WIDTH * Constant.RESIZED_IMAGE_HEIGHT))

                strFilePath = os.path.join(Constant.strCharacterSetsFilePath, strImageName)
                imgTrainingNumbers = cv2.imread(strFilePath)          #dosya dizinin içindeki karakter setlerini sırayla okur.

                # resim bulunamazsa hata mesajı döndür bir fonksiyonu bitir
                if imgTrainingNumbers is None:
                    print ("Hata dosyadan resim konunamadı \n\n")
                    os.system("pause")
                    return False
                # end if

                imgGray = cv2.cvtColor(imgTrainingNumbers, cv2.COLOR_BGR2GRAY)          # grayscale resim elde et
                imgBlurred = cv2.GaussianBlur(imgGray, (5,5), 0)                        # resmi bulanıklaştır

                # grayscale resmi eşikleme işleminden geçirerek renk tonlamalarını ortadan kaldır.
                imgThresh = cv2.adaptiveThreshold(imgBlurred,                           # resim girdisi
                                                  255,                                  # eşiği tam beyaz geçen pikseller yapar
                                                  cv2.ADAPTIVE_THRESH_GAUSSIAN_C,       # Gaussian Adaptive Threshold formülü
                                                  cv2.THRESH_BINARY_INV,                # ön plan beyaz olacak, arka plan siyah olacak
                                                  11,                                   # eşik değerini hesaplamak için kullanılan piksel komşuluğunun boyutu
                                                  2)                                    # ortalama veya ağırlıklı ortalamadan çıkarılan sabit

                imgThreshCopy = imgThresh.copy()        # oluşan yeni resmin bir kopyasını çıkar

                npaContours, npaHierarchy = cv2.findContours(imgThreshCopy,        # eşiklenmiş resmin kopyası
                                                             cv2.RETR_EXTERNAL,                 # sadece en dıştaki kontürları al
                                                             cv2.CHAIN_APPROX_SIMPLE)           # yatay, dikey ve çapraz bölümleri sıkıştırın ve yalnızca bitiş noktalarını bırak

                # eklenen karakter setlerinde geçerli kılınan harf ve sayıların ASCII değerlerinden oluşan liste
                intValidChars = [ord('0'), ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'),
                                 ord('A'), ord('B'), ord('C'), ord('D'), ord('E'), ord('F'), ord('G'), ord('H'), ord('I'), ord('J'),
                                 ord('K'), ord('L'), ord('M'), ord('N'), ord('O'), ord('P'), ord('Q'), ord('R'), ord('S'), ord('T'),
                                 ord('U'), ord('V'), ord('W'), ord('X'), ord('Y'), ord('Z')]

                for npaContour in npaContours:                                          # her bir kontür için
                    if cv2.contourArea(npaContour) > Constant.MIN_CONTOUR_AREA:         # eğer bulunan kontür minimum sınır değerinden büyükse
                        [intX, intY, intW, intH] = cv2.boundingRect(npaContour)         # sınırlayıcı dikdörtgeninin koordinant

                        # girişten kullanıcı istediğimizde her kenarın çevresine dikdörtgen çiz
                        cv2.rectangle(imgTrainingNumbers,           # orjinal resim
                                      (intX, intY),                 # üst sol köşe
                                      (intX+intW,intY+intH),        # alt sağ köşe
                                      (0, 0, 255),                  # kırmızı
                                      2)                            # kalınlık

                        imgROI = imgThresh[intY:intY+intH, intX:intX+intW]                                                      # eşiklenmiş resimden karakteri kırp
                        imgROIResized = cv2.resize(imgROI, (Constant.RESIZED_IMAGE_WIDTH, Constant.RESIZED_IMAGE_HEIGHT))       # kırpılan karakteri yeniden boyutlandır

                        cv2.imshow("imgROI", imgROI)
                        cv2.imshow("imgROIResized", imgROIResized)
                        cv2.imshow("training_numbers.png", imgTrainingNumbers)      # eğitme için kullanılan karakter işaretlenmiş şeklinde tekrar göster

                        intChar = cv2.waitKey(0)

                        if intChar == 27:                   # ESC'ye basılırsa programı bitirir.
                            sys.exit()
                        elif intChar in intValidChars:      # klavyeden okunan karakter geçerli karakterlerden biri ise

                            print("Basılan karakter: " + chr(intChar))
                            intClassifications.append(intChar)                                                # okunan ASCII kodunu listeye koy

                            npaFlattenedImage = imgROIResized.reshape((1, Constant.RESIZED_IMAGE_WIDTH * Constant.RESIZED_IMAGE_HEIGHT))  # kırpılan resmi tek boyutlu numpy dizisine çevirip düzleştir
                            npaFlattenedImages = np.append(npaFlattenedImages, npaFlattenedImage, 0)                   # oluşan sonucu listeye kaydet

                        # end if
                    # end if
                # end for
                fltClassifications = np.array(intClassifications, np.float32)  # int değerlerden oluşan sınıflandırma verileri listini 32 bitlik float değerlere çevir
                npaClassifications = fltClassifications.reshape((fltClassifications.size, 1))   # float değerler tutan numpy dizisini tek boyuta indirgeyerek düzleştir.

                np.savetxt(Constant.strCharacterSetsFilePath + "/" + splittedFileName + "_classifications.txt", npaClassifications)  # düzleştirilmiş resim verilerini kaydet
                np.savetxt(Constant.strCharacterSetsFilePath + "/" + splittedFileName + "_flattened_images.txt", npaFlattenedImages)
            # end if
            listOfClassificationsTxtFilePaths.append(Constant.strCharacterSetsFilePath + "/" + splittedFileName + "_classifications.txt")
            listOfFlattenedImagesTxtFilePaths.append(Constant.strCharacterSetsFilePath + "/" + splittedFileName + "_flattened_images.txt")
            intNumberOfTxtFilePairs += 1
            intTotalNumberOfChars += 36
        # end if
    #end for

    listOfNpaFlattenedImagesData = np.empty((0, Constant.RESIZED_IMAGE_WIDTH * Constant.RESIZED_IMAGE_HEIGHT))
    listOfNpaClassificationData = np.empty((0, intTotalNumberOfChars))
    for i in range(0, intNumberOfTxtFilePairs + 1):
        if i == intNumberOfTxtFilePairs:
            np.savetxt("E:/Repos/License-Plate-Recognizer-GitHub/src/data_processing/flattened_images_all_in_one.txt", listOfNpaFlattenedImagesData)
            np.savetxt("E:/Repos/License-Plate-Recognizer-GitHub/src/data_processing/classifications_all_in_one.txt", listOfNpaClassificationData)
            print("training is completed")
            cv2.destroyAllWindows()  # remove windows from memory
            return True
        npaClassificationsData = np.loadtxt(listOfClassificationsTxtFilePaths[i], np.float32)
        npaFlattenedImagesData = np.loadtxt(listOfFlattenedImagesTxtFilePaths[i], np.float32)
        listOfNpaFlattenedImagesData = np.append(listOfNpaFlattenedImagesData, npaFlattenedImagesData, 0)
        listOfNpaClassificationData = np.append(listOfNpaClassificationData, npaClassificationsData)

    return False

###################################################################################################
def loadKNNDataAndTrainKNN():

    try:
        npaClassifications = np.loadtxt("E:/Repos/License-Plate-Recognizer-GitHub/src/data_processing/classifications.txt", np.float32)  #kullanıcı girdilerinden oluşan sınıflandırma verilerini oku.
    except:  #eğer dosya açılmazsa hata mesajını göster ve False değeri döndür
        print("error, unable to open classifications.txt, exiting program\n")
        os.system("pause")
        return False
    # end try

    try:
        npaFlattenedImages = np.loadtxt("E:/Repos/License-Plate-Recognizer-GitHub/src/data_processing/flattened_images.txt", np.float32) # txt dosyasındaki resim verilerini oku.
    except:   # eğer dosya açılamazsa hata mesajı göster.
        print("error, unable to open flattened_images.txt, exiting program\n")
        os.system("pause")
        return False  # eğitme işlemi tamamlanamadı.
    # end try

    npaClassifications = npaClassifications.reshape((npaClassifications.size, 1))       # reshape numpy array to 1d, necessary to pass to call to train

    kNearest.setDefaultK(1)

    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)           # KNN nesnesini eğit

    return True                             # eğitme işlemi tamamlandı.
# end function