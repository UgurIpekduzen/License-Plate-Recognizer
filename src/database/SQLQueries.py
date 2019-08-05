import sys

sys.path.append("E:/Repos/License-Plate-Recognizer-GitHub/src/database")
from DBConnect import DBConnection

db = DBConnection('localhost','root','1234','lpr')

def deleteByLicensePlate(strLicensePlate):
    print("Silme işlemi başarılı!")
    db.delete('Vehicle',"licensePlate='"+ strLicensePlate +"'")

def deleteAllVehicles():
    print("Silme işlemi başarılı!")
    db.delete('Vehicle', None)

def selectAllVehicles():
    return db.select('Vehicle', None, '*')

def searchByLicensePlate(strLicensePlate):
    condition = 'licensePlate= %s'
    return db.select('Vehicle',condition,'*', licensePlate=strLicensePlate)

def insertNewLicensePlate(licensePlate):
    print("Kayıt işlemi başarılı!")
    return db.insert('Vehicle', licensePlate=licensePlate, isRegistered= 0, isBlackListed=0)

def showFoundVehicleDBInfo(strLicensePlate):
    VehicleDBInfo = searchByLicensePlate(strLicensePlate)
    return ' '.join(["Plaka:", VehicleDBInfo[0][0],
                     "\nSisteme kayıtlı mı:", "Evet" if VehicleDBInfo[0][1] == 1 else "Hayır",
                     "\nKara listede mi:", "Evet\n" if VehicleDBInfo[0][2] == 1 else "Hayır\n"])
