import cv2
import numpy as np
import json

SZ = 20          #Resim uzunluğu ve genişliği eğitimi
MAX_WIDTH = 1000 #Orijinal resim maksimum genişlik
Min_Area = 2000  #Plaka alanında izin verilen maksimum alan

def point_limit(point):
    if point[0] < 0:
        point[0] = 0
    if point[1] < 0:
        point[1] = 0

class LPDetector:
    def __init__(self):
        # Plaka tanıma parametrelerinin bazıları, resmin çözünürlüğüne göre ayarlamak için uygun olan js cinsinden saklanır.
        f = open('config.js')
        j = json.load(f)
        for c in j["config"]:
            if c["open"]:
                self.cfg = c.copy()
                break
        else:
            raise RuntimeError('Geçerli bir yapılandırma parametresi ayarlanmadı')

    def predict(self, imgCar):
        if type(imgCar) == type(""):
            img = cv2.imread(imgCar)
        else:
            img = imgCar
        imgHeight, imgWidth = img.shape[:2]

        if imgWidth > MAX_WIDTH:
            resize_rate = MAX_WIDTH / imgWidth
            img = cv2.resize(img, (MAX_WIDTH, int(imgWidth * resize_rate)), interpolation = cv2.INTER_AREA)

        blur = self.cfg["blur"]
        #Gauss'un kınaması
        if blur > 0:
            img = cv2.GaussianBlur(img, (blur, blur), 0)#Görüntü çözünürlüğü ayarı
        oldImg = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Resmin plaka olmayacak alanını kaldırın
        kernel = np.ones((20, 20), np.uint8)
        imgOpening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        imgOpening = cv2.addWeighted(img, 1, imgOpening, -1, 0);

        #Resmin kenarını bulun
        ret, img_thresh = cv2.threshold(imgOpening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        imgEdge = cv2.Canny(img_thresh, 100, 200)
        #Görüntü kenarını bir bütün yapmak için açma ve kapama işlemlerini kullanın.
        kernel = np.ones((self.cfg["morphologyr"], self.cfg["morphologyc"]), np.uint8)
        imgEdge1 = cv2.morphologyEx(imgEdge, cv2.MORPH_CLOSE, kernel)
        imgEdge2 = cv2.morphologyEx(imgEdge1, cv2.MORPH_OPEN, kernel)

        #Resmin kenarlarından oluşan dikdörtgen alanı arayın, çok sayıda olabilir ve plaka dikdörtgen alanlardan birinde olabilir.
        try:
            contours, hierarchy = cv2.findContours(imgEdge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        except ValueError:
            contours, hierarchy = cv2.findContours(imgEdge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cnt for cnt in contours if cv2.contourArea(cnt) > Min_Area]
        print('len(contours)', len(contours))
        #一一Plaka olmayan dikdörtgen alanları hariç tutun
        car_contours = []
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)
            area_width, area_height = rect[1]
            if area_width < area_height:
                area_width, area_height = area_height, area_width
            wh_ratio = area_width / area_height
            #2 ila 5.5 arasındaki dikdörtgen alan en boy oranı gerekli, 2 ila 5.5, plaka en boy oranıdır ve kalan dikdörtgenler hariç
            if wh_ratio > 2 and wh_ratio < 5.5:
                car_contours.append(rect)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

        print(len(car_contours))

        print("Hassas konumlandırma")
        card_imgs = []
        #Dikdörtgen alan, renk konumlandırmayı kullanmak için düzeltilmesi gereken eğimli bir dikdörtgen olabilir
        for rect in car_contours:
            if rect[2] > -1 and rect[2] < 1:#Sol, yüksek, sağ ve düşük için doğru değerleri elde etmek için açıları oluşturun
                angle = 1
            else:
                angle = rect[2]
            rect = (rect[0], (rect[1][0]+5, rect[1][1]+5), angle)#Plaka kenarının dışlanmaması için kapsamı genişletin

            box = cv2.boxPoints(rect)
            heigth_point = right_point = [0, 0]
            left_point = low_point = [imgWidth, imgHeight]
            for point in box:
                if left_point[0] > point[0]:
                    left_point = point
                if low_point[1] > point[1]:
                    low_point = point
                if heigth_point[1] < point[1]:
                    heigth_point = point
                if right_point[0] < point[0]:
                    right_point = point

            if left_point[1] <= right_point[1]:#Pozitif açı
                new_right_point = [right_point[0], heigth_point[1]]
                pts2 = np.float32([left_point, heigth_point, new_right_point])#Karakterler sadece oldukça değişkendir
                pts1 = np.float32([left_point, heigth_point, right_point])
                M = cv2.getAffineTransform(pts1, pts2)
                dst = cv2.warpAffine(oldImg, M, (imgWidth, imgHeight))
                point_limit(new_right_point)
                point_limit(heigth_point)
                point_limit(left_point)
                card_img = dst[int(left_point[1]):int(heigth_point[1]), int(left_point[0]):int(new_right_point[0])]
                card_imgs.append(card_img)
                cv2.imshow("card", card_img)
                cv2.waitKey(0)
            elif left_point[1] > right_point[1]:#Negatif açı

                new_left_point = [left_point[0], heigth_point[1]]
                pts2 = np.float32([new_left_point, heigth_point, right_point])#Karakterler sadece oldukça değişkendir
                pts1 = np.float32([left_point, heigth_point, right_point])
                M = cv2.getAffineTransform(pts1, pts2)
                dst = cv2.warpAffine(oldImg, M, (imgWidth, imgHeight))
                point_limit(right_point)
                point_limit(heigth_point)
                point_limit(new_left_point)
                card_img = dst[int(right_point[1]):int(heigth_point[1]), int(new_left_point[0]):int(right_point[0])]
                card_imgs.append(card_img)
                cv2.imshow("card", card_img)
                cv2.waitKey(0)

