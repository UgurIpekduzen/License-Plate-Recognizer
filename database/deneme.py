import mysql.connector
connection = mysql.connector.connect(user='root', password='mypassword', host='localhost', port='3306', database='lpr')
print("DB connected")

cursor = connection.cursor()

# cursor.execute('CREATE TABLE vehicle(licensePlate VARCHAR(50) NOT NULL, isRegistered TINYINT(1) DEFAULT 0, isBlacklisted TINYINT(1) DEFAULT 0);')
# connection.commit()
# connection.close()

cursor.execute('DROP TABLE vehicle;')
connection.commit()
connection.close()

# cursor.execute('INSERT INTO vehicle(licensePlate) VALUES("16CSF07");')
# connection.commit()
# connection.close()

# cursor.execute('Select * FROM students1')
# connection.commit()
# connection.close()

# def checkTableExists(tablename):
#     cursor.execute("""
#         SELECT COUNT(*)
#         FROM information_schema.tables
#         WHERE table_name = '{0}'
#         """.format(tablename.replace('\'', '\'\'')))
#     if cursor.fetchone()[0] == 1:
#         cursor.close()
#         return True

#     cursor.close()
#     return False

# print(checkTableExists('students1'))