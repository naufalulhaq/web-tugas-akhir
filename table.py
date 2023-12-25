from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    port=3306,
    database='web_tugas_akhir'
)

@app.route('/table')
def sql_table():
    sql = "SELECT * FROM sample;"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    # print(myresult)
    return render_template('table2.html', data=myresult)

if __name__ == '__main__':
    app.run()



# Get Data

