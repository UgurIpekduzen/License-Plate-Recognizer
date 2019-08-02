import sys

sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/database")
from DBConnect import DBConnection

db = DBConnection('localhost','root','1234','lpr')

def deleteByLicensePlate(strLicensePlate):
    print("Silme işlemi başarılı!")
    db.delete('Vehicle',"licensePlate='"+ strLicensePlate +"'")


def searchByLicensePlate(strLicensePlate):
    condition = 'licensePlate= %s'
    return db.select('Vehicle',condition,'*', licensePlate=strLicensePlate)

def insertNewLicensePlate(licensePlate):
    print("Kayıt işlemi başarılı!")
    return db.insert('Vehicle', licensePlate=licensePlate, isRegistered= 0, isBlackListed=0)