from re import search
from time import sleep
from os import system, name

import SQLQueries

clear = lambda: system('clear' if name == 'posix' else 'cls')

class UIScreens(object):
    def __init__(self):
        self.strMenuName = "mainmenuscr"

    def mainMenuScreen(self):

        print("-- BAŞLANGIÇ EKRANI --")
        print("1 - Yeni kayıt ekle")
        print("2 - Kayıt seç")
        print("3 - Kayıt sil")
        print("4 - Kayıt güncelle")
    # end function

    def insertionScreen(self):
        clear()
        print("-- YENİ KAYIT EKLEME --")
        while True:
            licensePlateInput = input("Plakayı giriniz: ")
            matchObj = search("^(0[1-9]|[1-7][0-9]|8[01])(([A-Z])(\d{4,5})|([A-Z]{2})(\d{3,4})|([A-Z]{3})(\d{2}))$",
                              licensePlateInput)

            if (matchObj):
                break
            else:
                print("Plaka metni formatına uygun bir giriş yapmadınız, lütfen tekrar deneyiniz!")
                sleep(1)
        SQLQueries.insertNewLicensePlate(licensePlateInput)
        print("\n0 - Ana menüye dön")
    # end function

    def deletionScreen(self):
        clear()
        print("-- KAYIT SİLME EKRANI --")
        print("1 - Tüm kayıtları sil")
        print("2 - Seçilmiş bir kayıt sil")
        print("0 - Ana menüye dön")
    # end function

    def selectionScreen(self):
        clear()
        print("-- KAYIT SEÇME EKRANI --")
        print("1 - Tüm kayıtları görüntüle")
        print("2 - Seçilmiş bir kayıt görüntüle")
        print("0 - Ana menüye dön")
    # end function

    def deleteAllScreen(self):
        clear()
        print("-- TÜM KAYITLARI SİLME EKRANI --")
        SQLQueries.deleteAllVehicles()

        print("\n3 - Kayıt silme ekranına geri dön")
    #end function

    def deleteOneScreen(self):
        clear()
        print("-- SEÇİLMİŞ KAYIT SİLME EKRANI --")

        while True:
            licensePlateInput = input("Plakayı giriniz: ")
            matchObj = search("^(0[1-9]|[1-7][0-9]|8[01])(([A-Z])(\d{4,5})|([A-Z]{2})(\d{3,4})|([A-Z]{3})(\d{2}))$", licensePlateInput)

            if(matchObj):
                break
            else:
                print("Plaka metni formatına uygun bir giriş yapmadınız, lütfen tekrar deneyiniz!")
                sleep(1)

        SQLQueries.deleteByLicensePlate(licensePlateInput)
        print("\n3 - Kayıt silme ekranına geri dön")
    # end function

    def selectAllScreen(self):
        clear()
        print("-- TÜM KAYITLARI GÖTÜNTÜLEME EKRANI --")
        allVehicles = SQLQueries.selectAllVehicles()
        print("   Plaka" + "      |     " + "Kayıtlı Mı?" + "     |   " + "Kara Listede Mi?")
        for vehicle in allVehicles:
            print("-------------------------------------------------------------")
            if(vehicle[0] == ""):
                print("Boş")
            else:
                print('       |         '.join([vehicle[0], "Evet" if vehicle[1] == 1 else "Hayır", "Evet\n" if vehicle[2] == 1 else "Hayır\n"]))

        print("\n3 - Kayıt seçme ekranına geri dön")
    # end function

    def selectOneScreen(self):
        clear()
        print("-- SEÇİLMİŞ KAYIT GÖTÜNTÜLEME EKRANI --")
        while True:
            licensePlateInput = input("Plakayı giriniz: ")
            matchObj = search("^(0[1-9]|[1-7][0-9]|8[01])(([A-Z])(\d{4,5})|([A-Z]{2})(\d{3,4})|([A-Z]{3})(\d{2}))$", licensePlateInput)

            if(matchObj):
                foundVehicle = SQLQueries.selectByLicensePlate(licensePlateInput)
                if(foundVehicle):
                    print("--------------------------------------------------------------------")
                    print("Plaka: " + foundVehicle[0][0])
                    print("Sisteme kayıtlı mı: ", "Evet" if foundVehicle[0][1] == 1 else "Hayır")
                    print("Kara listede mi: ", "Evet" if foundVehicle[0][2] == 1 else "Hayır")
                    break
                else:
                    print("Aranan plaka bulunamadı!")
            else:
                print("Plaka metni formatına uygun bir giriş yapmadınız, lütfen tekrar deneyiniz!")
                sleep(1)

        print("\n3 - Kayıt seçme ekranına geri dön")
    # end function

    def updateScreen(self):
        clear()
        print("-- KAYIT GÜNCELLEME EKRANI --")
        
        allVehicles = SQLQueries.selectAllVehicles()
        print("   Plaka" + "      |     " + "Kayıtlı Mı?" + "     |   " + "Kara Listede Mi?")
        for vehicle in allVehicles:
            print("-------------------------------------------------------------")
            if(vehicle[0] == ""):
                print("Boş")
            else:
                print('       |         '.join([vehicle[0], "Evet" if vehicle[1] == 1 else "Hayır", "Evet\n" if vehicle[2] == 1 else "Hayır\n"]))

        while True:
            licensePlateInput = input("Plakayı giriniz: ")
            matchObj = search("^(0[1-9]|[1-7][0-9]|8[01])(([A-Z])(\d{4,5})|([A-Z]{2})(\d{3,4})|([A-Z]{3})(\d{2}))$", licensePlateInput)

            if(matchObj):
                foundVehicle = SQLQueries.selectByLicensePlate(licensePlateInput)
                isRegisteredInput = int(input("Sisteme kayıt durumu: "))
                isBlacklistedInput = int(input("Kara liste durumu: "))
                SQLQueries.updateSelectedVehicleInfo(strLicensePlate=foundVehicle, intRegistryStatus=isRegisteredInput, intBlacklistStatus=isBlacklistedInput)
            else:
                print("Plaka metni formatına uygun bir giriş yapmadınız, lütfen tekrar deneyiniz!")
                sleep(1)
                
        return 0
    # end function
#end class