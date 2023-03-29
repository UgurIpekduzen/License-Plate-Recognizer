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

def selectByLicensePlate(strLicensePlate):
    condition = 'licensePlate= %s'
    return db.select('Vehicle',condition,'*', licensePlate=strLicensePlate)

def insertNewLicensePlate(licensePlate, registerStatus = 0, blackListStatus = 0):
    print("Kayıt işlemi başarılı!")
    return db.insert('Vehicle', licensePlate=licensePlate, isRegistered=registerStatus, isBlackListed=blackListStatus)

def showFoundVehicleDBInfo(strLicensePlate):
    VehicleDBInfo = selectByLicensePlate(strLicensePlate)
    return ' '.join(["Plaka:", VehicleDBInfo[0][0],
                     "\nSisteme kayıtlı mı:", "Evet" if VehicleDBInfo[0][1] == 1 else "Hayır",
                     "\nKara listede mi:", "Evet\n" if VehicleDBInfo[0][2] == 1 else "Hayır\n"])

def updateSelectedVehicleInfo(strLicensePlate, intRegistryStatus=0, intBlacklistStatus=0):
    condition = 'licensePlate= %s'
    return db.update('Vehicle', condition, strLicensePlate, isRegistered=intRegistryStatus, isBlackListed=intBlacklistStatus)

def identifyVehicleStatusByLicensePlate(strLicensePlate):
    vehicleDBInfo = selectByLicensePlate(strLicensePlate)

    if vehicleDBInfo:
        if vehicleDBInfo[0][1] is 0 and vehicleDBInfo[0][2] is 0:
            return 'G'
        elif vehicleDBInfo[0][1] is 1 and vehicleDBInfo[0][2] is 0:
            return 'R'
        elif vehicleDBInfo[0][1] is 1 and vehicleDBInfo[0][2] is 1:
            return 'B'
    else:
        return 'U'

