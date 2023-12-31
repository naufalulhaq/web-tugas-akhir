from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
import pandas as pd
import math
# from mlutils import predict

app = Flask(__name__, static_folder='src')

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'tugas_akhir',
}

conn = mysql.connector.connect(**mysql_config)

def Baseurl(address):
    return url_for('static', filename=address)

@app.route('/')
def index():
    return render_template('basic-table.html', baseurl=Baseurl)

@app.route('/form')
def form():
    return render_template('form.html', baseurl=Baseurl)

@app.route('/chart')
def chart():
    sql = "SELECT * FROM sample"

    mycursor = conn.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    Results = {}
    Results["date_time"] = [entry["date_time"] for entry in myresult]
    Results["traffic_volume"] = [entry["traffic_volume"] for entry in myresult]

    return render_template('chart.html', baseurl=Baseurl, results=Results)


@app.route('/table')
def sql_table():
    sql = "SELECT * FROM sample_v2"

    mycursor = conn.cursor(dictionary=True)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    return render_template('table.html', baseurl=Baseurl, data=myresult)

@app.route('/table_page')
def table_page():
    page = request.args.get('page', 1, type=int)
    sort_by = request.args.get('sort_by', 'default_column')
    sort_order = request.args.get('order', 'asc')
    per_page = 12
    offset = (page - 1) * per_page

    mycursor = conn.cursor(dictionary=True)

    # Validate sort_by and sort_order
    valid_sort_columns = ['traffic_volume', 'date_time', 'is_holiday']  # your actual column names
    valid_orders = ['asc', 'desc']
    sort_by = sort_by if sort_by in valid_sort_columns else 'id'
    sort_order = sort_order if sort_order in valid_orders else 'asc'


    # Query to get the total number of records
    mycursor.execute("SELECT COUNT(*) FROM second_half")
    total_records = mycursor.fetchone()['COUNT(*)']
    total_pages = math.ceil(total_records / per_page)

    # Query to fetch only the subset of data for the current page
    query = f"SELECT * FROM second_half ORDER BY {sort_by} LIMIT %s OFFSET %s"
    mycursor.execute(query, (per_page, offset))
    myresult = mycursor.fetchall()
    mycursor.close()

    return render_template('table_pagination.html', baseurl=Baseurl, data=myresult, page=page, total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug='True')