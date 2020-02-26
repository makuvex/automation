import mysql.connector

def create_db(name):
    mydb = mysql.connector.connect(
      host="localhost",
      user="makuvex7",
      passwd="malice77"
    )

    mycursor = mydb.cursor()

    query = "CREATE DATABASE " + name
    mycursor.execute(query)

