import SQLQueries
import time


# vehicles = ["16CSF07", "34E5758", "34JR6771", "34CJS67", "34CDA17"]
# for newLog in vehicles:
#     SQLQueries.insertNewLicensePlate(newLog)
#     print("Kayıt işlemi başarılı!")
#     time.sleep(1)
# vehicle1 = ("16CSF07",1,0)
# insert(mycursor, vehicle1)
# vehicle2 = ("34E5758",0,0)
# insert(mycursor, vehicle2)
# vehicle3 = ("34JR6771",0,1)
# insert(mycursor, vehicle3)
# vehicle4 = ("34CJS67",1,0)
# insert(mycursor, vehicle4)
# vehicle5 = ("34CDA17",0,1)
# insert(mycursor, vehicle5)

# foundVehicleLog = getVehicleByLicensePlate(mycursor, "34JR6771")
#
# for row in foundVehicleLog:
#     print("Plaka: ", row[0])
#     print("Sisteme kayıtlı mı:", "Evet" if row[1] == 1 else "Hayır")
#     print("Kara listede mi:", "Evet" if row[2] == 1 else "Hayır")
# print("-----------------------------------------------------------------")
# foundVehicleLogs = selectAll(mycursor)
# for row in foundVehicleLogs:
#     print("Plaka: ", row[0])
#     print("Sisteme kayıtlı mı:", "Evet" if row[1] == 1 else "Hayır")
#     print("Kara listede mi:", "Evet" if row[2] == 1 else "Hayır")

# deleteByLicensePlate(mycursor, "16CSF07")
# for deleteLog in vehicles:
#     deleteByLicensePlate(mycursor, deleteLog[0])
#     print("Silme işlemi başarılı!")
#     time.sleep(1)

# SQLQueries.deleteAllVehicles()
# foundVehicleLogs = SQLQueries.selectAllVehicles()
# for row in foundVehicleLogs:
#     print("Plaka: ", row[0])
#     print("Sisteme kayıtlı mı:", "Evet" if row[1] == 1 else "Hayır")
#     print("Kara listede mi:", "Evet" if row[2] == 1 else "Hayır")
#     print("-------------------------------------------------------------------")

print(SQLQueries.showFoundVehicleDBInfo("16CSF07"))