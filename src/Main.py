# Main.py
import cv2
import os
import sys

sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/read_and edit_images")
import ReadImage
sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/data_processing")
import GenerateAndTrainData

#####################################################################################################
def main():

    # list = os.listdir("E:/Repos/License-Plate-Recognizer-GitHub/dataset/characters")
    # print(len(list))
    # listAllClassificationData = np.loadtxt("E:/Repos/License-Plate-Recognizer-GitHub/dataset/classifications.txt")
    # print(str(listAllClassificationData.size/36))
    isDataGenerated = GenerateAndTrainData.generateData("E:/Repos/License-Plate-Recognizer-GitHub/dataset/characters")
    if isDataGenerated == False:
        print("\nerror: generating data was not successful\n")  # show error message
        return  # and exit program
        #end if
    #end if

    blnKNNTrainingSuccessful = GenerateAndTrainData.loadKNNDataAndTrainKNN()  # attempt KNN training

    if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
        print("\nerror: KNN training was not successful\n")  # show error message
        return  # and exit program
    # end if

    ReadImage.fromWebCam()
    # ReadImage.fromIPCAM()
    # ReadImage.fromLocalPath('E:/Repos/License-Plate-Recognizer-GitHub/testimages/32.jpg')
    # ReadImage.fromLPDatasetAndSaveXLS("E:/Repos/License-Plate-Recognizer-GitHub/LPs")
    cv2.waitKey(0)  # hold windows open until user presses a key
    return
# end main

#########################################################################################################################
if __name__ == "__main__":
    main()












