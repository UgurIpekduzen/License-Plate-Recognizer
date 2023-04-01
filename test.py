# Main.py
import cv2
import os
import glob

from src.read_and_edit_images import ReadImage
from src.data_processing import GenerateAndTrainData 

#####################################################################################################
def main():
    # f = open("E:\Repos\License-Plate-Recognizer-GitHub\src\data_processing\deneme.txt", "a+")
    # for i in range(5):
    #     f.write("This is line %d\r\n" % (i + 1))
    # f.close()
    # imgCharacterSets = []
    # images = glob.glob("E:/Repos/License-Plate-Recognizer-GitHub/dataset/characters/*.jpg")
    # for image in images:
    #     print(image)

    isDataGenerated = GenerateAndTrainData.generateData()
    if isDataGenerated == False:
        print("\nerror: generating data was not successful\n")  # show error message
        return  # and exit program
        #end if
    #end if
    #
    blnKNNTrainingSuccessful = GenerateAndTrainData.loadKNNDataAndTrainKNN()  # attempt KNN training

    if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
        print("\nerror: KNN training was not successful\n")  # show error message
        return  # and exit program
    # end if

    print(ReadImage.fromWebCam())
    # # ReadImage.fromIPCAM()
    # # ReadImage.fromLocalPath('E:/Repos/License-Plate-Recognizer-GitHub/testimages/32.jpg')
    # # ReadImage.fromLPDatasetAndSaveXLS("E:/Repos/License-Plate-Recognizer-GitHub/LPs")
    # cv2.waitKey(0)  # hold windows open until user presses a key
    return
# end main

#########################################################################################################################
if __name__ == "__main__":
    main()












