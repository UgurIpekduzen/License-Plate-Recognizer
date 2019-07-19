import DetLP
import DetCh
import cv2
import os

def main():
    isKNNTrainingSuccessful = DetCh.loadKNNDataAndTrainKNN()  # attempt KNN training

    if isKNNTrainingSuccessful == False:  # if KNN training was not successful
        print("\nerror: KNN training was not successful\n")  # show error message
        return  # and exit program
    # end if

    #Resim / Görüntü Okuma
    imgOriginalScene = cv2.imread("E:/Repos/License Plate Recognizer/testimages/32.jpg")  # open image

    if imgOriginalScene is None:  # if image was not read successfully
        print("\nerror: image not read from file \n\n")  # print error message to std out
        os.system("pause")  # pause so user can see error message
        return  # and exit program
    # end if

    print("resim okundu")

    listPlates = DetLP.detectPlatesInScene(imgOriginalScene)  # detect plates

    listChars = DetCh.detectCharsInPlates(listPlates)  # detect chars in plates

    cv2.imshow("imgOriginalScene", imgOriginalScene)  # show scene image


    return
#end
if __name__ == "__main__":
    main()