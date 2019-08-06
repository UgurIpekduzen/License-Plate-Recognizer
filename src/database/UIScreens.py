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

    def deletionScreen(self):
        clear()
        print("-- KAYIT SİLME EKRANI --")
        print("1 - Tüm kayıtları sil")
        print("2 - Seçilmiş bir kayıt sil")
        print("0 - Bir üst menüye dön")

    def selectionScreen(self):
        clear()
        print("-- KAYIT SEÇME EKRANI --")
        print("1 - Tüm kayıtları görüntüle")
        print("2 - Seçilmiş bir kayıt görüntüle")
        print("0 - Bir üst menüye dön")

    def deleteAllScreen(self):
        clear()
        print("-- TÜM KAYITLARI SİLME EKRANI --")
        SQLQueries.deleteAllVehicles()

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

    def selectAllScreen(self):
        clear()
        print("-- TÜM KAYITLARI GÖTÜNTÜLEME EKRANI --")
        allVehicles = SQLQueries.selectAllVehicles()
        print("Plaka" + "      |       " + "Kayıtlı Mı?" + "      |       " + "Kara Listede Mi?")
        for vehicle in allVehicles:
            print("-------------------------------------------------------------")
            if(vehicle[0] == ""):
                print("Boş")
            else:
                print('       |         '.join([vehicle[0], "Evet" if vehicle[1] == 1 else "Hayır", "Evet\n" if vehicle[2] == 1 else "Hayır\n"]))

    def selectOneScreen(self):
        clear()
        print("-- SEÇİLMİŞ KAYIT GÖTÜNTÜLEME EKRANI --")
        while True:
            licensePlateInput = input("Plakayı giriniz: ")
            matchObj = search("^(0[1-9]|[1-7][0-9]|8[01])(([A-Z])(\d{4,5})|([A-Z]{2})(\d{3,4})|([A-Z]{3})(\d{2}))$", licensePlateInput)

            if(matchObj):
                break
            else:
                print("Plaka metni formatına uygun bir giriş yapmadınız, lütfen tekrar deneyiniz!")
                sleep(1)

        foundVehicle = SQLQueries.selectByLicensePlate(licensePlateInput)

        print("--------------------------------------------------------------------")
        print("Plaka: " + foundVehicle[0][0])
        print("Sisteme kayıtlı mı: " + ["Evet" if foundVehicle[0][1] == 1 else "Hayır"])
        print("Kara listede mi: " + ["Evet" if foundVehicle[0][2] == 1 else "Hayır"])
