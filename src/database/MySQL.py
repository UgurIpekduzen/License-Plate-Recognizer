import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="lpr"
)

mycursor = db.cursor()

mycursor.execute("SELECT * FROM vehicle")

myresult = mycursor.fetchall()

for x in myresult:
    print(x)