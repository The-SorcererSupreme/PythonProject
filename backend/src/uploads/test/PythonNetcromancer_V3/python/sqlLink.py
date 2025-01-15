import mysql.connector
#global mycursor
mydb = mysql.connector.connect(
  host="localhost",
  user="dbuser",
  password="vv2j@&T2zax@HhApm2",
  database="sqlinthesky"
)

mycursor = mydb.cursor()