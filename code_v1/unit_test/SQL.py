import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rmutl",
    database="test"
)

mycursor = mydb.cursor()

while True:
    cmd = input("กรุณาใส่ค่า article หรือพิมพ์ 'exit' เพื่อออก: ")

    if cmd.lower() == "exit":
        break

    if cmd == "metal":
        table_name = "metal"
        print("ส่งค่าสำเร็จ")
    elif cmd == "plastic":
        table_name = "plastic"
        print("ส่งค่าสำเร็จ")
    elif cmd == "other":
        table_name = "other"
        print("ส่งค่าสำเร็จ")
    elif cmd == "glass":
        table_name = "glass"
        print("ส่งค่าสำเร็จ")

    else:
        print("ไม่พบค่า article ที่ถูกต้อง")
        continue

    mycursor.execute(f"SELECT MAX(trash_number) FROM {table_name}")
    last_trash_number = mycursor.fetchone()[0]

    if last_trash_number is None:
        last_trash_number = 1
    else:
        last_trash_number += 1

    sqlFormula = f"INSERT INTO {table_name} (article, trash_number, created_at) VALUES (%s, %s, %s)"
    data = (cmd, last_trash_number, datetime.now())

    mycursor.execute(sqlFormula, data)
    mydb.commit()