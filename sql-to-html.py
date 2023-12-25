import os
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port=3306,
    database='web_tugas_akhir'
)

# Get Data

sql = "SELECT * FROM train LIMIT 10;"
mycursor = mydb.cursor()
mycursor.execute(sql)
myresult = mycursor.fetchall()
print(myresult)

# Do Something
df = pd.DataFrame()
for x in myresult:
    df2 = pd.DataFrame(list(x)).T
    df = pd.concat([df, df2])

df.to_html('templates/sql-data.html')