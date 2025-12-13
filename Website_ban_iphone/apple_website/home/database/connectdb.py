import mysql.connector

# Kết nối MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234"
)



# Câu lệnh SQL
sql = "CREATE DATABASE `DB_WEB_PYTHON`;"
mycursor = db.cursor()
# Thực thi
mycursor.execute(sql)

#update 
